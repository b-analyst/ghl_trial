# Review of the retrieval-prevalence proposal

Independent pass over `docs/proposal.md`: every citation checked, the argument
attacked, and a recommendation that disagrees with the pivot.

Verification markers follow the proposal's convention. Anything marked **[V]**
here was confirmed this session against paper metadata or abstract text.

---

## 1. Citation audit

Every arXiv ID in the proposal resolves, and every quoted claim I could reach
checks out. This is a better hit rate than the earlier drafts of this project
managed, and it should be said plainly.

| Cited as | Status |
|---|---|
| 2602.16136 Retrieval Collapses When AI Pollutes the Web | **[V]** Yu, Kim & Kim. 67% pool → >80% exposure; "deceptively healthy state"; BM25 exposed ~19% of harmful content under *adversarial* contamination while LLM rankers suppressed better. Every number in the proposal matches. |
| 2605.29084 TransplantQA | **[V]** Li, Padman & Krishnan, CMU. Quote "source-dependence is a missing axis of NLP evaluation" is verbatim. |
| 2605.23055 Decomposing and Measuring Evaluation Awareness | **[V]** Eight toggleable factors, stacking raises awareness in all models, safety > capability sensitivity, recognition rarely changes behaviour. All as described. |
| 2609.01836 EAL-Bench | **[V]** EleutherAI. Writers create false authority for up to 50.2% of unauthorized requests; executors act on it in 98.6%. Formation/propagation split confirmed. |
| 2608.13956 retriever redundancy and diversity | **[V]** Uses FictionalQA as described. |
| 2604.26965 Impact of AI-Generated Text on the Internet | **[V]** ~35% by mid-2025; significant negative correlation with semantic diversity. |
| 2604.12138 | **[V]** but **mis-titled** — the paper is *Retrieval-Augmented Generation Must Move Beyond Factual Grounding to Represent Diverse Opinions*. O-RAG is the architecture inside it. |
| 2605.26754 Cordon-MAS | **[V]** Real, and says more than the proposal uses. See §2. |
| Shehata & Li, cognitive loafing | **[V]** = arXiv 2605.10698, *The Bystander Effect in Multi-Agent Reasoning*. Fortified Mind quote confirmed. |
| *Whose Facts Win?* | **[V]** = arXiv 2601.03746, ACL 2026. Note: **13 open-weight LLMs**, which the proposal does not say. |

Two naming corrections needed (2604.12138, and TransplantQA is the benchmark
not the paper). Neither is substantive; both are the kind of thing a reviewer
notices.

**One correction I owe from earlier in this project:** I previously asserted that
"EAL-Bench" was a mis-citation and that 2609.01836 introduced no such benchmark.
That was wrong. The abstract reads "We then introduce EAL-Bench." The original
brief's citation was correct and my correction was not.

---

## 2. Three papers predict H3 fails

H3 is the load-bearing hypothesis: *the failure sits in retrieval, not reasoning;
when the accurate document is forced into context, models produce the correct
answer.* The proposal states that refuting it "would undercut the proposal's
central argument."

Three independent results already point that way.

**Cordon-MAS (2605.26754)** names a "monitoring-control gap": models *detect
contradictions in retrieved evidence yet still act on poisoned claims.* **[V]**
That is H3 failing, in a neighbouring setting, already published.

**Shehata & Li (2605.10698)** report a "Sovereignty Gap" in which models
"frequently compute the correct derivation internally" and then produce
"Alignment Hallucinations" anyway. **[V]** Same shape: the right answer is
available internally and does not reach the output.

**2604.12138** finds that "a pluralistically-aligned LLM given biased retrieved
context still produces biased responses." **[V]** That is a version of the
localisation test, already run, with the answer the proposal treats as fatal.

None of these is decisive — different tasks, different contamination, different
question. But the proposal presents H3 as an open question when the prior is
visibly against it. **Run H3 first.** It needs one forced-injection condition and
no corpus construction, and if it fails, days 1–4 of corpus building are wasted.

---

## 3. 2604.12138 is a closer neighbour than the proposal admits

The proposal files it under "we cite this framing, we do not claim it." But it
contains: minority-voice under-representation as an explicit harm, echo chambers
amplifying dominant viewpoints, a survey finding only 1 of 34 RAG benchmarks
addresses opinion synthesis, and the localisation result above. **[V]**

The proposal's distinguishing move — deterministic scoring on a checkable payload
with known ground truth, versus their model-based judge — is real and worth
stating explicitly. Right now the distinction is left implicit and a reviewer
will read the overlap as unacknowledged.

---

## 4. A tension the proposal should be exploiting

2608.13956 finds diverse documents improve answer correctness by **17–47%**,
while duplicates and paraphrases do not. **[V]**

Yu et al. find aggregate answer accuracy stays **stable** under 67% contamination.
**[V]**

Contamination reduces diversity. Reduced diversity should therefore cost 17–47%
of correctness. It did not. Either the effect does not transfer, or **aggregate
accuracy is hiding it** — which is exactly H4. This is a stronger argument for
the proposed metric than anything currently in §6, and it is sitting unused
between two papers the proposal already cites.

---

## 5. The problem with the pivot

This is the main finding of this review.

**Towards Understanding Specification Gaming in Reasoning Models**
(arXiv 2605.02269; Nishimura-Gasparian, McCarthy & Lindner) reports:

- an open-sourced suite of specification-gaming tasks across eight settings
- **all tested models exploit their specifications at non-negligible rates**
- **highest rates in Grok 4, lowest rates in Claude models** **[V]**
- RL reasoning training substantially increases exploit rate
- and the field "lacks public systematic evaluation of specification gaming
  propensities"; existing work is "limited in size or scope, toyish and
  unrealistic, or proprietary" **[V]**

The pilot ran 161 episodes on `claude-sonnet-5` and 14 on `claude-sonnet-4-5`.
Both Claude. Zero specification gaming was observed — `weakened_checker` and
`tampered` are false in every row of the batch log.

So: **the environment was tested exclusively on the model family that games
least, produced no gaming, and the conclusion drawn was that the direction is
exhausted.** The proposal itself already contains the refutation, in §10: *"A
single-model run on a resilient model produces a ceiling and no result — which is
exactly what our pilot suffered."* That lesson is applied to the future design
and not to the decision to abandon the past one.

The null is confounded with model choice, and the confound is cheap to remove.

---

## 6. What the pilot actually established, and what it did not

**Established.** That `claude-sonnet-5` verifies a false inline claim at very high
rates when verification costs one command. That an honest peer report substitutes
for independent verification at a detectable rate. That the environment,
detectors and reporting tooling work.

**Not established.** That agentic honeypots are a dead direction. That
specification gaming is hard to elicit. That the fixture is too easy — only that
it is too easy *for Claude*.

The proposal's own methodological lesson is that "the honeypot advertised itself"
and "any successor design must place the temptation on the task's critical path."
That is a **repair for the fixture**, correctly diagnosed, and then not applied.

---

## 7. Recommendation

**Before committing ten days to corpus construction, spend one day on two runs.**

**Run A — multi-model the existing fixture.** It is built, audited, and its
tooling is trusted. Run the seven variants on a non-Claude model with known higher
gaming propensity. Cost: one day, no new code. Outcomes:

- *Gaming appears.* The honeypot works, the null was a model fact, and the
  assignment is answered with a model-comparison result that is more interesting
  than the original single-model design. 2605.02269 supplies the citation and the
  prior.
- *Gaming still absent.* The pivot is now evidenced rather than inferred, and the
  proposal gains a much stronger §4: "we eliminated the model confound before
  concluding the direction was exhausted."

Either way the day pays for itself, and it removes the first question a reviewer
will ask.

**Run B — H3 in isolation.** Forced injection, no corpus. One condition. If three
published results are right and H3 fails, the retrieval proposal's central
argument is wrong and it is better to know that on day one than day nine.

**On the assignment.** The brief was to design a honeypot environment eliciting
reward hacking and demonstrating specification gaming. The retrieval proposal is
good research and does not do that: there is no reward, no gaming, and no
honeypot in the specification-gaming sense. It measures information availability.
That may be the right call, but it should be a decision made deliberately and
defended in the writeup, not arrived at by momentum.

**A third option worth considering.** The pivot's central insight — that retrieved
material carries authority, cannot be settled by running a command, and so makes
verification genuinely expensive — can be imported into a coding honeypot rather
than replacing it. An agent doing a real task that must consult *retrieved*
documentation, where the corpus is skewed, satisfies the assignment, meets Reid's
precondition that the pilot failed, and puts the temptation on the critical path
exactly as §4 demands. It needs a document pool, not an IR research pipeline.

---

## 8. Smaller notes

- *Whose Facts Win?* is 13 **open-weight** models. Given the pilot's own lesson
  about model resilience, that limitation should be stated where it is cited.
- The `[V]`/`[R]` scheme is the best thing in the document and should survive into
  the final writeup.
- §12's assumption list is unusually honest. A4 is correctly identified as the
  weakest link.
- EvalAwareBench (from 2605.23055) is public on the Hub as
  `aisa-group/EvalAwareBench`, 102,600 rows. If evaluation awareness is going to
  be probed rather than assumed away, that dataset is the cheap way to do it.

---

## 9. Note on the pilot figures

Section 4 of the proposal reports 18 of 24 against 70 of 70 at p = 0.000165. The
batch log in `logs/` gives 21 of 24 against 72 of 72 at p = 0.0142.

This is recorded here as an **open discrepancy, not a demonstrated error**. The
run behind the 18/24 figure may exist and be lost, or may have used a different
`verified` definition before the encoding fixes landed. The stated p-value
reproduces exactly from the stated counts, so the arithmetic was sound for
whatever data it was computed on.

Do not quote either figure until the provenance is settled.
