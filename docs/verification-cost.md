# Verification cost

Specification. Not built. This is the response to the ceiling recorded in
`design.md` under "Observed, and what it changed": fourteen of fourteen episodes
verified, so the verification rate carries no variance and H1-H4 have no room to
move.

## Why the ceiling is structural

Checking costs one command against an eleven-line function, and it returns
certainty about the only claim in play. Under those terms verification is
unconditionally dominant. There is no calibration to observe because there is no
trade-off — the agent is not deciding *whether* to check, it is doing the only
sensible thing.

Reid's argument only bites when checking is expensive. Someone who verified
everything would never get out of bed; that is the whole force of it. The
environment as built has no version of "everything". It has one thing.

## What does not work

**Turn and message caps.** Not a cost, a truncation. Five of seven samples hit
the default fifty-message cap in the first run and the only effect was to corrupt
the data. An agent cut off mid-work has not made a triage decision.

**Longer or more obscure code.** Converts the study into a capability test —
whether the model *can* find the discrepancy — which is precisely what STALE
(2605.06527) already measures and what `design.md` positions against. The
distinction between capability and propensity is the contribution; spending it to
raise difficulty is a bad trade.

**Hiding the truth.** If the code cannot settle the claim, not checking stops
being a choice and the DV ceases to exist. Same reason the greenfield arm was cut.

**A slow test suite.** Real friction for a person, weak for an agent. It does not
get bored, and wall-clock cost is not something it experiences as pressure.

## The fix: make the claims plural

The handoff asserts **N claims** about the module. One is false. Checking all N
is expensive; checking none is cheap and risks the false one. The agent has to
decide *which* claims are worth its attention, which is the Hume-Reid problem
instantiated rather than gestured at.

Three consequences, in increasing order of importance.

**Verification stops being binary.** It becomes a rate over claims. Seven of
seven agents verified "the" claim because there was one to verify; nobody checks
twelve things. The measure regains headroom in both directions without any change
to the threat model, the grader, or the harness.

**Selectivity becomes measurable, and it is the real construct.** Coverage — what
fraction of inherited claims got checked — is only the denominator. The question
worth asking is whether the false claim was checked at a *higher* rate than a
true one. Random triage means the false claim is checked at exactly the coverage
rate. Calibration means it is checked more often than that. Deference means less.
This is the thing the project has been trying to measure, and with one claim it
was not identifiable at all.

**The design turns within-subjects.** Each episode contributes N observations
instead of one, so selectivity is estimable from far fewer episodes than the
between-condition comparison in `design.md`'s `## Scale`, which needs roughly
two hundred and ten runs.

## What selectivity actually costs

Power on selectivity is set by the number of **false** claims per episode, not by
N. The false arm has `F × E` observations against the true arm's `T × E`, and the
smaller arm governs. At 80% power and α=.05 two-sided, for
`P(check | false)` versus `P(check | true)`:

    effect          false/true per episode    episodes
    0.50 vs 0.25      1 false / 11 true            34
    0.50 vs 0.25      3 false /  9 true            13
    0.40 vs 0.25      1 false / 11 true            90
    0.40 vs 0.25      3 false /  9 true            35
    0.60 vs 0.30      1 false / 11 true            23

Better than 210 in every row, but not free, and one false claim per episode is
not the cheap option it looks like.

**The tension worth stating plainly.** More false claims buy power, and also
raise the base rate — at which point suspicion becomes the rational strategy and
the construct changes. So the most interesting condition, where trusting is
correct on average, is the *least* powered. The 1-in-12 cell needs roughly three
times the episodes of the 3-in-12 cell to say the same thing.

Two implications for planning. Do not read a null in the low-false-rate cell as
calibration; it is more likely to be underpowered, and that must be declared in
advance rather than after. And the base-rate manipulation below should be sized
per cell rather than uniformly, because equal n across cells buys unequal
information.

## The handoff must be mostly true

If most claims are false, checking everything is obviously right and the dilemma
evaporates. At eleven true claims out of twelve, trusting the handoff is
*correct on average* — which is Reid's position, and what makes the one false
claim genuinely hard rather than merely hidden.

That also restores the utility axis honestly. An agent that checks all twelve is
not being careful, it is being wasteful, and with a real budget it finishes less.
`noclaim-none` currently carries that axis alone; here it is priced into every
episode.

## The base rate is the manipulation

Vary the fraction of false claims across conditions: at 1 in 12 trust is
rational, at 6 in 12 suspicion is rational. A calibrated agent shifts its
coverage with the base rate. An agent that does not shift is miscalibrated
*whichever direction it is stuck in* — indiscriminate trust and indiscriminate
suspicion are both failures, and both are visible.

This is the strongest form available, because it does not require predicting the
direction of an effect. It tests calibration as such. It also subsumes the
existing manipulations: attribution, peer stance and corroboration all become
things that should move coverage *if* they carry information, and should not if
they do not.

## What a claim has to satisfy

Each claim in the manifest needs three things, all deterministic:

- **A truth predicate.** Executable, so the ledger needs no annotation and no
  model. Same discipline as the current grader.
- **A check signature.** A pattern that identifies a command as exercising that
  specific claim. This is the load-bearing requirement and the one that
  constrains claim design: two claims that cannot be distinguished by the
  commands that test them cannot be scored separately. The command-scoped
  matching in `detectors/verification.py` already does this for one claim;
  generalising it means one pattern per claim rather than one per repo.
- **A consequence in code.** If the false claim goes unchecked, something in the
  submitted code must violate an invariant. Otherwise deference has no outcome
  and only the transcript records it.

Claims that fail the second requirement are the common case and should be cut
rather than approximated. A claim whose verification cannot be told apart from
another's is not a claim, it is noise.

## Where the claims come from

The `allocate` module is too small to carry twelve claims. This composes with
`archive/fixtures.md`: four functions — allocation, retry safety, window boundaries, tie
order — at three claims each. Those fixtures were specified to give the study
more than one case; the same surface area is what makes plural claims possible.
Build them once, use them twice.

Each fixture already has an invariant grader with both error directions
prototyped, so the third requirement above is satisfied by construction.

## Relation to the two-session design

These are complements, not alternatives, and they price different things.

Plural claims raise the cost of checking *within* a session while leaving the
source fully available. The agent can verify anything; it cannot verify
everything. That is triage under abundance.

`archive/two-session-design.md` denies the source entirely — the executor never sees the
history that would settle the question. That is deference under scarcity, and it
is also where false-authority formation becomes observable.

Plural claims are the cheaper build and the one that rescues the existing
hypotheses. The two-session split is the one that earns the Sherif citation. If
only one gets built, build this one first: it needs no new harness, no chained
evals, and no change to the unit of analysis.
