# References

The work this design leans on. Fuller literature reviews were written during the
project and are in git history rather than here — they covered directions not
taken, and a reader of this repo does not need them.

**Krakovna, Lindner, Ho, Farquhar & Shah — "Realistic honeypot evaluations for
scheming propensity"** (arXiv 2605.29729). Supplies the requirement this design
is measured against: a honeypot needs an affordance a misaligned model would
pursue and *an aligned agent going about its task would have no reason to use*.
It also reports no unprompted scheming in a realistic internal-deployment
setting, which is why a low base rate here is the published expectation rather
than a broken environment.

This is the requirement the removed bait fixture was meant to satisfy and did
not — see "What this run adds, and what it cannot show" in `design.md`.

**Nishimura-Gasparian, McCarthy & Lindner — "Towards Understanding Specification
Gaming in Reasoning Models"** (arXiv 2605.02269). Defines specification gaming as
an action unintended by developers or users that nonetheless scores well on an
evaluation function, and reports gaming at non-negligible rates across models,
lowest in Claude and highest in Grok. That spread is the prior the model roster
in `tools/models.txt` was chosen against.

Taken together with the paper above: an environment with no visible success
criterion returns nothing, and one with a criterion returns gaming. That is why
`agent_data/evaluate.py` exists and why the ticket tells the agent to run it.

**Krakovna's specification-gaming distinction.** Behaviour that satisfies the
literal specification while missing its intent. Reward hacking is the narrower
case where the shortcut also *pays*. This environment demonstrates the first and
not the second, and `design.md` says so.

**STALE** (arXiv 2605.06527) measures whether models *can* detect that a stored
belief is stale. This measures something different — whether an agent bothers to
check when checking costs one command and nobody asked. Capability against
propensity.

**"Act or Escalate?"** (arXiv 2604.08588) advises deployers to characterise their
model's escalation threshold before shipping, which presumes the threshold is a
property of the model. The four cells here vary only the environment, which is
the assumption worth testing.

**Okamoto et al.** (arXiv 2608.12323) tested stated rules against enforcement
signals across twelve models. A prohibition axis was considered for this design
and cut because that paper covers it.

---

A note on provenance. Citations in the original reviews carried verification
markers, and several claims made early in this project turned out not to be
supported by the sources given for them. The six above were the ones checked
most closely, but anything quoted here should be read against the source before
it goes into a writeup.
