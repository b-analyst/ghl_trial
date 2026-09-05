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
    variants = json.loads((ROOT / "variants.json").read_text())["variants"]
    return Task(
        dataset=[
            Sample(
                # sys.executable, not "python": this runs on the host, and
                # Debian and Ubuntu ship no bare `python`.
                input=subprocess.run(
                    [sys.executable, str(ROOT / "task.py"), v],
                    capture_output=True, text=True, check=True,
                ).stdout,
                metadata={"variant": v},
                id=v,
            )
            for v in variants
        ],
        solver=basic_agent(tools=[bash(timeout=180), text_editor(timeout=180)]),
        scorer=shipped_grader(),
        sandbox=("docker", str(Path(__file__).parent / "compose.yaml")),
    )
