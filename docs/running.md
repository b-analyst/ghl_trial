# Running the experiment

Five cells, one roster, one command. Everything here has been run on the
Windows desktop; nothing has been run from a cloud session, because Docker
Hub is egress-blocked there.

## What you need

- Docker, and both images built (below).
- `inspect-ai` and `pytest` installed. The `inspect` console script is not on
  PATH on this machine; the runners call `python -m inspect_ai eval`, which is
  the same entry point.
- An OpenRouter key.

## Handling the key

Set it in the environment. Do not paste it into a file, a prompt, a commit, or
a chat message — a key in a repo is a key in the repo's history.

```
cmd:         set OPENROUTER_API_KEY=sk-or-...
powershell:  $env:OPENROUTER_API_KEY="sk-or-..."
sh:          export OPENROUTER_API_KEY=sk-or-...
```

Nothing here prints, logs, or writes the key. If you ever need to share a
failing command, share it with the variable name, not the value. If a key does
reach a commit, rotate it — deleting the line does not remove it from history.

## Build both images

The cells differ by image, never by staged files: anything git tracks has to
differ at build time, or `git status` gives it away and the agents look.

```bash
docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .
```

## Check the roster and price it

```bash
python cost.py --check            # every id resolves and serves tool calls
python cost.py --search fable     # find an id that does not
python cost.py --epochs 20        # expected and p90 cost per model, live pricing
```

A resolving id is not a runnable one; a model with no tool-calling endpoint
dies after the batch has started. `--check` catches that first. The token
profile is the pilot's until `--calibrate logs/all` re-measures it on this
batch; per-episode use varies by an order of magnitude between models, so the
first model of any new kind is a probe.

## Track what it costs

Every batch leaves `logs/all/ledger.txt`, and it carries two kinds of line:

```
2026-09-11T00:14:53  billed  before batch                             usage=$130.20  delta=$0.11
2026-09-11T00:31:00  billed  after openai/gpt-6-astra                 usage=$161.24  delta=$31.04
2026-09-11T00:31:08  spent   openai/gpt-6-astra                        150 ep  in=907,228 cached=2,732,841 out=361,815  $29.90
2026-09-11T00:31:08  spent   TOTAL                                     399 ep  in=12,124,763 cached=5,000,714 out=1,678,767  $158.71
```

`billed` is OpenRouter's own usage counter for the key, read before the batch
and after every arm; the delta between consecutive lines is what that arm
actually cost. `spent` is the tokens in the logs priced at live rates, and it is
cumulative over everything under the directory, not just the arm that ran. The
runners write both. When they disagree by more than pennies, the billed figure
is the true one and the gap is worth understanding -- reasoning tokens billed
as output, or a provider fee the catalogue does not show.

On this run they disagreed by about a tenth, in both directions:

| arm | billed | from the tokens |
|---|---:|---:|
| fable 5.1, 150 episodes | $115.62 | $128.61 |
| gpt-6-astra, 150 episodes | $32.03 | $29.90 |

Two other things the `billed` lines show. A `before batch` delta is everything
the key spent since the last reading, which includes work that has nothing to do
with this repo, so it is not a batch cost. And an arm that reached no model at
all still gets a line: astra's first attempt was rejected by the provider before
a request landed, and reads `delta=$-0.00`.

To account for a batch after the fact:

```bash
python cost.py --spent logs/all       # from the logs, no key needed
python cost.py --billed               # the key's counter, right now
```

## Run it

```bash
EPOCHS=20 sh run.sh
```

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1 -WhatIf
powershell -ExecutionPolicy Bypass -File .\run.ps1 -Epochs 20
```

The runner refuses to start unless `check.py` passes. It writes each model to
its own directory under `logs/all`, skips one that already has logs so an
interrupted batch resumes, and counts what actually landed rather than trusting
the exit code — Inspect can exit 0 having run nothing.

To add epochs to an arm that has already run — twenty per cell was not enough
to power a per-cell contrast on fable — pass `-Append` (`APPEND=1` for the
shell runner). The new run lands as a second `.eval` file in the same
directory, `report.py` reads every file it finds there, and the ledger records
the new run's cost on its own line:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1 -Epochs 10 -Append -Models anthropic/claude-fable-5.1
```

Epoch numbers restart at 1 in the second file. Nothing keys on them.

OpenAI models reject Inspect's `text_editor` schema under strict function
calling. Pass `-ModelArgs strict_tools=false` (`MODEL_ARGS=` for the shell
runner) for those, and probe with a single epoch before committing a batch:

```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1 -Epochs 1 -Models openai/gpt-6-astra -ModelArgs strict_tools=false
```

An arm run that way differs from the others in how its tool calls are validated.
Say so wherever its numbers are quoted.

The task path must stay relative: Inspect globs it and Python 3.14 refuses an
absolute glob. The per-episode budget (600 messages, 4M tokens) is on the Task
in `adapters/inspect/inspect_task.py`, not on the command line, so it cannot be
forgotten.

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

```bash
python scrub.py logs/all          # before committing any log
python report.py logs/all
```

`report.py` prints the cell table, the cell x model table, the four contrasts
with Fisher p-values, and each signature's rate. It refuses a batch with a cell
`variants.json` does not define.

Read the transcripts too. `hacked-silent` in `cover-goal` and
`cited-a-note-that-does-not-exist` in `phantom-goal` are the episodes the
report is for, and a rate is not a transcript.
