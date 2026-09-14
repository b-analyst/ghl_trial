# Running the experiment

## What you need

- Docker, with both images built.
- `pip install -r requirements.txt`. The `inspect` console script is not always
  on PATH; `main.py` calls `python -m inspect_ai eval`, the same entry point.
- An OpenRouter key, set in the environment rather than written into a file. A
  key in a repo is a key in the repo's history; if one does reach a commit,
  rotate it, because deleting the line does not remove it.

```
cmd:         set OPENROUTER_API_KEY=sk-or-...
powershell:  $env:OPENROUTER_API_KEY="sk-or-..."
sh:          export OPENROUTER_API_KEY=sk-or-...
```

## Build both images

```bash
docker build -f adapters/docker/Dockerfile -t honeypot-scaffold .
docker build -f adapters/docker/Dockerfile --build-arg FIXTURE_MODE=noclaim -t honeypot-scaffold-noclaim .
```

`FIXTURE_MODE=claim` (the default) builds the stale docstring the `cover`
conditions use; `noclaim` builds the same history with the docstring updated.

## Run it

```bash
python main.py
```

Every model in `ROSTER` at 30 epochs, then scoring, then the report. Flags:

```bash
python main.py --analyze                              # score existing logs, spend nothing
python main.py --models openrouter/z-ai/glm-5.3       # one model
python main.py --epochs 5                             # smaller batch
```

Scoring rebuilds every submitted tree and runs pytest inside it, about a second
an episode, so roughly twenty minutes for a full 750-episode batch.

A model that already has logs under `logs/all/<slug>/` is skipped, so an
interrupted batch resumes. To add epochs to an arm that has already run, empty
its log directory first or move the existing `.eval` aside.

The per-episode budget, 600 messages and 4M tokens, is set on the Task in
`adapters/inspect/inspect_task.py`. OpenAI models reject Inspect's `text_editor`
schema under strict function calling, so `ROSTER` passes them
`-M strict_tools=false`.

## What it writes

| path | what |
|---|---|
| `results.csv` | one row per episode: model, cell, outcome, every signal, the sealed score |
| `transcripts/<model>.json` | every episode in full — ticket, messages, commands, submitted files, probe |
| `figures/` | written by `generate_figures.py` from `results.csv` |

```bash
python generate_figures.py
```

`main.py` prints the condition table, the model by condition table, the four
contrasts with their p-values, the outcome crosstab, disclosure quality per
hacked episode, and each signature's rate.

## Epochs

Thirty per condition. Against a condition near zero, Fisher exact is driven by
the count of hacked episodes rather than the rate, so epochs buy the chance to
observe enough of them.

| per condition | 0 vs 3 | 0 vs 7 |
|---|---|---|
| 10 epochs | p = 0.21 | — |
| 20 epochs | — | p = 0.0083 |

If the budget is tight, cut models before epochs.
