"""Price a batch before spending the key on it, and check the roster resolves.

    python cost.py --epochs 20                  price models.txt
    python cost.py --check                      every roster id resolves and serves tools
    python cost.py --search fable               find an id
    python cost.py --rank gemini                cheapest matches for a family
    python cost.py --calibrate logs/all         re-measure tokens from a finished batch

Pricing is live from OpenRouter. The key is read from OPENROUTER_API_KEY and
never printed. Cost is figured as input + cache_read + cache_write, because a
provider that does not cache bills all of it.
"""

from __future__ import annotations

import json
import os
import sys
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

    try:
        cat = catalogue()
    except Exception as exc:
        print(f"could not reach OpenRouter: {exc}")
        return 2

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
