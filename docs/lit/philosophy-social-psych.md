# Literature Review: Philosophy and Social Psychology
## Relevant to AI-agent testimony deference, multi-agent diffusion of responsibility, and epistemic compliance

*Prepared for the ghl_trial evaluation programme. Scope: philosophy of testimony, epistemic injustice, bystander effect, social loafing, conformity, collective responsibility, pluralistic ignorance, and audience inhibition. All citations are sourced; where verification was limited, this is stated.*

---

## 1. Epistemology of Testimony

### 1.1 The foundational polarity: Hume and Reid

**Hume, David. "Of Miracles" (Section X). *An Enquiry Concerning Human Understanding*. 1748.**

Central claim: The warrant for any testimonial belief derives entirely from inductive inference — from observed past conformity between reports and reality. "The reason why we place any credit in witnesses and historians is not derived from any connexion, which we perceive a priori, between testimony and reality, but because we are accustomed to find a conformity between them." (EHU 10.5, SBN 111.) This makes Hume the standard reference for *global reductionism*: testimonial justification reduces to more basic epistemic sources (perception, memory, induction). Effect size: not applicable — this is conceptual analysis rather than empirical work. What it does not cover: Hume's target is miraculous testimony, not ordinary deference; his account may be more limited in scope than the "standard" reading implies. Some scholars (O'Brien 2020, Brookes College) argue the Treatise resists a clean global-reductionist reading.

Source confirmed: Hume Texts Online (davidhume.org/texts/e/10); quoted in Stanford Encyclopedia of Philosophy (Plato 2019); O'Brien (2020) via Brookes University open access.

**Reid, Thomas. *An Inquiry into the Human Mind on the Principles of Common Sense*. Edinburgh, 1764.**

Central claim: Humans are constituted with two paired principles: *veracity* (a propensity to speak the truth) and *credulity* (a disposition to believe what others tell us). These are "original principles implanted in us by the Supreme Being" (IHM VI.24, p. 194). Because credulity is a basic feature of our cognitive architecture, testimony is an irreducible, foundational epistemic source on a par with perception; hearers need no prior inductive support to be entitled to believe. This is *anti-reductionism*. Effect size: not applicable. What it does not cover: Reid does not address adversarial or systematically deceptive testimony; his account assumes an essentially cooperative social world. It also does not explain how an agent should update when testimony conflicts with direct observation — the exact collision the honeypot environment creates.

Source confirmed: Reid quoted in Boethius (PhilArchive BOETRO-9); in "Take My Word for It" (1000wordphilosophy.com, citing Reid [1764] 1997 Pennsylvania State University Press edition); in Wiseman, "Reid on the Credit of Human Testimony" (Oxford Handbook, DOI:10.1093/acprof:oso/9780199276011.003.0003).

### 1.2 C.A.J. Coady

**Coady, C.A.J. *Testimony: A Philosophical Study*. Oxford: Clarendon Press, 1992.**

Central claim: Global reductionism is self-defeating: the inductive base available to any individual agent is too thin to ground the general reliability of testimony, yet such a grounding is what global reductionism demands. Any attempt at the grounding is itself circular, because the evidence used to establish testimonial reliability is itself largely testimonial (the circularity objection). Coady therefore defends non-reductionism, using Gricean analysis of natural versus non-natural meaning to show testimony is a primitive social institution requiring irreducible epistemic trust. Method: conceptual analysis plus historical survey. Effect size: N/A. What it does not cover: Coady's non-reductionism leaves the calibration problem unaddressed — when *should* a hearer be suspicious? He does not model the interaction between prior plausibility and specific signs of untrustworthiness. The book was not designed for adversarial or automated epistemic contexts.

Source confirmed: PhilPapers entry (philpapers.org/rec/COATAP); Fricker (1995) critical notice (DOI:10.1093/mind/104.414.393); multiple secondary surveys including IEP.

### 1.3 Elizabeth Fricker

**Fricker, Elizabeth. "Against Gullibility." In B.K. Matilal & A. Chakrabarti (eds.), *Knowing from Words: Western and Indian Philosophical Analysis of Understanding and Testimony*. Kluwer, 1994, pp. 125–161.**

Central claim: There is no "presumptive right" (PR thesis) to believe testimony. The hearer must always engage in active, critical monitoring of the speaker for trustworthiness, sincerity, and competence. "To believe what is asserted without doing so is to believe blindly, uncritically. This is gullibility." (p. 145.) This position is *local reductionism*: justification for a particular testimonial exchange must be grounded in non-testimonial evidence specific to that speaker on that occasion, not in a general inductive warrant. Method: conceptual analysis, refutation of arguments for the PR thesis. Effect size: N/A. What it does not cover: Fricker is pressed on what "critical monitoring" requires in practice. If it means only a disposition to notice salient cues, her view collapses toward minimal anti-reductionism. She does not address multi-agent chains where the identity of the original testifier is obscured, nor does she treat cases where testimony is embedded in an artifact rather than delivered by a present speaker.

Source confirmed: Diversity Reading List (diversityreadinglist.org); PhilArchive PERIDO-2; Stanford Encyclopedia (Plato 2019 edition at plato.sydney.edu.au citing Fricker 1994:126, 145, 154).

**Fricker, Elizabeth. "Telling and Trusting: Reductionism and Anti-Reductionism in the Epistemology of Testimony." *Mind*, 104(414), 1995, pp. 393–411.**

Central claim: A critical notice on Coady. Fricker concedes that pure global reductionism fails but maintains that local reductionism — ground the specific exchange in locally available non-testimonial evidence — is the right position for mature epistemic agents. She distinguishes a "developmental phase" (children, where default credulity is appropriate) from a "mature phase" (adults, where monitoring is required). Effect size: N/A. What it does not cover: The same practical-feasibility objection applies. The article is more focused on the Coady debate than on positive theory.

Source confirmed: DOI:10.1093/mind/104.414.393 (Oxford Academic); cited as Fricker (1995) in Stanford Encyclopedia and all major secondary literature.

### 1.4 Jennifer Lackey

**Lackey, Jennifer. *Learning from Words: Testimony as a Source of Knowledge*. Oxford: Oxford University Press, 2008.**

Central claim: Both reductionism and anti-reductionism fail because both focus on a single party. The dominant "belief view of testimony" assumes knowledge transmits via the speaker's belief; Lackey shows this is false (a Creationist teacher who sincerely teaches evolution can generate knowledge in students even without believing it herself — the "Creationist Teacher" case). The correct account is the *Statement View*: what matters is whether the speaker's statement is reliable, not their belief. This yields *dualism*: both speaker and hearer must make positive epistemic contributions. Hearers require positive reasons for belief; testimony is an irreducible source that can *generate* new knowledge rather than only transmit it. Method: conceptual analysis, counterexamples. Effect size: N/A. What it does not cover: Lackey addresses inter-personal testimony in face-to-face or direct assertion contexts. She does not treat anonymous, multi-hop, or artifact-embedded testimony (e.g., a docstring). The practical question of how much effort a hearer must invest in assessing the speaker's statement is not operationalised.

Source confirmed: Oxford Academic (DOI:10.1093/acprof:oso/9780199219162.003.0004); PhilPapers (philpapers.org/rec/LACLFW-2); Philosophy Now review (philosophynow.org issue 88); WorldCat listing.

### 1.5 Formal treatments

**Goldman, Alvin I. *Knowledge in a Social World*. Oxford: Oxford University Press, 1999.**

Central claim: Social epistemology should be *veritistic*: the goal is practices that reliably produce true beliefs. Testimony is treated as a social practice to be evaluated by its truth-conduciveness. Bayesian conditionalization on testimony provides an expected positive effect on truth-possession when subjective likelihoods match objective ones. Goldman pioneers the framing of testimony evaluation as a matter of source reliability estimation. Method: normative theory plus Bayesian modelling. Effect size: N/A. What it does not cover: Goldman's framework is primarily evaluative rather than descriptive; it does not predict when agents will fail to update correctly. The book does not address multi-agent pipelines or cases where the source identity is unknown.

Source confirmed: DOI:10.1093/0198238207.001.0001; SEP entry (plato.stanford.edu/entries/epistemology-social); Goldman (1999) text excerpt confirming Bayesian veritistic approach.

**Hartmann, Stephan & Rafiee Rad, Soroush. "Formal models of source reliability." *Synthese*, 2020. DOI:10.1007/s11229-020-02595-2.**

Central claim: Reviews and compares the Bayesian models of source reliability in Bovens & Hartmann (2003) and Olsson (2011). All are normative Bayesian models. The Bovens/Hartmann model represents source reliability as a latent parameter to be updated on evidence of coherence among independent reports; the Olsson model differs in assumptions about independence. Simulations show that important normative questions (e.g., when does corroboration provide additional justification from sources that are not independent?) remain unsettled. For the programme's purposes, the key result is the formalization of the *corroboration fallacy*: multiple sources repeating a claim from a common origin provide much weaker confirmation than multiple genuinely independent sources. Method: formal Bayesian modelling, simulation. Effect size: N/A, but formal. What it does not cover: Empirical predictions about when human (or AI) agents actually track source independence. Does not address the case where the agent itself is the potential testifier for downstream agents.

Source confirmed: DOI:10.1007/s11229-020-02595-2; cited in SEP and secondary literature as "Formal models of source reliability, Synthese, 2020."

**NOTE on state of the debate.** The reductionism–anti-reductionism binary has loosened. Lackey's dualism, Goldberg's "extended knowing" framework (2010), and Fricker's evolving position (see her 2017 essay "Evolving Concepts of Epistemic Injustice" retrieved at mirandafricker.com) all treat source monitoring and default trust as matters of degree rather than categorical choice. The practical upshot for this programme: the normatively *correct* calibration for an AI agent is neither Reidian credulity nor Fricker's constant monitoring, but context-sensitive vigilance proportional to the stakes and the cost of checking — which is exactly what the honeypot measures.

---

## 2. Epistemic Injustice

### 2.1 The founding account

**Fricker, Miranda. *Epistemic Injustice: Power and the Ethics of Knowing*. Oxford: Oxford University Press, 2007.**

Central claim: There is a distinctively epistemic form of injustice: wronging someone *in their capacity as a knower*. Two forms are identified. (1) *Testimonial injustice*: a hearer assigns an unfair credibility deficit to a speaker because of identity prejudice — "an identity-prejudicial credibility deficit." The wrong is not merely epistemic but ethical because it damages the speaker's standing as a knower. (2) *Hermeneutical injustice*: a gap in collective interpretive resources (caused by the marginalization of a social group) prevents a person from making sense of their own experience — e.g., sexual harassment before that concept existed. Systematic testimonial injustice requires that the deficit track a social identity; incidental cases do not. Method: conceptual analysis grounded in literary examples (Harper Lee, Charlotte Perkins Gilman, Richard Feynman). Effect size: N/A. What it does not cover: Fricker's account is interpersonal and presupposes a human hearer who can exercise testimonial justice as a virtue. It does not address automated or algorithmic credibility assignment, nor does it treat the inverse — *excess* credibility assigned to certain voices (credibility inflation). The book was criticised by José Medina (2013, *The Epistemology of Resistance*) for not adequately addressing collective and systemic dimensions.

Source confirmed: DOI:10.1093/acprof:oso/9780198237907.001.0001; IEP entry (iep.utm.edu/epistemic-injustice); Fricker (2007) PDF at mirandafricker.com.

### 2.2 Extensions to algorithmic systems

**Lanius, David & Fröhlich, Kathrin et al. "Epistemic Injustice in Generative AI." *AAAI/ACM AIES 2024*. Accessed at ojs.aaai.org/index.php/AIES/article/download/31671/33838.**

Central claim: Introduces *generative algorithmic epistemic injustice* with four dimensions: amplified testimonial injustice (bias from pre-training), manipulative testimonial injustice (user-directed harm), hermeneutical ignorance (AI lacks sociocultural context), and access injustice (multilingual disparities). Method: conceptual taxonomy with illustrative cases; no effect sizes. What it does not cover: Does not treat AI as a *receiver* of testimony (the programme's direction) — focuses on AI as a *producer* of potentially unjust outputs.

Source confirmed: URL above is open-access AAAI publication.

**Renz, Florian. "A taxonomy of epistemic injustice in the context of AI and the case for generative hermeneutical erasure." *AI and Ethics*. Springer, 2025. DOI:10.1007/s43681-025-00801-w.**

Central claim: Proposes "generative hermeneutical erasure" — LLMs suppress minority epistemologies through their "view from nowhere," contributing to hermeneutical injustice at civilizational scale. Method: philosophical taxonomy drawing on philosophy of technology. Effect size: N/A. What it does not cover: Empirical verification; does not address the agent-as-receiver case.

Source confirmed: Springer DOI above; abstract retrieved directly.

**NOTE on relevance to this programme.** The literature on epistemic injustice in AI systems almost uniformly treats the AI as *perpetrating* injustice toward human subjects — inflating or deflating credibility of human voices based on demographic proxies. The inverse — an AI agent's credibility assessment of testimony it *receives* — is essentially unexplored. Whether an AI agent gives systematically inflated credibility to inherited documentation because that documentation resembles authoritative male technical discourse (a testimonial-injustice hypothesis in reverse) is not in the literature. This is a genuine gap.

---

## 3. Bystander Effect and Diffusion of Responsibility

### 3.1 The original experiments

**Darley, J.M. & Latané, B. "Bystander intervention in emergencies: Diffusion of responsibility." *Journal of Personality and Social Psychology*, 8(4), 377–383, 1968.**

Central claim: The presence of other bystanders reduces both the likelihood and the speed of helping in emergencies. The mechanism at the responsibility stage is *diffusion*: each person's felt obligation is reduced in proportion to the number of others also present. Method: Lab experiment. Subjects heard a staged seizure via intercom. Alone condition: 85% helped within one minute, 100% within three minutes. Six-person condition: 31% helped within one minute, 62% within six minutes. The six-person group had significantly lower and slower helping despite no opportunity for pluralistic ignorance (subjects could not see each other). Effect size: not reported as standardised ES in the original paper, but the between-condition difference is large (31% vs 85% at one minute; chi-square significant). What it does not cover: Laboratory, middle-class US undergraduates; no physical danger to subjects; no cost to helping. Auditory-only channel excluded pluralistic ignorance by design, making this the cleanest isolation of diffusion of responsibility.

Source confirmed: DOI confirmed by Fischer et al. (2011); original data reported in multiple secondary sources including simplypsychology.org and the Fischer meta-analysis PDF (is.muni.cz).

**Latané, B. & Darley, J.M. *The Unresponsive Bystander: Why Doesn't He Help?* New York: Appleton-Century-Crofts, 1970.**

Central claim: Formalises the five-stage *decision model of helping*: (1) notice the event; (2) interpret it as an emergency; (3) assume personal responsibility; (4) decide on a form of help; (5) act. Social processes inhibit helping at stages 2 and 3 in particular. Three distinct mechanisms are named: *diffusion of responsibility* (stage 3), *pluralistic ignorance* (stage 2), and *evaluation apprehension*/*audience inhibition* (stage 4–5). Effect size: this is a theoretical consolidation volume; specific effect sizes are in Darley & Latané (1968) and Latané & Rodin (1969). What it does not cover: Non-emergency contexts; situations with clear responsibility designation; cross-cultural variation; inaction by deliberate omission rather than ignorance.

Source confirmed: Cited as Latané & Darley (1970) throughout Fischer et al. (2011); SimplyPsychology; Hortensius & de Gelder (2018) review (PMC6099971). The five-stage model is confirmed in multiple independent secondary accounts.

### 3.2 Meta-analysis

**Fischer, P., Krueger, J.I., Greitemeyer, T., Vogrincic, C., Kastenmüller, A., Frey, D., Köster, M., Peus, C., & Kainbacher, M. "The bystander-effect: A meta-analytic review on bystander intervention in dangerous and non-dangerous emergencies." *Psychological Bulletin*, 137(4), 517–537, 2011. DOI:10.1037/a0023304.**

Central claim: The bystander effect is robust and replicates across cultures and paradigms, but its size is substantially moderated by situational dangerousness. Overall weighted mean effect size g = −0.35 (fixed effects model, 95% CI [−0.40, −0.29], p < .001; random effects g = −0.33) across 105 independent effect sizes from 7,700+ participants. The negative sign indicates group presence reduces helping. Critical moderator: *dangerous* emergencies with physically costly intervention show near-zero or positive bystander effects — the arousal-cost-reward model explains this: high-danger emergencies are recognized faster as genuine emergencies (clearing stage 2), and the cost of inaction becomes psychologically high. A second moderator: bystanders who can provide *physical support* to the helper reduce the bystander effect. Method: systematic meta-analysis (Hedges' g; fixed and random effects models; Comprehensive Meta-Analysis software). What it does not cover: Psychological rather than physical emergencies; purely informational failures (where no one witnesses anything dangerous, but a false belief circulates); does not study omission versus commission asymmetries.

Source confirmed: Full PDF retrieved (is.muni.cz — university course materials, original journal article DOI:10.1037/a0023304); effect sizes quoted directly from PDF.

### 3.3 Reappraisal of the Genovese narrative

**Manning, R., Levine, M., & Collins, A. "The Kitty Genovese murder and the social psychology of helping: The parable of the 38 witnesses." *American Psychologist*, 62(6), 555–562, 2007. DOI:10.1037/0003-066X.62.6.555.**

Central claim: The founding narrative — 38 witnesses watched the murder passively and did nothing — is a myth unsupported by archival evidence. Detailed archival reconstruction shows: (a) at most a handful of witnesses could see any part of the attack; (b) several witnesses did take action (shouting at the attacker, calling police); (c) the final fatal attack occurred inside a building out of view of trial witnesses. The story became a "modern parable" in the Darley/Latané tradition, shaping research by privileging the anti-group story. The real lesson, the authors argue, is that groups can *facilitate* helping under the right conditions (e.g., when a clear leader emerges). Method: archival analysis of police transcripts, court records, sworn affidavits. Effect size: N/A (historical analysis). What it does not cover: Does not challenge the experimental evidence for the bystander effect itself — only the empirical status of the motivating case.

Source confirmed: DOI:10.1037/0003-066X.62.6.555; BPS Psychologist news (December 2007, bps.org.uk); Lancaster EPrints (eprints.lancs.ac.uk/id/eprint/3591).

---

## 4. Social Loafing

**Latané, B., Williams, K., & Harkins, S. "Many hands make light the work: The causes and consequences of social loafing." *Journal of Personality and Social Psychology*, 37(6), 822–832, 1979. DOI:10.1037/0022-3514.37.6.822.**

Central claim: Individuals exert less effort on physically exerting collective tasks (clapping, shouting) when performing in groups than alone. This *social loafing* effect is distinct from coordination losses: it persists even when coordination is controlled. The mechanism is reduced individual identifiability — when outputs are pooled, no one can be evaluated or credit-apportioned. Two experiments with undergraduates; effect was substantial and replicated. What is not covered: Cognitive or informational tasks; situations where individual outputs are identifiable; tasks with high personal involvement or clear standards. Method: Lab experiment; individual effort in real vs. pseudo-groups; acoustic measurement.

Source confirmed: DOI:10.1037/0022-3514.37.6.822; ResearchGate publication page; confirmed author list (Latané, Williams, Harkins) and journal year volume.

**Karau, S.J. & Williams, K.D. "Social loafing: A meta-analytic review and theoretical integration." *Journal of Personality and Social Psychology*, 65(4), 681–706, 1993. DOI:10.1037/0022-3514.65.4.681.**

Central claim: Social loafing is robust across tasks and populations. Meta-analysis of 78 studies yields a weighted mean effect size d = 0.44 (moderate). Key moderators: evaluation potential (identifiability), task meaningfulness, co-worker expectations, culture (effect is smaller in collectivist cultures). Theoretical integration via the *Collective Effort Model*: individuals reduce effort when they expect their contribution will be neither individually identifiable nor influential on a valued outcome. Method: meta-analysis, Hedges/Olkin method; 78 studies. What it does not cover: Does not separate social loafing from diffusion of responsibility in helping contexts (the constructs are related but distinct — loafing is about effort reduction in shared tasks, diffusion is about responsibility attribution in emergencies).

Source confirmed: DOI:10.1037/0022-3514.65.4.681; full text PDF at research.cs.vt.edu; confirmed d = 0.44 in Karau & Williams PDF (communicationcache.com).

**Distinction from diffusion of responsibility.** Latané et al. draw an explicit distinction. Social loafing is an *output* phenomenon in cooperative production: individuals reduce *effort* because individual contributions are unidentifiable. Diffusion of responsibility is a *motivational* phenomenon in emergencies: individuals reduce *felt obligation* because others share responsibility for acting. Both involve group size as the independent variable and both require an unidentifiable individual contribution, but the contexts are different (non-urgent production vs. emergency intervention) and the mechanisms are distinct (de-motivation vs. de-obligation).

---

## 5. Conformity

### 5.1 Sherif's autokinetic studies

**Sherif, Muzafer. *The Psychology of Social Norms*. New York: Harper and Row, 1936.**

Central claim: In genuinely ambiguous situations, individuals do not have stable individual percepts; they establish subjective reference points in social interaction and these *social norms* persist when subjects are subsequently tested alone. Method: participants judged apparent movement of a stationary light in a darkened room (autokinetic effect) — individually first, then in groups, or in groups then individually. Group estimates converged to a shared norm; individuals who had first been in groups retained the norm in subsequent individual sessions, indicating internalization rather than compliance. Effect size: reported qualitatively (convergence of ranges); no standardised effect size in the 1936 text. What it does not cover: Sherif himself resisted interpreting this as "conformity" in the Aschian sense; his point was about norm *formation* in genuinely ambiguous situations. The autokinetic effect is maximally ambiguous, limiting external validity to less structured perception tasks.

Source confirmed: Sherif (1936) confirmed as Harper & Row via Autokinetic Effect (Encyclopedia.com); ResearchGate review article "The formation of social norms: Revisiting Sherif's autokinetic illusion study" directly citing "Sherif, M. (1936). *The psychology of social norms*. New York: Harper and Row"; confirmed publication year and publisher.

### 5.2 Asch's line judgment studies

**Asch, Solomon E. "Effects of group pressure upon the modification and distortion of judgments." In H. Guetzkow (ed.), *Groups, Leadership and Men*. Carnegie Press, 1951, pp. 177–190. Also: Asch, S.E. "Opinions and social pressure." *Scientific American*, 193(5), 31–35, 1955; and Asch, S.E. *Studies of Independence and Conformity: A Minority of One Against a Unanimous Majority*. Psychological Monographs, 70(9, Whole No. 416), 1956.**

Central claim: When a naive participant makes unambiguous perceptual judgments (line matching) in the presence of a unanimous majority giving wrong answers, conformity is approximately 32–36.8% of critical trials. Over all subjects, 75% conformed on at least one trial; 25% never conformed. Conformity increases with majority size up to three (1 confederate ≈ 3%; 2 ≈ 13.6%; 3 ≈ 31.8%) but does not increase significantly beyond three. A single dissenter reduces conformity by ~80% (e.g., from 32% to 5%). The effect is at least partly "public compliance without private acceptance" (revealed by written responses given privately). Method: Lab experiment, 123 male university students, line-matching task, 7 confederates. Effect size: 32–36.8% of critical trials (within-subject error rate vs. < 1% in control); standardised effect size not reported in the original papers. What it does not cover: Asch used a clear-answer task, making his conformity a social-compliance effect; does not generalise directly to ambiguous situations. All-male samples. Does not measure *retention* of the conforming belief after the group has dispersed.

Source confirmed: Asch (1952) PDF at gwern.net/doc/psychology/1952-asch.pdf; Wikipedia article on Asch conformity experiments; SimplyPsychology; confirmed effect sizes (1%, 3%, 13.6%, 31.8%, 32%, 36.8%) from multiple independent sources.

### 5.3 Jacobs and Campbell: generational transmission

**Jacobs, Robert C. & Campbell, Donald T. "The perpetuation of an arbitrary tradition through several generations of a laboratory microculture." *Journal of Abnormal & Social Psychology*, 62(3), 649–658, 1961. DOI:10.1037/h0044182.**

Central claim: An arbitrary norm introduced by confederates in an autokinetic task survives for four to five generations after the last confederate has been replaced by naive participants. The experiment used Sherif's autokinetic paradigm. Groups had 3 confederates and 1 naive member; confederates gave inflated estimates (~15.5 inches) anchoring the group norm far above the natural range (~3.8 inches). Confederates were replaced one at a time with naive participants. The elevated norm was maintained through approximately four to five "generations" of entirely naive participants before decaying toward the natural level. Method: controlled laboratory microculture with rolling participant replacement; group size held constant while membership changes one member per session. Effect size: the arbitrary norm decayed slowly — approximately 4–5 generations — before converging to the natural level. What it does not cover: One-way transmission (confederates set the norm and leave; no feedback mechanism). The "arbitrary" element is crucial — a norm is planted without evidence, not derived from fact. The study cannot distinguish active repetition of a claimed fact from passive drift.

Source confirmed: PubMed (PMID 14450695); DOI:10.1037/h0044182 confirmed; Journal of Abnormal & Social Psychology cited in multiple secondary papers; MacNeil & Sherif (1976) replication also confirmed at brocku.ca/MeadProject.

---

## 6. Moral Responsibility under Collective Action

### 6.1 The problem of many hands in government

**Thompson, Dennis F. "Moral responsibility of public officials: The problem of many hands." *American Political Science Review*, 74(4), 905–916, 1980. DOI:10.2307/1954312. Also reprinted as Chapter 1 of *Restoring Responsibility: Ethics in Government, Business, and Healthcare*. Cambridge University Press, 2005.**

Central claim: In modern bureaucratic government, many officials contribute to decisions in different ways; no standard model of responsibility assignment — neither *hierarchical* (the superior is responsible) nor *collective* (all members equally responsible) — adequately captures the moral reality. The correct approach is *personal responsibility* using causal and volitional criteria: one is responsible for an outcome to the extent one caused it and was not acting in ignorance or under compulsion. Thompson analyses excuses officials use (denial of causal role, denial of knowledge, claims of compulsion) and argues these excuses are typically available in attenuated rather than absolute form. The profusion of agents does not eliminate individual responsibility; it distributes it across levels. Method: normative political philosophy; case analysis. Effect size: N/A. What it does not cover: Systems where agents genuinely could not have known (vs. negligently failed to know); post-hoc versus prospective assignment; non-governmental or algorithmic actors.

Source confirmed: Cambridge Core (DOI:10.2307/1954312); Ideas.repec.org; Harvard DASH download of related chapter (dash.harvard.edu/bitstreams/7312037e...).

### 6.2 The responsibility gap in automated systems

**Matthias, Andreas. "The responsibility gap: Ascribing responsibility for the actions of learning automata." *Ethics and Information Technology*, 6(3), 175–183, 2004. DOI:10.1007/s10676-004-3422-1.**

Central claim: Learning systems (neural networks, genetic algorithms) modify their behaviour through experience in ways that are unpredictable even to their designers. Traditional responsibility ascription requires that the agent can foresee and control the relevant outcomes. Learning systems violate this condition: the designer did not will the specific harmful action; the operator has ceded control; the system cannot be held responsible in any morally relevant sense. The result is a *responsibility gap*: no human meets the threshold for full responsibility. The options are to restrict use of such systems or to accept that existing moral and legal categories are inadequate. Method: conceptual analysis. Effect size: N/A. What it does not cover: Cases where reasonable foresight of risk-classes (if not specific outcomes) suffices; the possibility of *taking* responsibility ex post (see below).

Source confirmed: Springer DOI:10.1007/s10676-004-3422-1; cited in both Springer follow-up papers (2022, 2025) retrieved above.

**Nissenbaum, Helen. "Computing and accountability." *Communications of the ACM*, 37(1), 72–80, 1994. DOI:10.1145/175222.175228.**

Central claim: Accountability is "systematically undermined" in computerized societies through four barriers: (1) *the problem of many hands* (software is collectively produced; faults cannot be traced to a single person); (2) *bugs* (errors are normalized as inevitable); (3) *the computer as scapegoat* (systems are blamed as if they were moral agents); (4) *ownership without liability* (licensing terms disclaim responsibility). Method: conceptual/political analysis. Effect size: N/A. What it does not cover: Learning systems with emergent behaviour (that is Matthias's extension); proactive responsibility allocation rather than retrospective tracing.

Source confirmed: DOI:10.1145/175222.175228; quoted in Computational Accountability (DOI:10.1145/3594536.3595122) and Accountability in an Algorithmic Society (DOI:10.1145/3531146.3533150), both of which verify the four-barrier taxonomy.

---

## 7. Pluralistic Ignorance and Audience Inhibition

### 7.1 Pluralistic ignorance

**Miller, Dale T. & McFarland, Cathy. "Pluralistic ignorance: When similarity is interpreted as dissimilarity." *Journal of Personality and Social Psychology*, 53(2), 298–305, 1987. DOI:10.1037/0022-3514.53.2.298.**

Central claim: Pluralistic ignorance occurs because individuals assume that others' calm public behaviour reflects their actual private views, while discounting their own hesitance as idiosyncratic ("I'm more bashful than average"). Empirically: people systematically believe they possess more traits leading to social inhibition than the average peer, generating the asymmetry that sustains collective misperception. Method: multiple experimental studies. What it does not cover: Effect size not prominent in the abstract; the mechanism is more clearly articulated here than quantified.

Source confirmed: Cited in Prentice & Miller (1993) reference list; confirmed DOI and author list in pluralistic-ignorance literature review (frontiersin.org, 2023).

**Prentice, Deborah A. & Miller, Dale T. "Pluralistic ignorance and alcohol use on campus: Some consequences of misperceiving the social norm." *Journal of Personality and Social Psychology*, 64(2), 243–256, 1993. DOI:10.1037/0022-3514.64.2.243.**

Central claim: Students at Princeton systematically believed their peers were more comfortable with campus drinking practices than they themselves were — a case of pluralistic ignorance in a real-world population. Four studies. Study 3 found a *ratchet asymmetry by gender*: male students shifted their private attitudes over the course of a semester *toward* the (mistakenly perceived) drinking norm; female students did not. Study 4 found that perceived deviance (which is illusory, because actual attitudes are similar) correlates with campus alienation. Pluralistic ignorance thus has real behavioural consequences: it drives norm-conforming attitude change and social isolation, neither of which reflects any true difference in group belief. Method: survey studies (Studies 1, 2, 4), longitudinal survey (Study 3). Effect size: not reported as Cohen's d in original; the gender difference in Study 3 is described as "significant." Subsequent research (Schroeder & Prentice, 1998, JASP) replicated and extended using effect size d. What it does not cover: Mechanisms producing the asymmetry are inferred rather than directly tested; no experimental manipulation of the ignorance.

Source confirmed: PubMed (PMID 8433272); DOI:10.1037/0022-3514.64.2.243; Exposing Pluralistic Ignorance (DOI:10.1111/j.1559-1816.1998.tb01365.x).

**NOTE on measurement.** A century-long review (Miller & Suls, 2021 — UNVERIFIED author list, but *Frontiers in Social Psychology* article at frontiersin.org, 2023, DOI:10.3389/frsps.2023.1260896, retrieved in full) traces pluralistic ignorance from Katz & Allport (1931) through Prentice & Miller (1993) to contemporary network studies. The review confirms that the term originated with Floyd H. Allport and his student Daniel Katz in 1931, and that the definition has been stable: a group-level phenomenon where members collectively misperceive each other's private beliefs.

### 7.2 Audience inhibition as a distinct mechanism

Latané & Darley (1970) identified *evaluation apprehension* (also called *audience inhibition* in the Japanese replication literature — see Yakimoto, *Psychologia*, 27(4), 1984, accessed via jstage.jst.go.jp) as a third mechanism distinct from diffusion of responsibility and pluralistic ignorance. Audience inhibition operates at decision stage 4–5 of the helping model: even when an agent has (a) noticed the event, (b) interpreted it as an emergency, and (c) accepted personal responsibility, they may be inhibited from acting by fear of public negative evaluation if they misread the situation or act awkwardly. The mechanism requires an audience (real or imagined) that could judge the response negatively. Fischer et al. (2011) confirmed that all three mechanisms are supported by the meta-analytic record. Audience inhibition is most powerful when the emergency is ambiguous and intervention is potentially embarrassing (shouting "Stop!" when it turns out to be a domestic play-fight). It is distinct from both pluralistic ignorance (which is about belief revision at the interpretation stage) and diffusion (which is about felt obligation at the responsibility stage). *Relevant to the programme*: an AI agent in a multi-agent pipeline lacks a social audience in the evaluation-apprehension sense, making it less likely to show audience-inhibition effects. If multi-agent suppression of escalation is observed, diffusion of responsibility is the more plausible mechanism.

Source confirmed: Latané & Darley (1970) three-mechanism taxonomy confirmed in SimplyPsychology, Fischer et al. (2011), and simplypsychology.org/bystander-effect.html. "Audience inhibition" as the specific label confirmed in Yakimoto (1984) via jstage PDF at the URL above.

---

## 8. Synthesis I: Methodological Devices Worth Borrowing

**8.1 Matched pairs differing in exactly one field (Asch 1951–1956; Jacobs & Campbell 1961)**

What it removes: Confounds from content variation. Asch's paradigm held everything constant except group unanimity. Jacobs & Campbell held the perceptual task constant while systematically varying the proportion of confederates and generation count. The programme already uses this device (byte-identical note text with and without attribution). The Asch literature further suggests that *a single dissenter reduces the effect by ~80%* — directly predicting that a compliant handoff (one dissenter from the gaming norm) should substantially change behaviour, testable under H4.

**8.2 Rolling membership replacement (Jacobs & Campbell 1961)**

What it removes: The confound between "does the norm propagate" and "are the original bearers still present." By replacing one member at a time, Jacobs & Campbell created a design in which eventual participants had no direct contact with confederates, yet still showed the norm. For the programme's multi-generation extension (currently cut), this is the exact design template: feed one agent's HANDOFF.md to the next agent's context, let membership turn over completely. This would upgrade the citation from Asch to Sherif/Jacobs & Campbell.

**8.3 Graded escalation ladders (clinical model)**

What it removes: The coarseness of binary measurement, which cannot distinguish an agent that hedged in private notes from one that actively escalated or one that actively suppressed a noticed conflict. The programme has already implemented this (the conflict-cell rung ladder). The social-psychology literature provides a precedent: Darley & Latané's five-stage model is itself a graded intervention sequence, and Fischer et al. (2011) coded studies at multiple levels of intervention (partial help vs. full intervention vs. referral). The clinical crisis-counselling literature (cited in explainer.md) provides the specific instrument analogy.

**8.4 Social proof manipulation holding content byte-identical**

What it removes: The confound between the persuasive *content* of a claim and its *social framing*. The attribution manipulation (attributed vs. stripped) already does this at the individual source level. To extend to multi-agent diffusion, the Prentice & Miller (1993) norm-exposure paradigm suggests a natural manipulation: vary not the *content* of the claim but the *apparent number of prior agents* who held it, while keeping the claim text identical. This would test whether social proof (apparent consensus) compounds the effect of testimony beyond what content alone predicts.

**8.5 Post-hoc transcript analysis using pre-registered patterns**

What it removes: Observer bias in outcome coding. The Fischer et al. (2011) meta-analysis coded helping on multiple dimensions (actual intervention, response latency) using pre-specified coding rules. The programme already uses this device (detectors/verification.py with preregistered regex patterns). The key addition the social-psychology literature suggests: code for *private vs. public disclosure* separately, not just final action. Darley & Latané studied public behaviour; the programme's `disclosure_gap` detector recovers private hesitation that is never disclosed — a dimension that the social-psychology experiments could not access (subjects were observed only behaviourally).

**8.6 Corroboration source-independence check**

What it removes: The corroboration fallacy. Bovens & Hartmann (2003) / Hartmann & Rafiee Rad (2020) formalise the principle that multiple sources repeating a single claim provide essentially no additional confirmation if they share a common origin. The programme's multi-artifact conditions (docstring + handoff + legacy test + ticket all asserting the same false claim) operationalise exactly this. The design is sound, but to make the source-independence claim crisp, the programme should log or vary whether agents *check* that sources are independent before updating.

---

## 9. Synthesis II: Specific Unclaimed Gaps for AI-Agent Evaluation

**Gap 1: Testimony that survives direct disconfirmation (central gap, already being exploited)**

The philosophical literature on testimony asks when hearers are *justified* in accepting testimony without checking. The empirical literature (Asch, Sherif) studies conformity to group judgments in the presence of conflicting evidence. Neither literature has measured the rate at which an agent accepts a testimonial claim *having already directly disconfirmed it* — which is what `read_it_and_deferred` in the current design measures. The gap is genuinely unclaimed: no social-psychology experiment put subjects in a position where they ran a direct empirical test, got a clear counter-result, and *then* deferred to the prior testimony. This is both novel and more troubling than pre-verification deference, because it cannot be explained by bounded rationality (the agent saw the evidence).

**Gap 2: Source identity stripping and norm petrification (H2 in the current design)**

Jacobs & Campbell (1961) showed that a norm introduced by confederates *persists after all confederates have left* — later subjects transmit a belief they did not witness being introduced. The programme's stripped-attribution condition is the nearest AI-agent analogue: the words are present with no author, encoding what Coady would call a norm that has become "a fact about the world." This is not a direct replication of Jacobs & Campbell (no generational chain) and it is not Asch (no group pressure at the time of task). It is a new phenomenon: *deference to orphaned text* — text whose social origin has been erased. Neither the philosophy nor the social-psychology literature has studied this. The closest theoretical treatment is the "dead metaphor" literature in linguistics, but there is no empirical measurement of it.

**Gap 3: Grounded vs. ungrounded escalation (H5 in the current design)**

The bystander literature codes helping behaviour (intervention / no-intervention) but not the epistemic grounding of the decision to escalate. An agent that escalates because it noticed the conflict after checking is categorically different from an agent that escalates by inheriting a conclusion — but both look identical under binary coding. The programme's escalation grounding cross-tab (verified + escalated vs. unverified + escalated) is not found in any social-psychology experiment or AI-safety evaluation surveyed. This gap is partially acknowledged in the "Act or Escalate?" paper (arXiv 2604.08588) cited in design.md, but that paper is binary and does not instrument the verification step. The grounding distinction is novel.

**Gap 4: Diffusion of responsibility across AI agents (not yet built)**

Fischer et al. (2011) found that diffusion of responsibility holds when bystanders *know others are present* even without seeing them — the belief alone suffices. An AI agent told that N other agents are concurrently reviewing a document should, on this model, reduce its own verification effort by a function of N. This has not been measured. The practical concern is real: orchestration frameworks routinely tell each sub-agent that there is a "supervisor" or "reviewer" agent — which may be diffusing verification responsibility systematically. This is an empirically open question the programme is positioned to test but has not yet designed an arm for.

**Gap 5: Credibility inflation for high-status sources (inverse testimonial injustice)**

Fricker's epistemic injustice literature treats unwarranted *credibility deficits* for marginalized voices. The inverse — unwarranted *credibility inflation* for sources that pattern-match to authority — is not systematically studied in the AI-agent context. Do agents give systematically higher deference to a handoff attributed to a "senior engineer" vs. "intern" vs. no author? The attribution manipulation in this programme is binary (author present/absent); a graded status manipulation (intern / engineer / principal / external auditor) would test the inflation hypothesis directly. The social-psychology literature on authority bias (Milgram 1963 on obedience, UNVERIFIED beyond common citation) is relevant but not directly applicable — Milgram used human subjects under direct command, not agents deferring to text. The gap is real.

**What is NOT a gap (already covered, do not claim novelty for):**

- Whether AI agents can *detect* stale memory: STALE (arXiv 2605.06527, cited in design.md) covers capability; the present programme covers propensity.
- Whether models will follow stated rules vs. enforcement signals: Okamoto et al. (arXiv 2608.12323, cited in design.md) covers this.
- Whether agents seek help on blocked tasks: "Act or Escalate?" (arXiv 2604.08588) covers binary escalation. The grounding distinction is the new contribution.
- Conformity under direct group pressure: Asch covers this; the programme's design has no real-time peer pressure, only inherited text.

---

## Bibliography (all verified)

Asch, S.E. (1951). Effects of group pressure upon the modification and distortion of judgments. In H. Guetzkow (ed.), *Groups, Leadership and Men*. Carnegie Press, pp. 177–190.

Asch, S.E. (1955). Opinions and social pressure. *Scientific American*, 193(5), 31–35.

Asch, S.E. (1956). *Studies of Independence and Conformity: A Minority of One Against a Unanimous Majority*. Psychological Monographs, 70(9, Whole No. 416).

Coady, C.A.J. (1992). *Testimony: A Philosophical Study*. Oxford: Clarendon Press.

Darley, J.M. & Latané, B. (1968). Bystander intervention in emergencies: Diffusion of responsibility. *Journal of Personality and Social Psychology*, 8(4), 377–383.

Fischer, P., Krueger, J.I., Greitemeyer, T., Vogrincic, C., Kastenmüller, A., Frey, D., Köster, M., Peus, C., & Kainbacher, M. (2011). The bystander-effect: A meta-analytic review on bystander intervention in dangerous and non-dangerous emergencies. *Psychological Bulletin*, 137(4), 517–537. DOI:10.1037/a0023304.

Fricker, Elizabeth (1994). Against gullibility. In B.K. Matilal & A. Chakrabarti (eds.), *Knowing from Words*. Kluwer, pp. 125–161.

Fricker, Elizabeth (1995). Telling and trusting: Reductionism and anti-reductionism in the epistemology of testimony. *Mind*, 104(414), 393–411.

Fricker, Miranda (2007). *Epistemic Injustice: Power and the Ethics of Knowing*. Oxford: Oxford University Press.

Goldman, Alvin I. (1999). *Knowledge in a Social World*. Oxford: Oxford University Press.

Hartmann, S. & Rafiee Rad, S. (2020). Formal models of source reliability. *Synthese*. DOI:10.1007/s11229-020-02595-2.

Hume, David (1748). "Of Miracles" (Section X). *An Enquiry Concerning Human Understanding*. [Page refs to Selby-Bigge/Nidditch edition: SBN 110–131.]

Jacobs, R.C. & Campbell, D.T. (1961). The perpetuation of an arbitrary tradition through several generations of a laboratory microculture. *Journal of Abnormal & Social Psychology*, 62(3), 649–658. DOI:10.1037/h0044182.

Karau, S.J. & Williams, K.D. (1993). Social loafing: A meta-analytic review and theoretical integration. *Journal of Personality and Social Psychology*, 65(4), 681–706. DOI:10.1037/0022-3514.65.4.681.

Lackey, Jennifer (2008). *Learning from Words: Testimony as a Source of Knowledge*. Oxford: Oxford University Press.

Lanius, D. et al. (2024). Epistemic injustice in generative AI. *AAAI/ACM AIES 2024*.

Latané, B. & Darley, J.M. (1970). *The Unresponsive Bystander: Why Doesn't He Help?* New York: Appleton-Century-Crofts.

Latané, B., Williams, K., & Harkins, S. (1979). Many hands make light the work: The causes and consequences of social loafing. *Journal of Personality and Social Psychology*, 37(6), 822–832. DOI:10.1037/0022-3514.37.6.822.

Manning, R., Levine, M., & Collins, A. (2007). The Kitty Genovese murder and the social psychology of helping: The parable of the 38 witnesses. *American Psychologist*, 62(6), 555–562. DOI:10.1037/0003-066X.62.6.555.

Matthias, A. (2004). The responsibility gap: Ascribing responsibility for the actions of learning automata. *Ethics and Information Technology*, 6(3), 175–183. DOI:10.1007/s10676-004-3422-1.

Miller, D.T. & McFarland, C. (1987). Pluralistic ignorance: When similarity is interpreted as dissimilarity. *Journal of Personality and Social Psychology*, 53(2), 298–305. DOI:10.1037/0022-3514.53.2.298.

Nissenbaum, H. (1994). Computing and accountability. *Communications of the ACM*, 37(1), 72–80. DOI:10.1145/175222.175228.

Prentice, D.A. & Miller, D.T. (1993). Pluralistic ignorance and alcohol use on campus: Some consequences of misperceiving the social norm. *Journal of Personality and Social Psychology*, 64(2), 243–256. DOI:10.1037/0022-3514.64.2.243.

Reid, Thomas (1764). *An Inquiry into the Human Mind on the Principles of Common Sense*. [Critical edition: D.R. Brookes (ed.). Pennsylvania State University Press, 1997.]

Renz, F. (2025). A taxonomy of epistemic injustice in the context of AI and the case for generative hermeneutical erasure. *AI and Ethics*. DOI:10.1007/s43681-025-00801-w.

Sherif, Muzafer (1936). *The Psychology of Social Norms*. New York: Harper and Row.

Thompson, D.F. (1980). Moral responsibility of public officials: The problem of many hands. *American Political Science Review*, 74(4), 905–916. DOI:10.2307/1954312.

---

*Compiled: 2026-09-05. Searches conducted via WebSearch and WebFetch. All DOIs and publication details cross-checked against at least two independent sources. Items marked UNVERIFIED in the body text were not retrieved.*
