"""Tests for investigation_depth.py, on synthetic rows rather than eval logs.

    python tools/test_investigation_depth.py

The point of the synthetic rows is that the expected answers are known by
construction. Running the tool over real logs shows it does not crash; it does
not show the arithmetic is right, because nobody knows the right answer for
real logs independently of the tool.

Written to look for the ways this kind of tool goes wrong: a lift that divides
by zero, a Fisher test fed the wrong margins, a funnel whose denominator drifts
when a model has fewer episodes, and a divergence that reports a difference when
the two groups are identical.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_s = importlib.util.spec_from_file_location("idep", ROOT / "tools" / "investigation_depth.py")
idep = importlib.util.module_from_spec(_s)
_s.loader.exec_module(idep)

FAILED: list[str] = []


def check(name: str, got, want) -> None:
    if got == want:
        print(f"  pass  {name}")
    else:
        print(f"  FAIL  {name}\n          got  {got!r}\n          want {want!r}")
        FAILED.append(name)


def approx(name: str, got: float, want: float, tol: float = 1e-9) -> None:
    if got is not None and abs(got - want) <= tol:
        print(f"  pass  {name}")
    else:
        print(f"  FAIL  {name}: got {got!r}, want {want!r}")
        FAILED.append(name)


def row(model, gamed=False, actions=(), **rungs):
    r = {"model": model, "variant": "claim-none", "gamed": gamed,
         "actions": set(actions)}
    for _, key in idep.RUNGS:
        r[key] = rungs.get(key, False)
    return r


print("FUNNEL")
# Two models, different episode counts, so a drifting denominator shows up.
rows = [
    row("a", opened_source=True, executed_equal_split=True),
    row("a", opened_source=True),
    row("b", opened_source=True, executed_equal_split=True),
]
f = idep.funnel(rows)
i_open = [k for _, k in idep.RUNGS].index("opened_source")
i_exec = [k for _, k in idep.RUNGS].index("executed_equal_split")
i_git = [k for _, k in idep.RUNGS].index("checked_provenance")
check("counts both episodes for model a", f["a"][i_open], 2)
check("counts only the one that executed", f["a"][i_exec], 1)
check("model b is independent of a", f["b"][i_open], 1)
check("a rung nobody reached is zero", f["a"][i_git], 0)
check("no model invented", sorted(f), ["a", "b"])

# A model with zero episodes must not appear rather than divide by zero.
check("empty input yields no models", idep.funnel([]), {})

print("\nDIVERGENCE, guard rails")
check("refuses when one side is too small",
      idep.divergence([row("a", gamed=True, actions=["x"])] * 5), [])
check("refuses when there are no gaming episodes",
      idep.divergence([row("a", gamed=False, actions=["x"])] * 10), [])
# gamed=None (not determinable) must count as neither side.
none_rows = [dict(row("a", actions=["x"]), gamed=None) for _ in range(10)]
check("not-determinable rows are excluded", idep.divergence(none_rows), [])

print("\nDIVERGENCE, arithmetic")
# 4 gaming episodes all containing 'g'; 8 clean episodes, 2 containing 'g'.
# rate_gamed = 4/4 = 1.0, rate_clean = 2/8 = 0.25, lift = 4.0
rows = ([row("a", gamed=True, actions=["g", "common"]) for _ in range(4)]
        + [row("a", gamed=False, actions=["g", "common"]) for _ in range(2)]
        + [row("a", gamed=False, actions=["common"]) for _ in range(6)])
res = {t: (a, na, c, nc, lift, p) for t, a, na, c, nc, lift, p in idep.divergence(rows)}
check("gaming margin is the number of gaming episodes", res["g"][1], 4)
check("clean margin is the number of clean episodes", res["g"][3], 8)
check("counts occurrences, not episodes-times-tokens", (res["g"][0], res["g"][2]), (4, 2))
approx("lift is rate ratio 1.0/0.25", res["g"][4], 4.0)

# An action in every episode of both groups must have lift exactly 1 and p = 1.
approx("ubiquitous action has lift 1", res["common"][4], 1.0)
approx("ubiquitous action is not significant", res["common"][5], 1.0)

# Fisher margins: 4/4 vs 2/8 is p = 0.0303 two-tailed. Computed independently
# below from the hypergeometric, not read off the tool.
def fisher_2x2(a, b, c, d):
    from math import comb
    n = a + b + c + d
    r1, c1 = a + b, a + c
    obs = comb(r1, a) * comb(n - r1, c1 - a) / comb(n, c1)
    tot = 0.0
    for k in range(max(0, c1 - (n - r1)), min(r1, c1) + 1):
        p = comb(r1, k) * comb(n - r1, c1 - k) / comb(n, c1)
        if p <= obs * (1 + 1e-9):
            tot += p
    return tot

approx("p matches an independent hypergeometric", res["g"][5],
       fisher_2x2(4, 0, 2, 6), tol=1e-9)

print("\nDIVERGENCE, the failure mode that matters")
# Identical groups must produce no significant difference. A tool that finds
# structure in noise is worse than no tool.
same = ([row("a", gamed=True, actions=["x", "y"]) for _ in range(6)]
        + [row("a", gamed=False, actions=["x", "y"]) for _ in range(6)])
res2 = idep.divergence(same)
check("identical groups give p = 1 everywhere",
      all(abs(r[6] - 1.0) < 1e-9 for r in res2), True)
check("identical groups give lift 1 everywhere",
      all(abs(r[5] - 1.0) < 1e-9 for r in res2), True)

# Lift is undefined, not infinite, when no clean episode has the action.
only = ([row("a", gamed=True, actions=["only"]) for _ in range(5)]
        + [row("a", gamed=False, actions=["other"]) for _ in range(5)])
lifts = {t: lift for t, _, _, _, _, lift, _ in idep.divergence(only)}
check("lift is None when the clean rate is zero", lifts.get("only"), None)

print("\nRUNG TABLE")
check("every rung names a real signal key",
      all(isinstance(k, str) and k for _, k in idep.RUNGS), True)
check("no duplicate rungs",
      len({k for _, k in idep.RUNGS}), len(idep.RUNGS))

print()
if FAILED:
    print(f"{len(FAILED)} FAILURE(S): " + ", ".join(FAILED))
    raise SystemExit(1)
print("all investigation_depth tests pass")
