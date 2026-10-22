# 3. Literature Review

**Document ID:** DOC-03 · **Version:** 1.0 (draft for pre-defense-1) · **Date:** 20.10.2026
**YouTrack:** DIP-5 · **Owner:** Nurgaly Ashkenov (lead), Ulan Orazbek · **Reviewer:** K. Tanyrbergenova
**Bibliography source:** [`docs/literature/references.bib`](literature/references.bib)

---

## 3.1 Scope and search strategy

**Research questions guiding the review**

- **RQ1.** Which emotion taxonomies and annotation schemes are used for text-based emotion recognition, and which fit operational feedback analysis?
- **RQ2.** Which model families give the best accuracy/cost trade-off for emotion classification, especially in multilingual and low-resource settings?
- **RQ3.** What resources (datasets, models, tools) exist for Kazakh and Russian sentiment/emotion analysis, and what are their gaps?
- **RQ4.** What is known about processing code-switched text, and how should it be evaluated?

**Sources searched:** ACL Anthology, arXiv, Google Scholar, ScienceDirect, IEEE Xplore, dblp, ISSAI (Nazarbayev University) publication list, Hugging Face Hub (for model/dataset cards).

**Keywords:** *emotion detection/recognition, text emotion classification, sentiment analysis, Kazakh, Russian, low-resource, multilingual transformer, cross-lingual transfer, XLM-RoBERTa, code-switching/code-mixing, dataset, annotation*.

**Inclusion criteria:** peer-reviewed publications or widely cited preprints; main pool from 2021–2025 (fast-moving field), plus foundational works on emotion theory and transformer architectures; technical documentation only for factual claims about existing products.

**Exclusion criteria:** speech/image-only emotion recognition (except where the taxonomy is directly reusable for Kazakh), non-reproducible blog posts, sources without verifiable bibliographic data.

**Result:** 26 sources used — **20 scientific publications** + **6 technical/documentation sources**. Every bibliographic record and DOI in this document was checked against the publisher, ACL Anthology or arXiv page; records without a DOI are cited by venue or arXiv ID rather than an invented identifier.

## 3.2 Source list

### Scientific publications

| ID | Reference | Year | Venue / identifier |
|---|---|---|---|
| S1 | P. Ekman. *An argument for basic emotions* | 1992 | Cognition and Emotion 6(3–4); DOI 10.1080/02699939208411068 |
| S2 | A. Vaswani et al. *Attention Is All You Need* | 2017 | NeurIPS 2017; arXiv:1706.03762 |
| S3 | J. Devlin, M.-W. Chang, K. Lee, K. Toutanova. *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding* | 2019 | NAACL-HLT 2019; DOI 10.18653/v1/N19-1423 |
| S4 | A. Conneau et al. *Unsupervised Cross-lingual Representation Learning at Scale* (XLM-R) | 2020 | ACL 2020; DOI 10.18653/v1/2020.acl-main.747 |
| S5 | P. He, J. Gao, W. Chen. *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing* | 2023 | ICLR 2023; arXiv:2111.09543 |
| S6 | C. Sun, X. Qiu, Y. Xu, X. Huang. *How to Fine-Tune BERT for Text Classification?* | 2019 | CCL 2019; arXiv:1905.05583 |
| S7 | S. Mohammad, F. Bravo-Marquez, M. Salameh, S. Kiritchenko. *SemEval-2018 Task 1: Affect in Tweets* | 2018 | SemEval-2018; DOI 10.18653/v1/S18-1001 |
| S8 | D. Demszky et al. *GoEmotions: A Dataset of Fine-Grained Emotions* | 2020 | ACL 2020; DOI 10.18653/v1/2020.acl-main.372 |
| S9 | F. A. Acheampong, H. Nunoo-Mensah, W. Chen. *Transformer models for text-based emotion detection: a review of BERT-based approaches* | 2021 | Artificial Intelligence Review 54; DOI 10.1007/s10462-021-09958-2 |
| S10 | S. H. Muhammad et al. *BRIGHTER: BRIdging the Gap in Human-Annotated Textual Emotion Recognition Datasets for 28 Languages* | 2025 | arXiv:2502.11926 (ACL 2025) |
| S11 | S. H. Muhammad et al. *SemEval-2025 Task 11: Bridging the Gap in Text-Based Emotion Detection* | 2025 | Proc. SemEval-2025, ACL |
| S12 | A. Sboev, A. Naumov, R. Rybka. *Data-Driven Model for Emotion Detection in Russian Texts* (CEDR) | 2021 | Procedia Computer Science 190; DOI 10.1016/j.procs.2021.06.075 |
| S13 | Y. Kuratov, M. Arkhipov. *Adaptation of Deep Bidirectional Multilingual Transformers for Russian Language* (RuBERT) | 2019 | Dialogue 2019; arXiv:1905.07213 |
| S14 | D. Zmitrovich et al. *A Family of Pretrained Transformer Language Models for Russian* | 2024 | LREC-COLING 2024 |
| S15 | R. Yeshpanov, H. A. Varol. *KazSAnDRA: Kazakh Sentiment Analysis Dataset of Reviews and Attitudes* | 2024 | LREC-COLING 2024 (2024.lrec-main.844); arXiv:2403.19335 |
| S16 | B. Yergesh, G. Bekmanova, A. Sharipbay. *Sentiment analysis of Kazakh text and their polarity* | 2019 | Web Intelligence 17(1):9–15; DOI 10.3233/WEB-190396 |
| S17 | S. Narynov, A. Zharmagambetov. *On One Approach of Solving Sentiment Analysis Task for Kazakh and Russian Languages Using Deep Learning* | 2016 | ICCCI 2016, LNCS, Springer |
| S18 | A. Abilbekov, S. Mussakhojayeva, R. Yeshpanov, H. A. Varol. *KazEmoTTS: A Dataset for Kazakh Emotional Text-to-Speech Synthesis* | 2024 | LREC-COLING 2024 (2024.lrec-main.841) |
| S19 | G. I. Winata, A. F. Aji, Z.-X. Yong, T. Solorio. *The Decades Progress on Code-Switching Research in NLP: A Systematic Survey on Trends and Challenges* | 2023 | Findings of ACL 2023; DOI 10.18653/v1/2023.findings-acl.185 |
| S20 | A. Rogers et al. *RuSentiment: An Enriched Sentiment Analysis Dataset for Social Media in Russian* | 2018 | COLING 2018 |

> 20 scientific entries are listed, well above the required minimum of 8. **Recent pool (2021–2025): S5, S9, S10, S11, S12, S14, S15, S18, S19 — 9 sources.** Foundational works (S1–S4, S6–S8, S13, S16, S17, S20) are retained because later work builds directly on them: transformer and multilingual pre-training (S2–S4, S6), emotion theory and benchmark design (S1, S7, S8), and the earliest Kazakh and Russian sentiment resources (S13, S16, S17, S20).

### Technical / documentation sources

| ID | Source | Used for |
|---|---|---|
| T1 | Microsoft Learn — *Sentiment Analysis and Opinion Mining language support* (Azure AI Language) | DOC-04 claims on Azure |
| T2 | Google Cloud — *Natural Language API: Language Support* | DOC-04 claims on Google |
| T3 | AWS — *Languages supported in Amazon Comprehend* | DOC-04 claims on AWS |
| T4 | Hugging Face — model card `cointegrated/rubert-tiny2-cedr-emotion-detection` | DOC-04, baseline candidate |
| T5 | GitHub — `bureaucratic-labs/dostoevsky` (Russian sentiment library) | DOC-04 |
| T6 | GitHub — ISSAI KazSAnDRA repository (dataset + fine-tuned models, CC BY 4.0) | Data source, DOC-04 |

## 3.3 Thematic critical review

### 3.3.1 Emotion models and taxonomies (RQ1)

Two families of emotion models dominate computational work: **categorical** models, built on the idea of a small set of universal basic emotions (Ekman's anger, disgust, fear, joy, sadness, surprise — S1), and **dimensional** models (valence–arousal). Categorical schemes are preferred in applied NLP because labels are directly interpretable by end users and map onto routing rules.

Dataset designers differ in granularity. GoEmotions (S8) uses 27 fine-grained emotions plus neutral on English Reddit comments and shows that fine taxonomies can be collapsed to Ekman-level groups for practical use. SemEval-2018 Task 1 (S7) frames emotion recognition as multi-label classification across English, Arabic and Spanish tweets, establishing **multi-label** output and **macro-averaged** metrics as standard practice. The recent BRIGHTER collection and SemEval-2025 Task 11 (S10, S11) apply a compact six-class, multi-label scheme across more than 28 predominantly low-resource languages.

For our two languages specifically: CEDR (S12) annotates Russian sentences with five basic emotions (joy, sadness, surprise, fear, anger) plus "no emotion", and KazEmoTTS (S18) — although a speech-synthesis corpus — uses neutral, angry, happy, sad, scared and surprised for Kazakh.

**Implication for this project.** We adopt **joy, sadness, anger, fear, surprise, neutral**. This set (a) is Ekman-based (S1), (b) aligns one-to-one with CEDR (S12) so Russian data can be reused without relabelling, (c) matches the label set already used in Kazakh emotional resources (S18), and (d) is small enough for reliable annotation of informal text. *Disgust* is excluded from the MVP because it is absent from CEDR and expected to be rare in service feedback; this is recorded as assumption AS-4 (DOC-02) and will be revisited after the annotation pilot. We keep single-label output for the MVP and treat multi-label as a stretch goal, acknowledging that S7, S10 and S12 show texts often carry several emotions.

### 3.3.2 Model families for text emotion classification (RQ2)

Earlier Kazakh and Russian sentiment work relied on **lexicons and morphological rules** (S16) or on shallow neural models (S17). Lexicon methods are transparent and need no labelled data, but they are brittle against slang, misspellings and transliteration — exactly the properties of real customer feedback (H7, DOC-02).

The **transformer** architecture (S2) and bidirectional pre-training (S3) changed the field: fine-tuning a pre-trained encoder with a small classification head became the strongest general recipe for text classification, and S6 gives practical guidance on learning-rate schedules, layer-wise learning rates and further in-domain pre-training. The review by Acheampong et al. (S9) confirms that BERT-family encoders dominate text-based emotion detection, while noting persistent difficulties: class imbalance, implicit emotion, and dependence on English data.

For multilingual settings, **XLM-R** (S4) was pre-trained on CommonCrawl data for 100 languages, including both Kazakh and Russian, and demonstrated strong cross-lingual transfer, with especially large gains for low-resource languages compared with multilingual BERT. **mDeBERTa-v3** (S5) uses the same multilingual corpus with a more parameter-efficient architecture and is a credible alternative. Language-specific encoders for Russian (RuBERT, S13; the ruBERT/ruRoBERTa family, S14) are stronger on Russian-only text but provide no Kazakh coverage.

**Limitations of existing work.** Most reported emotion results are for English or high-resource languages; S10/S11 explicitly show performance disparities across languages and report that large language models (LLMs) used via prompting struggle with perceived emotions, especially for low-resource languages. This supports fine-tuning a dedicated encoder rather than relying only on a general-purpose LLM, but also motivates **including an LLM zero-shot run as a reference baseline**.

**Implication.** Primary model: XLM-R (base, with large as an upper bound if compute allows). Baselines: TF-IDF + Logistic Regression (classical), multilingual BERT, and — for the Russian slice only — the existing CEDR-trained RuBERT-tiny2 model (T4). Selection is detailed in DOC-05 §5.5.

### 3.3.3 Resources for Kazakh and Russian (RQ3)

**Russian** is reasonably resourced: RuSentiment (S20) provides polarity labels for social-media posts; CEDR (S12) provides 9,410 emotion-labelled sentences, with its authors reporting macro-F1 of 0.78 using ELMo features and an ensemble; ready-made emotion models exist (T4).

**Kazakh** is substantially less resourced. Early work (S16, S17) used lexicons, morphological rules or largely Russian data. The most important recent contribution is **KazSAnDRA** (S15): about 180,000 Kazakh reviews with 1–5 ratings, released under CC BY 4.0 with fine-tuned models. Its authors report a best F1 of 0.81 for polarity but only 0.39 for five-way score classification, and they explicitly identify spelling errors and code-switching as open problems for future work.

**Gap.** We found no publicly available, human-annotated **emotion** dataset for Kazakh *text*. Kazakh resources are polarity-level (S15) or speech-oriented (S18); BRIGHTER (S10) includes Russian and several other low-resource languages but, to our knowledge, not Kazakh *(to be re-verified against the BRIGHTER language list before final submission)*.

**Implication.** Our corpus strategy is (1) reuse CEDR for Russian emotions, (2) use KazSAnDRA texts as a **pool of real Kazakh reviews** that we re-annotate with emotion labels (its polarity labels are used as a consistency check, e.g., a 1-star review should not be labelled *joy*), (3) collect and annotate additional mixed KZ–RU feedback, and (4) measure inter-annotator agreement (Cohen's κ) as done in S7/S8/S12-style annotation pipelines.

### 3.3.4 Code-switching (RQ4)

Winata et al. (S19) surveyed more than 400 code-switching papers from the ACL Anthology and ISCA proceedings up to October 2022. The survey identifies a concentration on a small set of language pairs, scarcity of annotated data and lack of standard evaluation as recurring obstacles, and notes that multilingual pre-trained models are the main practical tool but are not specifically trained for mixed input. KazSAnDRA (S15) documents that real Kazakh reviews already contain Russian, English and Arabic vocabulary, confirming that KZ–RU mixing is a natural property of the data rather than an edge case.

**Implication.** (1) Every text is tagged as `kk`, `ru` or `mixed` during preprocessing and annotation; (2) **all metrics are reported separately for each slice**, because a strong aggregate score can hide failure on mixed text; (3) the test set is stratified by language slice; (4) we explicitly avoid pipelines that translate everything into one language first, since that discards mixing cues and adds translation errors.

## 3.4 Concept matrix

Legend: ● = central contribution, ○ = addressed partially, blank = not addressed.

| Source | Emotion taxonomy | Transformer / fine-tuning | Multilingual / cross-lingual | Kazakh | Russian | Code-switching | Dataset contribution | Low-resource | Evaluation method |
|---|---|---|---|---|---|---|---|---|---|
| S1 Ekman 1992 | ● | | | | | | | | |
| S2 Vaswani 2017 | | ● | | | | | | | |
| S3 Devlin 2019 | | ● | ○ | | | | | | ○ |
| S4 Conneau 2020 | | ● | ● | ○ | ○ | | | ● | ● |
| S5 He 2023 | | ● | ● | | | | | ○ | ○ |
| S6 Sun 2019 | | ● | | | | | | | ● |
| S7 Mohammad 2018 | ● | | ○ | | | | ● | | ● |
| S8 Demszky 2020 | ● | ○ | | | | | ● | | ● |
| S9 Acheampong 2021 | ○ | ● | ○ | | | | | | ○ |
| S10 Muhammad 2025 (BRIGHTER) | ● | ○ | ● | | ○ | | ● | ● | ● |
| S11 Muhammad 2025 (SemEval) | ● | ○ | ● | | ○ | | ○ | ● | ● |
| S12 Sboev 2021 (CEDR) | ● | | | | ● | | ● | | ● |
| S13 Kuratov 2019 (RuBERT) | | ● | ○ | | ● | | | | ○ |
| S14 Zmitrovich 2024 | | ● | | | ● | | | | ● |
| S15 Yeshpanov 2024 (KazSAnDRA) | ○ | ● | | ● | | ○ | ● | ● | ● |
| S16 Yergesh 2019 | ○ | | | ● | | | ○ | ● | |
| S17 Narynov 2016 | | | ○ | ● | ● | | ○ | ○ | |
| S18 Abilbekov 2024 (KazEmoTTS) | ● | | | ● | | | ● | ● | |
| S19 Winata 2023 | | ○ | ● | | | ● | | ○ | ○ |
| S20 Rogers 2018 (RuSentiment) | ○ | | | | ● | | ● | | ● |
| **This project** | ● | ● | ● | ● | ● | ● | ● | ● | ● |

**Reading the matrix:** no single existing work covers the intersection *emotion taxonomy × Kazakh × code-switching*. The Kazakh column has no source that combines text emotion labels with transformer fine-tuning; the code-switching column has no source on KZ–RU emotion. This empty intersection is the research gap the project addresses.

## 3.5 Analytical summary table

| ID | Task | Method | Data | Key finding | Limitation | Use in our project |
|---|---|---|---|---|---|---|
| S1 | Theory of basic emotions | Psychological argument | — | Small set of universal basic emotions | Universality debated; not text-specific | Basis of label set |
| S2 | Sequence modelling | Self-attention transformer | MT benchmarks | Attention-only architecture outperforms recurrent models | Quadratic cost in sequence length | Architecture foundation; max-length setting |
| S3 | Language representation | Masked-LM pre-training + fine-tuning | English corpora; mBERT variant multilingual | Fine-tuned encoders set new SOTA across NLU tasks | English-centric; mBERT weak on low-resource | mBERT baseline |
| S4 | Cross-lingual representation | XLM-R, masked LM on 100 languages | CommonCrawl (CC-100) | Strong cross-lingual transfer, large gains for low-resource languages | Large model; capacity diluted across languages | **Primary model** |
| S5 | Efficient pre-training | DeBERTaV3 (multilingual mDeBERTa) | CC-100 for multilingual variant | Better parameter efficiency than earlier encoders | Fewer published Kazakh results | Alternative model (DOC-05) |
| S6 | Fine-tuning methodology | Systematic fine-tuning experiments | Text classification benchmarks | Layer-wise LR, warm-up and in-domain pre-training improve results | English benchmarks | Training recipe / hyper-parameters |
| S7 | Multilingual affect shared task | Shared-task benchmark | Tweets: EN, AR, ES | Multi-label emotion classification with macro metrics | Twitter domain only | Evaluation protocol |
| S8 | Fine-grained emotion dataset | Crowdsourced annotation, BERT baseline | English Reddit comments | 27 emotions + neutral; mapping to Ekman groups | English only; fine classes hard to annotate | Annotation guideline design, taxonomy mapping |
| S9 | Review | Survey of BERT-based emotion detection | Various | Transformers dominate; imbalance and implicit emotion remain hard | Mostly English studies | Justifies transformer choice; known pitfalls |
| S10 | Multilingual emotion datasets | Community annotation; LLM and encoder baselines | ~100k instances, 28 languages | Large cross-language disparities; LLMs weaker on low-resource languages | Kazakh not covered (to re-verify) | Motivates fine-tuning + LLM reference baseline |
| S11 | Shared task, 30+ languages | Benchmark: monolingual, intensity, cross-lingual tracks | BRIGHTER + additional sets | Cross-lingual emotion detection is an open problem | Kazakh not covered | Cross-lingual evaluation ideas |
| S12 | Russian emotion recognition | ELMo + ensemble classifier | CEDR: 9,410 sentences, 5 emotions | Macro-F1 0.78 reported for Russian | Pre-transformer method; no Kazakh | **Russian training data**, label alignment |
| S13 | Russian language model | mBERT adapted to Russian | Russian Wikipedia, news | Language-specific adaptation outperforms mBERT on Russian | Russian only | Comparison / RU slice reference |
| S14 | Russian model family | Encoder, decoder, encoder-decoder models | Large Russian corpora | Strong Russian-specific baselines on Russian benchmarks | Russian only | Alternative for RU-only experiments |
| S15 | Kazakh sentiment | Dataset + 4 fine-tuned models | ~180k Kazakh reviews, 1–5 ratings | Best F1 0.81 (polarity), 0.39 (score) | Polarity only; code-switching and spelling flagged as open issues | **Kazakh text pool**; polarity consistency check |
| S16 | Kazakh sentiment | Lexicon + morphological rules | Kazakh texts, sentiment dictionary | Rule-based polarity feasible for standard Kazakh | Brittle to informal text; polarity only | Lexicon features for error analysis |
| S17 | KZ/RU sentiment | Deep learning | Mostly Russian news | Early neural approach for the region | Small Kazakh share; older methods | Historical context |
| S18 | Kazakh emotional speech | TTS corpus with emotion labels | 54,760 audio-text pairs, 6 emotions | Emotion label set established for Kazakh | Speech synthesis, not recognition from text | Taxonomy alignment for Kazakh |
| S19 | Code-switching survey | Systematic review of 400+ papers | ACL Anthology, ISCA | Data scarcity and lack of standard evaluation for mixed text | KZ–RU not a focus | Slice-based evaluation, mixed-text handling |
| S20 | Russian sentiment dataset | Annotated social-media posts | VKontakte posts | Guidelines for informal Russian sentiment annotation | Polarity only | Annotation guideline examples |

## 3.6 Synthesis: what the project takes from the literature

| Known from literature | Limitation of existing work | How this project responds |
|---|---|---|
| Fine-tuned multilingual transformers are the strongest practical approach for low-resource text classification (S3, S4, S9) | Few reported results for Kazakh emotion | Fine-tune XLM-R and report Kazakh-specific results |
| Six basic emotions are an established, annotatable scheme (S1, S12, S18) | No Kazakh *text* emotion dataset | Create an annotated KZ/RU/mixed corpus aligned with CEDR labels |
| Kazakh polarity data exists (S15) | Polarity only; code-switching unresolved | Re-annotate KazSAnDRA texts with emotions; dedicated mixed slice |
| LLMs underperform on low-resource emotion recognition (S10) | Fine-tuned systems for Kazakh are missing | Compare fine-tuned encoder with LLM zero-shot baseline |
| Code-switching lacks standard evaluation (S19) | Aggregate metrics hide slice failures | Macro-F1, P, R per class **and per language slice** |
| Most research outputs are models or datasets only | No integrated system for organisations | Deliver API + batch processing + dashboard (DOC-04, DOC-06) |

## 3.7 Threats to validity of the review

- **Coverage bias:** Kazakh-language publications in local journals may be under-indexed in international databases; we will run an additional search on Kazakhstani journals (e.g., journals of ENU, Astana IT University) before the final thesis.
- **Recency:** the field moves quickly; the review will be updated at pre-defense-2.
- **Unverified claim:** Kazakh absence from BRIGHTER must be re-checked against the official language list.
