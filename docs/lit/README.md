# Literature

Six reviews. Each one grounds a specific decision in the build, and this table
says which — a review that grounds nothing belongs in `../archive/`, where four
of them now are.

Citations carry verification markers, and the scheme differs by file because
they were written at different points in the project:

- `cheating-and-rationalisation.md` marks each source **[V]** (checked against
  the live literature on 8 Sep 2026) or **[R]** (recalled from training, check
  before citing it anywhere a reviewer will look).
- The other four mark only what failed: a source searched for and not confirmed
  is flagged **UNVERIFIED** inline, and everything unmarked was located.

The markers are not decoration. An earlier draft of this project cited work that
turned out not to say what it was cited for, and `alignment.md` exists partly to
record which of those citations survived checking.

| file | what it grounds |
|---|---|
| `honeypot-eval-design.md` | The R1–R10 requirements in `../assignment-fit.md`. Krakovna et al. on realistic honeypots supplies R3, "an affordance an aligned agent has no reason to use", which is the requirement this environment fails and Part 2 exists to meet. |
| `alignment.md` | The specification-gaming definition the hack signatures use, and the deferral/omission framing. Also verifies works cited elsewhere in the repo, including several that did not survive checking. |
| `clinical-psych.md` | The escalation ladder in `../../detectors/escalation.py`. Its rungs are modelled on graded clinical disclosure instruments, where what is measured is what was voiced to the next person rather than what was privately understood — which is exactly the L0-vs-noticed_privately distinction the detector makes. |
| `philosophy-social-psych.md` | The naming of `deferred-to-the-claim`. The epistemology-of-testimony literature is why the signature is not called "believed": deference to testimony is a behaviour that can be measured, belief is a state that cannot, and 74% of the episodes firing this signature had already seen the code contradict the claim. |
| `cheating-and-rationalisation.md` | Experiment 2. Die-under-cup paradigms, the Abeler et al. meta-analysis, justified ethicality, and moral wiggle room. Leads with an integrity warning: Gino (tenure revoked May 2025, four retractions) and Ariely (2012 PNAS field data fabricated, retracted 2021) are two of this subfield's most-cited names, and the review marks which findings depend on them and which are independently replicated. |
| `gap-map.md` | What the design does not cover, and why. Cited by `../assignment-fit.md` and `../STATE.md`. |

## Reading order

If you are assessing the experiment, `honeypot-eval-design.md` first: it sets
the requirements the design is scored against. If you are picking up Part 2,
`cheating-and-rationalisation.md` and nothing else.
