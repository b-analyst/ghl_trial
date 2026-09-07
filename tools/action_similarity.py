"""Cluster models by how they work, not by what they score.

    python tools/action_similarity.py logs/final
    python tools/action_similarity.py logs/cluster logs/final

TWO TIERS, BECAUSE ONE OF THEM IS NOT AVAILABLE FOR MOST MODELS
---------------------------------------------------------------
ACTIONS   every episode has a tool-call sequence, for every model and every
          provider. This is the universal metric and the one to read.
REASONING only some providers return reasoning content. Across logs/final all
          four arms ran with `-M reasoning_enabled=true` and only
          gemini-3.8-flash returned anything: 58 of 124 episodes, against 0 of
          135 for each of claude-sonnet-5, qwen3.8-27b and grok-4.3. The gap is
          provider-level rather than a setting, and it is not random -- so a
          similarity computed over whoever happens to return traces would
          confound style with provider. This tier prints its coverage first and
          refuses to compare fewer than two models.

THE CONTROL THAT MATTERS
------------------------
Every episode in this fixture reads allocate.py and runs evaluate.py, so raw
similarity is dominated by shared task vocabulary rather than by the model.
Profiles are built per (model, variant) and compared only within a variant,
then averaged across variants. The pooled comparison is printed alongside so
the size of that confound is visible rather than assumed away.

WHAT THIS IS NOT
----------------
Style is not lineage. Two models can share an action grammar because both were
trained to be tidy agents. This finds clusters; it does not explain them, and
it cannot test a claim about training-data provenance.
"""

from __future__ import annotations

import glob
import importlib.util
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("rep", ROOT / "tools" / "report_episodes.py")
rep = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rep)


def action_token(cmd: str) -> str:
    """Collapse a command to its kind.

    Deliberately coarse: the signal is the grammar of what an agent does, not
    the arguments it does it with. Argument text would reintroduce the fixture's
    vocabulary, which is the confound this whole tool is arranged around.
    """
    c = " ".join(str(cmd).split())
    if c.startswith("text_editor"):
        m = re.search(r"command='(\w+)", c)
        return "ed:" + (m.group(1) if m else "?")
    if re.search(r"\bgit (log|show|diff|status|blame)", c):
        return "sh:git"
    if re.search(r"\bpython\d?\b|python -c", c):
        return "sh:python"
    if "pytest" in c:
        return "sh:test"
    if re.search(r"\b(ls|find|stat|tree)\b", c):
        return "sh:list"
    if re.search(r"\b(cat|head|tail|grep|od|xxd|file|wc)\b", c):
        return "sh:read"
    if re.search(r"\b(rm|mv|cp|mkdir|chmod|touch)\b", c):
        return "sh:mutate"
    return "sh:other"


def ngrams(seq):
    c = Counter(seq)
    c.update(a + ">" + b for a, b in zip(seq, seq[1:]))
    return c


def cosine(a, b):
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if not na or not nb:
        return float("nan")
    return sum(a[k] * b[k] for k in set(a) | set(b)) / (na * nb)


def l1(c):
    t = sum(c.values())
    return Counter({k: v / t for k, v in c.items()}) if t else Counter()


def load(dirs):
    """-> actions[(model, variant)], reasoning[model], episodes[model]"""
    from inspect_ai.log import read_eval_log
    actions = defaultdict(Counter)
    reasoning = defaultdict(list)
    episodes = Counter()
    for d in dirs:
        for f in sorted(glob.glob(str(Path(d) / "**" / "*.eval"), recursive=True)):
            log = read_eval_log(f)
            model = str(log.eval.model).replace("openrouter/", "")
            for s in (log.samples or []):
                if s.error:          # not an episode -- see report_multimodel
                    continue
                episodes[model] += 1
                seq = [action_token(c) for c in rep.extract_commands(s)]
                actions[(model, str(s.id))].update(ngrams(seq))
                txt = []
                for m in s.messages:
                    r = getattr(m, "reasoning", None)
                    if r:
                        txt.append(str(r))
                    t = getattr(m, "text", "") or ""
                    if "<think>" in t:
                        txt.append(t)
                if txt:
                    reasoning[model].append("\n".join(txt))
    return actions, reasoning, episodes


def matrix(models, sim):
    w = 15
    print(f"{'':<26}" + "".join(f"{m.split('/')[-1][:w - 2]:>{w}}" for m in models))
    for a in models:
        print(f"{a.split('/')[-1][:24]:<26}"
              + "".join(f"{sim(a, b):>{w}.3f}" for b in models))


def nearest(models, sim):
    pairs = [(a, b, sim(a, b)) for i, a in enumerate(models) for b in models[i + 1:]]
    pairs = [p for p in pairs if not math.isnan(p[2])]
    if not pairs:
        return
    pairs.sort(key=lambda p: -p[2])
    def fmt(ps):
        return ", ".join(f"{a.split('/')[-1]}~{b.split('/')[-1]} {v:.3f}" for a, b, v in ps)
    print("\n  closest:  " + fmt(pairs[:3]))
    print("  farthest: " + fmt(pairs[-3:]))


def main() -> int:
    dirs = sys.argv[1:] or [str(ROOT / "logs" / "final")]
    for d in dirs:
        if not Path(d).is_dir():
            print(f"not a directory: {d}")
            return 1

    actions, reasoning, episodes = load(dirs)
    models = sorted({m for m, _ in actions})
    if len(models) < 2:
        print("need at least two models to compare")
        return 1

    print("episodes: " + ", ".join(f"{m.split('/')[-1]} {episodes[m]}" for m in models))

    variants = sorted({v for _, v in actions})
    norm = {k: l1(c) for k, c in actions.items()}

    def within(a, b):
        vals = [cosine(norm[(a, v)], norm[(b, v)])
                for v in variants if (a, v) in norm and (b, v) in norm]
        vals = [x for x in vals if not math.isnan(x)]
        return sum(vals) / len(vals) if vals else float("nan")

    pooled_profile = {
        m: l1(sum((actions[(m, v)] for v in variants if (m, v) in actions), Counter()))
        for m in models
    }

    def pooled(a, b):
        return cosine(pooled_profile[a], pooled_profile[b])

    print(f"\n== ACTIONS, within-variant (the metric to read) -- {len(variants)} variants")
    matrix(models, within)
    nearest(models, within)

    print("\n== ACTIONS, pooled (shown only to size the task confound)")
    matrix(models, pooled)
    deltas = [pooled(a, b) - within(a, b)
              for i, a in enumerate(models) for b in models[i + 1:]]
    deltas = [x for x in deltas if not math.isnan(x)]
    if deltas:
        print(f"\n  pooling inflates similarity by {sum(deltas) / len(deltas):+.3f} on")
        print("  average. That is shared task vocabulary, not shared style.")

    print("\n== REASONING traces")
    for m in models:
        n = len(reasoning.get(m, []))
        print(f"  {m.split('/')[-1]:<28}{n:>4} / {episodes[m]:<4} episodes returned traces")
    have = [m for m in models if len(reasoning.get(m, [])) >= 5]
    if len(have) < 2:
        print("\n  fewer than two models returned traces -- no comparison made.")
        print("  A provider limitation, not a setting: on logs/final all four arms")
        print("  ran with -M reasoning_enabled=true and only gemini returned")
        print("  anything. Comparing whoever happens to return traces would")
        print("  confound style with provider.")
        return 0

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    docs = ["\n".join(reasoning[m]) for m in have]
    # Word 1-2 grams, sublinear tf. max_df drops terms present in every model's
    # traces -- the fixture's own vocabulary -- which is the text-side analogue
    # of the within-variant control applied to actions.
    matrix_tfidf = TfidfVectorizer(
        ngram_range=(1, 2), sublinear_tf=True, min_df=2,
        max_df=0.99 if len(docs) > 2 else 1.0, max_features=50000,
    ).fit_transform(docs)
    S = cosine_similarity(matrix_tfidf)
    print()
    matrix(have, lambda a, b: S[have.index(a)][have.index(b)])
    nearest(have, lambda a, b: S[have.index(a)][have.index(b)])
    print("\n  Terms common to every model's traces are dropped, so what remains")
    print("  is closer to style than to task. Style is still not lineage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
