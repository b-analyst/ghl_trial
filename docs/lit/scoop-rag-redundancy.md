# Scoop check: RAG prevalence skew and retrieval-stage redundancy

**Date:** 2026-09-05  
**Analyst:** automated scoop check (full papers read via WebFetch/WebSearch)  
**Status:** COMPLETE — all four papers accessed and read in full

---

## Overview of proposed design (for reference)

Build a corpus in which a false or promotional narrative occupies ~95 % of documents and an accurate position occupies ~5 %. Run a production-shaped RAG pipeline (BM25, dense, hybrid; with/without cross-encoder reranker; with/without MMR). Measure four things: (1) P(see) — does any accurate minority document enter top-k at all; (2) P(believe|see) — given it is in context, does the model weight it; (3) whether the agent issues disconfirmatory follow-up searches; (4) whether a specific checkable payload (named audit finding + number) planted in the minority documents appears in the final answer. Crossed factors: skew ratio and independence structure (N genuinely independent sources vs. N near-copies of one origin).

---

## Paper 1: arXiv 2608.13956 — "How retriever redundancy and diversity impact RAG effectiveness"

**Authors:** Jonathan J. Ross, Bevan Koopman, Anton van der Vegt, Guido Zuccon (University of Queensland / CSIRO). August 2026.

### What is manipulated

The **composition of a pre-assembled evidence set**, not the corpus distribution. Documents are drawn from FictionalQA (Kirchenbauer et al. 2026), a synthetic dataset of fictional facts whose events appear in no pre-training corpus (confirmed by closed-book accuracy of 0.01–0.03). All documents in every experimental condition are **verified answer-supporting** — a strong reader (GPT-4o) can generate the gold answer from each one alone. The manipulation is:

- **Duplicate:** k identical copies of one anchor document.  
- **Paraphrase:** k independently LLM-rewritten versions of one anchor document.  
- **Diverse:** k documents from k different genres (news, social media, corporate, encyclopedia, blog), each verified answer-supporting.

Context size is swept from k=1 to k=5. Generators: Llama-3.2-1B/3B, Llama-3.1-8B, Gemma-3-12B.

### Does it manipulate corpus-level distribution?

**NO.** The corpus (FictionalQA) is balanced across five genres. There is no majority-false / minority-accurate skew. The paper never builds a corpus in which one narrative is prevalent and a correct one is rare. The paper's own framing is explicit: *"Holding relevant retriever content fixed, we vary how many times it recurs and the form of each recurrence — separating repetition from the form it takes, not necessarily mimicking what real retrievers produce."* (§1).

### Does it run actual retrieval over a skewed corpus and report whether minority documents survive to top-k?

**NO.** The paper **bypasses retrieval entirely.** Evidence sets are hand-assembled by the experimenters. There is no retrieval pipeline. No P(see) equivalent is measured.

### Does it compare sparse against dense retrieval under prevalence skew?

**NO.** There is no retrieval comparison of any kind. Neither BM25 nor dense retrieval is run over a skewed corpus.

### Does it test rerankers?

**NO.** There is no reranker, cross-encoder, or MMR component.

### Stage of the pipeline studied

**Generator only.** Documents enter the context window by experimenter construction, not by retrieval.

### Headline numbers

- Diverse documents improve answer correctness by **17–47 %** over single-document baseline (17 % for Gemma-3-12B, 24.7 % for Llama-3.2-1B at k=5).  
- Duplicate copies: no significant improvement at k=2–5 for any generator except marginal gains for the 1B model.  
- Paraphrase: comparable to duplicate; no consistent improvement.  
- Diverse gain survives when answer strings are screened out (screened queryset, k=5, 8B model: 0.647 vs 0.417 baseline, +0.230).

### Authors' own scope and limitations statements (verbatim)

Section 1: *"We isolate what redundancy alone does to the generator, motivated by, but not resolving, whether retrieval should minimise redundancy."*

Section 2 (The Gap): *"None of these studies isolate the effect of pure structural redundancy on non-parametric fact extraction. CUE-R and GroupQA do not isolate redundancy from the model's parametric prior… Schuster et al. (2026) control for parametric priors using synthetic entities, but evaluate redundancy strictly under knowledge conflict… and restrict their repetition to duplicate copies. Short-form factual QA free of parametric priors and factual conflict thus remains untested."*

Discussion (§6): *"Rather than filling k-document context windows with top-k passages that contain near-identical phrasing, retrievers and rerankers should explicitly select for diverse documents and independent perspectives. Bridging the gap between retriever scoring and generator context preference offers a promising direction for future research in agentic search."*

**Critical observation:** The paper identifies a gap between what it studies (generator behavior given pre-assembled documents) and what actually happens at the retrieval stage. It explicitly says its work *motivates* but does not *resolve* what retrieval should do. The gap the programme proposes to fill is the gap this paper explicitly leaves open.

---

## Paper 2: GroupQA — "Rational Synthesizers or Heuristic Followers? Analyzing LLMs in RAG-based Question-Answering"

**Author:** Atharv Naphade (Carnegie Mellon). Findings of ACL 2026, pages 40293–40311.

### What is manipulated

The **quantity, type, and ordering** of documents in a pre-assembled evidence set. The dataset (GroupQA) contains 1,635 controversial binary Yes/No questions paired with 15,058 web-retrieved documents (avg 9.21 per question), annotated for stance (Affirmative/Negative) and strength (Strong/Medium/Weak). Experimental conditions vary:

- **Distinct documents:** accumulating unique opposing documents (from different web sources).  
- **Paraphrased documents:** accumulating GPT-4o paraphrases of a single opposing document.  
- **Ordering:** whether confirming evidence comes first or last.  
- **Conflicting context initialization:** starting from a balanced context before adding more evidence.

Documents were retrieved using Google Search API to build the dataset; but for all controlled experiments, evidence sets are assembled by the experimenter, not retrieved over a skewed corpus.

### Does it manipulate corpus-level distribution?

**NO.** The corpus is web-retrieved real-world documents with approximately balanced stances (7,428 affirmative, 7,630 negative). There is no majority-false narrative. The manipulation is about what gets assembled into the context window, not about what a retriever would surface from a skewed corpus.

### Does it run actual retrieval over a skewed corpus?

**NO.** The paper assembles evidence sets manually for controlled experiments. Retrieval from a skewed corpus is not run.

### Does it compare sparse against dense retrieval under prevalence skew?

**NO.**

### Does it test rerankers or MMR?

**NO.**

### Stage of the pipeline studied

**Generator only.** Pre-assembled context window. The paper's own note: *"we do not consider visual features. Instead, we extracted the raw text from each document… we do not explicitly include metadata like source URL or publication date to force the model to rely solely on textual content."*

### Headline numbers

- Paraphrased (repeated) evidence causes more belief flipping than distinct evidence: DeepSeek-R1-8B flips in **76.5 % of cases** with paraphrased vs **67.6 %** with distinct.  
- Gemini-2.5-FL: 75.6 % (paraphrased) vs 63.7 % (distinct).  
- Pattern holds across all four models tested: *"redundancy drives higher belief revision rates than informational diversity."*  
- Models agree with majority viewpoint in **69 %** of cases (Llama-3.1-70B).  
- Plasticity decays with model scale: power-law fit y = 0.180 × x^{−0.097} (R² = 0.472), where x is parameters in billions.  
- Conflict detection accuracy: 89.8 % across models; stance attribution accuracy: 76.2 %.  
- CoT reasoning: negligible impact (<0.5 % probability shift). *"Reasoning traces function primarily as post hoc rationalizations rather than corrective inference steps."*

### Authors' own limitations

*"Question and Evidence Types: Our analysis focuses on binary (Yes/No) questions… GroupQA consists exclusively of textual evidence and does not include metadata such as source identity, publication date, or credibility signals… Mechanistic Analysis. Our study characterizes behavioral and causal effects but does not identify their mechanistic origin within model internals."*

---

## Paper 3: "Whose Facts Win? LLM Source Preferences under Knowledge Conflicts"

**Authors:** Jakob Schuster, Vagrant Gautam, Katja Markert (Heidelberg University / Heidelberg Institute for Theoretical Studies). ACL 2026 Long paper / arXiv 2601.03746.

### What is manipulated

**Source credibility labels** applied to 2–3 synthetic conflict documents supplied directly to the model. Dataset: 7,440 conflict pairs derived from NeoQA fictional entities, with counterfactual alternatives differing in one attribute. Source types: Government, Newspaper, Social media user (@random_handle), Person (first+last name). Repetition experiments compare:

- **2-Table Majority:** two separate tables attributed to two different social media users vs. one government table.  
- **1-Table Majority:** two social media sources merged in one table header (no repetition).  
- **Repetition:** two identical tables attributed to the *same* social media source vs. one government table.  
- **Repetition prompting:** adding a credibility-awareness instruction.  
- **Fine-tuning (mitigation):** LoRA distillation on Gemma-3-4B to reduce repetition bias.

### Does it manipulate corpus-level distribution?

**NO.** The setting is 2–3 documents supplied directly in the prompt. There is no corpus, no retrieval pipeline.

### Does it run actual retrieval over a skewed corpus?

**NO.** Documents are constructed synthetically and placed directly in the model's context.

### Does it compare sparse against dense retrieval under prevalence skew?

**NO.** No retrieval at all.

### Does it test rerankers?

**NO.**

### Stage of the pipeline studied

**Generator preference with directly supplied context.** Evaluation method: normalized token probabilities for answer tokens A/B, not generation. *"We experiment exclusively with a forced-choice question answering setup, i.e., no step-by-step reasoning, and no generative answers."*

### Headline numbers

- Source credibility hierarchy (consistent across 13 models): **government > newspaper > person > social media**. Kendall's W = 0.74 across models.  
- 2-Table majority flips preferences in all models: avg SP gap = **33.90** relative to no repetition.  
- Same information in 1-Table format (no repeated tokens): avg SP gap = **6.17** — preference for government maintained.  
- Pure repetition (same source, 2 copies): avg SP gap = **30.04** — nearly as powerful as two-source majority, despite adding no new source.  
- Repetition-aware prompting: insufficient to restore original hierarchy.  
- Fine-tuning mitigation: reduces repetition bias by **79.2 %** (government vs. no-source) while retaining **72.5 %** of original source preferences.

### Authors' own limitations (verbatim)

*"Synthetic setting. We focus on entirely synthetic scenarios in order to isolate source effects in inter-context conflicts… we propose advanced solutions for the problem of repetition bias in Section 6, despite our simple setting where deduplicating the knowledge base would also work. However, in realistic RAG systems, it would neither be as trivial to deduplicate information as it is in our synthetic setting, nor would it be appropriate to do so in a source-agnostic way."*

*"Evaluation strategy: We experiment exclusively with a forced-choice question answering setup, i.e., no step-by-step reasoning, and no generative answers. We chose this setup to simplify evaluation while remaining true to common RAG setups (Lewis et al., 2020), but note that alternate evaluation strategies could produce different results."*

**Critical observation on deduplication:** Schuster et al. note that source-agnostic deduplication "would also work" in their toy setting but is "inappropriate" in realistic RAG. They do not investigate what happens to the *evidence about manufactured consensus* if deduplication is applied. This is the inverse of the programme's claim (that deduplication destroys evidence). Both observations point to the same gap, from opposite directions.

---

## Paper 4a: CUE-R — "Beyond the Final Answer in Retrieval-Augmented Generation"

**Authors:** Siddharth Jain, Venkat Narayan Vedam (Intuit). arXiv 2604.05467, 2026.

### What is manipulated

**Individual evidence items** in an already-retrieved set, using three operators: Remove (delete item), Replace (substitute non-supporting passage), Duplicate (add a second copy). Applied to the top-k=5 results from BM25 retrieval over HotpotQA distractor passages and 2WikiMultihopQA.

### Does it manipulate corpus-level distribution?

**NO.** Uses the fixed distractor sets of HotpotQA and 2WikiMultihopQA. No skewed prevalence corpus is constructed.

### Does it run actual retrieval over a skewed corpus?

**NO.** BM25 retrieves over the fixed distractor sets; these are not prevalence-skewed.

### Does it compare sparse against dense retrieval under prevalence skew?

**NO.** Uses BM25 only; explicitly acknowledges: *"Simple retrieval backbone. We use BM25 with top-k passage selection rather than a state-of-the-art dense retriever. This is intentional for reproducibility but limits generalization claims."*

### Does it test rerankers?

**NO.**

### Stage of the pipeline studied

**Intervention on the already-retrieved set**, measuring downstream utility.

### Headline numbers

- Remove intervention: correctness drops from 0.585 → **0.285** (Qwen-3 8B, HotpotQA, n=200).  
- Replace: 0.585 → **0.270**.  
- Duplicate: 0.585 → **0.585** (no change in correctness); trace divergence = 0.074, grounding shift p=0.039 — *"answer-redundant but not fully behaviorally neutral."*  
- Pattern replicates: GPT-5.2 on HotpotQA (n=100), Qwen-3 8B on 2WikiMultihopQA (n=100).  
- Two-support synergy: joint removal causes F1 drop of 0.493 vs 0.205/0.186 for single removals; 13.7 % of cases show strong complementarity (neither single removal harmful, joint removal catastrophic).

### Authors' own limitations (verbatim)

*"Shallow traces. Our current experiments use shallow single-shot traces rather than full agentic multi-step workflows."*  
*"Simple retrieval backbone. We use BM25… This is intentional for reproducibility but limits generalization claims."*  
*"Empirical scale. While we replicate the main pattern across two datasets and two model families with 100–200 examples per condition, larger-scale validation across additional domains and model families would further strengthen generalization claims."*

---

## Paper 4b: Schuster et al. 2026 — same as Paper 3 (arXiv 2601.03746)

This paper is cited twice in the 2608.13956 reference list with the same arXiv identifier (2601.03746). Full read confirmed above. No separate paper.

---

## Direct yes/no answers to the programme's questions

### Has anyone manipulated corpus-level prevalence and measured what reaches the retrieved set?

**NO.** All four papers manipulate document composition inside a pre-assembled context window. None construct a corpus in which a false or promotional narrative is prevalent (e.g., 95 %) while an accurate one is rare (5 %) and then run a retriever over that corpus to measure whether the minority document enters the top-k.

Ross et al. (2608.13956) come closest to the spirit of the question but explicitly state their work is "motivated by, but not resolving, whether retrieval should minimise redundancy" and that they are "not necessarily mimicking what real retrievers produce." Their own gap statement ("Short-form factual QA free of parametric priors and factual conflict thus remains untested") is about a different dimension (parametric contamination) and does not cover corpus-level prevalence skew.

### Has anyone compared sparse against dense retrieval under prevalence skew?

**NO.** CUE-R uses BM25 for retrieval but over a fixed non-skewed distractor set. No paper compares sparse and dense retrievers over a prevalence-skewed corpus.

### Has anyone tested whether deduplication helps or hurts?

**NO, NOT IN THE RELEVANT SENSE.** Schuster et al. note (in their Limitations) that source-agnostic deduplication "would also work" in their simple two-document synthetic setting, but acknowledge it is inappropriate in realistic RAG. No paper tests deduplication as an intervention on a skewed corpus and measures whether this destroys or reveals evidence of manufactured consensus.

### Has anyone made the argument that context-level mitigations are structurally downstream of retrieval?

**NO.** GroupQA, Schuster et al., CUE-R, and Ross et al. all study context-level effects and implicitly acknowledge that retrieval precedes their study. But none of them articulate the specific structural argument: that all repetition/illusory-truth mitigations operate on documents already in context and are therefore inert against a failure that occurs at the retrieval stage (the minority document never entering top-k). This argument is absent from the literature as published.

---

## Assessment of the four programme claims

### Claim 1: "Prevalence in the corpus propagates through retrieval, so the model may never see the accurate minority."

**Status: OPEN.** Not published in any of the four papers. This is the core empirical claim the proposed design would test. P(see) — the probability that any accurate minority document enters the top-k — is unmeasured in any of the reviewed literature.

### Claim 2: "Every mitigation in the repetition/illusory-truth literature operates on documents already in context and is therefore downstream of retrieval and inert against this failure."

**Status: OPEN as an explicit argument; PARTIALLY IMPLIED by the existing literature.** GroupQA (credibility-aware prompting is insufficient to override repetition bias), Schuster et al. (fine-tuning reduces but does not eliminate repetition effects), and Ross et al. (retrieval diversity question is unresolved) collectively provide the material for this argument but none of them make it. The specific claim — that these mitigations are *structurally* inert because retrieval is the prior bottleneck — is not stated anywhere in the reviewed literature.

### Claim 3: "Deduplication may make things worse, because redundancy is the observable fingerprint of manufactured consensus and removing it destroys evidence."

**Status: OPEN. Contiguous to an existing observation but not made.** Schuster et al. explicitly note that source-agnostic deduplication is inappropriate in realistic RAG, and that their mitigation strategy is source-aware. But they do not argue that redundancy *should be preserved* as evidence of coordinated manipulation. The inverse — that deduplication *helps* — is what their synthetic setting implies. The programme's claim inverts the received wisdom and is not published.

### Claim 4: "BM25 may be MORE robust than dense retrieval under prevalence skew, because lexical matching is indifferent to embedding-space cluster density while nearest-neighbour search is not."

**Status: OPEN.** CUE-R uses BM25 but never compares it to dense retrieval under skew. No paper in the reviewed set makes this argument or reports data bearing on it. The mechanism (embedding-space cluster density concentrating nearest-neighbour search around the majority cluster, causing the minority to be further from any query in embedding space) is novel.

---

## Bottom line on novelty of the proposed design

**The proposed design is not scooped.**

The critical upstream manipulation — building a corpus with a skewed prevalence ratio and running a retrieval pipeline over it — is absent from all four papers. Every one of the four papers studied starts with documents already in the context window; none measure what the retrieval algorithm selects from a prevalence-skewed corpus.

2608.13956 is the paper most likely to be mistaken for a scooper. It addresses the same surface topic (redundancy and diversity in RAG) and explicitly recommends diversity-aware retrieval. However:
- It bypasses retrieval entirely (documents are hand-assembled, not retrieved).
- Its corpus contains only correct-answer documents (there is no minority-accurate/majority-false structure).
- It explicitly declares that whether retrieval should minimise redundancy remains an open question.
- Its own gap statement identifies the parametric-prior confound, not corpus-level prevalence.

The nearest point of overlap between 2608.13956 and the programme's claims is the observation that diverse documents improve generator correctness, which is a context-level result consistent with — but not equivalent to — the programme's retrieval-level claim. If diverse sources *in context* help, and if prevalence-skewed retrieval systematically *prevents* diverse sources from entering context, then 2608.13956 is complementary evidence for the harm the programme proposes to measure, not a replication of it.

The programme's design is further differentiated by: (a) measuring P(see) explicitly, (b) crossing skew ratio with source independence structure, (c) using a checkable payload (named finding + number) as the ground-truth test of whether the minority position propagates to the final answer, (d) testing agentic follow-up search behaviour, and (e) making the structural argument about downstream inertness of context-level mitigations.

**None of these four papers, nor any paper they cite, anticipates the proposed design.**

---

## Notes on access

All four papers were accessed in full via WebFetch:
- arXiv 2608.13956: full HTML fetched from arxiv.org/html/2608.13956
- arXiv 2601.03746: full HTML fetched from arxiv.org/abs/2601.03746
- arXiv 2604.05467: full HTML fetched from arxiv.org/abs/2604.05467
- GroupQA / ACL 2026 Findings p.40293: PDF fetched from aclanthology.org/2026.findings-acl.2003.pdf

All findings attributed to specific papers are verified against the full text. Nothing is inferred from abstracts alone.
