# Running the experiment

One command. Everything here has been run on Windows with Docker Desktop.

## What you need

- Docker, with both images built (below).
- `pip install -r requirements.txt`. The `inspect` console script is not always
  on PATH; `main.py` calls `python -m inspect_ai eval`, the same entry point.
- An OpenRouter key.

## Handling the key

Set it in the environment. Do not paste it into a file, a prompt, a commit, or
a chat message — a key in a repo is a key in the repo's history.

```
cmd:         set OPENROUTER_API_KEY=sk-or-...
powershell:  $env:OPENROUTER_API_KEY="sk-or-..."
sh:          export OPENROUTER_API_KEY=sk-or-...
```

Nothing here prints, logs, or writes the key. If you need to share a failing
command, share it with the variable name, not the value. If a key does reach a
commit, rotate it — deleting the line does not remove it from history.

## Build both images

The cells differ by image, never by staged files: anything git tracks has to
differ at build time, or `git status` gives it away and the agents look.

```bash
docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .
```

`FIXTURE_MODE=claim` (the default) builds the stale docstring the `cover` cells
use; `noclaim` builds the same history with the docstring updated.

## Run it

```bash
python main.py
```

That runs every model in `ROSTER` at 30 epochs, then scores the logs and writes
the artifacts. Useful flags:

```bash
python main.py --analyze                              # score existing logs, spend nothing
python main.py --models openrouter/z-ai/glm-5.3       # one model
python main.py --epochs 5                             # smaller batch
```

Scoring rebuilds every submitted tree and runs pytest inside it, which is about
a second an episode — roughly twenty minutes for a full 750-episode batch. It
prints per-model progress so it does not look hung.

A model that already has logs under `logs/all/<slug>/` is skipped, so an
interrupted batch resumes where it stopped. To add epochs to an arm that has
already run, point `--log-dir` at the same directory by re-running with the
directory emptied, or move the existing `.eval` aside first.

The per-episode budget (600 messages, 4M tokens) lives on the Task in
`adapters/inspect/inspect_task.py`, not on a command line, so it cannot be
forgotten. The task path stays relative: Inspect globs it and Python refuses an
absolute glob.

OpenAI models reject Inspect's `text_editor` schema under strict function
calling, so `ROSTER` passes them `-M strict_tools=false`. An arm run that way
differs from the others in how its tool calls are validated. Say so wherever its
numbers are quoted.

## What it writes

| path | what |
|---|---|
| `results.csv` | one row per episode: cell, outcome, every signal, the sealed score |
| `transcripts/<model>.json` | every episode in full — ticket, messages, commands, submitted files, probe |
| `figures/` | written by `generate_figures.py` from `results.csv` |

```bash
python generate_figures.py
```

## Epochs

Against a cell near zero, Fisher exact is driven by the count of hacked
episodes rather than the rate, so epochs buy the chance to observe enough of
them.

| per cell | 0 vs 3 | 0 vs 7 |
|---|---|---|
| 10 epochs | p = 0.21 | — |
| 20 epochs | — | p = 0.0083 |

Thirty is what this run needed. At twenty per cell the goal contrast read
p = 0.057 and looked like a near-miss; ten more epochs per cell turned it into a
null (p = 0.71) and turned the phantom contrast into a real effect. If the
budget is tight, cut models before epochs.

## Read the result

`main.py` prints the cell table, the model x cell table, the four contrasts with
Fisher p-values and the Bonferroni threshold, the outcome crosstab, disclosure
quality per hacked episode, and each signature's rate.

Read the transcripts too. `hacked-silent` in `cover-goal` and
`cited-a-note-that-does-not-exist` in `phantom-goal` are the episodes the report
is for, and a rate is not a transcript.
