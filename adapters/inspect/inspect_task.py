"""Inspect adapter.

    inspect eval adapters/inspect/inspect_task.py --model <provider>/<model>

The image sets `USER agent`, so solver tools run unprivileged and the scorer
escalates with `user="root"` to grade.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import Score, Target, mean, scorer, stderr
from inspect_ai.solver import TaskState, basic_agent
from inspect_ai.tool import bash, text_editor
from inspect_ai.util import sandbox

ROOT = Path(__file__).resolve().parents[2]


def sample_files(spec: dict) -> dict[str, str]:
    """Per-variant files staged into the sandbox after the container starts.

    The image is built once and shared by every variant, so anything that
    differs between conditions cannot be baked in at build time. Inspect copies
    `Sample.files` into the sandbox per sample, which is the only hook that
    varies agent-visible content across cells sharing one image.

    Keys are destination paths in the sandbox; values are source paths relative
    to the repo root (Inspect also accepts inline text here).
    """
    peer_log = spec["data"].get("peer_log")
    if peer_log is None:
        return {}
    return {"/workdir/HANDOFF.md": str(ROOT / peer_log)}


@scorer(metrics=[mean(), stderr()])
def shipped_grader():
    async def score(state: TaskState, target: Target) -> Score:
        result = await sandbox().exec(
            ["python", "/grader/grader.py", state.metadata["variant"]], user="root"
        )
        if not result.success:
            return Score(value=0.0, explanation=f"grader failed: {result.stderr}")
        graded = json.loads(result.stdout)
        return Score(value=graded["score"], explanation=graded.get("reason", "graded"))

    return score


@task
def honeypot() -> Task:
    variants: dict = json.loads((ROOT / "variants.json").read_text())["variants"]
    return Task(
        dataset=[
            Sample(
                # sys.executable, not "python": this runs on the host, and
                # Debian and Ubuntu ship no bare `python`.
                input=subprocess.run(
                    [sys.executable, str(ROOT / "task.py"), v],
                    capture_output=True, text=True, check=True,
                ).stdout,
                metadata={"variant": v, **spec["data"]},
                files=sample_files(spec),
                id=v,
            )
            for v, spec in variants.items()
        ],
        solver=basic_agent(tools=[bash(timeout=180), text_editor(timeout=180)]),
        scorer=shipped_grader(),
        sandbox=("docker", str(Path(__file__).parent / "compose.yaml")),
    )
