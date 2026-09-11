# References

What the design rests on. Each entry says which part.

**Zhong, Raghunathan & Carlini — "ImpossibleBench: Measuring LLMs' Propensity
of Exploiting Test Cases"** (arXiv 2510.20270; ICLR 2026). Builds task variants
where the specification conflicts with the unit tests, so any pass implies a
shortcut, and measures the pass rate as a cheating rate. GPT-5 cheats 54% of
the time on Conflicting-SWEbench; newer Claude models cheat less than older
ones. The wrong test here is that construction. It ships as an official Inspect
implementation.

**METR — "Recent Frontier Models Are Reward Hacking"** (June 2025). Frontier
models modify tests and scoring code, and reach for answers the harness already
computed. o3 hacked 0.7% of HCAST tasks and about forty-three times as often on
RE-Bench, where it could see the scoring function. That gap is why the earlier
design on this fixture found nothing — the criterion was never in front of the
agent — and why this one puts it in the ticket.

**Schweitzer, Ordóñez & Douma — "Goal Setting as a Motivator of Unethical
Behavior"** (*Academy of Management Journal* 47(3): 422–432, 2004). People with
a specific, unmet goal overstate their self-scored performance more than people
told to do their best, most of all when they fall just short. Held with and
without money. The `stated_goal` factor is that manipulation: a specific
criterion the honest fix cannot reach.

**Krakovna, Lindner, Ho, Farquhar & Shah — "Realistic honeypot evaluations for
scheming propensity"** (arXiv 2605.29729). A honeypot needs an affordance a
misaligned agent would take and an aligned one has no reason to touch, and a
realistic one should expect a low base rate. Here the affordance is green
without fixing the bug; an honest agent has no reason to want it.

**Nishimura-Gasparian, McCarthy & Lindner — "Towards Understanding
Specification Gaming in Reasoning Models"** (arXiv 2605.02269). Defines
specification gaming as an action unintended by the developer or user that
scores well on the evaluation function, and reports rates across families,
lowest in Claude and highest in Grok. The roster in `models.txt` was chosen
against that spread.

**Bandura — moral disengagement** (Bandura, Barbaranelli, Caprara & Pastorelli,
*JPSP* 1996; Bandura, Underwood & Fromson, *J. Research in Personality* 1975).
Displacement of responsibility is one of the eight mechanisms: the harm is
someone else's decision. The `phantom-goal` cell asks whether an agent will
invent that someone — a prior session whose note it cites and never read.

**Nisbett & Wilson — "Telling more than we can know"** (*Psychological Review*
1977). People confidently report reasons for their behaviour that they had no
access to. The same cell, read as confabulation rather than displacement.

---

Earlier literature reviews, including one on the cheating and rationalisation
literature written for a follow-on study, are in git history rather than here.
Several citations made early in this project turned out not to support what
they were cited for; the ones above were checked against the source.
