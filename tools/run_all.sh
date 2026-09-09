#!/bin/sh
# Run the experiment: four cells, every model on the roster, one command.
#
#   export OPENROUTER_API_KEY=sk-or-...
#   sh tools/run_all.sh            # 10 epochs per cell
#   EPOCHS=20 sh tools/run_all.sh  # 20, which is what a per-model claim needs
#
# The POSIX twin of tools/run_all.ps1. Same roster, same checks, same layout.
#
# THE DESIGN, read from variants.json rather than hardcoded here:
#
#                     no false claim      false claim
#     no conflict     control             claim
#     conflict        conflict            claim-conflict
#
# EPOCHS. Ten establishes the effect pooled across the roster and is not enough
# per model -- control 0/10 against conflict 3/10 is Fisher p = 0.21, while
# 0/20 against 7/20 is p = 0.0083.
#
# BUILD BOTH IMAGES FIRST. The claim-free cells have their own:
#   docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
#   docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim \
#       -t honeypot-scaffold-noclaim .
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT"

EPOCHS="${EPOCHS:-10}"
OUT="logs/all"
PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null 2>&1 || PY=python

if [ -z "${OPENROUTER_API_KEY:-}" ]; then
    echo "OPENROUTER_API_KEY is not set." >&2
    echo "  export OPENROUTER_API_KEY=sk-or-..." >&2
    exit 2
fi

for img in honeypot-scaffold honeypot-scaffold-noclaim; do
    docker image inspect "$img" >/dev/null 2>&1 || {
        echo "$img is not built. See the header of this file." >&2; exit 2; }
done

echo "checking the fixture before spending anything..."
for c in tools/audit_fixture.py tools/check_staging.py \
         tools/check_detectors.py tools/test_open_scorer.py; do
    "$PY" "$c" >/dev/null || { echo "$c FAILED -- run it directly" >&2; exit 2; }
done
echo "  ok"

# Cells come from variants.json, never from a list kept in step by hand.
CELLS=$("$PY" -c "import json;print(len(json.load(open('variants.json',encoding='utf-8'))['variants']))")
PER_MODEL=$((CELLS * EPOCHS))
echo ""
echo "$CELLS cells x $EPOCHS epochs = $PER_MODEL episodes per model"

mkdir -p "$OUT"
# Comments and blanks stripped before the loop, not inside it.
ROSTER=$(grep -v '^[[:space:]]*#' tools/models.txt | grep -v '^[[:space:]]*$')

for model in $ROSTER; do
    slug=$(printf '%s' "$model" | tr '/:.' '___')
    dest="$OUT/$slug"
    if [ -n "$(ls -A "$dest" 2>/dev/null || true)" ]; then
        echo "  skip  $model  -- logs already present, delete to rerun"
        continue
    fi
    echo ""
    echo "=== $model : $PER_MODEL episodes ==="
    mkdir -p "$dest"

    # The task path MUST be relative. inspect globs it, and Python 3.14's
    # pathlib refuses an absolute glob pattern outright.
    set +e
    "$PY" -m inspect_ai eval "adapters/inspect/inspect_task.py" \
        --model "openrouter/$model" --epochs "$EPOCHS" --log-dir "$dest"
    eval_exit=$?
    # inspect can exit 0 having completed nothing, so read the log instead.
    # 0 complete, 2 short but real, 1 nothing worth keeping. Only 1 deletes.
    "$PY" tools/check_arm.py "$dest" "$PER_MODEL"
    arm=$?
    set -e

    if [ "$eval_exit" -ne 0 ] || [ "$arm" -ne 0 ]; then
        echo "FAILED $model -- continuing"
        echo "$model" >> "$OUT/failed.txt"
        [ "$arm" -eq 1 ] && rm -rf "$dest"
    else
        echo "done  $model"
    fi
done

echo ""
echo "done. Then:"
echo "  $PY tools/scrub_check.py logs/all"
echo "  $PY tools/outcome_tree.py logs/all --by-model"
echo "  $PY tools/report_multimodel.py logs/all"
