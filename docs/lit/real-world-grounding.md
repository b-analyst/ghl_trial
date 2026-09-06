# Real-World Grounding for the Motivation Section
## AI-Generated Content, Volume, and Retrieval Contamination

*Compiled: 5 September 2026. Searched by agent; primary sources verified via WebSearch and WebFetch. All unverified or contested claims are flagged explicitly.*

---

## Purpose

This document provides citable evidence that well-resourced actors — states in particular, but also commercial content operations — are already using generative AI to produce information at volume in ways that change the base rate of what exists on the open web, and that this creates structural problems for search and retrieval rather than merely adding random noise. The paper's empirical contribution is a controlled experiment; the motivation must rest on documented fact, not inference from plausibility.

Evidence is rated:
- **STRONG**: measured quantity, methodology published, reputable organisation
- **MODERATE**: documented by a reputable organisation but methodology thin, unstated, or contested
- **WEAK**: widely repeated, primary source not located, or figure that circulates without verification
- **UNVERIFIED**: searched but not confirmed

---

## Section 1 — NewsGuard AI Content Farm Tracking

### Source
NewsGuard Technologies (founded 2018); partnership with Pangram Labs (AI detection provider).

### Key press release
"NewsGuard Launches Real-time 'AI Content Farm' Detection Datastream to Counter Onslaught of AI Slop in News." NewsGuard, March 2026. URL: https://www.newsguardtech.com/press/newsguard-launches-real-time-ai-content-farm-detection-datastream-to-counter-onslaught-of-ai-slop-in-news/

Earlier tracker reports: November 2024, July 2024, February 2024.

### What was measured
NewsGuard classifies sites as "Unreliable AI-Generated News Sites" (UAINs) or "AI Content Farms" based on three criteria applied jointly:
1. A substantial portion of content is produced by AI (detected via Pangram Labs' transformer-based classifier, which uses sliding-window analysis at the document level and outputs a three-way classification: fully AI-generated / AI-assisted / human-written);
2. The practice is not disclosed to readers;
3. The content is presented in a way designed to mimic human-written journalism.

NewsGuard analysts then review machine-flagged sites to confirm and remove false positives. The methodology is described in the press release and in the UAIN tracker documentation.

### Numbers with dates
| Date | Count |
|------|-------|
| May 2023 | ~50 sites |
| December 2023 | ~600 sites |
| February 2024 | 725 sites |
| July 2024 | 966 sites |
| November 2024 | 1,121 sites (combined UAINs and disinformation operations) |
| March 2026 | 3,006 sites |

Growth rate as of March 2026: 300–500 new sites per month (stated in the press release).

### Assessment: **STRONG**
The methodology is published, the organisation is long-established, and human analyst review distinguishes this from purely automated counts. The Pangram detection model is itself documented (see Section 4). Limitation: the threshold for "substantial" AI content is not numerically specified in publicly available documentation; the verification step introduces human discretion.

### Caution
NewsGuard has a commercial interest in the severity of this problem (it sells the UAIN dataset to advertisers and platforms). This does not invalidate the findings but should be acknowledged. The counts should be characterised as a lower bound on a defined category, not as a census of all AI-generated news.

---

## Section 2 — Platform Adversarial Threat Reports

### 2a. OpenAI Threat Intelligence Reports (series, February 2024 – October 2025)

**Sources (all public):**
- "AI and Covert Influence Operations: Latest Trends." OpenAI, May 2024. https://downloads.ctfassets.net/kftzwdyauwt9/5IMxzTmUclSOAcWUXbkVrK/3cfab518e6b10789ab8843bcca18b633/Threat_Intel_Report.pdf
- "Influence and Cyber Operations: An Update." OpenAI, October 2024. https://cdn.openai.com/threat-intelligence-reports/influence-and-cyber-operations-an-update_October-2024.pdf
- "Disrupting Malicious Uses of Our Models: An Update." OpenAI, February 2025. https://cdn.openai.com/threat-intelligence-reports/disrupting-malicious-uses-of-our-models-february-2025-update.pdf
- "Disrupting Malicious Uses of AI." OpenAI, October 2025. https://cdn.openai.com/threat-intelligence-reports/7d662b68-952f-4dfd-a2f2-fe55b041cc4a/disrupting-malicious-uses-of-ai-october-2025.pdf

**What was documented**
Since February 2024, OpenAI has disrupted and publicly reported on more than 40 networks that violated usage policies. Operations named across the series include: Bad Grammar, Doppelganger, Spamouflage, IUVM, Zero Zeno (May 2024); STORM-2035 (August 2024); Peer Review, Sponsored Discontent (February 2025). Attributed actors include Russia (multiple networks), China, Iran, and Israel-based commercial operators.

AI's role varied: content generation for social media posts, translation of existing propaganda, debugging of code, creating personas. In all documented cases, threat actors were "building AI into existing workflows, rather than building new workflows around AI" (October 2025 report).

**What was NOT found**
None of the five case studies in the May 2024 report scored above 2 on a 6-point Breakout Scale (scale assesses whether an operation achieved authentic audience engagement). OpenAI explicitly states: "So far, these campaigns do not appear to have meaningfully increased their audience engagement or reach as a result of their use of our services."

**Assessment: STRONG for the claim that AI is being used in influence operations at scale; MODERATE for any claim about effect on public information**

The reports describe detected and disrupted operations — there is a survivor bias problem (undetected operations are not counted). The finding that AI provides productivity gains but not audience-building breakthroughs is consistent across all reports, including in platform adversaries.

---

### 2b. Meta Quarterly Adversarial Threat Reports (Q1–Q4 2024)

**Sources:**
- Q1 2024: https://transparency.meta.com/sr/Q1-2024-Adversarial-threat-report/
- Q3 2024: https://transparency.meta.com/sr/Q3-2024-Adversarial-threat-report
- Q4 2024: https://transparency.meta.com/sr/Q4-2024-Adversarial-threat-report/

**What was documented**
Meta documents uses of AI by Coordinated Inauthentic Behaviour (CIB) networks: AI-generated profile photos (GAN-based); AI-generated video newsreaders; AI-generated comment text. Meta's Q3 2024 report states: "GenAI-powered tactics have provided only incremental productivity and content-generation gains to the threat actors, and have not impeded our ability to disrupt their covert influence operations."

Doppelganger (Russia-linked) is documented as a persistent operation with high expenditure, high detection rate, and consistent failure to build authentic audiences. By Q4 2024 it had shifted geographic focus and largely abandoned linking to its spoof news sites on Meta's own platforms after detection.

Reuters reported (December 2024) that Meta's president of global affairs Nick Clegg characterised AI-generated disinformation's impact on 2024 elections as "low volume" and quickly labelled or removed.

**Assessment: STRONG for the factual claim that AI is used in operations; STRONG (in the opposite direction) for any claim that these operations reliably breach platform defences or reach audiences**

---

### 2c. Google Threat Intelligence Group (GTIG)

**Sources:**
- "Adversarial Misuse of Generative AI." Google GTIG, January 2025. (Referenced in Cloud CISO blog.)
- "Advances in Threat Actor Usage of AI Tools." Google GTIG, November 2025. https://services.google.com/fh/files/misc/advances-in-threat-actor-usage-of-ai-tools-en.pdf
- Blog post: https://blog.google/innovation-and-ai/technology/safety-security/google-threat-intelligence-group-report-ai-november-2025/

**What was documented**
State-sponsored actors from China (PRC), Russia, North Korea, and Iran used Gemini for productivity-oriented tasks: reconnaissance, phishing lure creation, code troubleshooting, translation, data exfiltration support. The January 2025 analysis found actors "largely unsuccessful in bypassing safety guardrails or achieving novel offensive capabilities." The November 2025 report documents a shift toward AI-native malware (tools like PROMPTFLUX and PROMPTSTEAL, which generate code at runtime), but this concerns cyber operations, not content influence operations.

**Assessment: STRONG for state actor AI use; MODERATE for influence operations specifically** — GTIG's primary focus is cyber operations (intrusions, espionage). Content pollution and information environment contamination are not the primary subject of these reports.

---

## Section 3 — Pravda Network / Portal Kombat and LLM Retrieval

### Sources (multiple independent organisations)

1. VIGINUM (French government information integrity agency). "PORTAL KOMBAT: A Structured and Coordinated Pro-Russian Propaganda Network." February 2024. (Publicly available PDF.) First official identification of the network; 193 websites identified.

2. American Sunlight Project (ASP). "Bad Actors are Grooming LLMs to Produce Falsehoods." February 2025. https://americansunlight.substack.com/p/bad-actors-are-grooming-llms-to-produce — Introduced the term "LLM grooming"; estimated publishing rate at ≥3.6 million articles/year; noted network design apparently targets automated crawlers.

3. DFRLab (Atlantic Council) + Check First. Series of investigations including:
   - "Russia's Pravda Network Expands Worldwide." February 2025. https://dfrlab.org/2025/02/24/russia-pravda-network-expands-worldwide/
   - "Russia-linked Pravda Network Cited on Wikipedia, LLMs, and X." (Undated; referenced in DFRLab Pravda dashboard.)
   - Dashboard: https://dfrlab.org/the-pravda-network/

4. NewsGuard. "A Well-Funded Moscow-Based Global 'News' Network Has Infected Western Artificial Intelligence Tools Worldwide with Russian Propaganda." March 2025. https://www.newsguardrealitycheck.com/p/a-well-funded-moscow-based-global

### What the network is

Pravda (also called Portal Kombat from VIGINUM's naming) is a centralised operation running 150–193 websites (depending on measurement date) across 49+ countries, attributed via website forensics to TigerWeb, a digital agency based in Russian-occupied Crimea (DFRLab/Check First, 2025). The sites aggregate content from Russian state media, pro-Kremlin Telegram channels, and government officials, re-publish it at automated scale across country-specific domains (e.g. English, French, German, Polish, Tagalog), and employ SEO techniques to rank in search engines. ASP and DFRLab both estimate publishing volume at approximately 3.6–3.7 million articles in 2024.

### What was measured regarding LLM contamination

**DFRLab/Check First methodology (Wikipedia and LLM citation analysis):** The investigation used Wikipedia API access to track hyperlinks to Pravda-network domains across 1,907 hyperlinks in 1,672 Wikipedia pages in 44 languages. This is a direct, verifiable measurement of how Pravda content entered a primary training and retrieval source. Posting activity with hyperlinks to Pravda domains on X grew exponentially after February 24, 2022. The LLM analysis involved querying popular AI chatbots and logging when they cited Pravda domains or reproduced Pravda-sourced claims. Specific methodology details (which models, which queries, how many) are less fully described than the Wikipedia analysis; the GitHub repository of raw data is cited as publicly available.

**NewsGuard chatbot audit (March 2025):** 10 chatbots tested (ChatGPT-4o, Grok, Gemini, Copilot, Claude, Meta AI, Perplexity, le Chat, Pi, You.com Smart Assistant). 15 false narratives drawn from NewsGuard's Misinformation Fingerprints catalog; each narrative tested with 3 prompt styles (Innocent, Leading, Malign), yielding 450 total responses. Result: 33.55% of responses repeated the false narrative; 18.22% non-response; 48.22% debunked. **Caveat:** NewsGuard did not publicly release its specific prompts and declined to share them with journalists who asked. Al Jazeera researchers (July 2025) independently replicated with different prompts using the few examples NewsGuard published and found a 5% false-claim rate; Pravda sites appeared in only 8% of chatbot outputs, mostly to debunk. The researchers found false-claim incidence concentrated in "data void" scenarios — topics with thin mainstream coverage — supporting a retrieval-driven rather than training-driven mechanism.

**American Sunlight Project supplementary testing (2025):** ASP tested OpenAI's GPT-4o and o3 models specifically with queries targeting known Pravda narratives. GPT-4o cited Pravda content in 5 out of 7 targeted prompts (71.4%); o3 cited in 28.6% of targeted prompts. These tests are relevant but narrowly targeted — they represent worst-case retrieval scenarios rather than average user interactions.

### Assessment: **STRONG** for the existence and scale of the Pravda network. **MODERATE** for the retrieval contamination claim.

The network infrastructure is robustly documented by multiple independent organisations using verifiable methods. The SEO-optimised content at this volume plausibly changes the retrieval landscape for certain queries. However:

- The claim that this "pollutes" AI chatbots is supported by some testing but contested by independent replication
- The specific mechanism (training data ingestion vs. live retrieval/RAG) has not been distinguished empirically; the ASP and NewsGuard reports conflate them
- The 33% figure should not be cited without its methodological caveats and the Al Jazeera 5% counterpoint

---

## Section 4 — Proportion of New Web Content That Is Machine-Generated

### Source
Kneidinger, B. et al. "The Impact of AI-Generated Text on the Internet." arXiv:2604.26965, April 2026. https://arxiv.org/abs/2604.26965

### Methodology (most rigorous available)
- Corpus: Publicly accessible web pages sampled from the Internet Archive Wayback Machine spanning mid-2022 to mid-2025.
- Sampling: Multi-dimensional stratified sampling of the Internet Archive CDX index across time of first capture, MIME type, URL depth, and top-level domain — designed to approximate a uniform random draw from the accessible web and correct for the archive's increasing crawl capacity over time.
- Detector: Pangram v3 (transformer-based neural network, sliding-window document-level inference, three-way output: fully AI-generated / AI-assisted / human-written). The paper evaluates Pangram v3 against three other detectors and reports superior stability across multilingual and HTML vs. plain-text conditions.
- Output metric: Proportion of monthly website samples classified as fully AI-generated, and combined AI-generated + AI-assisted.

### Finding
By the first half of 2025, approximately 35% of websites uploaded to the internet in a given month were AI-generated or AI-assisted (combined metric). The paper plots this as a continuous time series from November 2022 (ChatGPT launch) forward.

Pangram Labs separately reported (cited in the Pangram Wikipedia article): 9% of news articles published in summer 2025 were fully AI-generated; 41% of LinkedIn content >250 words in early 2026 was AI-generated; Substack was the lowest major platform at 10% of long-form content.

### Assessment: **STRONG** for the arXiv paper's core finding.

The sampling methodology is explicitly designed to correct for known biases in web archive research. The three-way detection scheme is more informative than binary classifiers. Limitation: the paper covers all website types; the 35% figure includes commercial, spam, and personal sites, not only news and information. The methodological detail is sufficient to cite with confidence, provided the paper's definition of "AI-generated or AI-assisted" is not collapsed into simply "AI-generated."

### Other figures in circulation — credibility ratings

| Figure | Source | Rating |
|--------|--------|--------|
| 35% of new websites AI-generated or AI-assisted by mid-2025 | arXiv:2604.26965 (April 2026), Internet Archive sampling + Pangram v3 | STRONG |
| 9% of news articles AI-generated, summer 2025 | Pangram Labs (via Wikipedia article on Pangram) | MODERATE — secondary citation; primary report not located during search |
| 74.2% of new web pages contain AI content (April 2025) | Ahrefs, 900k pages, own detector "bot_or_not" | WEAK FOR STRONG CLAIMS — "any AI content" includes light editing; only 2.5% were "pure AI" in Ahrefs' own breakdown; proprietary detector, methodology not fully published |
| 57% of all online text AI-generated or translated | Circulates on HN; attributed to unnamed "analysis" | UNVERIFIED — no primary source located despite search; do not cite |
| 90% of online content AI-generated by 2026 | Attributed to Europol | WEAK — widely repeated; no primary Europol document with methodology was located; do not cite |

---

## Section 5 — State Contracts with AI Content or Influence Operations

### 5a. RT / Meliorator bot farm (Russia) — STRONG

**Source:** U.S. Department of Justice press release and court affidavit, July 9, 2024. Joint cybersecurity advisory from US, Canada, and Netherlands, July 9, 2024. Reporting: AP News, The Verge, BleepingComputer.

**What is documented**
- A deputy editor-in-chief at RT (Russia Today, a Russian state-funded media organisation registered as a foreign agent with the DOJ) commissioned development of software named Meliorator.
- Meliorator is an "AI-enabled bot farm generation and management software" that created authentic-appearing social media personas at scale, including text generation, persona backstories, and obfuscation techniques to bypass X's verification systems.
- In early 2023 an FSB officer created a private intelligence organisation, with membership including the RT deputy editor and other RT staff, whose stated purpose was to advance FSB/Russian government goals via the bot farm.
- The DOJ seized two domains (mlrtr.com and otanmail.com) and 968 social media accounts on X.
- FBI Director Christopher Wray described this as "a first in disrupting a Russian-sponsored Generative AI-enhanced social media bot farm."

**Attribution strength:** Very high. Court documents, DOJ affidavit, multi-government advisory.

**Assessment: STRONG**

The state contract and Kremlin approval are documented in DOJ court filings. The AI component (Meliorator) is technically described in the joint advisory. This is the cleanest documented case of a state-directed, AI-powered content operation.

---

### 5b. Israeli government / Clock Tower X / Brad Parscale content farms — MODERATE

**Source:** Drop Site News investigation (primary). Foreign Agents Registration Act (FARA) filings (public record). Quincy Institute report. Corroborating reporting by Responsible Statecraft and The Intercept.

**URL:** https://www.dropsitenews.com/p/israel-brad-parscale-ai-chatbots-gaza

**What is documented in public record**
- Clock Tower X LLC (Brad Parscale, sole owner) is registered under FARA (registration #7649, 18 September 2025) as a foreign agent for the State of Israel (via Havas Media Germany as intermediary).
- FARA filings confirm the contract value grew from $1.5M/month to approximately $4.5M/month; total reported at ~$46.5M by the Quincy Institute's analysis of the filings.
- The FARA filing's Statement of Work explicitly states the contractor will "deploy websites and content to deliver GPT framing results on GPT conversations."
- Clock Tower X built approximately 10 websites (including Allyvia.org, FactSignal.org, Paxpoint.org) that publish moderately toned, professionally sourced articles averaging only a few hundred unique human visitors per month.
- All sites carry a mandatory FARA footer: "This material is distributed by Clock Tower X LLC on behalf of the State of Israel."
- Drop Site News tested major chatbots: Perplexity and Copilot cited the sites without noting the FARA disclosure; Claude, ChatGPT, and Gemini flagged the Israeli government connection.
- A Rift TV investigation found the pages are archived at an 85% rate in Common Crawl.

**What is NOT documented**
- The causal effect on AI output at population scale (how many users encounter this content in chatbot responses) has not been measured. The effect is "unproven" according to an independent analysis of the operation's record.
- The SOW language describes intent; intent is not the same as demonstrated effect.

**Assessment: MODERATE**
The contract, its stated intent to influence AI systems, and FARA compliance are all documented in public government filings. The claim is notably different from most: this is an openly registered foreign agent operation explicitly targeting AI retrieval, not a covert operation. It is citable as evidence that state-directed AI content operations that explicitly target LLM retrieval exist. The effect claim must be stated as limited and contested.

---

## Section 6 — AI Assistant or Search Product Repeating Disinformation Network Content

### Documented cases

**Case 1: DFRLab/Check First — Pravda domains cited by chatbots**
Multiple popular AI chatbots were observed citing Pravda-network domains as sources. The investigation found Wikipedia editors citing Pravda domains (1,907 hyperlinks across 1,672 pages), and some chatbot outputs repeating claims sourced to Pravda. Specific chatbots and responses are documented in the investigation. This is the strongest independently verified case.

**Case 2: NewsGuard chatbot audit (March 2025)**
As described in Section 3. 33.55% false narrative repetition rate. Contested by independent replication.

**Case 3: Drop Site News / Clock Tower X (2025)**
Perplexity and Copilot cited FARA-registered Israeli government websites without flagging government authorship. Claude, ChatGPT, and Gemini did flag it. This is a live-retrieval case, not a training-contamination case.

**Assessment for the claim "AI assistants have repeated content from known disinformation networks": MODERATE**

The DFRLab/Check First investigation is the most methodologically sound (Wikipedia API analysis is independently verifiable). The NewsGuard 33% figure is contested and should not be cited without caveats. The Drop Site case documents retrieval without appropriate provenance disclosure, but the sites carry FARA disclosures that are available to models that retrieve them; the failure is in surfacing provenance, not necessarily in training contamination.

---

## Section 7 — Summary Assessment and Paper-Ready Citations

### Three to Four Strongest Citable Items

**1. NewsGuard UAIN tracker: volume of AI content farms**

> As of March 2026, NewsGuard identified 3,006 AI content farm websites — sites that publish AI-generated news with no editorial oversight or transparency — up from approximately 50 in May 2023 (NewsGuard, March 2026). The count grew from 725 in February 2024 to 966 by July 2024, with the current growth rate estimated at 300–500 new sites per month. Detection combines automated AI classification (Pangram Labs) with human analyst review to remove false positives.

**Rating: STRONG**

---

**2. RT / Meliorator: documented state-directed AI content operation**

> In July 2024, the U.S. Department of Justice, in a joint action with Dutch and Canadian authorities, seized 968 AI-generated social media accounts and two associated domains operated on behalf of the Russian government. The operation used AI-powered software (Meliorator), developed at the direction of an RT editor-in-chief and backed by FSB and Kremlin approval, to generate authentic-appearing social media personas and amplify pro-Kremlin narratives on X. The FBI described this as "a first in disrupting a Russian-sponsored Generative AI-enhanced social media bot farm" (DOJ press release, 9 July 2024; joint advisory: US, Canada, Netherlands).

**Rating: STRONG**

---

**3. arXiv 2604.26965: proportion of new web content that is machine-generated**

> A preprint (Kneidinger et al., arXiv:2604.26965, April 2026) using stratified sampling of the Internet Archive and a validated three-way AI detector (Pangram v3) found that by the first half of 2025, approximately 35% of websites newly uploaded to the web in a given month were AI-generated or AI-assisted. The paper plots a continuous time series from the ChatGPT launch in November 2022 forward, showing a clear structural break.

**Rating: STRONG** (subject to the caveat that "AI-assisted" is a broad category encompassing anything from light editing to full generation)

---

**4. Pravda/Portal Kombat network: documented volume and retrieval presence**

> The Pravda network (also called Portal Kombat, first identified by France's VIGINUM in February 2024) is a centralised operation running 150–193 websites across 49+ countries, publishing an estimated 3.6–3.7 million articles in 2024, attributed via web forensics to a Crimea-based IT company with links to Russian-occupied Crimea's administration (DFRLab and Check First, February 2025). The DFRLab/Check First investigation found Pravda domains cited in 1,907 hyperlinks across 1,672 Wikipedia pages in 44 languages; exponential growth in Pravda-linked posting on X from February 2022; and chatbot outputs citing Pravda-affiliated sources. A subsequent NewsGuard audit (March 2025) found 10 major chatbots repeated false Pravda-sourced narratives in 33.55% of 450 test prompts, though an independent replication by Al Jazeera-affiliated researchers using different prompts found a 5% repetition rate, supporting a "data void" mechanism rather than systematic training contamination (Al Jazeera, July 2025).

**Rating: STRONG** for network existence and volume. **MODERATE** for retrieval contamination: present evidence supports the claim that Pravda content appears in AI outputs on contested/thin-coverage topics, but the scale and mechanism are disputed.

---

### OpenAI / Meta Threat Reports — Appropriate Limited Use

These reports are valuable as evidence that AI is used in influence operations by state-linked actors, and as sources that explicitly name named operations. They are **not appropriate** as evidence that AI influence operations are succeeding at audience manipulation — both OpenAI and Meta consistently find that AI provides only productivity gains, operations fail to build authentic audiences, and platform detection remains effective. The paper may cite these reports for the first claim but must not cite them for the second without noting the consistent finding of limited effectiveness.

---

## Section 8 — Claims the Paper Should NOT Make

The following claims circulate in the literature or public commentary but are not supported by evidence that meets the programme's standards. Do not cite these without retracting to a weaker and verifiable formulation.

| Claim | Problem |
|-------|---------|
| "AI chatbots reliably repeat Russian disinformation from the Pravda network 33% of the time" | The NewsGuard figure is from unpublished prompts (refused to journalists); independent replication found 5%. The 33% should not be cited as a population statistic. |
| "AI-generated content now constitutes 57% [or 90%] of the internet" | No primary source or methodology was located for 57%. The Europol "90% by 2026" figure has no published methodology and may be extrapolative inference. |
| "74% of new web pages are AI-generated" | The Ahrefs finding covers "any AI content" — their own breakdown shows 2.5% "pure AI"; the rest includes light AI use. Citing this as AI-generated content is misleading. |
| "Pravda content has entered AI training datasets" | This is inferred from publishing volume and chatbot output behaviour. No direct measurement of training data contamination has been published. The mechanism (training vs. live retrieval) has not been empirically distinguished. |
| "AI influence operations have shifted public opinion" | Both OpenAI and Meta explicitly find operations fail to build authentic audiences. There is no published causal evidence of opinion shift attributable to AI content operations. |
| "AI provides novel capabilities that existing defences cannot detect" | OpenAI and Meta both consistently find that behavioural detection (rather than content-based detection) remains effective against AI-enhanced operations. |

---

## Appendix: Key Sources with URLs

| Item | Organisation | Date | URL |
|------|-------------|------|-----|
| UAIN Tracker overview | NewsGuard | Nov 2024 | https://www.newsguardtech.com/insights/watch-out-ai-news-sites-are-on-the-rise |
| AI Content Farm datastream launch | NewsGuard | Mar 2026 | https://www.newsguardtech.com/press/newsguard-launches-real-time-ai-content-farm-detection-datastream-to-counter-onslaught-of-ai-slop-in-news/ |
| OpenAI first IO report | OpenAI | May 2024 | https://downloads.ctfassets.net/kftzwdyauwt9/5IMxzTmUclSOAcWUXbkVrK/3cfab518e6b10789ab8843bcca18b633/Threat_Intel_Report.pdf |
| OpenAI Oct 2024 update | OpenAI | Oct 2024 | https://cdn.openai.com/threat-intelligence-reports/influence-and-cyber-operations-an-update_October-2024.pdf |
| OpenAI Oct 2025 update | OpenAI | Oct 2025 | https://cdn.openai.com/threat-intelligence-reports/7d662b68-952f-4dfd-a2f2-fe55b041cc4a/disrupting-malicious-uses-of-ai-october-2025.pdf |
| Meta Q3 2024 Adversarial Threat Report | Meta | Q3 2024 | https://transparency.meta.com/sr/Q3-2024-Adversarial-threat-report |
| Meta Q4 2024 Adversarial Threat Report | Meta | Q4 2024 | https://transparency.meta.com/sr/Q4-2024-Adversarial-threat-report/ |
| Google GTIG Jan 2025 report | Google GTIG | Jan 2025 | Referenced in Cloud CISO blog: https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-recent-advances-in-how-threat-actors-use-ai-tools |
| Google GTIG Nov 2025 report | Google GTIG | Nov 2025 | https://services.google.com/fh/files/misc/advances-in-threat-actor-usage-of-ai-tools-en.pdf |
| DOJ Meliorator press release | DOJ/FBI | Jul 2024 | https://apnews.com/article/russia-disinformation-fbi-justice-department-50910729878377c0bf64a916983dbe44 |
| US-Canada-Netherlands Meliorator advisory | US/Canada/Netherlands | Jul 2024 | Referenced in Verge/BleepingComputer coverage |
| Pravda network expansion | DFRLab + Check First | Feb 2025 | https://dfrlab.org/2025/02/24/russia-pravda-network-expands-worldwide/ |
| ASP LLM grooming report | American Sunlight Project | Feb 2025 | https://americansunlight.substack.com/p/bad-actors-are-grooming-llms-to-produce |
| NewsGuard chatbot audit | NewsGuard | Mar 2025 | https://www.newsguardrealitycheck.com/p/a-well-funded-moscow-based-global |
| Al Jazeera methodological critique | Al Jazeera | Jul 2025 | https://www.aljazeera.com/opinions/2025/7/8/is-russia-really-grooming-western |
| AI-generated text on the internet | Kneidinger et al. | Apr 2026 | https://arxiv.org/abs/2604.26965 |
| Drop Site News: Clock Tower X / Israel | Drop Site News | 2025 | https://www.dropsitenews.com/p/israel-brad-parscale-ai-chatbots-gaza |
| Parscale FARA record analysis | brandonmyers.net | 2025 | https://brandonmyers.net/writing/parscale-information-operations |
