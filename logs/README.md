# Logs

Inspect `.eval` logs, one directory per batch, one subdirectory per model.

| directory | episodes | cells | status |
|---|---|---|---|
| `all/` | — | 4 | **This run.** Written by `tools/run_all.sh` / `run_all.ps1`. Empty until it happens. |
| `pilot-11cell/` | 402 | 11 | The pilot, under the design that preceded this one. Every pilot number quoted in the docs comes from here. |

Run `python tools/scrub_check.py logs/all` before committing anything produced
with a paid key.

## The pilot cannot be re-analysed by the current tools

They will refuse it, by design:

```
unknown cell 'claim-compliant-attributed'. variants.json defines
['claim', 'claim-conflict', 'conflict', 'control'].
```

The cell definitions changed when the design was cut to four cells, and the
lookup that resolves a cell's factor settings used to default to "no conflict"
for any name it did not recognise. That meant an eleven-cell batch came back
with every `conflict-*` episode marked as a claim cell, and scored against a
signature that inverts there. It failed silently and produced plausible numbers.

The pilot figures in `docs/design.md` were computed before that change and are
the ones to quote. To recompute them, check out the pilot-era tools from git
history rather than pointing the current ones at the old logs.

## Batches are not interchangeable

The container and the cell definitions both changed during the project, in ways
an agent inside the sandbox could see:

1. **The control was leaking.** Claim-free files were copied over ones the
   fixture's git history tracks, so `git status` reported them modified and
   `git diff` printed the removed claim to the cell whose purpose was to be free
   of it. 58 of 176 claim-free episodes ran one of those commands, and one ran
   `git checkout` and reverted the override mid-episode. Fixed by giving those
   cells their own image.

2. **The container announced itself.** `/task.py`, `/variants.json` and a
   directory named `/grader` sat at the filesystem root. `ls /` now shows
   `workdir` and nothing else.

3. **The cells were cut to four**, and renamed.

Seven earlier batches — `final/`, `cluster/`, `multimodel/`, `repair/`,
`topup/`, `probes/` and five loose logs — were removed once none of them could
be read by the current tools. They are in git history.
