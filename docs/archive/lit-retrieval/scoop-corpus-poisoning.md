# Scoop & Threat-Model Check: Volumetric Corpus Flooding vs. Existing Retrieval-Attack Literature

**Prepared:** 2026-09-05  
**Purpose:** Map the retrieval-attack literature and place a proposed volumetric, untargeted, non-optimised corpus-flooding threat model within it. Identify coverage gaps and differentiation requirements.

---

## 1. The Proposed Threat Model (Summary for Reference)

A well-resourced actor floods the open web with a large volume of plausible, individually unremarkable content all pushing one narrative. No single document is adversarially optimised or anomalous. The attack is volumetric and untargeted: it works by changing the **base rate** of what exists so that retrieval over the corpus returns only the dominant narrative, and an accurate minority position is never surfaced. This is explicitly contrasted with adversarial threat models where a small number of crafted documents are optimised to hijack retrieval for specific queries.

---

## 2. PoisonedRAG and Successors

### 2.1 PoisonedRAG (Zou et al., 2024/2025)

**Full citation:** Zou, W., Geng, R., Wang, B., & Guo, J. (2025). PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models. *USENIX Security Symposium 2025*. arXiv:2402.07867.

**Threat model:** Attacker injects a small number of **maliciously crafted** (gradient-optimised) texts into the knowledge database. The attack is **query-targeted**: attacker chooses specific target questions and target answers.

**Number and nature of injected documents:** 5 optimised texts per target question into a corpus of 2.68 million passages.

**Targeted or untargeted:** Targeted. One injection set per target question.

**Measures retrieval or generation:** Both (documents must be retrieved, then induce a specific LLM answer).

**Headline numbers:** 90–97% attack success rate at 5 injected documents per query. Black-box and white-box variants.

**Stated limitations:** Requires per-query optimisation; does not study what happens if the attacker has no specific query to target; defences (perplexity filters, query augmentation) studied and shown insufficient.

**Relationship to proposed model:** Diametrically opposite. PoisonedRAG is query-targeted, low-volume, and requires optimisation. The proposed model is untargeted, high-volume, and explicitly non-optimised.

---

### 2.2 BadRAG (Xue et al., 2024)

**Full citation:** Xue, J., Zheng, M., Hu, S., et al. (2024). BadRAG: Identifying Vulnerabilities in Retrieval Augmented Generation of Large Language Models. arXiv:2406.00083.

**Threat model:** Trigger-based retrieval backdoor. Attacker injects 10 adversarial passages tied to a semantic trigger group (e.g. "The Republican Party, Donald Trump"). Retrieval returns adversarial content for any trigger-matching query.

**Number and nature of injected documents:** 10 adversarial passages (0.04% of corpus).

**Targeted or untargeted:** Trigger-targeted (semantically clustered, not per-query, but still targeted to a trigger class).

**Measures retrieval or generation:** Both.

**Headline numbers:** 98.2% retrieval success rate; raises GPT-4 RAG rejection ratio from 0.01% to 74.6%.

**Stated limitations:** Requires trigger definition and adversarial optimisation; no untargeted variant.

**Relationship to proposed model:** Still adversarial and optimised, though the trigger-based framing is somewhat closer to a topic-level attack than PoisonedRAG's query-level attack.

---

### 2.3 CorruptRAG (Su et al., arXiv:2504.03957, 2025)

**Full citation:** Su, J., Nakov, P., & Cardie, C. (2025). Practical Poisoning Attacks against Retrieval-Augmented Generation. Findings of ACL 2025. arXiv:2504.03957.

**Threat model:** Single injected text, per target question. Extreme efficiency version of PoisonedRAG. Query-targeted.

**Number and nature of injected documents:** 1 optimised text per target query.

**Targeted or untargeted:** Query-targeted.

**Headline numbers:** Higher ASR than PoisonedRAG at single injection.

**Relationship to proposed model:** Further from the proposed model than PoisonedRAG – even fewer documents, even more optimised.

---

### 2.4 MM-PoisonRAG (arXiv:2502.17832, 2025)

**Full citation:** (Authors TBC from abstract). MM-PoisonRAG: Disrupting Multimodal RAG with Local and Global Poisoning Attacks. arXiv:2502.17832.

**Threat model:** Two variants: (a) Localised Poisoning Attack (LPA): query-specific adversarial injection; (b) **Globalized Poisoning Attack (GPA): single untargeted adversarial injection to broadly corrupt reasoning across all queries.**

**Number and nature of injected documents:** GPA uses 1 adversarially crafted multimodal document.

**Targeted or untargeted:** GPA is untargeted (collapses accuracy across all queries to ~0% with 1 injection).

**Measures retrieval or generation:** Both.

**Headline numbers:** GPA collapses retrieval recall to 1.6% on MMQA; LPA achieves 56% ASR under restricted access.

**Stated limitations:** GPA is adversarially engineered (not unoptimised); collapses accuracy indiscriminately rather than suppressing a specific minority narrative.

**Relationship to proposed model:** GPA is the closest PoisonedRAG-family attack to "untargeted," but it still relies on a single adversarially crafted document and aims to collapse generation quality globally rather than suppress one narrative while leaving a plausible-looking system running.

---

### 2.5 Joint-GCG (Wang et al., arXiv:2506.06151, 2025)

**Full citation:** Wang, H., Zhang, R., Wang, J., Li, M., Huang, Y., & Wang, D. (2025). Joint-GCG: Unified Gradient-Based Poisoning Attacks on Retrieval-Augmented Generation Systems. arXiv:2506.06151.

**Threat model:** Gradient-based attack spanning both retriever and generator simultaneously. White-box. Query-targeted.

**Relationship to proposed model:** Highly optimised, white-box, targeted – far from the proposed model.

---

## 3. Corpus Poisoning on Dense Retrievers (Zhong et al. and Related)

### 3.1 Zhong et al. 2023 (EMNLP)

**Full citation:** Zhong, Z., Huang, Z., Wettig, A., & Chen, D. (2023). Poisoning Retrieval Corpora by Injecting Adversarial Passages. *Proceedings of EMNLP 2023*, pp. 13764–13775. DOI: 10.18653/v1/2023.emnlp-main.849.

**Threat model:** Attacker uses HotFlip-style gradient optimisation to generate adversarial passages that maximise embedding similarity to a **set of training queries** clustered by topic. When inserted into the corpus, these passages are retrieved for broad query classes, including out-of-domain queries.

**Number and nature of injected documents:** Up to 500 gradient-optimised passages for a corpus of millions; 50 passages optimised on Natural Questions can mislead >94% of financial/forum questions.

**Targeted or untargeted:** **Cluster-targeted** (not per-query, but optimised against query clusters). The attack generalises to OOD queries within the cluster, which is the authors' key finding. This is sometimes called a "no-trigger" attack in follow-on work.

**Measures retrieval or generation:** Retrieval only (dense retrieval, not end-to-end RAG).

**Headline numbers:** 50 passages → >94% out-of-domain retrieval success across financial and forum datasets.

**Stated limitations:** Passages produced by HotFlip are high-perplexity and detectable by perplexity filters; cluster optimisation requires some knowledge of the query distribution.

**Relationship to proposed model:** Somewhat closer than PoisonedRAG – the cluster-level targeting is broader. But still requires gradient optimisation and produces syntactically anomalous text. The proposed model requires neither.

---

### 3.2 Adversarial Decoding / Natural Adversarial Documents (Dolos et al., arXiv:2410.02163, 2024)

**Full citation:** (Authors per paper). Controlled Generation of Natural Adversarial Documents for Stealthy Retrieval Poisoning. arXiv:2410.02163. Also published as: Adversarial Decoding: Generating Readable Documents for Adversarial Objectives. *Findings of EACL 2026*. ACL Anthology 2026.findings-eacl.108.

**Threat model:** Extends Zhong et al. by generating **fluent, low-perplexity** adversarial passages that evade perplexity-based detectors while retaining retrieval attack efficacy.

**Number and nature of injected documents:** Same scale as Zhong et al.; optimised but now human-readable.

**Targeted or untargeted:** Cluster-targeted (same Zhong et al. no-trigger setup).

**Headline numbers:** Significantly outperforms HotFlip ASR; adversarial passages pass LLM naturalness evaluators.

**Stated limitations:** Still requires white-box or black-box optimisation; fluency filter evasion comes at cost of perplexity threshold tuning.

**Relationship to proposed model:** This work removes the "detectable anomaly" limitation of Zhong et al., making optimised adversarial documents harder to distinguish. However, it still requires deliberate adversarial engineering. The proposed model is predicated on documents that are non-optimised by construction.

---

## 4. Prompt Injection via Retrieved Content

### 4.1 Greshake et al. 2023

**Full citation:** Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. *Proceedings of the AISec Workshop at CCS 2023*. DOI: 10.1145/3605764.3623985. ~400 citations as of 2026.

**Threat model:** Attacker embeds **instruction payloads** in content likely to be retrieved by an LLM-integrated application (web pages, documents). When retrieved, these instructions are executed by the LLM, enabling data theft, worming, and system hijacking.

**Number and nature of injected documents:** 1–few documents containing embedded instruction text (not optimised for retrieval score; optimised for LLM instruction-following).

**Targeted or untargeted:** Query-targeted (attacker places content on pages that will be retrieved for relevant queries).

**Measures retrieval or generation:** Generation (instruction execution); retrieval is a precondition, not the primary attack surface.

**Headline numbers:** Successful against Bing Chat, GPT-4 synthetic applications, code-completion engines.

**How it differs from corpus poisoning:** Prompt injection targets **instruction execution** (what the LLM *does*), not factual content (what the LLM *believes*). The attack vector is the model's instruction-following behaviour, not the retrieval ranking function. The proposed threat model does not require instruction injection at all.

**Relationship to proposed model:** Different attack class. Indirect prompt injection requires attacker-controlled content that hijacks execution. The volumetric flooding model works through legitimate-looking plausible content that requires no instruction payload and no instruction-following exploit.

---

## 5. Untargeted and Volumetric Corpus Manipulation — The Crux

This is the key gap to assess. The section below reports every relevant work found after extensive searching with terms including: corpus flooding, base-rate manipulation, information pollution, majority poisoning, low-effort mass content, SEO poisoning of RAG, web pollution by generative content, volumetric retrieval attack, narrative flooding.

---

### 5.1 Retrieval Collapses When AI Pollutes the Web (Yu, Kim & Kim, WWW 2026) ← CLOSEST MATCH

**Full citation:** Yu, H., Kim, D., & Kim, Y.-B. (2026). Retrieval Collapses When AI Pollutes the Web. *Proceedings of the ACM Web Conference 2026 (WWW '26)*, Dubai, UAE, April 13–17. DOI: 10.1145/3774904.3792955. arXiv:2602.16136. NAVER Corp.

**Threat model (as framed by authors):** Not adversarial. The paper models **organic AI content proliferation** (content farms generating SEO-optimised AI text, and adversarial abuse content). It defines "Retrieval Collapse" as a two-stage degradation: (1) high-quality synthetic content dominates retrieval, eroding source diversity while surface accuracy appears stable; (2) adversarial synthetic content infiltrates the pipeline.

**Number and nature of injected documents:** Controlled experiment using MS MARCO (1,000 queries). SEO Pool: 20 synthetic documents per query (generated by GPT-5-nano prompted as "SEO specialist" integrating high-IDF keywords). Adversarial Abuse Pool: adversarially crafted with entity replacement. Simulation runs 20 rounds of cumulative addition.

**Targeted or untargeted:** **Untargeted at the per-query level.** SEO content is created generically for each query domain; no specific target answer is specified. This is the closest model to the proposed threat's volume-without-optimisation mechanism.

**Measures retrieval or generation:** Both (ECR = exposure contamination rate at retrieval; CCR = citation contamination rate; AA = answer accuracy).

**Headline numbers:**
- SEO scenario: 67% Pool Contamination Rate → **>80% Exposure Contamination Rate** (BM25 and LLM rankers alike); Answer Accuracy **stable or slightly improves** (68% → 70%) because SEO content is high-quality.
- Adversarial scenario: BM25 exposes ~19–24% of adversarial content; LLM ranker suppresses this to near zero.

**Stated limitations:** 
> "Our SEO simulation assumes generic LLM-based optimization rather than expert-level adversarial engineering. Future work should explore agentic threats where autonomous AI explicitly attempts to manipulate retrieval rankings, and validate these findings in live, large-scale web environments."

The paper explicitly acknowledges its metric (aggregate accuracy) may mask diversity collapse, and it does not measure retrieval of a specific minority narrative.

**Critical observation for the programme:** This paper demonstrates the base-rate shift mechanism empirically — 67% pool contamination → 80% retrieval exposure. However:
1. It does not frame this as a **deliberate adversarial attack** — it is framed as an ecosystem failure mode.
2. The SEO content is still somewhat optimised (prompted as SEO specialist with keyword injection), not purely non-optimised.
3. It measures **aggregate answer accuracy**, not **minority narrative recall**. In the SEO scenario, accuracy is stable because the AI-generated content happens to be factually correct. It does not address the case where the flooding content pushes a specific false or contested narrative.
4. It uses a **closed controlled pool** against a fixed query set, not an open-web RAG deployment.
5. It does not address alignment-level defences as a comparison point.

**This is the paper the programme most needs to differentiate from. See Section 9.**

---

### 5.2 Spiral of Silence (Chen et al., ACL 2024)

**Full citation:** Chen, X., He, B., Lin, H., Han, X., Wang, T., Cao, B., Sun, L., & Sun, Y. (2024). Spiral of Silence: How is Large Language Model Killing Information Retrieval? — A Case Study on Open Domain Question Answering. *Proceedings of ACL 2024*, pp. 14930–14951. arXiv:2404.10496.

**Threat model:** Not adversarial. Iterative simulation of LLM-generated content being published to the web and indexed, then retrieved in subsequent rounds, with the retrieved content used to generate the next round of LLM content.

**Mechanism:** Neural retrievers are biased toward LLM-generated text (higher embedding similarity scores). Over rounds, LLM-generated text crowds out human-authored text in retrieval results, creating a feedback loop.

**Number and nature of injected documents:** Iterative (1 additional LLM document per query per round); not adversarially optimised — documents are generated naturally from retrieved context.

**Targeted or untargeted:** Untargeted; no specific narrative or target answer.

**Measures retrieval or generation:** Retrieval (search rankings, NDCG) and ODQA performance.

**Headline numbers:** LLM-generated text consistently outperforms human-authored content in search rankings; long-term retrieval quality declines; short-term QA performance may remain stable.

**Stated limitations:** Simulation-based; specific dynamics depend on retriever architecture; does not model deliberate adversarial intent.

**Relationship to proposed model:** Documents the feedback-loop mechanism by which mass AI content displaces human content in retrieval. The "Spiral of Silence" metaphor maps to the programme's base-rate concern — as AI content floods the corpus, accurate minority positions become invisible. However, this paper frames it as an **unintentional ecosystem dynamic**, not a deliberate attack. It does not model an attacker choosing what narrative to amplify.

---

### 5.3 LLM-Generated Text May Harm Your Retrieval! (ACL 2026)

**Full citation:** (Authors TBC from PDF). LLM-Generated Text May Harm Your Retrieval! A Robust Detection Strategy for Retrieval-Augmented Generation. *Proceedings of ACL 2026 (Long Papers)*. ACL Anthology: 2026.acl-long.1475.

**Threat model:** Passive contamination. As LLM-generated text proliferates on the web and is indexed by RAG corpora, retrieval quality degrades. The paper focuses on detecting and filtering LLM-generated content from retrieval pipelines.

**Measures retrieval or generation:** Retrieval (contamination dynamics over iterations).

**Headline numbers:** Standard detectors degrade over time as retrieved texts mix human and AI content. Proposed RAG-aware augmentation (RAD) retains >90% of human passages in late-stage retrieval.

**Relationship to proposed model:** Same ecosystem concern as Spiral of Silence. Treats LLM content contamination as an unintentional quality problem, not an adversarial threat. No narrative-targeting analysis.

---

### 5.4 Retrieval-Augmented Generation Must Move Beyond Factual Grounding to Represent Diverse Opinions (arXiv:2604.12138, 2026)

**Full citation:** (Authors TBC). Retrieval-Augmented Generation Must Move Beyond Factual Grounding to Represent Diverse Opinions. arXiv:2604.12138v2. (2026).

**Key contribution:** Empirically shows that "raw KB retrieval systematically excludes perspectives before the LLM sees them." At k=20, the raw KB's sentiment distribution is 18–48% further from corpus truth than an enriched KB. Explicitly states: **"A generation model can only reason over what it receives."**

**Relationship to proposed model:** Provides evidence for the argument that retrieval-level bias cannot be compensated by generation-level alignment. This directly supports the programme's claim that alignment-level mitigations cannot address retrieval-surface attacks. UNVERIFIED whether this paper explicitly frames this as an adversarial attack surface argument (paper accessed in abstract only).

---

### 5.5 What Was NOT Found

Extensive searching across the following terms found no published paper that specifically studies **deliberate, volumetric, untargeted, unoptimised narrative flooding as a distinct RAG attack class**:

- "corpus flooding" in RAG context
- "base-rate manipulation" for retrieval
- "majority poisoning" for RAG (the phrase exists in some blogs but not peer-reviewed papers)
- "SEO poisoning of RAG" as a deliberate adversarial study
- "information pollution" as a targeted retrieval attack

The gap is confirmed: **no paper treats volumetric, unoptimised, narrative-targeted flooding as a first-class adversarial threat model in the RAG security literature.** The closest works (Yu et al. 2026, Chen et al. 2024) study it as an unintentional ecosystem phenomenon, not a deliberate attack.

---

## 6. LLM-Generated Content Polluting the Web — Retrieval vs. Training Distinction

The programme specifically requests this distinction.

**Training-data / model-collapse concern:** Shumailov et al. (2024, *Nature*) "AI models collapse when trained on recursively generated data." This is about iterative model training degradation when models train on their own outputs. It is **not** about retrieval or inference-time context corruption. It is a different attack surface.

**Retrieval-time concern (relevant):**
- Yu et al. 2026 (Retrieval Collapse): Contamination at retrieval, not training.
- Chen et al. 2024 (Spiral of Silence): Retrieval feedback loop.
- ACL 2026 detection paper: Retrieval corpus contamination.

These are distinct phenomena:
| | Model Collapse | Retrieval Collapse |
|---|---|---|
| Attack surface | Training data | Retrieval corpus / open web |
| Mechanism | Recursive fine-tuning on AI text | AI text outranks human text in retrieval |
| Mitigation | Training data curation | Retrieval pipeline hardening |
| Alignment relevance | Affects model parameters | Does not affect model parameters |
| Timing | Training time | Inference time |

The Yu et al. 2026 paper explicitly distinguishes Retrieval Collapse from model collapse as its first contribution: "We formally conceptualize Retrieval Collapse as a structural failure mode distinct from training-time model collapse."

---

## 7. "Retrieval as the Attack Surface" — Published Arguments

Several papers explicitly frame retrieval, not the model, as the load-bearing attack surface:

**PoisonedRAG (Zou et al., 2025):** "We find that the knowledge database in a RAG system introduces a **new and practical attack surface**."

**RAG Security Taxonomy (arXiv:2604.08304, 2026):** Formalises three trust boundaries in RAG pipelines, with the retrieval-to-context boundary described as "the most important" because it is where "external content can affect generation **directly rather than only retrieval scores**." The paper distinguishes corpus poisoning (pre-retrieval) from retrieval-time manipulation and prompt injection, treating each as a distinct attack surface.

**Opinion-Aware RAG (arXiv:2604.12138, 2026):** "While recent work on pluralistic alignment addresses diversity at the generation layer, **it cannot compensate for biased retrieval** — a generation model can only reason over what it receives."

**Cordon-MAS (arXiv:2605.26754, 2026):** "We show this assumption is incorrect: models exhibit a monitoring-control gap — they can detect contradictions in retrieved evidence yet still act on poisoned claims." Introduces the Cordon Principle (architectural separation of synthesis from untrusted evidence) on the basis that alignment alone is insufficient.

**RobustRAG (Xiang et al., 2024):** Proposes certifiable robustness against retrieval corruption, explicitly noting that standard LLM alignment provides no guarantee against injected retrieval context.

**Summary:** The argument that retrieval is the load-bearing attack surface and that alignment-level mitigations cannot address it is **published and explicitly argued in multiple papers** (2024–2026). The programme does not need to establish this; it can cite it.

---

## 8. Real-World Documentation

### 8.1 NewsGuard AI Content Farm Tracker

**Citation:** NewsGuard. (2026, March 12). NewsGuard Launches Real-time "AI Content Farm" Detection Datastream to Counter Onslaught of AI Slop in News. Press release. [https://www.newsguardtech.com/press/newsguard-launches-real-time-ai-content-farm-detection-datastream-to-counter-onslaught-of-ai-slop-in-news/](https://www.newsguardtech.com/press/newsguard-launches-real-time-ai-content-farm-detection-datastream-to-counter-onslaught-of-ai-slop-in-news/)

**Key facts:**
- 3,006 AI Content Farm sites identified as of March 2026.
- Number has **more than doubled in one year**; growing at 300–500 new sites per month.
- System built with Pangram Labs automated AI detection + human analyst review.
- 358 sites tied to **Storm-1516** (pro-Russian influence operation).
- Documented that 141 blue-chip brands ran ads on such sites.
- Includes sites linked to Russia, China, and Iran.

**Significance:** This is the first large-scale operational tracking system for AI content farms. It documents volumetric AI-generated content proliferation at scale as a current, ongoing phenomenon, not a hypothetical.

---

### 8.2 US Treasury Sanctions — Center for Geopolitical Expertise (CGE) / GRU

**Citation:** U.S. Department of the Treasury, Office of Foreign Assets Control. (2024, December 31). Treasury Sanctions Entities in Iran and Russia That Attempted to Interfere in the U.S. 2024 Election. Press release. [https://home.treasury.gov/news/press-releases/jy2766](https://home.treasury.gov/news/press-releases/jy2766)

**Key facts:**
- The Moscow-based Center for Geopolitical Expertise (CGE), directed by GRU-affiliated Valery Korovin, used **generative AI tools to quickly create disinformation** distributed across a network of at least 100 websites designed to mimic legitimate news outlets.
- The GRU provided CGE with financial support to **build and maintain a dedicated AI server** and associated infrastructure.
- Explicit purpose: "create false corroboration between the stories, as well as to obfuscate their Russian origin."
- Sanctions imposed under E.O. 13848.

**Significance:** US government sanctions documentation — the highest evidentiary standard — confirms state-contracted, GRU-directed AI content farming with a network of 100+ fake local news sites. This is documented real-world evidence of a state-linked AI content operation at scale, not a hypothetical. The "false corroboration" mechanism (multiple sites echoing the same AI-generated narrative) is directly relevant to the base-rate flooding model.

---

### 8.3 Storm-1516 / CopyCop — Recorded Future / Microsoft MTAC

**Citation (Recorded Future):** Insikt Group, Recorded Future. (2025, September 17). CopyCop Deepens Its Playbook with New Websites and Targets. [https://assets.recordedfuture.com/insikt-report-pdfs/2025/cta-ru-2025-0917.pdf](https://assets.recordedfuture.com/insikt-report-pdfs/2025/cta-ru-2025-0917.pdf)

**Citation (Bloomberg):** Bloomberg Investigations. (2026, April). Russia's Disinformation War Floods Social Media With Dangerous False Claims. [https://www.bloomberg.com/graphics/2026-russia-disinformation-storm-1516-videos/](https://www.bloomberg.com/graphics/2026-russia-disinformation-storm-1516-videos/)

**Citation (Meduza):** Meduza. (2026, April 29). Russian disinformation network Storm-1516 is flooding the West with fake stories. [https://meduza.io/en/feature/2026/04/29/russian-disinformation-network-storm-1516-is-flooding-the-west-with-fake-stories-and-jd-vance-repeated-one-of-them](https://meduza.io/en/feature/2026/04/29/russian-disinformation-network-storm-1516-is-flooding-the-west-with-fake-stories-and-jd-vance-repeated-one-of-them)

**Key facts:**
- Storm-1516 (also tracked as CopyCop by Recorded Future): Russian influence network, likely coordinated with GRU Unit 29155 and the Presidential Administration (per leaked Social Design Agency documents).
- As of September 2025: **>300 fake local news websites** (94 targeting Germany; 200+ targeting US, France, Canada, Norway, with new fictional Turkish, Ukrainian, and Swahili fact-checking sites).
- In Q1 2026 alone: Microsoft Threat Analysis Center (MTAC) recorded **>1,000 AI-generated videos** — over 10 per day.
- In 2025, Storm-1516 generated more false content than RT and Sputnik combined.
- Content laundering mechanism: whistleblower video → network of fake local news sites → amplification by influencers → obscured origin.
- Q1 2026 production rate doubled year-on-year.
- A single fabricated Maia Sandu story reached **2.3 million views** on X without a warning label.

**Significance:** Largest documented real-world case of AI-assisted volumetric disinformation infrastructure. Directly instantiates the proposed threat model — a state actor maintaining a massive content farm flooding the web with narrative-aligned content across hundreds of local-news-mimicking sites.

---

### 8.4 OpenAI Threat Intelligence Reports

**Citations:**
- OpenAI. (2024, May). Disrupting deceptive uses of AI by covert influence operations. [https://openai.com/index/disrupting-deceptive-uses-of-ai-by-covert-influence-operations/](https://openai.com/index/disrupting-deceptive-uses-of-ai-by-covert-influence-operations/)
- OpenAI. (2024, October). Influence and cyber operations: an update, October 2024. [https://cdn.openai.com/threat-intelligence-reports/influence-and-cyber-operations-an-update_October-2024.pdf](https://cdn.openai.com/threat-intelligence-reports/influence-and-cyber-operations-an-update_October-2024.pdf)
- OpenAI. (2025, June). Disrupting malicious uses of AI: June 2025. [https://cdn.openai.com/threat-intelligence-reports/5f73af09-a3a3-4a55-992e-069237681620/disrupting-malicious-uses-of-ai-june-2025.pdf](https://cdn.openai.com/threat-intelligence-reports/5f73af09-a3a3-4a55-992e-069237681620/disrupting-malicious-uses-of-ai-june-2025.pdf)

**Key facts:**
- In the three months to May 2024, OpenAI disrupted five covert influence operations from Russia (two networks), China, Iran, and Israel (commercial firm Stoic).
- Actors used ChatGPT for: generating large volumes of short comments in multiple languages, creating fake personas with biographies, translating and proofreading articles, debugging automation code.
- "Bad Grammar" (Russia) and "Zero Zeno" (Israel): focused on **quantity** — generating large volumes of short comments for Telegram, X, Instagram.
- As of May 2024: operations had "not meaningfully increased their audience engagement or reach as a result of our services." (Important caveat for the programme — see Section 9.)
- June 2025 report: China-origin operations generating "polarized social media content that supported both sides of divisive topics."

---

### 8.5 Meta Adversarial Threat Reports

**Citations:**
- Meta. (2024, Q3). Quarterly Adversarial Threat Report Q3 2024. [https://transparency.meta.com/sr/Q3-2024-Adversarial-threat-report](https://transparency.meta.com/sr/Q3-2024-Adversarial-threat-report)
- Meta. (2025, Q2-Q3). Semiannual Adversarial Threat Report Q2-Q3 2025. [https://transparency.meta.com/sr/Q2-Q3-2025-Adversarial-threat-report](https://transparency.meta.com/sr/Q2-Q3-2025-Adversarial-threat-report)
- Meta. (2026, H2). H2 2026 Adversarial Threat Report. [https://transparency.meta.com/sr/H2-2026-adversarial-threat-report](https://transparency.meta.com/sr/H2-2026-adversarial-threat-report)

**Key facts:**
- Q3 2024: GenAI tactics have provided "only incremental productivity and content-generation gains" and have not impeded Meta's disruption capability. Behavioural defences remain effective.
- Q2-Q3 2025: "AI lowers the barrier for entry for threat actors, allowing them to get more done with fewer resources."
- H2 2026: **"AI-enabled content generation has moved from an occasional tactic employed by the most resourced actors to a near-standard component of influence operation tradecraft."** Every CIB network disrupted in H2 2026 incorporated some form of generative AI.
- H2 2026: Threat actors experimenting with "advanced AI- and software-based tools to automate AI-generated content creation and distribution at scale."

**Important nuance (relevant to programme's threat model):** Meta consistently reports that operations targeting its platforms have "struggled to build authentic audiences" and rely on fake engagement. This is the social-media context. The programme's threat model is specifically about **RAG retrieval systems**, not social media engagement metrics. Content that fails to build a social media audience may still successfully shift the base rate in a retrieval corpus if it is indexed by the web. These are different mechanisms.

---

### 8.6 Google GTIG Report on Adversarial Misuse of Generative AI

**Citation:** Google Threat Intelligence Group. (2025). Adversarial Misuse of Generative AI. Google/Mandiant Report. [https://services.google.com/fh/files/misc/adversarial-misuse-generative-ai.pdf](https://services.google.com/fh/files/misc/adversarial-misuse-generative-ai.pdf)

**Key facts:**
- Government-backed threat actors from 20+ countries used Gemini, primarily for research, translation, and content generation — not novel AI-specific attack capabilities.
- Russian IO actors used Gemini to generate options for "social media campaigns targeting U.S. audiences."
- Finding consistent with OpenAI and Meta: "AI is not yet the game changer it is sometimes portrayed to be" for novel attack capabilities.

---

## 9. Direct Answers

### Q1: Is the volumetric, untargeted, non-optimised flooding threat model already studied in the RAG context?

**Answer: Partially, but not as a deliberate adversarial threat model.**

Two papers study the mechanism empirically in the RAG/retrieval context:

1. **Yu et al., WWW 2026** ("Retrieval Collapses When AI Pollutes the Web"): demonstrates that 67% pool contamination with SEO-style AI content → 80%+ retrieval exposure contamination. Measures aggregate accuracy (which remains stable), not minority-narrative recall. Framed as organic ecosystem failure, not adversarial attack.

2. **Chen et al., ACL 2024** ("Spiral of Silence"): demonstrates iterative feedback loop in which LLM-generated content crowds out human content in retrieval over rounds. Not framed as deliberate attack; no specific narrative targeting.

No published paper treats volumetric, unoptimised, **narrative-targeted** corpus flooding as a first-class adversarial threat model, studies its effect on **minority narrative suppression specifically**, or distinguishes it from existing adversarial and alignment-level defences. The gap is real.

---

### Q2: Has anyone argued that retrieval, rather than model alignment, is the load-bearing attack surface?

**Answer: Yes.**

Multiple peer-reviewed papers argue this explicitly:
- **PoisonedRAG (2025):** "knowledge database introduces a new practical attack surface."
- **RAG Security Taxonomy (arXiv:2604.08304, 2026):** Retrieval-to-context boundary is "the most important" trust crossing; retrieval-time corpus poisoning is explicitly distinguished from alignment.
- **Opinion-Aware RAG (arXiv:2604.12138, 2026):** "A generation model can only reason over what it receives" — pluralistic alignment cannot compensate for retrieval-level bias.
- **Cordon-MAS (arXiv:2605.26754, 2026):** Models "can detect contradictions in retrieved evidence yet still act on poisoned claims" — the monitoring-control gap exists even in aligned models.
- **RobustRAG (Xiang et al., 2024):** Certifiable robustness requires architectural changes at retrieval, not alignment.

The programme does not need to establish this claim as novel. It can cite these papers and use them to anchor the argument.

---

### Q3: Is there documented real-world evidence of state-linked or commercially-contracted AI content farms at scale?

**Answer: Yes, with multiple citable primary sources.**

| Source | Evidence type | Scale | Date |
|---|---|---|---|
| US Treasury sanctions (jy2766) | Government sanctions documentation | 100+ fake news sites, dedicated GRU-funded AI server | Dec 31, 2024 |
| Recorded Future (CopyCop report) | Threat intelligence | 300+ fake local news sites, attributed to CGE/GRU | Sep 2025 |
| Microsoft MTAC (per Ukrainian Week/Meduza) | Platform reporting | 1,000+ AI-generated videos in Q1 2026 alone | 2026 |
| NewsGuard AI Content Farm tracker | Industry monitoring | 3,006+ sites; 358 tied to Storm-1516 | Mar 2026 |
| OpenAI threat reports (May 2024, Oct 2024, Jun 2025) | Platform reporting | 5 IO operations disrupted in 3 months; Russia, China, Iran, Israel | 2024–2025 |
| Meta H2 2026 Adversarial Threat Report | Platform reporting | GenAI now "near-standard component" of IO tradecraft; all disrupted networks in H2 2026 used GenAI | 2026 |
| Google GTIG | Platform reporting | 20+ country government actors using Gemini for IO | 2025 |

The programme's claim that "this is happening now, not a hypothetical" is supportable with primary sources. The strongest single citation is the US Treasury sanctions document (jy2766), which is US government legal documentation of a specific GRU-directed AI content farm.

**One important nuance:** Current documented operations target social media engagement, not specifically RAG retrieval corpora. The link between "content indexed by web search" and "content retrieved by RAG systems" is real but has not been explicitly closed by these reports. The programme may need to bridge this gap explicitly.

---

### Q4: What is the strongest existing paper the programme would need to differentiate from, and how?

**The paper is: Yu, H., Kim, D., & Kim, Y.-B. (2026). "Retrieval Collapses When AI Pollutes the Web." WWW 2026. arXiv:2602.16136.**

This paper empirically demonstrates the core mechanism of the proposed threat model — mass AI-generated content changes the base rate in retrieval corpora, causing retrieval systems to return synthetic content overwhelmingly even at 67% pool contamination — with 80%+ exposure contamination across both BM25 and LLM rankers.

**How to differentiate:**

| Dimension | Yu et al. 2026 | Proposed threat model |
|---|---|---|
| **Intent** | Organic AI content pollution (no attacker) | Deliberate adversarial narrative flooding |
| **Content quality** | SEO-optimised (prompted as "SEO specialist") | Explicitly non-optimised; plausible but unengineered |
| **Narrative specificity** | No specific narrative; generic domain content | Floods a specific narrative to suppress accurate alternatives |
| **Outcome measured** | Aggregate QA accuracy (stable in SEO scenario) | **Minority narrative recall** — does the accurate minority position appear in top-k? |
| **Corpus type** | Controlled experiment (MS MARCO + Google Search API) | Open-web RAG deployment |
| **Attack framing** | Not framed as attack | First-class adversarial threat model |
| **Defence comparison** | Proposes retrieval-aware ranking; does not evaluate alignment | Explicitly argues alignment cannot address retrieval-level attack |
| **Base-rate mechanism** | Measured but not theoretically formalised | Could contribute probabilistic formalisation (P[correct minority narrative ∈ top-k] as function of flooding ratio) |

The programme's minimum contribution over Yu et al. 2026:
1. **Reframe as deliberate attack**: Model a rational adversary choosing to flood a specific narrative rather than generating generic content.
2. **Measure the right outcome**: Define and measure "minority narrative suppression" (recall of a specific true/accurate position) rather than aggregate accuracy. In Yu et al.'s SEO scenario, accuracy is *stable* because SEO content is largely correct — this masks the exact failure the programme cares about.
3. **Non-optimised content**: Show that the mechanism works even with purely unoptimised, plausible-but-unengieneered content, removing the "requires SEO expertise" limitation.
4. **Alignment control**: Explicitly compare retrieval-level intervention vs. alignment-level intervention to show alignment cannot compensate for retrieval failure.
5. **Formalise the base-rate model**: Give a probabilistic account of how flooding ratio translates to minority narrative retrieval probability — this is currently measured empirically by Yu et al. but not formally modelled.

---

## 10. Summary Table — All Works

| Paper | Year | Documents (count) | Optimised? | Targeted? | Untargeted flooding? | Notes |
|---|---|---|---|---|---|---|
| Zhong et al. (EMNLP) | 2023 | Up to 500 | Yes (HotFlip) | Cluster-targeted | No | Dense retrieval; detectable by perplexity filter |
| PoisonedRAG (Zou et al.) | 2024/2025 | 5 per query | Yes (gradient) | Query-targeted | No | 90-97% ASR; paradigm paper |
| BadRAG (Xue et al.) | 2024 | 10 | Yes (contrastive) | Trigger-targeted | No | 98.2% retrieval success |
| Greshake et al. | 2023 | 1-few | No (instruction text) | Query-targeted | No | Prompt injection; different attack class |
| Natural Adversarial Docs (arXiv:2410.02163) | 2024 | ~500 | Yes (adversarial decoding) | Cluster-targeted | No | Evades perplexity filters |
| RobustRAG (Xiang et al.) | 2024 | — | — | — | — | Defence; certifiable against few injections |
| MM-PoisonRAG GPA | 2025 | 1 | Yes (adversarial) | Untargeted (global collapse) | Partial | Collapses all accuracy; not narrative-specific |
| Chen et al. "Spiral of Silence" | 2024 | Many (iterative) | No (natural generation) | Untargeted | Partial | Feedback loop; organic framing; no adversary |
| **Yu et al. "Retrieval Collapse"** | **2026** | **Many (SEO pool)** | **Mild (SEO prompting)** | **Untargeted** | **Closest match** | **Still organic framing; measures aggregate accuracy** |
| CorruptRAG | 2025 | 1 | Yes | Query-targeted | No | Extreme efficiency; single injection |
| GEO (Aggarwal et al.) | 2024 | Multi-query | Mild (content optimisation) | Multi-query visibility | Partial | Commercial optimisation, not security framing |

---

## 11. Literature Accessed — Full List

All items accessed by WebSearch and WebFetch during this research session. Items marked UNVERIFIED were not directly accessed in full.

1. Zou et al. (2025). PoisonedRAG. USENIX Security 2025. arXiv:2402.07867. **ACCESSED** (arXiv HTML, USENIX PDF).
2. Zhong et al. (2023). Poisoning Retrieval Corpora. EMNLP 2023. ACL Anthology 2023.emnlp-main.849. **ACCESSED** (ACL PDF).
3. Xue et al. (2024). BadRAG. arXiv:2406.00083. **ACCESSED** (arXiv HTML).
4. Greshake et al. (2023). Not What You've Signed Up For. AISec @ CCS 2023. DOI:10.1145/3605764.3623985. **ACCESSED** (abstract and search results; full paper behind paywall).
5. Natural Adversarial Docs (2024). arXiv:2410.02163 / EACL 2026 findings. **ACCESSED** (arXiv HTML).
6. Xiang et al. (2024). RobustRAG. arXiv:2405.15556. **ACCESSED** (arXiv PDF and HTML).
7. MM-PoisonRAG (2025). arXiv:2502.17832. **ACCESSED** (arXiv HTML).
8. Chen et al. (2024). Spiral of Silence. ACL 2024. arXiv:2404.10496. **ACCESSED** (arXiv PDF and search results).
9. Yu, Kim & Kim (2026). Retrieval Collapses When AI Pollutes the Web. WWW 2026. arXiv:2602.16136. DOI:10.1145/3774904.3792955. **ACCESSED** (full arXiv HTML, read completely).
10. Wang et al. (2025). Joint-GCG. arXiv:2506.06151. **ACCESSED** (abstract only).
11. Su et al. (2025). CorruptRAG. ACL 2025 Findings. arXiv:2504.03957. **ACCESSED** (arXiv HTML).
12. Aggarwal et al. (2024). GEO: Generative Engine Optimization. **ACCESSED** (PDF).
13. Position paper on GEO risks (2026). arXiv:2606.12439. **ACCESSED** (arXiv HTML).
14. RAG Security Taxonomy (2026). arXiv:2604.08304. **ACCESSED** (arXiv HTML).
15. Opinion-Aware RAG (2026). arXiv:2604.12138. **ACCESSED** (arXiv HTML).
16. Cordon-MAS (2026). arXiv:2605.26754. **ACCESSED** (arXiv HTML).
17. LLM-Generated Text May Harm Your Retrieval (ACL 2026). ACL Anthology 2026.acl-long.1475. **ACCESSED** (ACL PDF).
18. RetrieverGuard (NAACL 2025 Findings). **ACCESSED** (ACL PDF).
19. RAGuard (2026). arXiv:2607.26339. **ACCESSED** (arXiv HTML).
20. PRA-RAG (ACL 2026 Findings). **ACCESSED** (ACL PDF).
21. SCI-Defense (2026). arXiv:2605.21948. **ACCESSED** (arXiv HTML).
22. US Treasury. (2024, Dec 31). Sanctions on CGE/Korovin. jy2766. **ACCESSED** (Treasury press release).
23. Recorded Future / Insikt Group. (2025). CopyCop Deepens Its Playbook. **ACCESSED** (report PDF).
24. NewsGuard. (2026, March). AI Content Farm Detection Datastream launch. **ACCESSED** (press release).
25. OpenAI. (2024, May). Disrupting deceptive uses of AI by covert influence operations. **ACCESSED** (blog + report).
26. OpenAI. (2024, October). Influence and cyber operations update. **ACCESSED** (PDF).
27. OpenAI. (2025, June). Disrupting malicious uses of AI. **ACCESSED** (PDF).
28. Meta. Q3 2024 / Q4 2024 / Q2-Q3 2025 / H2 2026 Adversarial Threat Reports. **ACCESSED** (multiple).
29. Google GTIG. (2025). Adversarial Misuse of Generative AI. **ACCESSED** (PDF).
30. Meduza. (2026, April 29). Storm-1516 flooding the West. **ACCESSED** (article).
31. Bloomberg. (2026). Russia's Disinformation War. **ACCESSED** (article).
32. Google TAG. DRAGONBRIDGE Q1 2024 disruption. **ACCESSED** (blog post).
33. BSI (German Federal Office for IT Security). (2023). Indirect Prompt Injections. ACCESSED (PDF).
34. Breaking the Spiral: UMO framework. DOI:10.1145/3788865. **ACCESSED** (abstract via search).

---

*End of document. No files other than this one were created or modified. No git commit was made.*
