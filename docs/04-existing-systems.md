# 4. Existing System Comparison

**Document ID:** DOC-04 · **Version:** 1.0 (draft) · **Date:** 20.10.2026
**YouTrack:** DIP-7 · **Owner:** Ulan Orazbek (lead), Nurgaly Ashkenov
**Facts checked:** 20.10.2026 against official documentation (T1–T6 in DOC-03). Cloud language lists change; the check date is part of the evidence.

---

## 4.1 Selection of systems

Systems were selected to represent the three realistic options an organisation in Kazakhstan has today:

| Category | System | Why selected |
|---|---|---|
| Commercial cloud NLP API | **A. Microsoft Azure AI Language — Sentiment Analysis** | The only major cloud API found whose sentiment feature officially lists Kazakh |
| Commercial cloud NLP API | **B. Google Cloud Natural Language API** | Market-leading general NLP API |
| Commercial cloud NLP API | **C. Amazon Comprehend** | Market-leading general NLP API with batch jobs |
| Open-source research model (Kazakh) | **D. ISSAI KazSAnDRA models** | Strongest public Kazakh sentiment resource (S15) |
| Open-source model (Russian emotions) | **E. RuBERT-tiny2 fine-tuned on CEDR** | Ready-to-use Russian *emotion* model (T4) |
| Open-source library (Russian sentiment) | **F. Dostoevsky** | Popular Russian sentiment library (T5) |
| Generic approach | **G. General-purpose LLM via prompting** | Increasingly used as a "no-training" alternative |

> Commercial social-listening platforms that operate in the region (e.g., brand-monitoring SaaS) were considered but excluded from the scored comparison because their language support and model details are not publicly documented; claims about them could not be supported by facts. They are listed for follow-up via demo requests (DIP-7 sub-task).

## 4.2 Comparison criteria

| ID | Criterion | Why it matters (link to DOC-02) |
|---|---|---|
| C1 | Kazakh language support | Core problem (H1, H3) |
| C2 | Russian language support | Bilingual environment (D1) |
| C3 | Code-switched KZ–RU handling | Real feedback is mixed (H1, S15) |
| C4 | Output granularity: discrete emotions vs. polarity | Users need finer categories (H4) |
| C5 | Batch processing of large volumes | Primary scenario (H5) |
| C6 | End-user interface (dashboard/reports) | Analysts are non-programmers |
| C7 | Self-hosting / data residency | Privacy constraints of public and banking sector |
| C8 | Customisation / fine-tuning on own data | Domain adaptation |
| C9 | Cost model | Feasibility for SMEs and public bodies |
| C10 | Transparency of evaluation (published metrics for KZ/RU) | Trust and verifiability |

## 4.3 Comparison matrix

Legend: ✔ supported · ◐ partial / with limitations · ✘ not supported · ? not documented.

| Criterion | A. Azure AI Language | B. Google Cloud NL | C. Amazon Comprehend | D. KazSAnDRA models | E. RuBERT-tiny2-CEDR | F. Dostoevsky | G. LLM prompting | **Our system** |
|---|---|---|---|---|---|---|---|---|
| C1 Kazakh | ✔ (`kk` listed for sentiment and opinion mining) | ✘ (not in sentiment language list) | ✘ (not in supported languages) | ✔ | ✘ | ✘ | ◐ (works, quality unverified for KZ) | ✔ |
| C2 Russian | ✔ | ✘ for sentiment (Russian listed for other features only) | ✘ | ◐ (trained on Kazakh reviews that contain some Russian) | ✔ | ✔ | ✔ | ✔ |
| C3 Code-switching | ? (single language code per document) | ✘ | ✘ (one language per job) | ◐ (present in data, flagged by authors as open issue) | ✘ | ✘ | ◐ | ✔ (explicit `mixed` slice, evaluated) |
| C4 Granularity | ◐ polarity (+ aspect-level opinion mining) | ◐ score/magnitude polarity | ◐ positive/negative/neutral/mixed | ◐ polarity or 1–5 score | ✔ 5 emotions + no-emotion | ◐ polarity (+ speech/skip classes) | ✔ any label set | ✔ 6 emotions + polarity |
| C5 Batch | ◐ multi-document requests via API | ◐ via API calls | ✔ asynchronous batch jobs | ✘ (model only) | ✘ (model only) | ◐ (library, code required) | ◐ (rate limits, cost per token) | ✔ file upload + async job |
| C6 UI / reports | ✘ (developer API) | ✘ | ✘ | ✘ | ✘ | ✘ | ✘ (chat UI not an analytics tool) | ✔ dashboard + export |
| C7 Self-hosting | ◐ Docker containers available for sentiment | ✘ cloud only | ✘ cloud only | ✔ | ✔ | ✔ | ◐ (only open-weight models) | ✔ Docker |
| C8 Customisation | ◐ custom sentiment in preview | ✘ for sentiment | ◐ custom classification (limited languages) | ✔ (open weights) | ✔ | ◐ | ◐ prompt engineering only | ✔ retrainable pipeline |
| C9 Cost | Pay per text record | Pay per unit | Pay per unit | Free (CC BY 4.0) | Free | Free | Pay per token / GPU | Free / self-hosted |
| C10 Published KZ/RU metrics | ✘ (no per-language metrics published) | — | — | ✔ (F1 0.81 polarity) | ✔ (model card metrics on CEDR test) | ◐ (~0.71 F1 on RuSentiment) | ✘ | ✔ (per-slice evaluation, DOC-09) |

## 4.4 Fact sheet (evidence for each claim)

| System | Verified facts (source) | Key limitation for our use case |
|---|---|---|
| **A. Azure** | Kazakh (`kk`) appears in the Sentiment Analysis language list and was recently added for Opinion Mining; the same languages are supported in the cloud API and in Docker containers. Output labels are positive/neutral/negative. Microsoft's documentation states that sentiment analysis and opinion mining are scheduled to **retire on 31 March 2029** (T1). | Polarity only; no emotions; no per-language accuracy published; retirement date is a long-term dependency risk |
| **B. Google** | Sentiment analysis language list: Arabic, Chinese, Dutch, English, French, German, Indonesian, Italian, Japanese, Korean, Portuguese, Spanish, Thai, Turkish — **neither Kazakh nor Russian** (T2). | Unusable for the target languages |
| **C. Amazon** | Supported languages: de, en, es, it, pt, fr, ja, ko, hi, ar, zh, zh-TW; sentiment returns POSITIVE/NEGATIVE/NEUTRAL/MIXED; all documents in one job must share a language; single-call text limit 5 KB (T3). | No Kazakh or Russian; one-language-per-job model conflicts with mixed text |
| **D. KazSAnDRA** | ~180k Kazakh reviews with 1–5 ratings, CC BY 4.0, fine-tuned models released; best F1 0.81 polarity, 0.39 score classification; authors list code-switching and spelling errors as future work (S15, T6). | Polarity only; research artefact without API, batch, UI |
| **E. RuBERT-tiny2-CEDR** | RuBERT-tiny2 fine-tuned on CEDR for multi-label classification of no emotion, joy, sadness, surprise, fear, anger; per-label AUC and F1 published on the CEDR test set (T4, S12). | Russian only; model artefact only |
| **F. Dostoevsky** | Python library; FastText model trained on RuSentiment reaching about 0.71 F1 (T5, S20). | Russian only; polarity only; older approach |
| **G. LLM prompting** | BRIGHTER/SemEval-2025 report that LLMs struggle with perceived emotion in text, especially for low-resource languages, and often do better when prompted in English (S10, S11). | Quality for Kazakh unverified; data leaves the organisation (for API models); cost and non-determinism at batch scale |

## 4.5 Gap analysis — why this project is needed

1. **No system combines Kazakh + Russian + emotions.** The only cloud API with Kazakh (A) gives polarity, the only open Russian emotion model (E) has no Kazakh, and the only strong Kazakh resource (D) is polarity-level.
2. **Mixed-language text is not a supported input anywhere.** Cloud APIs expect one language per document or job (A, C); open models are monolingual (E, F); D documents mixing as an unsolved issue.
3. **No end-user analytics layer.** Every option is either a developer API or a model file; analysts still need custom engineering to upload a file and get a report (C5, C6).
4. **Privacy-sensitive users lack a self-hosted option with Kazakh support**, except Azure containers with polarity only.
5. **No transparent per-language evaluation** for commercial services, so organisations cannot verify quality on their own language mix.

**Positioning statement.** The project does not compete with cloud vendors on breadth; it targets the specific, undocumented niche of *emotion-level, self-hostable analysis of Kazakh, Russian and mixed feedback with a ready analytics interface and published per-slice metrics*.

## 4.6 Use of existing systems inside the project

| System | Planned use |
|---|---|
| D. KazSAnDRA | Source of Kazakh texts for emotion re-annotation; polarity labels as sanity check |
| E. RuBERT-tiny2-CEDR | Baseline for the Russian slice |
| A. Azure (optional, if free tier permits) | Polarity reference on a small Kazakh sample to illustrate the granularity gap |
| G. LLM zero-shot | Reference baseline in DOC-09 (small sample, no personal data) |
