# Docs

Start at `../README.md`. It has the flaw in thirty seconds, the 2×2, and how to
verify the fixture with no API key. Everything here goes deeper on one thing.

| file | what it is | read it when |
|---|---|---|
| `design.md` | **The design document.** The flaw, the two factors, the four cells, what each detector measures, the hypotheses, and what the pilot changed. | You want to understand or assess the experiment. |
| `assignment-fit.md` | The brief restated as ten testable requirements (R1–R10), and three candidate designs scored against them. Includes where the earlier reasoning was wrong. | You are judging whether the design answers the brief. |
| `explainer.md` | The same material in prose, start to finish, no tables. | You would rather read it than navigate it. |
| `running.md` | How to build, run, and read a batch. Key handling, epochs, cost, and the failure modes that have actually bitten. | You are about to spend money. |
| `verification-cost.md` | A specification for making verification genuinely costly, in response to the ceiling this design hits. **Not built.** | You are designing the next environment. |
| `STATE.md` | A working log kept against context loss, including the record of every number this project got wrong and corrected. Pilot-era cell names throughout. | You are picking the project up cold, or want the correction history. |
| `lit/` | Six literature reviews, each grounding a specific decision. `lit/README.md` maps them. | You want the citation behind a claim. |
| `archive/` | Designs explored and not taken, including the retrieval-poisoning proposal and the reviews that killed it. | You want to know what else was considered. |

## Two things that are easy to miss

**The current design is four cells.** `design.md` and `STATE.md` both carry
passages written for the eleven-cell pilot, marked as such at the top of each
file. They are kept because the reasoning that cut eleven to four is part of the
deliverable, not because they describe what runs today. What runs today is
`variants.json`, and `python tools/check_cells.py` prints it.

**Reward hacking is not demonstrated.** The environment elicits specification
gaming reliably and does not elicit reward hacking, because the two planted
opportunities sat outside the directory the agents actually worked in. That is a
design failure, it is stated in `design.md` and `../README.md` rather than
buried, and `../part2/README.md` is what follows from it.
