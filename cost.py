"""Price a batch before running it, and account for it afterwards.

    python cost.py --epochs 20                  price models.txt before spending
    python cost.py --check                      every roster id resolves and serves tools
    python cost.py --search fable               find an id
    python cost.py --rank gemini                cheapest matches for a family
    python cost.py --calibrate logs/all         re-measure tokens from a finished batch

    python cost.py --spent logs/all             what a batch cost, from its logs
    python cost.py --billed                     what the key has spent, per OpenRouter
    python cost.py --billed --note "after grok" ...and record it in the ledger

Pricing is live from OpenRouter. The key is read from OPENROUTER_API_KEY and
never printed. --spent prices the tokens in the logs; --billed reads the key's
own usage counter. The runners write both to logs/all/ledger.txt, so the
computed and the billed figure sit side by side for every arm.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API = "https://openrouter.ai/api/v1"
CELLS = len(json.loads((ROOT / "variants.json").read_text(encoding="utf-8"))["variants"])

# Measured on the pilot. Re-measure with --calibrate once this batch has run;
# per-episode use varies by an order of magnitude between models.
PROFILE = {"prompt_mean": 80_005, "prompt_p90": 140_917,
           "output_mean": 6_563, "output_p90": 12_108, "n": 167, "source": "pilot"}


def get(path: str) -> dict:
    req = urllib.request.Request(f"{API}{path}", headers={"Accept": "application/json"})
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def catalogue() -> dict[str, dict]:
    """{id: {name, prompt, completion, cache_read, tools}} for every model served."""
    out = {}
    for m in get("/models").get("data", []):
        p = m.get("pricing") or {}
        try:
            out[m["id"]] = {
                "name": m.get("name", ""),
                "prompt": float(p.get("prompt") or 0),
                "completion": float(p.get("completion") or 0),
                "cache_read": float(p.get("input_cache_read") or 0),
                "tools": "tools" in (m.get("supported_parameters") or []),
            }
        except (TypeError, ValueError):
            continue
    return out


def roster() -> list[str]:
    lines = (ROOT / "models.txt").read_text(encoding="utf-8").splitlines()
    return [s.strip() for s in lines if s.strip() and not s.lstrip().startswith("#")]


def episode_cost(price: dict, prompt: int, output: int) -> float:
    return prompt * price["prompt"] + output * price["completion"]


def usage_cost(price: dict, u) -> float:
    """Cost of one recorded ModelUsage. Cache reads at the cache rate, cache
    writes at the prompt rate, which is what OpenRouter charges for most
    providers."""
    fresh = (u.input_tokens or 0) + (u.input_tokens_cache_write or 0)
    cached = u.input_tokens_cache_read or 0
    out = u.output_tokens or 0
    cache_rate = price["cache_read"] or price["prompt"]
    return fresh * price["prompt"] + cached * cache_rate + out * price["completion"]


def ledger(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}  {line}\n")


def spent(log_dir: Path, cat: dict) -> int:
    """What a batch cost: tokens from every log under log_dir, at live prices."""
    from inspect_ai.log import read_eval_log

    totals: dict[str, dict] = {}
    for p in sorted(log_dir.rglob("*.eval")):
        log = read_eval_log(str(p))
        mid = str(log.eval.model).replace("openrouter/", "")
        t = totals.setdefault(mid, {"episodes": 0, "in": 0, "cached": 0, "out": 0, "cost": 0.0})
        price = cat.get(mid)
        t["priced"] = price is not None
        for smp in log.samples or []:
            t["episodes"] += 1
            for u in (smp.model_usage or {}).values():
                t["in"] += (u.input_tokens or 0) + (u.input_tokens_cache_write or 0)
                t["cached"] += u.input_tokens_cache_read or 0
                t["out"] += u.output_tokens or 0
                if price:
                    t["cost"] += usage_cost(price, u)
    if not totals:
        print(f"no logs under {log_dir}")
        return 1

    led = log_dir / "ledger.txt"
    print(f"spent under {log_dir} -- tokens from the logs, prices live from OpenRouter\n")
    print(f"  {'model':<42}{'episodes':>9}{'in':>13}{'cached':>11}{'out':>11}{'cost':>9}")
    grand = {"episodes": 0, "in": 0, "cached": 0, "out": 0, "cost": 0.0}
    for mid, t in sorted(totals.items()):
        c = f"${t['cost']:.2f}" if t["priced"] else "?"
        print(f"  {mid:<42}{t['episodes']:>9}{t['in']:>13,}{t['cached']:>11,}{t['out']:>11,}{c:>9}")
        ledger(led, f"spent   {mid:<40} {t['episodes']:>4} ep  in={t['in']:,} cached={t['cached']:,} out={t['out']:,}  {c}")
        for k in grand:
            grand[k] += t[k]
    print(f"  {'total':<42}{grand['episodes']:>9}{grand['in']:>13,}{grand['cached']:>11,}{grand['out']:>11,}{'$%.2f' % grand['cost']:>9}")
    ledger(led, f"spent   {'TOTAL':<40} {grand['episodes']:>4} ep  in={grand['in']:,} cached={grand['cached']:,} out={grand['out']:,}  ${grand['cost']:.2f}")
    unpriced = [m for m, t in totals.items() if not t["priced"]]
    if unpriced:
        print("  unpriced, not in the OpenRouter catalogue:", ", ".join(unpriced))
    print(f"\nappended to {led}")
    return 0


def billed(note: str, led: Path) -> int:
    """What OpenRouter says the key has spent, now. With a note, it goes in the
    ledger with the change since the last billed line."""
    try:
        d = get("/key").get("data", {})
    except Exception as exc:
        print(f"could not read /key: {exc}")
        return 2
    usage = float(d.get("usage") or 0)
    limit = d.get("limit")
    print(f"billed: ${usage:.2f} used" + (f" of ${float(limit):.2f}" if limit else ""))
    if note:
        prev = None
        if led.exists():
            for line in led.read_text(encoding="utf-8").splitlines():
                if "  billed  " in line and "usage=$" in line:
                    prev = float(line.split("usage=$")[1].split()[0])
        delta = f"  delta=${usage - prev:.2f}" if prev is not None else ""
        ledger(led, f"billed  {note:<40} usage=${usage:.2f}{delta}")
        print(f"appended to {led}")
    return 0


def calibrate(log_dir: Path) -> dict | None:
    from inspect_ai.log import read_eval_log

    prompts, outputs = [], []
    for p in sorted(log_dir.rglob("*.eval")):
        for s in read_eval_log(str(p)).samples or []:
            pt = ot = 0
            for u in (s.model_usage or {}).values():
                pt += (u.input_tokens or 0) + (u.input_tokens_cache_read or 0) + (u.input_tokens_cache_write or 0)
                ot += u.output_tokens or 0
            if pt or ot:
                prompts.append(pt)
                outputs.append(ot)
    if not prompts:
        return None
    prompts.sort()
    outputs.sort()
    i = int(0.9 * (len(prompts) - 1))
    return {"prompt_mean": sum(prompts) // len(prompts), "prompt_p90": prompts[i],
            "output_mean": sum(outputs) // len(outputs), "output_p90": outputs[i],
            "n": len(prompts), "source": str(log_dir)}


def check(cat: dict) -> int:
    """Every roster id must resolve and serve tool calls, or the arm dies after
    the batch has started."""
    bad = 0
    for mid in roster():
        entry = cat.get(mid)
        if entry is None:
            bad += 1
            near = [k for k in cat if any(t in k for t in mid.split("/")[-1].split("-")[:2])][:5]
            print(f"  MISSING  {mid}" + (f"   near: {', '.join(near)}" if near else ""))
        elif not entry["tools"]:
            bad += 1
            print(f"  NO TOOLS {mid}")
        else:
            print(f"  ok       {mid}")
    print(f"\n{len(roster()) - bad} of {len(roster())} roster ids are runnable")
    return 1 if bad else 0


def search(term: str, cat: dict) -> int:
    hits = sorted(k for k, v in cat.items() if term.lower() in k.lower() or term.lower() in v["name"].lower())
    for k in hits[:30]:
        print(f"  {k:<50} {'tools' if cat[k]['tools'] else 'no tools'}")
    print(f"\n{len(hits)} match(es) for {term!r}")
    return 0 if hits else 1


def rank(term: str, cat: dict, prof: dict, epochs: int) -> int:
    n = CELLS * epochs
    hits = sorted((episode_cost(p, prof["prompt_mean"], prof["output_mean"]) * n, mid)
                  for mid, p in cat.items() if term.lower() in mid.lower() and p["tools"])
    print(f"cheapest matches for {term!r}, {n} episodes each:")
    for total, mid in hits[:20]:
        print(f"  ${total:>7.2f}  {mid}")
    return 0 if hits else 1


def price(cat: dict, prof: dict, epochs: int, budget: float | None) -> int:
    n = CELLS * epochs
    print(f"{epochs} epochs x {CELLS} cells = {n} episodes per model")
    print(f"tokens per episode: prompt {prof['prompt_mean']:,} (p90 {prof['prompt_p90']:,}), "
          f"output {prof['output_mean']:,} (p90 {prof['output_p90']:,}) -- {prof['source']}\n")
    print(f"  {'expected':>9}  {'p90':>9}  model")
    expected = ceiling = 0.0
    for mid in roster():
        p = cat.get(mid)
        if p is None:
            print(f"  {'?':>9}  {'?':>9}  {mid}   (unknown id -- try --check)")
            continue
        e = episode_cost(p, prof["prompt_mean"], prof["output_mean"]) * n
        c = episode_cost(p, prof["prompt_p90"], prof["output_p90"]) * n
        expected += e
        ceiling += c
        print(f"  ${e:>8.2f}  ${c:>8.2f}  {mid}")
    print(f"  ${expected:>8.2f}  ${ceiling:>8.2f}  total")

    try:
        d = get("/key").get("data", {})
        remaining = (d.get("limit") or 0) - (d.get("usage") or 0)
        print(f"\nkey has ${remaining:.2f} remaining")
        budget = budget or remaining
    except Exception:
        pass
    if budget:
        verdict = ("fits at the p90 ceiling" if ceiling <= budget else
                   "fits on expected cost, not at the ceiling -- cut models before epochs" if expected <= budget else
                   f"does not fit; about {int(budget / (expected / epochs))} epochs would")
        print(f"against ${budget:.2f}: {verdict}")
    return 0


def main() -> int:
    args = sys.argv[1:]

    def opt(flag, default=None):
        return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default

    if "--billed" in args:
        return billed(opt("--note", ""), Path(opt("--ledger", "logs/all/ledger.txt")))

    try:
        cat = catalogue()
    except Exception as exc:
        print(f"could not reach OpenRouter: {exc}")
        return 2

    if "--spent" in args:
        return spent(Path(opt("--spent", "logs/all")), cat)

    prof = calibrate(Path(opt("--calibrate"))) or PROFILE if "--calibrate" in args else PROFILE
    if "--check" in args and "--search" not in args:
        return check(cat)
    if "--search" in args:
        return search(opt("--search", ""), cat)
    if "--rank" in args:
        return rank(opt("--rank", ""), cat, prof, int(opt("--epochs", "20")))
    return price(cat, prof, int(opt("--epochs", "20")), float(opt("--budget", "0")) or None)


if __name__ == "__main__":
    raise SystemExit(main())
