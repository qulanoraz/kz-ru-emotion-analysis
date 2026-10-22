# 1. Project Proposal

**Document ID:** DOC-01 · **Version:** 1.0 (draft for pre-defense-1) · **Date:** 20.10.2026
**YouTrack:** DIP-3 · **Owner:** Ulan Orazbek, Nurgaly Ashkenov · **Reviewer:** K. Tanyrbergenova

---

## 1.1 Title

| Language | Title |
|---|---|
| English | Identifying emotions from text (sentiment analysis) for the Kazakh and Russian languages |
| Russian | Определение эмоций по тексту (анализ тональности) для казахского и русского языков |
| Kazakh | Мәтіннен эмоцияларды анықтау (көңіл-күйді талдау) қазақ және орыс тілдерінде |

## 1.2 Team and supervision

| Member | Group | Role | Primary responsibilities |
|---|---|---|---|
| Nurgaly Kuanyshevich Ashkenov | SE-2406 | ML/NLP Engineer | Corpus collection and annotation for Kazakh, Russian and mixed texts; preprocessing accounting for Kazakh agglutinative morphology; fine-tuning multilingual transformers (e.g., XLM-RoBERTa); baselines; model evaluation |
| Ulan Abzalovich Orazbek | SE-2406 | Backend Developer & System Integrator | System architecture; REST API for single-text analysis; batch processing with aggregated statistics; PostgreSQL design; web UI with charts and reports; testing; Docker containerisation and deployment |

**Scientific supervisor:** Kamila Tanyrbergenova.

## 1.3 Problem statement

Organisations operating in Kazakhstan — customer-support departments, social-media monitoring teams and units responsible for the quality of public and commercial services — receive large volumes of unstructured textual feedback every day: reviews, complaints, citizen appeals, chat messages and social-media comments. This feedback is produced in **Kazakh, Russian, and frequently in both languages within a single message (intra-sentential code-switching)**, often written informally, with transliteration, non-standard spelling and mixed Cyrillic/Latin script.

Three gaps make this feedback hard to exploit:

1. **Manual processing does not scale.** Reading and categorising messages by emotional tone is slow, subjective, and delays the reaction to critical cases (e.g., angry or frightened customers).
2. **Language coverage gap.** The majority of commercial and open-source emotion/sentiment tools target English; Russian is moderately covered, while Kazakh — a low-resource, agglutinative Turkic language — has very few publicly available, validated emotion-recognition models and datasets. Code-switched KZ–RU text is practically unsupported.
3. **Granularity gap.** Where Kazakh resources exist, they mostly address *polarity* (positive/negative/neutral). Operational teams need finer-grained *emotions* (e.g., distinguishing anger from sadness or fear) to prioritise and route messages.

**Problem:** there is no accessible, evaluated software solution that automatically identifies emotions in Kazakh, Russian and mixed Kazakh–Russian texts and integrates into organisational workflows via an API and an analytics interface.

## 1.4 Target users

| User group | Context of use | Key need |
|---|---|---|
| **Customer-support operators and team leads** (banks, telecom, e-commerce, delivery) | Incoming tickets, chats, app-store reviews | Prioritise negative/angry messages; see emotional trends per period |
| **Social-media / brand monitoring analysts** | Comments under posts, mentions | Aggregate emotional reaction to an event or campaign |
| **Service-quality analysts in public sector** | Citizen appeals and feedback on public services | Summary reports by emotion for management, without reading every message |
| **Developers of external systems** (CRM, helpdesk, chatbot) | Machine-to-machine integration | Simple REST API returning emotion labels and confidence |

Primary persona for MVP: *a support/quality analyst who uploads an export of several thousand reviews and needs a dashboard with emotion distribution and examples within minutes.*

## 1.5 Aim

To design, implement and evaluate a software system that automatically identifies emotions in Kazakh, Russian and code-switched Kazakh–Russian texts using a fine-tuned multilingual transformer model, and provides this capability through a REST API and a web-based analytics interface supporting both single-text and batch processing.

## 1.6 Objectives

| ID | Objective | Owner | Verifiable output |
|---|---|---|---|
| O1 | Analyse the problem domain and validate requirements with 3–5 representatives of target users | Both | Interview notes, evidence report (DOC-02) |
| O2 | Review ≥ 12 sources (≥ 8 scientific) on emotion recognition, multilingual transformers and Kazakh NLP | Nurgaly (lead) | Literature review with analytical table (DOC-03) |
| O3 | Define an emotion taxonomy and annotation guidelines; build a labelled KZ/RU/mixed corpus combining existing public datasets and newly annotated texts | Nurgaly | Annotated dataset, guidelines, inter-annotator agreement (Cohen's κ) report |
| O4 | Implement preprocessing that handles Kazakh-specific characters, Cyrillic/Latin variants, noise and language identification (kk / ru / mixed) | Nurgaly | Preprocessing module with unit tests |
| O5 | Train baselines (TF-IDF + Logistic Regression; multilingual BERT) and fine-tune XLM-RoBERTa; compare them per language slice | Nurgaly | Experiment report with Macro-F1, Precision, Recall per class for KZ, RU, mixed |
| O6 | Design the system architecture and specify FR/NFR with measurable acceptance criteria | Ulan (lead) | Requirements spec (DOC-06), architecture & diagrams (DOC-07) |
| O7 | Implement a REST API for single-text analysis and asynchronous batch analysis of uploaded files (CSV/XLSX/TXT) with aggregated statistics | Ulan | API service, OpenAPI contract, integration tests |
| O8 | Design and implement a PostgreSQL schema for requests, batches, predictions and reports | Ulan | Migrations, ER diagram |
| O9 | Develop a web interface for batch upload, dashboard (charts by emotion, language, time) and report export | Ulan | Web UI, usability walkthrough with target users |
| O10 | Containerise and deploy the system; perform unit, integration and load testing | Ulan | Docker Compose stack, test reports, load-test results |

## 1.7 Expected outcomes

1. **Labelled corpus** of Kazakh, Russian and mixed texts annotated with six emotion classes (`joy`, `sadness`, `anger`, `fear`, `surprise`, `neutral`), with documented guidelines and agreement statistics.
2. **Fine-tuned emotion classification model** with a reproducible training pipeline and an evaluation report broken down by language slice. *Target (hypothesis to be confirmed against baselines):* the fine-tuned transformer outperforms the TF-IDF baseline in Macro-F1 on each of the KZ, RU and mixed test slices.
3. **Inference service** returning emotion label, class probabilities, derived polarity and detected language for each text.
4. **Backend REST API** with single-text and batch endpoints, API-key authentication and an OpenAPI specification.
5. **Web application** with batch upload, processing status, dashboards (emotion distribution, distribution by language, trend over time if timestamps are provided) and export of reports (CSV/PDF).
6. **Deployment package** (Docker Compose) and test reports (unit, integration, load).
7. **Diploma thesis** documenting analysis, design, implementation and evaluation.

## 1.8 Project scope

### In scope

- Text-only emotion classification for **Kazakh (Cyrillic, with tolerance to common Latin transliteration)**, **Russian** and **code-switched KZ–RU** texts.
- Single-label classification into six classes; derived three-way polarity.
- Automatic language identification per text (kk / ru / mixed).
- Combination of existing public datasets with project-specific annotation of domain texts (reviews, comments, appeals).
- Fine-tuning and comparison of at least three models (classical baseline, mBERT-class model, XLM-RoBERTa).
- REST API: single analysis (synchronous) and batch analysis (asynchronous job with status polling).
- Supported batch formats: CSV, XLSX, TXT (one text per line); file size limit defined in requirements.
- PostgreSQL storage of batches, predictions and aggregated statistics.
- Web dashboard with charts and downloadable reports.
- API-key authentication, basic role separation (analyst / admin).
- Docker-based deployment on a single server or cloud VM.

### Out of scope

- Speech, audio, image or video emotion recognition.
- Languages other than Kazakh and Russian (English or other code-switching is not evaluated).
- Sarcasm and irony detection as a dedicated task (noted as a limitation).
- Aspect-based sentiment analysis (emotion per product feature).
- Real-time streaming ingestion from social networks via their APIs (batch upload and REST only).
- Training large language models from scratch.
- Multi-tenant SaaS billing, enterprise SSO, high-availability cluster deployment.
- Official certification for use in government information systems.

### Stretch goals (only if time allows)

- Multi-label emotion output (a text may express several emotions).
- Model explainability (highlighting tokens that influenced the prediction).
- ONNX/quantised model for CPU-efficient inference.

## 1.9 Engineering complexity

The project combines two non-trivial engineering tracks:

**ML/NLP complexity**
- Kazakh is a low-resource, agglutinative language: a single root can produce many surface forms through suffix chains, which inflates vocabulary and harms word-level models; subword tokenisation and normalisation must be evaluated explicitly.
- Code-switching inside one message requires models and evaluation that do not assume a single language per text.
- Scarcity of emotion-labelled Kazakh data requires an annotation process with quality control (guidelines, double annotation of a subset, agreement measurement) and possibly cross-lingual transfer from Russian data.
- Fair evaluation requires stratified test sets and per-slice metrics, since an aggregate score can hide poor Kazakh performance.

**Software/architecture complexity**
- Separation of the backend API and the ML inference service to isolate GPU/CPU-heavy inference from request handling.
- Asynchronous batch pipeline (file validation → parsing → chunked inference → aggregation → report) with job status tracking and failure handling.
- Relational data model for batches, items, predictions and aggregates, with efficient querying for dashboards.
- Non-functional requirements on latency, throughput and file size, verified by load testing.
- Containerised, reproducible deployment and CI.

## 1.10 Preliminary success criteria

| Criterion | Measure | Verified in |
|---|---|---|
| Model quality | Macro-F1 of fine-tuned model > baseline on KZ, RU and mixed slices | DOC-09, experiment report |
| API correctness | All Must-have FR acceptance tests pass | Integration test report |
| Performance | Single-text latency and batch throughput meet NFR targets (defined in DOC-06) | Load-test report |
| Usability | ≥ 2 target-user representatives complete the batch-upload scenario without assistance | Usability walkthrough notes |
| Traceability | Every Must-have FR is linked to DIP tasks, commits and tests | Traceability matrix (DOC-06/DOC-10) |

## 1.11 High-level timeline

| Phase | Period | Main result |
|---|---|---|
| Analysis & design | Sep – Oct 2026 | Pre-defense-1 package (this repository state, tag `pre-defense-1`) |
| Data & baselines | Nov – Dec 2026 | Annotated corpus v1, baseline results, API skeleton, DB schema |
| Core implementation | Jan – Mar 2027 | Fine-tuned model, single + batch API, dashboard MVP (pre-defense-2) |
| Evaluation & hardening | Apr 2027 | Full evaluation, load tests, usability sessions |
| Thesis & final defense | May – Jun 2027 | Final thesis, release `final-defense` |

*Detailed milestones and the YouTrack backlog are given in DOC-10.*
