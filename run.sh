#!/bin/sh
# Run the experiment: every cell, every model in models.txt, one command.
#
#   export OPENROUTER_API_KEY=sk-or-...
#   EPOCHS=20 sh run.sh
#   APPEND=1 EPOCHS=10 sh run.sh     add epochs to arms that already have logs
#
# Build both images first:
#   docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
#   docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .
#
# An arm whose logs already exist is skipped, so an interrupted batch resumes.
set -eu
cd "$(dirname "$0")"

EPOCHS="${EPOCHS:-20}"
APPEND="${APPEND:-}"
OUT="logs/all"
PY="${PYTHON:-python}"

# inspect can exit 0 having run nothing, so what landed is counted, not trusted.
count_episodes() {
    "$PY" -c "
import glob
from inspect_ai.log import read_eval_log
print(sum(1 for f in glob.glob('$1/*.eval') for s in (read_eval_log(f).samples or []) if not s.error))"
}

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
    before=0
    if [ -n "$(ls -A "$dest" 2>/dev/null || true)" ]; then
        if [ -z "$APPEND" ]; then
            echo "skip  $model  (logs present; APPEND=1 to add epochs)"
            continue
        fi
        before=$(count_episodes "$dest")
    fi
    echo "=== $model ==="
    mkdir -p "$dest"
    # The task path must be relative: Inspect globs it, and Python 3.14 rejects
    # an absolute glob.
    "$PY" -m inspect_ai eval adapters/inspect/inspect_task.py \
        --model "openrouter/$model" --epochs "$EPOCHS" --log-dir "$dest" || true

    n=$(count_episodes "$dest")
    new=$((n - before))
    if [ "$new" -eq 0 ]; then
        echo "FAILED $model -- no new episodes"; echo "$model" >>"$OUT/failed.txt"
        # An empty directory would be skipped next time; one with earlier logs stays.
        [ "$before" -eq 0 ] && rm -rf "$dest"
    elif [ "$new" -lt "$PER_MODEL" ]; then
        echo "SHORT  $model -- $new of $PER_MODEL new, kept ($n total)"; echo "$model" >>"$OUT/failed.txt"
    else
        echo "done   $model -- $new new episodes, $n total"
    fi
    "$PY" cost.py --billed --note "after $model" --ledger "$OUT/ledger.txt" || true
done

echo
"$PY" cost.py --spent "$OUT" || true
echo
echo "then:  $PY scrub.py $OUT && $PY report.py $OUT"
