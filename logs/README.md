# Logs

Inspect `.eval` logs, one directory per batch, one subdirectory per model.

| directory | episodes | cells | status |
|---|---|---|---|
| `all/` | 699 | 5 | **This run.** Five models at 30 epochs per cell: fable 5.1, gpt-6-astra, qwen3.8-max and gemini-3.8-flash; gpt-oss-120b at 20. |
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

## gemini ran twice

Its first attempt died partway through on an OpenRouter 402: the key had hit its
spend limit mid-batch, 27 of 34 samples errored, and the partial log was
replaced rather than kept. The arm here is the complete 30-epoch rerun. Three of
its `cover` episodes hit the token limit and are counted but not scored, which
is why that cell reads out of 27.

## Two runs per model directory

fable's 150 episodes are two files: 20 epochs, then 10 more added with
`-Append`. astra's are a 1-epoch probe and a 29-epoch run. `report.py` reads
every `.eval` under a model's directory together. Epoch numbers restart at 1 in
the second file and nothing keys on them.
