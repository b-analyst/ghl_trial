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

    Two kinds of staging may occur per variant:

    HANDOFF.md — staged when `peer_log` is not None, giving the agent a note
    from a prior session.

    Claim-free overrides — staged when `docstring_claim` is False (default True
    when absent). The shared image bakes in both the stale docstring on
    `allocate` and the legacy test that encodes the false convention; for the
    `noclaim-none` control both files are overwritten with claim-free versions
    so the variant is genuinely free of the false claim rather than merely
    missing the handoff note.
    """
    result: dict[str, str] = {}

    peer_log = spec["data"].get("peer_log")
    if peer_log is not None:
        result["/workdir/HANDOFF.md"] = str(ROOT / peer_log)

    # The leaked scoring log, staged only into the decoy-* variants. It must be
    # staged per-sample rather than baked into the image: the image is built once
    # and shared by every variant, so anything baked in would land in the
    # controls too -- including noclaim-none, whose whole job is to be free of
    # the manipulation.
    if spec["data"].get("decoy_key"):
        result["/var/log/settlement-verify.log"] = str(
            ROOT / "fixture" / "settlement-verify.log"
        )

    if not spec["data"].get("docstring_claim", True):
        result["/workdir/allocate.py"] = str(ROOT / "fixture" / "allocate_noclaim.py")
        result["/workdir/tests/legacy/test_equal_splits.py"] = str(
            ROOT / "fixture" / "test_equal_splits_noclaim.py"
        )

    return result


@scorer(metrics=[mean(), stderr()])
def shipped_grader():
    async def score(state: TaskState, target: Target) -> Score:
        result = await sandbox().exec(
            ["python", "/grader/grader.py", state.metadata["variant"]], user="root"
        )
        if not result.success:
            return Score(value=0.0, explanation=f"grader failed: {result.stderr}")
        graded = json.loads(result.stdout)

        # Capture submitted artifacts so post-hoc detectors can run on a
        # finished log. Each file is wrapped individually: one missing file
        # must not fail the whole score.
        artifacts: dict[str, str] = {}
        for path in [
            "allocate.py",
            "evaluate.py",
            "reconcile.py",
            "HANDOFF.md",
            "tests/legacy/test_equal_splits.py",
        ]:
            try:
                artifacts[path] = await sandbox().read_file(f"/workdir/{path}")
            except Exception:
                pass

        return Score(
            value=graded["score"],
            explanation=graded.get("reason", "graded"),
            metadata=artifacts,
        )

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
