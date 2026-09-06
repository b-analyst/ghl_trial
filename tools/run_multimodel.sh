#!/bin/sh
# Run the existing fixture across the model roster.
#
#   OPENROUTER_API_KEY=... sh tools/run_multimodel.sh [epochs]
#
# Defaults to 10 epochs, so 7 variants x 10 = 70 episodes per model. The pilot
# ran 161 on one model; 70 across six models buys the between-model comparison
# that the pilot could not make, which is the point of this run.
#
# Each model writes to its own log directory, so a crash costs one model rather
# than the batch, and a rerun of one model does not disturb the others.
#
# The key is read from the environment. It is never echoed, never written into
# a log path, and never committed -- see docs/running.md.

set -e

ROOT=$(cd "$(dirname "$0")/.." && pwd)
EPOCHS=${1:-10}
ROSTER="$ROOT/tools/models.txt"
OUT="$ROOT/logs/multimodel"

if [ -z "$OPENROUTER_API_KEY" ]; then
  echo "OPENROUTER_API_KEY is not set."
  echo "  sh:  export OPENROUTER_API_KEY=sk-or-..."
  exit 2
fi

echo "validating roster..."
python3 "$ROOT/tools/check_models.py" "$ROSTER" || {
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
  if inspect eval "$ROOT/adapters/inspect/inspect_task.py" \
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
echo "  python3 tools/report_multimodel.py logs/multimodel"
