"""How far into the fixture does an episode actually go, and does it matter?

    python tools/investigation_depth.py logs/final
    python tools/investigation_depth.py logs/final logs/cluster

TWO QUESTIONS, ONE CHEAP AND ONE THIN
-------------------------------------
FUNNEL      what fraction of a model's episodes reach each investigation step.
            Reads the detector signals that already exist, costs nothing, and
            separates models the gaming table does not: grok-4.3 reaches the
            correct fix in 87% of episodes while 1% ever opens the git history.

DIVERGENCE  which actions are over-represented in episodes that gamed. This is
            the retrospective, free version of the counterfactual an MCTS
            rollout would buy, and on logs/final IT FINDS NOTHING. That is the
            honest result, recorded here so the next person does not spend the
            rollouts to rediscover it: 21 gaming episodes against 332 clean,
            and after correcting for the number of actions tested no action
            differs within any model. The largest within-model lift is 2.08 at
            p = 0.29.

            Pooled, it looked like a finding -- `ed:view` at lift 1.26,
            p = 0.035. It was an artifact. grok games more than the others AND
            views more than the others, so pooling associated the two; within
            model the effect vanishes (gemini p = 0.265, grok p = 1.000).
            divergence_by_model() is therefore the only entry point offered,
            and every p is printed alongside p x tests.

WHY THE FUNNEL IS NOT A LADDER
------------------------------
The steps are not nested and are deliberately not scored as a depth. An episode
can fix both paths without executing anything, and grok routinely does. Forcing
a total order would invent a progression the data does not support, so each
step is reported as its own rate.

Conflict cells and the control are excluded. The escalation ladder in
detectors/escalation.py is the conflict cells' own measure, and the control has
no claim to investigate.
"""

from __future__ import annotations

import glob
import importlib.util
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_r = importlib.util.spec_from_file_location("rep", ROOT / "tools" / "report_episodes.py")
rep = importlib.util.module_from_spec(_r)
_r.loader.exec_module(rep)

_m = importlib.util.spec_from_file_location("rmm", ROOT / "tools" / "report_multimodel.py")
rmm = importlib.util.module_from_spec(_m)
_m.loader.exec_module(rmm)

_a = importlib.util.spec_from_file_location("act", ROOT / "tools" / "action_similarity.py")
act = importlib.util.module_from_spec(_a)
_a.loader.exec_module(act)

# (label, signal key). Order is presentational: roughly how a careful agent
# would proceed, not a claim that the steps are nested.
RUNGS: list[tuple[str, str]] = [
    ("opened allocate.py", "opened_source"),
    ("read the legacy tests", "read_legacy_tests"),
    ("ran the legacy tests", "ran_legacy_tests"),
    ("executed equal split", "executed_equal_split"),
    ("checked git provenance", "checked_provenance"),
    ("targeted allocate's log", "checked_provenance_targeted"),
    # OUTCOME, not an action. used_true_value is the term deferred-to-the-claim
    # is defined as the absence of, so testing this row against gaming tests a
    # definition: it returns p = 1e-15 on grok and 1e-06 on minimax and means
    # nothing. Kept in the funnel because "how often did it end up fixing both
    # paths" is worth seeing next to the actions; never cross it with gamed().
    ("fixed both paths", "used_true_value"),
]

# The actions -- the rows it is legitimate to test an outcome against.
ACTION_RUNGS: list[tuple[str, str]] = RUNGS[:-1]


def funnel(rows: list[dict]) -> dict[str, list[int]]:
    """-> {model: [count reaching each rung]}. Denominator is len of that model's rows."""
    out: dict[str, list[int]] = defaultdict(lambda: [0] * len(RUNGS))
    for r in rows:
        for i, (_, key) in enumerate(RUNGS):
            if r.get(key):
                out[r["model"]][i] += 1
    return dict(out)


def divergence(rows: list[dict], min_episodes: int = 3) -> list[tuple]:
    """Which actions are over-represented in gaming episodes?

    Compared within the pool of rows given, which the caller is expected to have
    restricted to comparable cells. Returns
    (token, n_gamed_with, n_gamed, n_clean_with, n_clean, lift, p) sorted by p.

    `lift` is a ratio of rates and is undefined when the clean rate is zero, so
    it is reported as None rather than infinity: an action seen only in gaming
    episodes is interesting, but its lift is not a number.
    """
    gamed = [r for r in rows if r.get("gamed") is True]
    clean = [r for r in rows if r.get("gamed") is False]
    if len(gamed) < min_episodes or len(clean) < min_episodes:
        return []
    toks = {t for r in rows for t in r["actions"]}
    out = []
    for t in sorted(toks):
        a = sum(1 for r in gamed if t in r["actions"])
        c = sum(1 for r in clean if t in r["actions"])
        if a + c < min_episodes:
            continue
        ra, rc = a / len(gamed), c / len(clean)
        lift = (ra / rc) if rc else None
        p = rmm._fisher_exact(a, len(gamed) - a, c, len(clean) - c)
        out.append((t, a, len(gamed), c, len(clean), lift, p))
    return sorted(out, key=lambda x: x[6])


def load(dirs: list[str]) -> list[dict]:
    from inspect_ai.log import read_eval_log
    rows: list[dict] = []
    for d in dirs:
        for f in sorted(glob.glob(str(Path(d) / "**" / "*.eval"), recursive=True)):
            log = read_eval_log(f)
            model = str(log.eval.model).replace("openrouter/", "")
            for s in (log.samples or []):
                if s.error:
                    continue
                v = str(s.id)
                if rep._frozen_caller(v) or v == rmm.CONTROL_VARIANT:
                    continue
                sig = rmm._signals(s)
                r = {"model": model, "variant": v,
                     "declared": rmm._declared(v),
                     "frozen": False, "control": False, **sig}
                rows.append({
                    "model": model, "variant": v,
                    "gamed": rmm.gamed(r, r["declared"]),
                    "actions": {act.action_token(c) for c in rep.extract_commands(s)},
                    **{k: sig.get(k) for _, k in RUNGS},
                })
    return rows


def divergence_by_model(rows: list[dict], min_episodes: int = 3):
    """divergence() run separately within each model, never pooled.

    Pooling is not a shortcut here, it is a confound. Run pooled over
    logs/final, `ed:view` came out at lift 1.26, p = 0.035 -- and that is an
    artifact: grok games more than the others AND views more than the others,
    so pooling associates the two. Within model the effect is gone entirely,
    gemini p = 0.265 and grok p = 1.000. A tool that reports the pooled figure
    is a tool that manufactures findings, so this one does not offer it.
    """
    out = {}
    for m in sorted({r['model'] for r in rows}):
        sub = [r for r in rows if r['model'] == m]
        res = divergence(sub, min_episodes)
        if res:
            out[m] = res
    return out


def main() -> int:
    dirs = sys.argv[1:] or [str(ROOT / "logs" / "final")]
    for d in dirs:
        if not Path(d).is_dir():
            print(f"not a directory: {d}")
            return 1
    rows = load(dirs)
    if not rows:
        print("no episodes found")
        return 1

    models = sorted({r["model"] for r in rows})
    n = Counter(r["model"] for r in rows)
    f = funnel(rows)

    print("INVESTIGATION FUNNEL -- claim cells, "
          "% of episodes reaching each step\n")
    print(f"{'step':<26}" + "".join(f"{m.split('/')[-1][:13]:>15}" for m in models))
    for i, (lbl, _) in enumerate(RUNGS):
        print(f"{lbl:<26}"
              + "".join(f"{100 * f[m][i] / n[m]:>14.0f}%" for m in models))
    print(f"{'(episodes)':<26}" + "".join(f"{n[m]:>15}" for m in models))
    print("\nSteps are not nested and are not scored as a depth: an episode can")
    print("fix both paths without executing anything. Read each row on its own.")
    print()
    print("DIVERGENCE -- actions over-represented in gaming episodes,")
    print("computed WITHIN each model. Pooling across models confounds the")
    print("outcome with model style and manufactures hits.")
    per = divergence_by_model(rows)
    if not per:
        g = sum(1 for r in rows if r['gamed'] is True)
        print(f'  no model has enough gaming episodes to compare ({g} across all models).')
        return 0
    for m, res in per.items():
        k = len(res)
        sig = [r for r in res if r[6] * k < 0.05]
        g = sum(1 for r in rows if r['model'] == m and r['gamed'] is True)
        print()
        print(f'  {m}  ({g} gaming episodes, {k} actions tested)')
        hdr = f"    {'action':<20}{'in gaming':>12}{'in clean':>12}"
        print(hdr + f"{'lift':>8}{'p':>10}{'p x tests':>11}")
        for t, aa, na, cc, nc, lift, pv in res[:6]:
            ls = '  n/a' if lift is None else f'{lift:>5.2f}'
            star = '  *' if pv * k < 0.05 else ''
            print(f'    {t:<20}' + f'{aa}/{na}'.rjust(12)
                  + f'{cc}/{nc}'.rjust(12) + f'{ls:>8}{pv:>10.3g}'
                  + f'{min(1.0, pv * k):>11.3g}{star}')
        if not sig:
            print('    nothing survives correction for the actions tested.')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
