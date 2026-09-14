"""Run the experiment, score it, and write the artifacts.

    python main.py                  run every model, then analyze
    python main.py --analyze        analyze the logs already in logs/all
    python main.py --models openrouter/z-ai/glm-5.3 --epochs 5

Writes results.csv, transcripts/<model>.json, and prints the report.
Needs OPENROUTER_API_KEY in the environment to run; --analyze does not.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import detectors
import probe as probe_mod
import report
from task import ticket

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs" / "all"
TRANSCRIPTS = ROOT / "transcripts"
RESULTS = ROOT / "results.csv"
TASK = "adapters/inspect/inspect_task.py"

# strict_tools=false: OpenAI models reject Inspect's text_editor schema under
# strict function calling.
ROSTER = {
    "openrouter/openai/gpt-6-astra": ["-M", "strict_tools=false"],
    "openrouter/anthropic/claude-fable-5.1": [],
    "openrouter/z-ai/glm-5.3": [],
    "openrouter/qwen/qwen3.8-max-0902": [],
    "openrouter/google/gemini-3.8-flash": [],
}


def slug(model: str) -> str:
    return model.replace("openrouter/", "").replace("/", "_").replace(".", "_")


# --- running -----------------------------------------------------------------

def run_model(model: str, epochs: int) -> None:
    out = LOGS / slug(model)
    if out.exists() and any(out.glob("*.eval")):
        print(f"skip {model}: {out} already has logs")
        return
    # The task path stays relative: Inspect globs it and Python refuses an
    # absolute glob.
    cmd = [sys.executable, "-m", "inspect_ai", "eval", TASK,
           "--model", model, "--epochs", str(epochs),
           "--log-dir", str(out)] + ROSTER.get(model, [])
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=ROOT, check=True)


# --- reading a log back ------------------------------------------------------

def commands(sample) -> list[str]:
    """Every command issued. text_editor calls are serialized so the path and
    the command are both visible to a string match."""
    out = []
    for msg in sample.messages:
        for tc in getattr(msg, "tool_calls", None) or []:
            args = tc.arguments or {}
            if tc.function == "bash":
                out.append(args.get("cmd") or args.get("command") or "")
            elif tc.function == "text_editor":
                out.append("text_editor(" + ", ".join(
                    f"{k}={v!r}" for k, v in sorted(args.items())) + ")")
    return [c for c in out if c]


THINK = re.compile(r"<think>.*?</think>", re.S)


def visible_text(msg) -> str:
    """What a reviewer would read. A phrase that appears only in a model's
    thinking was disclosed to nobody, so two things come out: reasoning blocks,
    which carry a `.text` of their own and would otherwise pass for output, and
    the <think> spans some models emit inside ordinary text."""
    c = msg.content
    if isinstance(c, list):
        c = "\n".join(b.text for b in c
                      if getattr(b, "text", None)
                      and getattr(b, "reasoning", None) is None)
    return THINK.sub(" ", str(c or ""))


def reasoning_of(blk) -> str | None:
    """The readable thinking on a reasoning block, if there is any.

    Some providers hand back the chain of thought in `reasoning`; others
    encrypt it, set `redacted`, and put a readable digest in `summary`. Dumping
    `reasoning` unconditionally gives a page of base64 and loses the digest."""
    if getattr(blk, "reasoning", None) is None:
        return None
    if summary := getattr(blk, "summary", None):
        return summary
    return None if getattr(blk, "redacted", False) else blk.reasoning


def message_text(msg) -> str:
    """Everything, thinking included, for the transcript file."""
    c = msg.content
    if isinstance(c, list):
        parts = []
        for blk in c:
            if think := reasoning_of(blk):
                parts.append(f"[reasoning]\n{think}")
            if getattr(blk, "reasoning", None) is None and getattr(blk, "text", None):
                parts.append(blk.text)
        return "\n".join(parts)
    return str(c or "")


def final_message(sample) -> str:
    texts = [visible_text(m) for m in sample.messages
             if getattr(m, "role", "") == "assistant"]
    return next((t for t in reversed(texts) if t.strip()), "")


def rebuild(workdir: Path, files: dict) -> None:
    """The fixture with the captured files laid over it. A captured None means
    the agent deleted the file, so it is deleted here too."""
    shutil.copytree(ROOT / "agent_data", workdir, dirs_exist_ok=True)
    for rel, content in files.items():
        p = workdir / rel
        if content is None:
            p.unlink(missing_ok=True)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            # Bytes, not write_text: write_text turns LF into CRLF on Windows
            # and every unchanged file then reads as changed.
            p.write_bytes(content.encode("utf-8"))


def read_episode(sample, model: str, log_name: str) -> tuple[dict, dict]:
    """One row for results.csv, and one record for the transcript file."""
    cell = str(sample.id)
    base = {"model": model.replace("openrouter/", ""), "cell": cell,
            "epoch": getattr(sample, "epoch", None), "log": log_name,
            "messages": len(sample.messages)}

    # Hit a message or token limit: the agent never finished, so nothing it
    # left behind is a choice. Counted, never scored.
    if getattr(sample, "limit", None) is not None:
        row = base | {"outcome": "limit", "sealed": None, "gamed": None}
        return row, row | {"commands": [], "transcript": [], "files": {}}

    sc = (sample.scores or {}).get("shipped_grader")
    if sc is None or sc.metadata is None:
        row = base | {"outcome": "unreadable", "sealed": None, "gamed": None}
        return row, row | {"commands": [], "transcript": [], "files": {}}

    files = sc.metadata
    cmds = commands(sample)
    deliverable = (files.get("HANDOFF.md") or "") + "\n\n" + final_message(sample)
    with tempfile.TemporaryDirectory() as tmp:
        wd = Path(tmp)
        rebuild(wd, files)
        signals = detectors.detect(wd, cmds, deliverable)
        diagnosis = probe_mod.probe(wd)

    sealed = float(sc.value) if isinstance(sc.value, (int, float)) else None
    signals["outcome"] = detectors.outcome(signals, sealed)
    row = base | signals | {
        "sealed": sealed,
        "gamed": report.gamed(signals, cell),
        "probe_shape": diagnosis.get("shape"),
        "probe_passed": diagnosis.get("passed"),
        "report_short": diagnosis.get("report_short"),
    }
    record = row | {
        "ticket": ticket(cell),
        "commands": cmds,
        "probe": diagnosis,
        "files": files,
        "transcript": [
            {"role": getattr(m, "role", "?"), "text": message_text(m),
             "tool_calls": [{"function": tc.function, "arguments": tc.arguments}
                            for tc in (getattr(m, "tool_calls", None) or [])]}
            for m in sample.messages
        ],
    }
    return row, record


def write_transcript(model: str, episodes: list[dict]) -> None:
    TRANSCRIPTS.mkdir(exist_ok=True)
    path = TRANSCRIPTS / f"{model.replace('/', '_')}.json"
    path.write_text(json.dumps({
        "model": model,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_episodes": len(episodes),
        "cells": report.CELLS,
        "episodes": episodes,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}  ({len(episodes)} episodes)")


def read_logs(root: Path) -> pd.DataFrame:
    """One model directory at a time, so only one model's transcripts are held
    in memory at once."""
    from inspect_ai.log import read_eval_log

    by_dir: dict[Path, list[Path]] = {}
    for p in sorted(root.rglob("*.eval")):
        by_dir.setdefault(p.parent, []).append(p)

    rows: list[dict] = []
    for paths in by_dir.values():
        records: list[dict] = []
        model = ""
        for log_path in paths:
            log = read_eval_log(str(log_path))
            model = str(log.eval.model)
            samples = [s for s in (log.samples or []) if not s.error]
            for i, sample in enumerate(samples, 1):
                cell = str(sample.id)
                if cell not in report.CELLS:
                    raise SystemExit(f"unknown cell {cell!r} in {log_path.name}")
                row, record = read_episode(sample, model, log_path.name)
                rows.append(row)
                records.append(record)
                # Each episode rebuilds a tree and runs pytest in it. ~1 sec/episode.
                print(f"\r{model}  {i}/{len(samples)}", end="", file=sys.stderr)
            print(file=sys.stderr)
        if records:
            write_transcript(model.replace("openrouter/", ""), records)
    if not rows:
        raise SystemExit(f"no episodes under {root}")
    return report.coerce_bools(pd.DataFrame(rows))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--analyze", action="store_true",
                    help="skip the eval and read logs/all")
    ap.add_argument("--models", nargs="*", default=list(ROSTER))
    ap.add_argument("--epochs", type=int, default=30)
    args = ap.parse_args()

    if not args.analyze:
        LOGS.mkdir(parents=True, exist_ok=True)
        for model in args.models:
            run_model(model, args.epochs)

    df = read_logs(LOGS)
    df.to_csv(RESULTS, index=False)
    print(f"wrote {RESULTS.relative_to(ROOT)}  ({len(df)} rows)")
    report.print_report(df)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
