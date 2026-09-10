"""Estimate what a batch will cost before spending the key on it.

    python tools/estimate_cost.py                          # roster, 10 epochs
    python tools/estimate_cost.py --epochs 10 --budget 10
    python tools/estimate_cost.py --roster tools/models.txt
    python tools/estimate_cost.py --rank claude             # cheapest matches
    python tools/estimate_cost.py --calibrate logs          # re-measure tokens

Pricing comes live from OpenRouter. Token counts come from THIS environment's
own logs, not from a guess: 167 pilot episodes on claude-sonnet-5 give a
measured profile, and --calibrate re-derives it from any log directory.

WHY THE CACHE FIELDS MATTER. Anthropic reported almost every prompt token as a
cache read (mean input_tokens 24, mean cache_read 70,759). A provider that does
not cache bills all of it, so the figure that matters for a cost ceiling is
input + cache_read + cache_write, not input alone. Reading `input_tokens` here
would underestimate the batch by three orders of magnitude.

The key is read from the environment and never printed or written to disk.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://openrouter.ai/api/v1"

# Measured over 167 episodes of the shipped fixture (claude-sonnet-5).
# Regenerate with --calibrate. p90 rather than mean for the ceiling, because a
# budget that only holds for the average episode is not a budget.
PROFILE = {
    "prompt_mean": 80_005, "prompt_p90": 140_917,
    "output_mean":  6_563, "output_p90":  12_108,
    "n": 167, "source": "pilot logs, claude-sonnet-5",
}

VARIANTS = len(json.loads((ROOT / "variants.json").read_text(encoding="utf-8"))["variants"])


def _get(path: str, key: str | None) -> dict:
    req = urllib.request.Request(f"{API}{path}", headers={"Accept": "application/json"})
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def catalogue(key: str | None) -> dict[str, dict]:
    """{id: {name, prompt_usd_per_token, completion_usd_per_token}}"""
    out = {}
    for m in _get("/models", key).get("data", []):
        pricing = m.get("pricing") or {}
        try:
            p = float(pricing.get("prompt", 0) or 0)
            c = float(pricing.get("completion", 0) or 0)
        except (TypeError, ValueError):
            continue
        out[m["id"]] = {"name": m.get("name", ""), "prompt": p,
                        "completion": c,
                        "cache_read": float(pricing.get("input_cache_read", 0) or 0)}
    return out


def credit(key: str | None) -> tuple[float | None, float | None]:
    """(usage_usd, limit_usd) for the key, or (None, None) if unavailable."""
    if not key:
        return None, None
    try:
        d = _get("/key", key).get("data", {})
        return d.get("usage"), d.get("limit")
    except Exception:
        return None, None


def read_roster(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [s.strip() for s in lines if s.strip() and not s.lstrip().startswith("#")]


def episode_cost(price: dict, prompt_tok: int, output_tok: int,
                 cache_ratio: float = 0.0) -> float:
    """Cost of one episode.

    `cache_ratio` is the fraction of prompt tokens served from cache. At 0.0
    this is the no-cache ceiling, which is the safe number to budget against
    before a model has ever run. Afterwards use the measured ratio: providers
    price input_cache_read at roughly a tenth of prompt, so the ceiling is not
    the expected cost and treating it as one overstates spend badly.

    Measured across every log in this repo, the ceiling came to $296.90
    against $147.56 actually payable -- 101% over. Worst on
    google/gemini-3.8-flash, whose prompts are 80% cache reads: $161.90
    ceiling against $68.04 real. Runs were talked out of on that arithmetic.
    """
    cached = prompt_tok * cache_ratio
    fresh = prompt_tok - cached
    rate = price.get('cache_read') or price['prompt']
    return fresh * price['prompt'] + cached * rate + output_tok * price['completion']


def cache_ratio_from(log_dir) -> float | None:
    """Fraction of prompt tokens served from cache, measured from finished logs."""
    try:
        from inspect_ai.log import read_eval_log
    except ImportError:
        return None
    import glob as _g
    fresh = cached = 0
    for f in _g.glob(str(Path(log_dir) / '**' / '*.eval'), recursive=True):
        log = read_eval_log(f)
        for u in (log.stats.model_usage or {}).values():
            fresh += (u.input_tokens or 0)
            cached += (u.input_tokens_cache_read or 0)
    total = fresh + cached
    return (cached / total) if total else None


def calibrate(log_dir: Path) -> dict | None:
    """Re-derive the token profile from finished eval logs."""
    try:
        from inspect_ai.log import read_eval_log
    except ImportError:
        print("inspect_ai not installed -- cannot calibrate.")
        return None

    prompts, outputs = [], []
    for p in sorted(log_dir.rglob("*.eval")):
        try:
            log = read_eval_log(str(p))
        except Exception:
            continue
        for s in (log.samples or []):
            pt = ot = 0
            for _, u in (getattr(s, "model_usage", None) or {}).items():
                pt += (getattr(u, "input_tokens", 0) or 0)
                pt += (getattr(u, "input_tokens_cache_read", 0) or 0)
                pt += (getattr(u, "input_tokens_cache_write", 0) or 0)
                ot += (getattr(u, "output_tokens", 0) or 0)
            if pt or ot:
                prompts.append(pt); outputs.append(ot)

    if not prompts:
        print(f"no usage data under {log_dir}")
        return None

    prompts.sort(); outputs.sort()
    idx = int(0.9 * (len(prompts) - 1))
    return {
        "prompt_mean": sum(prompts) // len(prompts), "prompt_p90": prompts[idx],
        "output_mean": sum(outputs) // len(outputs), "output_p90": outputs[idx],
        "n": len(prompts), "source": str(log_dir),
    }


def rank(term: str, cat: dict[str, dict], prof: dict, epochs: int) -> int:
    """Cheapest catalogue models matching `term`, by cost for one model's run."""
    n = VARIANTS * epochs
    hits = [
        (episode_cost(p, prof["prompt_mean"], prof["output_mean"]) * n, mid, p)
        for mid, p in cat.items()
        if term.lower() in mid.lower() or term.lower() in p["name"].lower()
    ]
    if not hits:
        print(f"no catalogue entry matches {term!r}.")
        return 1
    hits.sort()
    print(f"cheapest matches for {term!r} -- {n} episodes ({epochs} epochs x {VARIANTS} variants):\n")
    print(f"  {'est. run':>9}  {'$/episode':>10}  {'$/Mtok in':>10}  {'$/Mtok out':>11}  model")
    for total, mid, p in hits[:20]:
        print(f"  {'$%.2f' % total:>9}  {'$%.4f' % (total / n):>10}  "
              f"{'$%.2f' % (p['prompt'] * 1e6):>10}  {'$%.2f' % (p['completion'] * 1e6):>11}  {mid}")
    if len(hits) > 20:
        print(f"  ... and {len(hits) - 20} more")
    return 0


def main() -> int:
    args = sys.argv[1:]

    def opt(flag, default=None):
        if flag in args:
            i = args.index(flag)
            if i + 1 < len(args):
                return args[i + 1]
        return default

    epochs = int(opt("--epochs", "10"))
    budget = float(opt("--budget", "0")) or None
    roster_path = Path(opt("--roster", str(ROOT / "tools" / "models.txt")))
    key = os.environ.get("OPENROUTER_API_KEY")

    prof = dict(PROFILE)
    if "--calibrate" in args:
        got = calibrate(Path(opt("--calibrate", "logs")))
        if got:
            prof = got
            print("calibrated token profile:")
            print(json.dumps(prof, indent=2))
            print()

    try:
        cat = catalogue(key)
    except Exception as exc:
        print(f"could not reach OpenRouter: {exc}")
        return 2

    if "--rank" in args:
        return rank(opt("--rank", ""), cat, prof, epochs)

    if not roster_path.exists():
        print(f"roster not found: {roster_path}")
        return 2
    roster = read_roster(roster_path)

    n = VARIANTS * epochs
    print(f"token profile: prompt mean {prof['prompt_mean']:,} / p90 {prof['prompt_p90']:,}, "
          f"output mean {prof['output_mean']:,} / p90 {prof['output_p90']:,}")
    print(f"  measured over {prof['n']} episodes ({prof['source']})")
    print(f"batch: {epochs} epochs x {VARIANTS} variants = {n} episodes per model\n")

    hdr = f"  {'expected':>9}  {'ceiling':>9}  {'$/episode':>10}  model"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))

    exp_total = ceil_total = 0.0
    unknown: list[str] = []
    for mid in roster:
        price = cat.get(mid)
        if price is None:
            unknown.append(mid)
            print(f"  {'?':>9}  {'?':>9}  {'?':>10}  {mid}   << unknown id")
            continue
        exp = episode_cost(price, prof["prompt_mean"], prof["output_mean"]) * n
        hi = episode_cost(price, prof["prompt_p90"], prof["output_p90"]) * n
        exp_total += exp
        ceil_total += hi
        print(f"  {'$%.2f' % exp:>9}  {'$%.2f' % hi:>9}  {'$%.4f' % (exp / n):>10}  {mid}")

    print("  " + "-" * (len(hdr) - 2))
    print(f"  {'$%.2f' % exp_total:>9}  {'$%.2f' % ceil_total:>9}  "
          f"{'':>10}  TOTAL over {len(roster) - len(unknown)} priced models")

    if unknown:
        print(f"\n{len(unknown)} unpriced id(s) -- resolve with "
              f"`python tools/check_models.py --search TERM`:")
        for mid in unknown:
            print(f"  {mid}")

    usage, limit = credit(key)
    if limit is not None:
        remaining = limit - (usage or 0)
        print(f"\nkey: ${usage or 0:.2f} used of ${limit:.2f} limit -- ${remaining:.2f} remaining")
        budget = budget or remaining

    if budget:
        print(f"\nagainst a ${budget:.2f} budget:")
        if ceil_total <= budget:
            print(f"  fits even at the p90 ceiling (${ceil_total:.2f}). Run it.")
        elif exp_total <= budget:
            print(f"  fits on expected cost (${exp_total:.2f}) but not at the p90 "
                  f"ceiling (${ceil_total:.2f}).")
            print(f"  Long episodes are the risk. Cut models before epochs -- a model")
            print(f"  with too few episodes to show six gaming hits proves nothing.")
        else:
            print(f"  DOES NOT FIT: expected ${exp_total:.2f} > ${budget:.2f}.")
            safe = int(budget / (exp_total / epochs)) if exp_total else 0
            print(f"  At this roster, ~{safe} epochs fits ({safe * VARIANTS} episodes/model).")
            print(f"  Or drop the most expensive rows above and re-run this estimate.")

    print("\nCaveat that the arithmetic cannot carry: one profile is applied to every")
    print(f"row, and it was measured on {prof.get('source', 'the built-in default')}.")
    print("Per-episode token use varies by an order of magnitude between models --")
    print("gemini-3.8-flash spent 1,001,117 input tokens per episode on this fixture")
    print("against grok-4.3's 45,493 -- so a row for a model unlike the ones measured")
    print("is a guess. A model that emits long reasoning traces bills them as output")
    print("and can exceed this by several times. Treat the first model of any new kind")
    print("as a probe: run one epoch, re-run --calibrate on its log, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
