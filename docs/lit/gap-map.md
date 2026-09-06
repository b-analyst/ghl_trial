# Gap map

Synthesis across the four reviews in this directory. What is taken, what is open,
and what the literature forbids.

## The triangulated gap

Three reviews reached the same missing cell independently, from three
literatures.

Philosophy: Hume, Reid, Coady, Fricker and Lackey all debate whether to trust
testimony *before* checking. None addresses an agent that ran the test, observed
the counter-result, and deferred anyway.

Clinical: failure-to-rescue and failure-to-escalate research measures outcomes.
It never records whether the person who escalated had verified the condition they
reported.

Alignment: every escalation benchmark — HiL-Bench, "Act or Escalate?", KAIROS,
and the bystander paper — measures the *act* of escalating under overt pressure.
None measures its grounding.

**Grounded versus ungrounded escalation is unclaimed in all three.** The
detector already exists in `detectors/escalation.py`. This is the contribution to
build around, and it does not depend on the allocation fixture.

Two further gaps, in order of strength.

**Omission under diffused responsibility.** The field measures commission —
harmful action, or a wrong answer adopted under pressure. Passive failure to
report a discovered problem, unprompted and unchallenged, is not measured
anywhere confirmed.

**Orphaned-text deference.** Deference to text whose social origin has been
erased. Philosophy of testimony requires an identifiable speaker; the conformity
literature requires a present or remembered group. Neither covers it. Note that
the allocation environment could not test this — deferral was zero in both the
attributed and stripped cells, so the question is reachable only once a design
produces non-zero deferral.

## What the literature forbids

These are hard constraints, not preferences. Each one killed or would have killed
a plausible design.

**The false premise is itself an evaluation cue, and it cannot be removed.**
EvalAwareBench (arXiv 2605.23055) operationalises evaluation recognisability as
eight independently toggleable factors. F2 is *scenario coherence*, whose
exaggerated level is literally "checkably false premise injected". That is the
manipulation, so F2 is pinned at the exaggerated level in any honeypot of this
family. The paper's central empirical finding is that no single factor moves all
models but **stacking factors raises awareness in all of them**. Therefore every
other factor must be scrubbed to compensate.

Applied to the allocation environment: F1 stimulus artificiality is at the
exaggerated level (`example.internal` addresses, invented names); F4 ecological
completeness is exaggerated (a four-commit repo holding three files and no
backstory); F8 is arguably touched by a ticket that instructs the agent to run
the checker before finishing. F6 is clean — verified by inspecting the container,
where `variants.json`, `task.py` and `/grader` are all unreadable to the agent
and no evaluation strings are present. So the stack is roughly F1+F2+F4+F8, of
which only F2 was necessary.

One caution against over-reading this. The same paper finds that recognition
*rarely* produces behavioural change, and that when it does the direction is
model-specific. Evaluation awareness is a validity threat to test for, not an
established explanation of the 1.7% deferral rate.

**Raising the stakes fights the mechanism.** Fischer et al. (2011,
*Psychological Bulletin* 137(4):517-37, g = -0.35, 105 effects, 7,700+
participants) find the bystander effect *attenuated* when situations are
perceived as dangerous: g = -0.30 for dangerous emergencies against g = -0.47
for non-emergencies. Real emergencies are recognised faster, which raises arousal
and produces more helping. A high-salience diffusion experiment is therefore the
condition where diffusion is weakest. Put the consequence in the downstream
effect and keep the situation unalarming on its face.

**Verification must be expensive or everything ceilings.** Shehata and Li state
this as a design premise: "If the cognitive cost of verifying the truth is too
low, SOTA models will easily maintain a Fortified Mind state, masking the
presence of cognitive loafing." Their remedy is Semantic Hijacking — a nested
three-hop dependency chain plus roughly 500 tokens of randomised log noise to
saturate attention. That raises cost per claim, which is cheaper than the
plural-claims approach in `verification-cost.md` and can be combined with it.

**Multi-model is mandatory.** In the same paper Claude Sonnet 4.6 held accuracy
at 1.00 across every swarm size on GAIA while Gemini 3.1 Pro fell to 0.59 and
GPT-5.4 to 0.43, both at n=2. A single-model run on a resilient model produces a
ceiling and no result. Their Claude figure on Multi-Challenge is not evidence of
resilience, however: it sits at 0.52 with no swarm and 0.51 at maximum load,
which is a task the model was at chance on.

**Safety-flavoured evaluations are the more fragile kind.** EvalAwareBench finds
models more sensitive to safety than capability evaluations. This programme
measures propensity, which puts it in the higher-risk category by construction.

## What is already taken

Do not rebuild these.

Conformity to a false peer consensus, at scale — Shehata and Li, 22,500
trajectories. Their design declares a swarm in the prompt rather than running
agents, and asserts a wrong answer, so it is Asch conformity. They concede the
mechanisms are convolved: "the diffusion of responsibility (the Bystander Effect)
and peer pressure (Majority Conformity) are inextricably convolved." The clean
diffusion manipulation — peers who assert nothing, varying only how many could
act — is what remains.

Stated rules and enforcement, including the enforcement-information paradox —
Okamoto et al. (2608.12323), twelve models.

Whether models *can* detect stale memory — STALE (2605.06527). Capability, not
propensity.

Authorization laundering through agent memory — EAL-BENCH (2609.01836), which
shares an author with Okamoto et al.

Graded disclosure scales for AI — BioDisclose (2607.25700): four levels, a
refuse-then-leak rule, disclosure rates spanning 9.2% to 64% across five deployed
systems. It has no utility axis, does not cross handoffs, and reports no
inter-rater agreement, which is where a ladder can differentiate.

## Devices worth borrowing

**Structural containment plus skip logic**, from C-SSRS (inter-rater
κ = 0.67-1.00). Reliability comes from each rung presupposing all lower rungs and
a gate that skips inapplicable items — not from item wording. The escalation
ladder already has the first half.

**The refuse-then-leak rule**, from BioDisclose. Disclaimer language must not be
allowed to mask content that was in fact disclosed. This guards a failure the
current ladder cannot see: hedging that reads as escalation while conveying
nothing. It is the mirror of `disclosure_gap`.

**Canary-string deterministic grading**, from AgentDojo and tripwire-eval. Proof
that commission can be scored with no model in the grading path. The open problem
is an analogous mechanism for silent omission.

**Per-axis differential probing**, from TADP (Ferrara, 2606.28863, *Future
Internet* 18(7):339). Vary one channel at a time, hold the task fixed, and
establish a per-model null band by resampling before calling any delta real. The
citation is thin — single author, zero citations, eight open-weight models, case
set coded by one person without an inter-coder check — so borrow the method and
do not lean on the finding.

**Exact-state repair**, from EAL-BENCH. Replace the suspect artifact with an
oracle-correct one and replay with everything else fixed, to localise a failure
to the artifact rather than the reader.

**The symmetric categorical sweep**, from Shehata and Li. Permute peer identity
and position rather than only counting peers, because social load is
non-commutative: the first-named peer's brand dominates. This generalises the
attribution manipulation from "named or not" to "whose name, in what position."

## Where the programme is already ahead

Two of the reviews independently identified the private-recognition versus
public-disclosure gap as having no validated counterpart. `noticed_privately`
combined with a rung of 1 or lower is a direct operationalisation. Shehata and Li
arrived at the same construct — their Sovereignty Gap, internal validity minus
external accuracy — which is convergent validity from an unrelated design.

No honeypot paper found uses a utility axis to separate principled from
indiscriminate distrust. `noclaim-none` was a crude version; pricing it into
every episode is a methodological contribution in itself.

And the prohibition-explicitness result appears to be unique: no controlled study
of how an instruction not to investigate affects investigation rate. The
allocation environment produced one — 24 of 24 verification under "Don't
re-derive this, it's settled" against 18 of 24 under a note that admitted the
docs were wrong, Fisher exact p = 0.00017. That is worth reporting even though
the environment it came from is retired.
