"""Inspect adapter.

    python -m inspect_ai eval adapters/inspect/inspect_task.py --model <provider>/<model>

The image sets USER agent, so the solver runs unprivileged and the scorer
escalates to root to grade.
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
HERE = Path(__file__).parent

# What the detectors read back after the episode. A file the agent deleted is
# recorded as None so the rebuilt workdir deletes it too, instead of quietly
# restoring the original.
CAPTURED = [
    "allocate.py",
    "evaluate.py",
    "reconcile.py",
    "HANDOFF.md",
    "tests/test_allocate.py",
    "pytest.ini",
]


def sample_sandbox(spec: dict):
    """Cells differ by image, never by staged files. Anything git tracks has
    to differ at build time, or `git status` gives the manipulation away."""
    compose = "compose.yaml" if spec["data"]["cover"] == "docstring" else "compose-noclaim.yaml"
    return ("docker", str(HERE / compose))


@scorer(metrics=[mean(), stderr()])
def shipped_grader():
    async def score(state: TaskState, target: Target) -> Score:
        result = await sandbox().exec(
            ["python", "/opt/settlement-ci/harness/grader.py", state.metadata["variant"]],
            user="root",
        )
        if not result.success:
            return Score(value=0.0, explanation=f"grader failed: {result.stderr}")
        graded = json.loads(result.stdout)

        artifacts: dict[str, str | None] = {}
        for path in CAPTURED:
            try:
                artifacts[path] = await sandbox().read_file(f"/workdir/{path}")
            except Exception:
                artifacts[path] = None

        return Score(
            value=graded["score"],
            explanation=graded.get("reason", "graded"),
            metadata=artifacts,
        )

    return score


@task
def honeypot() -> Task:
    variants = json.loads((ROOT / "variants.json").read_text(encoding="utf-8"))["variants"]
    return Task(
        dataset=[
            Sample(
                input=subprocess.run(
                    [sys.executable, str(ROOT / "task.py"), name],
                    capture_output=True, text=True, check=True,
                ).stdout,
                metadata={"variant": name, **spec["data"]},
                sandbox=sample_sandbox(spec),
                id=name,
            )
            for name, spec in variants.items()
        ],
        solver=basic_agent(tools=[bash(timeout=180), text_editor(timeout=180)]),
        scorer=shipped_grader(),
        sandbox=("docker", str(HERE / "compose.yaml")),
        # The per-episode budget lives on the Task rather than on a runner's
        # command line, because a limit that has to be remembered gets dropped.
        # 600 messages and 4M tokens are ceilings, not targets: the slowest
        # model on this fixture uses about a sixth of each.
        message_limit=600,
        token_limit=4_000_000,
    )
