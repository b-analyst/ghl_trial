#!/bin/sh
# Checks the four things that commonly waste a first build, before you spend
# time on one.   sh tools/preflight.sh
ok=0

say() { printf '%-34s %s\n' "$1" "$2"; }

command -v docker >/dev/null 2>&1 \
  && say "docker" "$(docker --version 2>/dev/null | cut -d, -f1)" \
  || { say "docker" "MISSING"; ok=1; }

docker info >/dev/null 2>&1 \
  && say "docker daemon" "running" \
  || { say "docker daemon" "NOT RUNNING -- start Docker Desktop"; ok=1; }

# The scaffold pins a buildkit frontend that must be fetched from Docker Hub.
# It exists only for COPY --chmod, which modern buildkit supports natively, so
# it is the first thing to drop if the registry is unreachable.
if docker pull -q docker/dockerfile:1.4 >/dev/null 2>&1; then
    say "buildkit frontend" "reachable"
else
    say "buildkit frontend" "UNREACHABLE -- see note below"
    ok=2
fi

v=$(python3 -c "import inspect_ai; print(inspect_ai.__version__)" 2>/dev/null || true)
[ -n "$v" ] \
  && say "inspect-ai" "$v" \
  || { say "inspect-ai" "MISSING -- pip install inspect-ai"; ok=1; }

[ -n "${ANTHROPIC_API_KEY:-}${OPENAI_API_KEY:-}" ] \
  && say "provider api key" "set" \
  || say "provider api key" "unset -- needed only to run an episode"

echo
if [ "$ok" = "2" ]; then
    cat <<'NOTE'
The frontend pin on line 1 of adapters/docker/Dockerfile is unreachable. It is
inherited from the scaffold and buys nothing on modern Docker. To drop it:

    sed -i.bak '1d' adapters/docker/Dockerfile

Keeps a .bak so it is one move to put back.
NOTE
fi
exit 0
