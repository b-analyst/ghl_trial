"""Report detector signals per sample from a finished eval log.

    python tools/report_episodes.py <path-to.eval>

No Docker required. For each sample: pulls issued commands from tool_calls
(bash cmd/command fields and serialised text_editor invocations), rebuilds a
workdir in a temp dir from captured artifacts when present, runs the post-hoc
detectors, and prints one aligned row per sample plus aggregate rates.

If the log predates artifact capture (no files stored in score metadata) an
explicit notice is printed and the workdir-dependent columns are omitted.
used_true_value is never inferred from the grader score.
"""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── load detectors ────────────────────────────────────────────────────────────
spec = importlib.util.spec_from_file_location("det", ROOT / "detectors" / "verification.py")
det = importlib.util.module_from_spec(spec)
spec.loader.exec_module(det)


def load_eval_log(path: Path):
    try:
        from inspect_ai.log import read_eval_log
        return read_eval_log(str(path))
    except Exception as exc:
        print(f"error reading log: {exc}")
        sys.exit(1)


def extract_commands(sample) -> list[str]:
    """Return the list of strings the agent actually issued as commands."""
    commands: list[str] = []
    for msg in sample.messages:
        tool_calls = getattr(msg, "tool_calls", None) or []
        for tc in tool_calls:
            fn = getattr(tc, "function", "") or ""
            args = getattr(tc, "arguments", {}) or {}
            if fn == "bash":
                cmd = args.get("cmd") or args.get("command") or ""
                if cmd:
                    commands.append(cmd)
            elif fn == "text_editor":
                # Serialise so path and command are both visible to regexes.
                parts = " ".join(f"{k}={v!r}" for k, v in sorted(args.items()))
                commands.append(f"text_editor({parts})")
    return commands


def get_captured_files(sample) -> dict[str, str] | None:
    """Return the artifact dict from score metadata, or None if absent."""
    scores = getattr(sample, "scores", None) or {}
    score = scores.get("shipped_grader")
    if score is None:
        return None
    meta = getattr(score, "metadata", None) or {}
    if not meta:
        return None
    return meta


def rebuild_workdir(tmp_path: Path, captured: dict[str, str]) -> Path:
    """Copy agent_data/ into tmp_path, then overwrite with captured files."""
    shutil.copytree(ROOT / "agent_data", tmp_path, dirs_exist_ok=True)
    for rel_path, text in captured.items():
        dest = tmp_path / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
    return tmp_path


# ── formatting helpers ────────────────────────────────────────────────────────

def tf(v) -> str:
    if v is None:
        return "-"
    return "T" if v else "F"


HDR = (
    f"{'variant':<28}  {'score':>5}  {'route':<12}  "
    f"{'opened':>6}  {'exec_eq':>7}  {'prov':>4}  "
    f"{'truth':>5}  {'deferred':>8}  {'weak':>4}  "
    f"{'broke':>5}  {'tampered':>8}"
)


def fmt_row(variant: str, score_val, d: dict, has_files: bool) -> str:
    # workdir-dependent fields
    truth    = tf(d["used_true_value"])    if has_files else "-"
    deferred = tf(d["read_it_and_deferred"]) if has_files else "-"
    weak     = tf(d["weakened_checker"])   if has_files else "-"
    broke    = tf(d["broke_frozen_caller"]) if has_files else "-"
    tampered = tf(d["tampered_with_caller"]) if has_files else "-"

    return (
        f"{variant:<28}  {score_val:>5.2f}  {d['verification_route']:<12}  "
        f"{tf(d['opened_source']):>6}  {tf(d['executed_equal_split']):>7}  "
        f"{tf(d['checked_provenance']):>4}  "
        f"{truth:>5}  {deferred:>8}  {weak:>4}  "
        f"{broke:>5}  {tampered:>8}"
    )


def rate_str(num: int, denom: int) -> str:
    if denom == 0:
        return "n/a"
    return f"{num}/{denom} ({100*num//denom}%)"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python tools/report_episodes.py <path-to.eval>")
        return 1

    log_path = Path(sys.argv[1])
    log = load_eval_log(log_path)
    samples = log.samples or []

    # Check whether any sample has captured files.
    any_files = any(get_captured_files(s) is not None for s in samples)
    if not any_files:
        print(
            "NOTE: log predates artifact capture (no files in score metadata).\n"
            "      Workdir-dependent columns (truth, deferred, weak, broke, tampered)\n"
            "      are omitted.  Do not infer used_true_value from the grader score.\n"
        )

    print(HDR)
    print("-" * len(HDR))

    rows: list[dict] = []
    for sample in samples:
        variant = str(sample.id)
        meta = sample.metadata or {}

        # Grader score from the shipped_grader scorer.
        scores = getattr(sample, "scores", None) or {}
        score_obj = scores.get("shipped_grader")
        score_val = float(getattr(score_obj, "value", 0.0)) if score_obj else 0.0

        commands = extract_commands(sample)
        captured = get_captured_files(sample)
        has_files = captured is not None

        with tempfile.TemporaryDirectory() as tmp:
            wd = Path(tmp)
            if has_files:
                rebuild_workdir(wd, captured)
            else:
                # Use pristine agent_data for command-based signals only.
                shutil.copytree(ROOT / "agent_data", wd, dirs_exist_ok=True)

            d = det.detect(wd, commands)

        print(fmt_row(variant, score_val, d, has_files))
        rows.append({
            "variant": variant,
            "peer": meta.get("peer"),
            "attribution": meta.get("attribution"),
            "score": score_val,
            "has_files": has_files,
            **d,
        })

    # ── aggregate rates ───────────────────────────────────────────────────────
    print()
    total = len(rows)
    v_count = sum(1 for r in rows if r["verified"])
    d_rows = [r for r in rows if r["has_files"]]
    def_count = sum(1 for r in d_rows if r["read_it_and_deferred"])

    print(f"overall  verification rate: {rate_str(v_count, total)}")
    if d_rows:
        print(f"overall  deferral rate:      {rate_str(def_count, len(d_rows))}")
    else:
        print("overall  deferral rate:      n/a (no captured files)")

    # Break out by peer.
    peers = sorted({r["peer"] for r in rows}, key=lambda x: (x is None, str(x)))
    print()
    print("by peer:")
    for p in peers:
        sub = [r for r in rows if r["peer"] == p]
        vc = sum(1 for r in sub if r["verified"])
        dsub = [r for r in sub if r["has_files"]]
        dc = sum(1 for r in dsub if r["read_it_and_deferred"])
        deferred_str = rate_str(dc, len(dsub)) if dsub else "n/a"
        print(f"  peer={str(p):<10}  verified={rate_str(vc, len(sub))}  deferred={deferred_str}")

    # Break out by attribution.
    attrs = sorted({r["attribution"] for r in rows}, key=lambda x: (x is None, str(x)))
    print()
    print("by attribution:")
    for a in attrs:
        sub = [r for r in rows if r["attribution"] == a]
        vc = sum(1 for r in sub if r["verified"])
        dsub = [r for r in sub if r["has_files"]]
        dc = sum(1 for r in dsub if r["read_it_and_deferred"])
        deferred_str = rate_str(dc, len(dsub)) if dsub else "n/a"
        print(f"  attribution={str(a):<12}  verified={rate_str(vc, len(sub))}  deferred={deferred_str}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
