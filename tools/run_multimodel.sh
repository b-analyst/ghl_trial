#!/bin/sh
# Run the existing fixture across the model roster.
#
#   OPENROUTER_API_KEY=... sh tools/run_multimodel.sh [epochs] [roster]
#
# Defaults to 10 epochs and tools/models.txt. For a capped key use the budget
# roster, which is three non-Claude models sized for about $10:
#
#   sh tools/run_multimodel.sh 10 tools/models-smoke.txt
#
# Price it first -- `python3 tools/estimate_cost.py --roster <roster>` reads
# live pricing and the key's remaining credit. 7 variants x 10 epochs = 70
# episodes per model.
#
# Each model writes to its own log directory, so a crash costs one model rather
# than the batch, and a rerun of one model does not disturb the others.
#
# The key is read from the environment. It is never echoed, never written into
# a log path, and never committed -- see docs/running.md.

set -e

ROOT=$(cd "$(dirname "$0")/.." && pwd)
EPOCHS=${1:-10}
ROSTER=${2:-"$ROOT/tools/models.txt"}
OUT="$ROOT/logs/multimodel"

# Module invocation, not the bare `inspect` console script: pip puts that in a
# bin/Scripts directory that is often off PATH. `python -m inspect_ai` is the
# same entry point and always resolves to the interpreter holding the package.
PY=${PYTHON:-python3}

if [ -z "$OPENROUTER_API_KEY" ]; then
  echo "OPENROUTER_API_KEY is not set."
  echo "  sh:  export OPENROUTER_API_KEY=sk-or-..."
  exit 2
fi

echo "roster: $ROSTER"
echo "validating..."
"$PY" "$ROOT/tools/check_models.py" "$ROSTER" || {
  echo "roster has unknown ids -- fix tools/models.txt before running."
  exit 2
}

mkdir -p "$OUT"

# Strip comments and blanks the same way check_models.py does.
sed -e 's/#.*//' -e '/^[[:space:]]*$/d' "$ROSTER" | while read -r MODEL; do
  MODEL=$(echo "$MODEL" | tr -d '[:space:]')
  [ -z "$MODEL" ] && continue

  SLUG=$(echo "$MODEL" | tr '/:.' '___')
  DEST="$OUT/$SLUG"

  if [ -d "$DEST" ] && [ -n "$(ls -A "$DEST" 2>/dev/null)" ]; then
    echo "skip  $MODEL  (logs already in $DEST -- delete to rerun)"
    continue
  fi

  echo ""
  echo "=== $MODEL  ($EPOCHS epochs) ==="
  mkdir -p "$DEST"

  # A failure on one model must not abort the batch: a provider outage or a
  # refused model is a fact about that cell, not a reason to lose the rest.
  if "$PY" -m inspect_ai eval "$ROOT/adapters/inspect/inspect_task.py" \
      --model "openrouter/$MODEL" \
      --epochs "$EPOCHS" \
      --log-dir "$DEST"; then
    echo "done  $MODEL"
  else
    echo "FAILED $MODEL -- continuing with the rest of the roster" >&2
    echo "$MODEL" >> "$OUT/failed.txt"
  fi
done

echo ""
echo "all models attempted. report with:"
echo "  python3 tools/report_multimodel.py logs/multimodel --baseline logs"
echo ""
echo "(--baseline folds in the pilot's Claude episodes, which are already paid"
echo " for and are the arm this batch is measured against.)"
