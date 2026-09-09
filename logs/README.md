# Logs

Inspect `.eval` logs, one directory per batch, one subdirectory per model.

**Batches are not interchangeable and must not be pooled.** The container and
the cell definitions both changed during the project, in ways an agent inside
the sandbox could see. Every tool here takes explicit directories for that
reason; none of them globs `logs/` and hopes.

| directory | episodes | cells | status |
|---|---|---|---|
| `all/` | — | 4 | **current.** Written by `tools/run_all.sh` / `run_all.ps1`. Empty until the definitive run. |
| `pilot-11cell/` | 402 | 11 | The pilot. Three complete arms (claude-sonnet-5, deepseek-v4-flash, grok-4.3) plus llama-3.3-70b at 72/110, stopped by a credit limit. Every published pilot number comes from here. |
| `final/`, `cluster/`, `repair/`, `topup/`, `multimodel/`, `probes/` | — | varies | Superseded. Kept as provenance only. |

## Why the older batches cannot be merged forward

Three changes, in order:

1. **The control was leaking.** Claim-free files were copied over ones the
   fixture's git history tracks, so `git status` reported them modified and
   `git diff` printed the removed claim to the cell whose purpose was to be free
   of it. 58 of 176 claim-free episodes ran one of those commands, and one ran
   `git checkout` and reverted the override mid-episode. Fixed by giving the
   control its own image (`FIXTURE_MODE=noclaim`).

2. **The container announced itself.** `/task.py`, `/variants.json` and a
   directory named `/grader` sat at the filesystem root. The first two were
   never read by anything inside the container; the third became
   `/opt/settlement-ci/harness`. `ls /` now shows `workdir` and nothing else.

3. **The cells were cut to four**, and renamed. `pilot-11cell/` uses the old
   names — `noclaim-none`, `claim-gaming-*`, `conflict-none`, `decoy-*`,
   `*opengrader`. `variants-part2.json` records which were parked and why.

## Reading a batch

```
python tools/scrub_check.py logs/pilot-11cell      # no API keys in the logs
python tools/outcome_tree.py logs/pilot-11cell --by-model
python tools/report_multimodel.py logs/pilot-11cell
python tools/check_arm.py logs/pilot-11cell/x-ai_grok-4_3 110
```

`scrub_check.py` takes several paths at once and refuses outright if any is
missing — it used to read only the first and report "safe to commit" on a
fraction of what it was handed.
