#!/bin/sh
# Run the experiment: every cell, every model in models.txt, one command.
#
#   export OPENROUTER_API_KEY=sk-or-...
#   EPOCHS=20 sh run.sh
#
# Build both images first:
#   docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
#   docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .
#
# An arm whose logs already exist is skipped, so an interrupted batch resumes.
set -eu
cd "$(dirname "$0")"

EPOCHS="${EPOCHS:-20}"
OUT="logs/all"
PY="${PYTHON:-python}"

[ -n "${OPENROUTER_API_KEY:-}" ] || { echo "OPENROUTER_API_KEY is not set" >&2; exit 2; }
for img in honeypot-scaffold honeypot-scaffold-noclaim; do
    docker image inspect "$img" >/dev/null 2>&1 || { echo "$img is not built" >&2; exit 2; }
done
"$PY" check.py >/dev/null || { echo "check.py failed -- run it to see why" >&2; exit 2; }

CELLS=$("$PY" -c "import json;print(len(json.load(open('variants.json'))['variants']))")
PER_MODEL=$((CELLS * EPOCHS))
echo "$CELLS cells x $EPOCHS epochs = $PER_MODEL episodes per model"
mkdir -p "$OUT"
# The key's own spend counter, before and after every arm, so the ledger shows
# what OpenRouter actually billed next to what the tokens compute to.
"$PY" cost.py --billed --note "before batch" --ledger "$OUT/ledger.txt" || true

for model in $(grep -v '^[[:space:]]*#' models.txt | grep -v '^[[:space:]]*$'); do
    dest="$OUT/$(printf '%s' "$model" | tr '/:.' '___')"
    if [ -n "$(ls -A "$dest" 2>/dev/null || true)" ]; then
        echo "skip  $model  (logs present)"
        continue
    fi
    echo "=== $model ==="
    mkdir -p "$dest"
    # The task path must be relative: Inspect globs it, and Python 3.14 rejects
    # an absolute glob.
    "$PY" -m inspect_ai eval adapters/inspect/inspect_task.py \
        --model "openrouter/$model" --epochs "$EPOCHS" --log-dir "$dest" || true

    # inspect can exit 0 having run nothing, so count what actually landed.
    # Nothing at all: delete the directory so the skip above does not skip it.
    n=$("$PY" -c "
import glob,sys
from inspect_ai.log import read_eval_log
print(sum(1 for f in glob.glob('$dest/*.eval') for s in (read_eval_log(f).samples or []) if not s.error))")
    if [ "$n" -eq 0 ]; then
        echo "FAILED $model -- no episodes"; echo "$model" >>"$OUT/failed.txt"; rm -rf "$dest"
    elif [ "$n" -lt "$PER_MODEL" ]; then
        echo "SHORT  $model -- $n of $PER_MODEL, kept"; echo "$model" >>"$OUT/failed.txt"
    else
        echo "done   $model -- $n episodes"
    fi
    "$PY" cost.py --billed --note "after $model" --ledger "$OUT/ledger.txt" || true
done

echo
"$PY" cost.py --spent "$OUT" || true
echo
echo "then:  $PY scrub.py $OUT && $PY report.py $OUT"
