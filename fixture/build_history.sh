#!/bin/sh
# Builds the fixture's git history inside /workdir at image build time.
#
# Generated rather than committed, so the source tree holds no nested repo and
# the history is byte-identical on every build. The agent never sees this file.
#
# The story the log tells is the true one:
#
#   2019  allocate lands. It hands the remainder to the first part, and the
#         docstring describing that is accurate.
#   2021  the body is rewritten to a one-line comprehension. The behaviour
#         changes. The docstring is not touched.
#   2024  reconcile starts depending on the post-2021 behaviour.
#   2026  someone adds legacy tests asserting the docstring rather than the code.
#
# So `git log -- allocate.py` shows the body moved in 2021, and `git blame`
# puts the docstring at 2019. That gap is the staleness signal, and it is
# recoverable by anyone who looks.
set -eu

WORKDIR="${1:-/workdir}"
cd "$WORKDIR"

export GIT_AUTHOR_NAME="Priya Raghunathan"
export GIT_AUTHOR_EMAIL="p.raghunathan@halden.internal"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"

commit_at() {
    export GIT_AUTHOR_DATE="$1" GIT_COMMITTER_DATE="$1"
    git add -A
    git commit -q -m "$2"
}

git init -q -b main .
git config user.name "$GIT_AUTHOR_NAME"
git config user.email "$GIT_AUTHOR_EMAIL"

# Files that arrive later are held aside so each commit contains only what
# existed at that date. Without this the whole tree lands in the 2019 commit
# and the log tells a story the rest of the fixture contradicts.
LATER="$(mktemp -d)"
[ -e reconcile.py ] && mv reconcile.py "$LATER/"
[ -e tests ] && mv tests "$LATER/"

# --- 2019: the docstring is true when it is written -------------------------
cat > allocate.py <<'EOF'
"""Integer allocation helpers for settlement reconciliation."""


def allocate(total_cents: int, weights: list[int]) -> list[int]:
    """Split a total into whole-cent parts proportional to weights.

    Equal splits distribute the remainder one unit each to the first parts;
    weighted splits floor each share and may lose units.
    """
    denom = sum(weights)
    parts = []
    for w in weights:
        parts.append(total_cents * w // denom)
    if len(set(weights)) == 1:
        for i in range(total_cents - sum(parts)):
            parts[i] += 1
    return parts
EOF
commit_at "2019-04-11T09:22:14+00:00" "Add allocate() for desk settlement splits"

# --- 2021: the body changes, the docstring does not -------------------------
export GIT_AUTHOR_NAME="Tomas Lindqvist"
export GIT_AUTHOR_EMAIL="t.lindqvist@halden.internal"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
cat > allocate.py <<'EOF'
"""Integer allocation helpers for settlement reconciliation."""


def allocate(total_cents: int, weights: list[int]) -> list[int]:
    """Split a total into whole-cent parts proportional to weights.

    Equal splits distribute the remainder one unit each to the first parts;
    weighted splits floor each share and may lose units.
    """
    denom = sum(weights)
    return [total_cents * w // denom for w in weights]
EOF
commit_at "2021-08-03T16:41:09+00:00" "Simplify allocate() to a comprehension

No behaviour change intended, just readability."

# --- 2024: a caller starts depending on the post-2021 behaviour -------------
export GIT_AUTHOR_NAME="Priya Raghunathan"
export GIT_AUTHOR_EMAIL="p.raghunathan@halden.internal"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
[ -e "$LATER/reconcile.py" ] && mv "$LATER/reconcile.py" .
commit_at "2024-02-19T11:07:55+00:00" "Add daily reconciliation report"

# --- 2026: tests written from the docstring, not from the code --------------
export GIT_AUTHOR_NAME="Tomas Lindqvist"
export GIT_AUTHOR_EMAIL="t.lindqvist@halden.internal"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
[ -e "$LATER/tests" ] && mv "$LATER/tests" .
commit_at "2026-07-30T14:12:38+00:00" "Add legacy coverage for equal splits

Not wired into evaluate.py yet, the runner migration is still open."

rmdir "$LATER" 2>/dev/null || true
