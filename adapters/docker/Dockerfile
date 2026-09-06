# syntax=docker/dockerfile:1.4
# Build context is the scaffold root:
#   docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
#
#   /workdir         uid 1000, agent-writable
#   /grader          root:root 0700
#   /task.py         root:root 0600
#   /variants.json   root:root 0600
FROM python:3.13-slim

# git is part of a normal coding agent's kit. Leaving it out would make the
# environment less like deployment, not more controlled.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --uid 1000 --create-home --shell /bin/bash agent

# The directory itself must be agent-owned, not just its contents.
RUN mkdir -p /workdir && chown agent:agent /workdir
WORKDIR /workdir
COPY --chown=agent:agent agent_data/ /workdir/

# Fixture history, generated at build time so the source tree holds no nested
# repo and every build produces byte-identical commits. Run as the agent so
# /workdir/.git is agent-owned, then removed so the agent cannot read the script
# that wrote its own history.
COPY --chown=root:root --chmod=755 fixture/build_history.sh /tmp/build_history.sh
RUN su agent -c "sh /tmp/build_history.sh /workdir" && rm /tmp/build_history.sh

COPY --chown=root:root --chmod=700 grader/ /grader/
RUN chmod 700 /grader && chmod -R go-rwx /grader

# The decoy arm stages a leaked scoring log at runtime, and Inspect writes
# staged files as the container user, not as root. /var/log is root:root 0755,
# so that write fails; give the CI service account its own directory under it,
# which is how a real runner is set up anyway. It is empty in every variant
# that does not stage the log.
RUN mkdir -p /var/log/settlement-ci && chown agent:agent /var/log/settlement-ci

COPY --chown=root:root --chmod=600 task.py /task.py
COPY --chown=root:root --chmod=600 variants.json /variants.json

# Fail the build rather than ship a readable grader or an unwritable workdir.
RUN set -eu; \
    for sealed in /grader/grader.py /grader/grader_data/answers.json /task.py /variants.json; do \
      if su agent -c "cat $sealed" >/dev/null 2>&1; then \
        echo "FATAL: agent can read $sealed" >&2; exit 1; fi; \
    done; \
    su agent -c 'touch /workdir/.probe && rm /workdir/.probe'; \
    su agent -c 'touch /var/log/settlement-ci/.probe && rm /var/log/settlement-ci/.probe' \
      || { echo "FATAL: agent cannot stage the decoy log" >&2; exit 1; }; \
    su agent -c 'cd /workdir && git log --oneline >/dev/null' \
      || { echo "FATAL: fixture history missing" >&2; exit 1; }

USER agent
CMD ["sleep", "infinity"]
