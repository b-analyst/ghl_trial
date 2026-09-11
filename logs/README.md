# Logs

Inspect `.eval` logs, one directory per batch, one subdirectory per model.

| directory | episodes | cells | status |
|---|---|---|---|
| `all/` | — | 5 | **This run.** Written by `run.sh` / `run.ps1`. Empty until it happens. |
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
