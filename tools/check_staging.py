"""Prove per-variant file staging resolves correctly, without Docker.

The image is built once and shared by every variant, so any agent-visible file
that differs between cells has to arrive at runtime. This asserts that the
Sample objects the task builds carry the right files for each cell, and that
Inspect resolves every source path.

Expected files per variant, derived from metadata:
  - "/workdir/HANDOFF.md"                         iff peer_log is not None
  - "/workdir/allocate.py"                         iff docstring_claim is False
  - "/workdir/tests/legacy/test_equal_splits.py"  iff docstring_claim is False

    python tools/check_staging.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_task_module():
    spec = importlib.util.spec_from_file_location(
        "inspect_task", ROOT / "adapters" / "inspect" / "inspect_task.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    from inspect_ai._eval.task.sandbox import resolve_sample_files

    task = load_task_module().honeypot()
    failures = []

    print(f"{'variant':<34} {'peer':<10} {'attribution':<12} {'claim':<6} staged")
    for sample in task.dataset:
        data = sample.metadata
        files = sample.files or {}

        # Build the expected destination-key set from metadata.
        expected_keys: set[str] = set()
        if data.get("peer_log") is not None:
            expected_keys.add("/workdir/HANDOFF.md")
        if not data.get("docstring_claim", True):
            expected_keys.add("/workdir/allocate.py")
            expected_keys.add("/workdir/tests/legacy/test_equal_splits.py")

        # Inspect resolves sources at runtime; do it here so a bad path fails now.
        resolved = resolve_sample_files(files) if files else {}
        for dest, src in resolved.items():
            if not Path(src).exists():
                failures.append(f"{sample.id}: source for {dest} missing ({src})")

        actual_keys = set(files.keys())
        missing = expected_keys - actual_keys
        unexpected = actual_keys - expected_keys
        if missing:
            failures.append(f"{sample.id}: missing staged files: {sorted(missing)}")
        if unexpected:
            failures.append(f"{sample.id}: unexpected staged files: {sorted(unexpected)}")

        print(
            f"{str(sample.id):<34} {str(data.get('peer')):<10} "
            f"{str(data.get('attribution')):<12} "
            f"{str(data.get('docstring_claim', True)):<6} "
            f"{', '.join(sorted(files)) if files else '-'}"
        )

    # The whole point: cells sharing one image must not share agent-visible content.
    bodies = {}
    for sample in task.dataset:
        src = (sample.files or {}).get("/workdir/HANDOFF.md")
        if src:
            bodies[sample.id] = Path(src).read_text()
    if len(set(bodies.values())) != len(bodies):
        failures.append("two variants stage identical HANDOFF.md content")

    print(f"\n{len(bodies)} variants stage a peer log, "
          f"{len(set(bodies.values()))} distinct bodies")

    if failures:
        print("\nFAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nper-variant staging resolves correctly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
