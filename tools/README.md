# tools

Sixteen scripts in three groups. Nothing here is part of the environment the
agent runs in — these build it, check it, and read it afterwards.

## Run

| | |
|---|---|
| `run_all.ps1` / `run_all.sh` | **The runner.** One command, four cells, every model in `models.txt`. Same roster, same checks, same layout on both platforms. `-WhatIf` / dry run prices the batch and spends nothing. |
| `models.txt` | The roster, and the single source of truth for it. Also records four model ids that resolve but cannot run this fixture, with the reason. |
| `check_arm.py` | Called by the runner after each arm. Exits **0** complete, **2** short but real, **1** nothing worth keeping. Only 1 deletes — the split is load-bearing, because deleting on "short" once destroyed two arms that had already run. |

## Check — all offline, no API key, no container

Run these to satisfy yourself the fixture is what the docs say. The runner
refuses to start unless the first three pass.

| | |
|---|---|
| `check_cells.py` | **The design.** All four cells present and correctly crossed, signatures and cells cross-referenced, `conflict` and `claim-conflict` given byte-identical tickets, each cell in the right image, nothing staged. Prints the 2×2. |
| `audit_fixture.py` | **The fixture.** The docstring claim is false now and was true in 2019, the ticket's goal matches the grader's, both recovery routes actually work, both images build a clean tree, line endings are LF. |
| `check_detectors.py` | **The detectors**, against cases whose answer is known. |
| `check_bands.py` | **The bands in `qc.json`.** Scores the reference and the trap solution: reference 1.0, trap 0.0, visible checker passes both. |
| `test_investigation_depth.py` | Tests `investigation_depth.py`. |
| `check_models.py` | Validates the roster against OpenRouter's live catalogue. Needs network. `--search <term>` finds a renamed slug. |

## Read a finished batch

| | |
|---|---|
| `scrub_check.py` | **Run before committing any log.** Refuses outright if any path it is handed is missing — it used to read only the first and report "safe to commit" on a fraction of what it was given. |
| `report_multimodel.py` | The main cross-model report. Gaming is read off `variants.json`'s `hack_signatures` per cell, never by picking detector fields by name. |
| `outcome_tree.py` | Every episode in a cell placed on exactly one leaf of a decision tree. Refuses to print if the leaves do not sum to the episode count. |
| `investigation_depth.py` | The funnel: how far an episode got before deciding. Uses `action_similarity.py`. |
| `action_similarity.py` | Two-tier similarity over action sequences. A library for the above, not a command. |
| `estimate_cost.py` | Live OpenRouter pricing against the measured token profile. `--calibrate <logs>` re-derives that profile from a batch that ran. |
| `report_episodes.py` | Per-episode detail, **pilot-era pooling.** It folds the control into the claim aggregates, so its printed rates understate the real per-cell ones. Left as it is deliberately: the older logs were read under it, and changing it now would silently move published numbers. Read it per-variant, and use `report_multimodel.py` for anything aggregate. |

## The rule these encode

The detectors either match a literal string in a command the agent issued, or
execute the code it submitted. **No model judges anything, anywhere.** An
episode that crashed, ran out of budget, or changed no behaviour leaves the
denominator rather than counting as clean — a truncated episode looks exactly
like one that declined to fix anything, and the two must not be pooled.
