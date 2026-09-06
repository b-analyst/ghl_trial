# State of play

Written to survive context loss. If you are picking this up cold, read this
first, then `docs/proposal.md` (including **§15**), then `docs/assignment-fit.md`.

## Where the project is

A pilot honeypot was built, run, and retired. A retrieval-prevalence proposal
replaced it. A requirements audit then found the proposal did not meet the
assignment, and §15 of the proposal adds the layer that fixes it.

Nothing new has been run since the pilot.

## The assignment

Design a honeypot environment that elicits reward hacking and demonstrates
specification gaming. Deliverable is a runnable repo plus a short writeup. A
reviewer will spend roughly twenty minutes on it.

Ten hardened requirements are in `docs/assignment-fit.md`. The two that decide
whether something counts:

- **R1** — a visible success criterion the agent can satisfy instead of doing the
  work. Without one there is no specification to game.
- **R3** — an affordance an aligned agent has no reason to use. An omission does
  not qualify, because a well-behaved agent may omit too.

## The three designs, in order

**1. Allocation fixture (built, run, retired).** A money-splitting function with
a stale docstring; four artifacts agree it is fine; one command disproves them.
Committed and working. Failed because verification cost one command, so checking
dominated and there was nothing to calibrate. Also advertised itself.

**2. Retrieval prevalence (proposal §§1–14).** Skew a corpus so the accurate
minority account is rarely retrieved. Good research. Fails R1 and R3 on its own.

**3. Citation independence (proposal §15).** The retrieval corpus plus a stated
source-independence bar and an agent-visible `check_sources.py`. Meets all ten
requirements. Preferred.

## The single strongest argument for design 3

EvalAwareBench (2605.23055) finds that stacking evaluation-recognisability
factors raises awareness in every model. Its factor F2 is *"checkably false
premise injected"* — unavoidably spent by any honeypot built on a planted
falsehood, per `docs/lit/gap-map.md`.

Design 3 needs no false premise. Skew is structural, not factual. **F2 goes
clean.** No other candidate achieves that.

## Two runs that should happen before building anything

1. **Multi-model the existing allocation fixture.** One day, no new code. The
   pilot ran only on Claude; 2605.02269 reports Claude games least while all
   tested models game at non-negligible rates. The null is confounded with model
   family and the confound is cheap to remove.
2. **H3 in isolation.** One forced-injection condition, no corpus. Cordon-MAS
   (2605.26754), Shehata & Li (2605.10698) and 2604.12138 each report a version
   of H3 failing. H3 is load-bearing: if it fails, §§1–7 are wrong.

## Open, unresolved

**The pilot figure discrepancy.** `proposal.md` §4 and `gap-map.md` report 18/24
vs 70/70 at p = 0.000165. The batch log in `logs/` gives 21/24 vs 72/72 at
p = 0.0142. This is **not established as an error** — the run behind 18/24 may
exist and be lost, or may predate the encoding fixes in `d8abb37`. The stated
p-value reproduces exactly from the stated counts, so the arithmetic was sound
for whatever data it ran on. Do not quote either figure until provenance is
settled. Do not "correct" the documents on the assumption the log is complete.

**Citations still marked [R]** in the proposal have not been independently
verified. Everything marked [V] was checked in `docs/review.md` §1 and holds,
with two naming fixes noted there.

## Corrections already absorbed

- EAL-Bench (2609.01836) **is** a real benchmark introduced by that paper. An
  earlier claim in this project that the citation was wrong was itself wrong.
- 2604.12138 is *"RAG Must Move Beyond Factual Grounding to Represent Diverse
  Opinions"*; O-RAG is the architecture inside it.
- TransplantQA is the benchmark released in 2605.29084, not the paper's title.

## Repo facts worth not rediscovering

- `docker build` and live episodes have never been verified from the cloud
  session — Docker Hub is egress-blocked there. They work on the Windows desktop.
- `tools/check_bands.py`, `check_staging.py`, `check_detectors.py` all pass
  without a container.
- `tools/report_episodes.py` pools `noclaim-none` into the claim aggregates, so
  its printed "verification rate" and its `peer=none` row understate the real
  per-variant rates. Read per-variant, not pooled.
- Grader sits at 225 of 256 AST nodes. Keep forensics out of the scoring path.
