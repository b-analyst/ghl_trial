# Logs

Inspect `.eval` logs, one directory per batch, one subdirectory per model.

| directory | episodes | cells | status |
|---|---|---|---|
| `all/` | 549 | 5 | **This run.** Four models: fable 5.1, gpt-6-astra and qwen3.8-max at 30 epochs per cell, gpt-oss-120b at 20. |
| `pilot-11cell/` | 402 | 11 | The earlier design on the same fixture. Every pilot number quoted in the docs comes from here. |

Run `python scrub.py logs/all` before committing anything produced with a paid
key.

## The pilot cannot be re-analysed by the current tools

They refuse it, by design:

```
unknown cell 'claim-compliant-attributed' in ...; variants.json defines
['control', 'cover', 'goal', 'cover-goal', 'phantom-goal'].
```

The pilot varied a false docstring and a conflicting requirement; this design
varies a stated goal and a source of justification against a wrong test the
pilot did not have. Its episodes are not the same experiment. The pilot figures
in `docs/design.md` were computed by the pilot-era tools, which are in git
history.

## Batches are not interchangeable

The container and the cell definitions both changed during the project, in
ways an agent inside the sandbox could see: claim-free files were once staged
over tracked ones and showed up in `git status`; the container once had
`/task.py`, `/variants.json` and a directory named `/grader` at its root; and
the cells were cut and renamed twice. Seven earlier batches were removed once
no current tool could read them. They are in git history.

## `failed.txt` names astra, which has 150 episodes

The runner appends an arm to `failed.txt` when it lands no new episodes. astra's
first attempt did exactly that: OpenAI's strict function-calling rejected
Inspect's `text_editor` schema before a single request went through, which cost
nothing and is visible in `ledger.txt` as a `delta=$-0.00` line. It was re-run
with `-M strict_tools=false` and is the arm that setting applies to. The line
stays because it is what happened.

## Two runs per model directory

fable's 150 episodes are two files: 20 epochs, then 10 more added with
`-Append`. astra's are a 1-epoch probe and a 29-epoch run. `report.py` reads
every `.eval` under a model's directory together. Epoch numbers restart at 1 in
the second file and nothing keys on them.
