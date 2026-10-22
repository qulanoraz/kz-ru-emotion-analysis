# 6. Requirements Specification

**Document ID:** DOC-06 · **Version:** 1.0 (draft for pre-defense-1) · **Date:** 20.10.2026
**YouTrack:** DIP-9 · **Owner:** Ulan Orazbek (lead), Nurgaly Ashkenov (ML requirements) · **Reviewer:** K. Tanyrbergenova
**Related:** DOC-01 (objectives O1–O10), DOC-02 (hypotheses H1–H7), DOC-05 (decision drivers), DOC-07 (architecture), DOC-09 (test cases)

---

## 6.1 Purpose and conventions

This document specifies **what** the system must do (functional requirements, FR), **how well** it must do it (non-functional requirements, NFR), and the requirements on the **ML pipeline** (MLR). Every requirement has:

- a unique ID (`FR-xx`, `NFR-xx`, `MLR-xx`) used in tests, commits and YouTrack;
- a **MoSCoW** priority for the diploma release (`final-defense`);
- an **evidence source** (hypothesis or finding from DOC-02/DOC-03/DOC-04); requirements resting only on assumptions are marked **[A]** and re-validated after interviews;
- one or more **acceptance criteria (AC)**, written so that a test can pass or fail unambiguously.

| Priority | Meaning in this project |
|---|---|
| **Must** | Required for the diploma release; absence means the project aim (DOC-01 §1.5) is not met |
| **Should** | Important, planned for the release; may slip to post-defense if a Must is at risk |
| **Could** | Desirable; implemented only if time remains after all Must/Should items |
| **Won't (this release)** | Explicitly out of scope for the diploma; documented to prevent scope creep |

### 6.1.1 Glossary

| Term | Definition |
|---|---|
| **Text item** | One unit of analysis: a review, comment or appeal, up to 2,000 characters |
| **Emotion label** | One of `joy`, `sadness`, `anger`, `fear`, `surprise`, `neutral` |
| **Polarity** | Derived label `positive` / `negative` / `neutral` (mapping in FR-03) |
| **Language tag** | `kk` (Kazakh), `ru` (Russian) or `mixed` (both languages in one item) |
| **Batch** | A file of text items submitted for asynchronous analysis |
| **Analyst** | Web-UI user who uploads batches and reads reports |
| **Admin** | User who manages accounts, API keys and views system status |
| **Integrator** | External system calling the REST API with an API key |
| **Reference server** | 4 vCPU, 16 GB RAM, no GPU, SSD; the hardware on which NFRs are measured |

### 6.1.2 Actors

| Actor | Interface | Source |
|---|---|---|
| Analyst (support / SMM / quality analyst) | Web UI | Target users, DOC-01 §1.4 |
| Admin | Web UI | Operational need |
| Integrator (CRM, helpdesk, chatbot) | REST API + API key | H6 |
| ML engineer | Training pipeline (CLI) | O3–O5 |

## 6.2 Functional requirements — summary

| ID | Requirement | Priority | Evidence | Objective |
|---|---|---|---|---|
| FR-01 | Analyse a single text and return its emotion | Must | H4, DOC-04 gap 1 | O5, O7 |
| FR-02 | Identify the language of each text (`kk` / `ru` / `mixed`) | Must | H1, S15, S19 | O4 |
| FR-03 | Return class probabilities and derived polarity | Must | H4 | O5 |
| FR-04 | Validate input and return structured errors | Must | Engineering practice | O7 |
| FR-05 | Upload a batch file (CSV, XLSX, TXT) | Must | H5 [A] | O7 |
| FR-06 | Map file columns (text, optional date, optional channel) | Should | H5 [A] | O7 |
| FR-07 | Process batches asynchronously with status and progress | Must | H5, DD2 | O7 |
| FR-08 | Retrieve batch results with filtering and pagination | Must | H5 | O7 |
| FR-09 | Compute aggregated statistics per batch | Must | H5 | O7, O9 |
| FR-10 | Show emotion trend over time when dates are provided | Should | Interview guide Q7 [A] | O9 |
| FR-11 | Provide a web dashboard with charts | Must | DOC-04 gap 3 | O9 |
| FR-12 | Export batch results and report (CSV; PDF) | Must (CSV) / Could (PDF) | H5 [A] | O9 |
| FR-13 | Show representative example texts per emotion | Should | H4 [A] | O9 |
| FR-14 | Authenticate API calls with API keys | Must | H6, C7 | O7 |
| FR-15 | Authenticate web users; roles Analyst / Admin | Must (login) / Should (roles) | Privacy constraints [A] | O9 |
| FR-16 | List and delete own batches | Should | Privacy, retention | O8 |
| FR-17 | Admin: manage API keys and users | Should | Operations | O7 |
| FR-18 | Health check and model information endpoints | Must | DD5, ops | O10 |
| FR-19 | Allow analysts to correct a predicted label | Could | Active-learning idea | O3 |
| FR-20 | Multi-label emotion output | Won't (stretch goal) | S7, S10 | — |
| FR-21 | Real-time ingestion from social networks | Won't | Out of scope, DOC-01 §1.8 | — |
| FR-22 | Aspect-based emotion per product feature | Won't | Out of scope | — |

## 6.3 Functional requirements — detailed specification with acceptance criteria

### FR-01 Single-text emotion analysis — **Must**

The system shall accept one text via `POST /api/v1/analyze` and return the predicted emotion label.

| AC | Criterion |
|---|---|
| AC-01.1 | **Given** a valid API key and a JSON body with a non-empty `text` (1–2,000 characters), **when** the request is sent, **then** the response has HTTP 200 and contains `emotion` ∈ {joy, sadness, anger, fear, surprise, neutral}. |
| AC-01.2 | The response contains `model_version` equal to the version reported by `GET /api/v1/model` (FR-18). |
| AC-01.3 | Identical input sent twice to the same model version returns identical `emotion` and probabilities (deterministic inference). |
| AC-01.4 | Texts longer than the model's maximum sequence length (512 subword tokens) are truncated and the response contains `"truncated": true`. |
| AC-01.5 | By default the text itself is **not** persisted; only request metadata (time, key ID, language, label, latency) is logged. With `"store": true` the item is persisted (privacy, NFR-09). |

### FR-02 Language identification — **Must**

| AC | Criterion |
|---|---|
| AC-02.1 | Every analysed item (single or batch) has `language` ∈ {kk, ru, mixed}. |
| AC-02.2 | An item is tagged `mixed` when it contains at least two tokens identified as Kazakh and at least two identified as Russian (token-level rule documented in `ml/src/preprocessing/README.md`). |
| AC-02.3 | On the labelled test set, language-tag accuracy is **≥ 95 %** for `kk` and `ru` items and **≥ 85 %** for `mixed` items (measured by TC-ML-07, DOC-09). |
| AC-02.4 | Kazakh-specific Cyrillic letters (ә, ғ, қ, ң, ө, ұ, ү, һ, і) are preserved through preprocessing; a unit test asserts that normalisation does not replace them with Russian look-alikes. |

### FR-03 Probabilities and derived polarity — **Must**

Polarity is derived from the emotion label by a fixed, documented mapping:

| Emotion | joy | sadness | anger | fear | surprise | neutral |
|---|---|---|---|---|---|---|
| **Polarity** | positive | negative | negative | negative | neutral | neutral |

*Surprise is mapped to `neutral` because it can be positive or negative; this is a known simplification recorded as a limitation.*

| AC | Criterion |
|---|---|
| AC-03.1 | The response contains `probabilities` with exactly six keys (all labels); each value is in [0, 1] and their sum is 1 ± 0.001. |
| AC-03.2 | `emotion` equals the arg-max of `probabilities`; `confidence` equals that maximum value. |
| AC-03.3 | `polarity` follows the mapping table above for 100 % of responses (unit test over all six labels). |

### FR-04 Input validation and error handling — **Must**

| AC | Criterion |
|---|---|
| AC-04.1 | Empty or whitespace-only text → HTTP 422 with error code `TEXT_EMPTY`. |
| AC-04.2 | Text longer than 2,000 characters → HTTP 422 with code `TEXT_TOO_LONG`. |
| AC-04.3 | Missing or invalid API key → HTTP 401 with code `UNAUTHORIZED`; the response does not reveal whether the key exists. |
| AC-04.4 | All error responses follow one schema: `{ "error": { "code", "message", "details" } }`, documented in `docs/api/openapi.yaml`. |
| AC-04.5 | ML-service unavailability → HTTP 503 with code `MODEL_UNAVAILABLE` within 5 s (timeout), never an unhandled 500. |

### FR-05 Batch file upload — **Must**

| AC | Criterion |
|---|---|
| AC-05.1 | `POST /api/v1/batches` (multipart) accepts `.csv` (UTF-8, comma or semicolon), `.xlsx` (first sheet) and `.txt` (UTF-8, one item per line); response HTTP 202 with `batch_id` and status `queued`. |
| AC-05.2 | Files larger than **10 MB** or with more than **50,000** items are rejected with HTTP 413 / code `BATCH_TOO_LARGE` before processing starts. |
| AC-05.3 | Unsupported extensions or undecodable encodings → HTTP 415 / code `UNSUPPORTED_FILE`. |
| AC-05.4 | Empty rows are skipped and counted in `skipped_count`; rows longer than 2,000 characters are truncated and counted in `truncated_count`. |
| AC-05.5 | The same upload is available in the web UI via drag-and-drop with a visible list of accepted formats and limits (UI walkthrough, DOC-08). |

### FR-06 Column mapping — **Should**

| AC | Criterion |
|---|---|
| AC-06.1 | For CSV/XLSX the user can specify `text_column` (required), `date_column` and `channel_column` (optional) by header name. |
| AC-06.2 | If `text_column` is not specified, the system auto-selects a column named `text`, `review`, `comment`, `отзыв`, `пікір` (case-insensitive) or returns HTTP 422 / `TEXT_COLUMN_NOT_FOUND` listing the available headers. |
| AC-06.3 | Dates in ISO-8601, `DD.MM.YYYY` and `DD.MM.YYYY HH:MM` are parsed; unparseable dates are stored as null and counted in `invalid_date_count`. |

### FR-07 Asynchronous processing, status and progress — **Must**

| AC | Criterion |
|---|---|
| AC-07.1 | `GET /api/v1/batches/{id}` returns `status` ∈ {queued, processing, completed, failed, cancelled} and `progress` = processed / total items (0–100 %). |
| AC-07.2 | Status transitions follow the state machine in DOC-07 §7.7; any other transition is rejected (unit test of the state model). |
| AC-07.3 | Uploading a batch never blocks `POST /analyze`: during processing of a 10,000-item batch, single-text p95 latency still meets NFR-01. |
| AC-07.4 | If the ML service fails mid-batch, the chunk is retried up to 3 times; after that the batch becomes `failed` with `error_message`, and already processed items remain retrievable. |
| AC-07.5 | The web UI refreshes progress at least every 3 s without reloading the page. |

### FR-08 Batch results — **Must**

| AC | Criterion |
|---|---|
| AC-08.1 | `GET /api/v1/batches/{id}/items` returns items with `text`, `emotion`, `polarity`, `language`, `confidence`, `date`, `channel`. |
| AC-08.2 | Supports filters `emotion`, `language`, `polarity`, `min_confidence`, and pagination `page`, `page_size` (max 200). |
| AC-08.3 | The number of returned items across all pages equals `total_count − skipped_count`. |
| AC-08.4 | A user can access only batches they own (Analyst) or any batch (Admin); otherwise HTTP 404. |

### FR-09 Aggregated statistics — **Must**

| AC | Criterion |
|---|---|
| AC-09.1 | `GET /api/v1/batches/{id}/stats` returns counts and percentages per emotion, per polarity, per language, and an emotion × language cross-table. |
| AC-09.2 | Counts sum to the number of analysed items; percentages sum to 100 ± 0.1 (integration test on a fixture file with known labels). |
| AC-09.3 | For a completed 50,000-item batch the endpoint responds in **≤ 1 s** (pre-aggregated statistics, NFR-03). |

### FR-10 Emotion trend over time — **Should**

| AC | Criterion |
|---|---|
| AC-10.1 | If a date column was mapped, stats include `timeline`: counts per emotion per day, week or month (`granularity` parameter). |
| AC-10.2 | If no dates exist, `timeline` is absent and the UI hides the trend chart with an explanatory message. |

### FR-11 Web dashboard — **Must**

| AC | Criterion |
|---|---|
| AC-11.1 | For a completed batch the dashboard shows at minimum: emotion distribution (bar or donut), polarity share, language share, and a filterable table of items. |
| AC-11.2 | Clicking a chart segment filters the item table to that category. |
| AC-11.3 | All UI text is available in Russian and English; Kazakh UI localisation is Could. |
| AC-11.4 | Two target-user representatives complete the scenario "upload file → open dashboard → find angry Kazakh reviews" without assistance in ≤ 5 minutes (usability walkthrough, DOC-09). |

### FR-12 Export — **Must (CSV) / Could (PDF)**

| AC | Criterion |
|---|---|
| AC-12.1 | `GET /api/v1/batches/{id}/export?format=csv` returns the original columns plus `emotion`, `polarity`, `language`, `confidence`, UTF-8 with BOM so Excel shows Kazakh characters correctly. |
| AC-12.2 | Exported row count equals analysed item count. |
| AC-12.3 *(Could)* | `format=pdf` produces a report with batch metadata, charts from FR-11 and top examples from FR-13. |

### FR-13 Representative examples — **Should**

| AC | Criterion |
|---|---|
| AC-13.1 | For each emotion, the dashboard lists up to 5 items with the highest confidence. |
| AC-13.2 | Examples respect active filters (e.g., language = kk). |

### FR-14 API-key authentication — **Must**

| AC | Criterion |
|---|---|
| AC-14.1 | All `/api/v1/*` endpoints except `/health` require header `X-API-Key` or a valid web session. |
| AC-14.2 | Keys are stored only as salted hashes; the plaintext key is shown once at creation. |
| AC-14.3 | A revoked key is rejected within 1 minute of revocation. |
| AC-14.4 | Per-key rate limit (default 60 requests/min for `/analyze`) returns HTTP 429 with `Retry-After` when exceeded. |

### FR-15 Web authentication and roles — **Must (login) / Should (roles)**

| AC | Criterion |
|---|---|
| AC-15.1 | Users log in with e-mail and password; passwords are hashed with bcrypt or Argon2. |
| AC-15.2 | Sessions expire after 8 hours of inactivity. |
| AC-15.3 *(Should)* | Analyst cannot access admin pages or other users' batches (HTTP 403/404); Admin can. |

### FR-16 Batch history and deletion — **Should**

| AC | Criterion |
|---|---|
| AC-16.1 | The user sees a list of own batches with name, date, item count, status. |
| AC-16.2 | Deleting a batch removes its file, items, predictions and statistics; subsequent requests return 404. |
| AC-16.3 | Batches older than the retention period (default 30 days, configurable) are deleted automatically by a scheduled job. |

### FR-17 Administration — **Should**

| AC | Criterion |
|---|---|
| AC-17.1 | Admin can create, list and revoke API keys and user accounts via UI and API. |
| AC-17.2 | Admin sees system status: model version, queue length, number of batches processed in the last 24 h. |

### FR-18 Health and model information — **Must**

| AC | Criterion |
|---|---|
| AC-18.1 | `GET /api/v1/health` returns 200 with status of database, broker and ML service (`ok` / `degraded`). |
| AC-18.2 | `GET /api/v1/model` returns model name, version, training date, label set and evaluation summary (Macro-F1 per slice). |

### FR-19 Label correction — **Could**

| AC | Criterion |
|---|---|
| AC-19.1 | An analyst can change the label of an item; the original prediction and the correction are both stored with user ID and timestamp. |
| AC-19.2 | Corrections can be exported as a CSV usable as additional training data (MLR-01). |

## 6.4 Requirements for the ML pipeline (MLR)

| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| MLR-01 | **Reproducible training** from a YAML config | Must | Running the training command twice with the same config and seed produces Macro-F1 within ± 0.01; config, seed, data version and git commit are saved with the model. |
| MLR-02 | **Annotated corpus** with documented guidelines | Must | Guidelines in `ml/annotation/guidelines.md` with ≥ 3 examples per label per language slice; ≥ 15 % of items double-annotated; Cohen's κ reported (target ≥ 0.60, assumption AS-6). |
| MLR-03 | **Stratified splits** | Must | Train/validation/test split 70/15/15 stratified by label × language slice; no duplicate or near-duplicate texts (cosine similarity of char n-grams > 0.95) across splits. |
| MLR-04 | **Test set composition** | Must | Test set contains each slice (kk, ru, mixed) with ≥ 300 items, and each label with ≥ 30 items per slice where data permits; exact counts published in the evaluation report. |
| MLR-05 | **Per-slice evaluation report** | Must | Report contains Macro-F1, per-class Precision/Recall/F1 and confusion matrices separately for kk, ru, mixed and overall, for every model in the grid (DOC-05 §5.5). |
| MLR-06 | **Quality target** | Must | Fine-tuned primary model's Macro-F1 exceeds the TF-IDF baseline on **each** slice; the difference is statistically significant (paired bootstrap, p < 0.05). *Absolute target (e.g., Macro-F1 ≥ 0.60) to be fixed after the pilot experiment — DIP-23.* |
| MLR-07 | **Model export and versioning** | Must | Model saved with semantic version (`emotion-xlmr-kkru-vX.Y.Z`), label map and tokenizer; inference service loads it by version from configuration. |
| MLR-08 | **Data provenance and licences** | Must | `ml/data/README.md` lists every source with licence (e.g., CC BY 4.0 for KazSAnDRA) and how texts were anonymised. |

## 6.5 Non-functional requirements

Measured on the **reference server** (§6.1.1) unless stated otherwise. Performance targets are initial engineering estimates and will be **re-baselined after the first inference benchmark (DIP-26)**; any change is recorded in DOC-11.

| ID | Category | Requirement | Priority | Acceptance criterion / measurement |
|---|---|---|---|---|
| NFR-01 | Performance | Single-text latency | Must | p95 of `POST /analyze` ≤ **1,000 ms** for texts ≤ 500 characters at 5 concurrent clients over 5 minutes (Locust, TC-LOAD-01). |
| NFR-02 | Performance | Batch throughput | Must | A 10,000-item batch (mean 150 characters) completes in ≤ **15 minutes** on CPU (≈ 11 items/s); ≤ 3 minutes on a single GPU if available (TC-LOAD-02). |
| NFR-03 | Performance | Dashboard responsiveness | Must | Stats and first page of items for a 50,000-item batch load in ≤ 1 s (server time) and ≤ 3 s in the browser. |
| NFR-04 | Scalability | Concurrent batches | Should | Three 10,000-item batches submitted simultaneously all complete; no item is lost or processed twice (TC-LOAD-03). |
| NFR-05 | Reliability | Fault tolerance | Must | Killing the ML-service container during a batch leads to automatic retry and successful completion after restart, with no duplicate predictions (TC-INT-09). |
| NFR-06 | Availability | Service availability | Could | Not critical for a diploma prototype; health endpoint and Docker restart policy `unless-stopped` are sufficient. |
| NFR-07 | Security | Transport and secrets | Must | All external traffic over HTTPS via reverse proxy; secrets only in environment variables; `.env` excluded from Git (verified by `.gitignore` and a CI secret scan). |
| NFR-08 | Security | OWASP basics | Must | No findings of severity High in an automated scan (e.g., OWASP ZAP baseline) of the API; SQL access only through the ORM / parameterised queries. |
| NFR-09 | Privacy | Data minimisation and retention | Must | Single texts not stored by default (AC-01.5); batches deleted after retention period (AC-16.3); logs contain no full texts. |
| NFR-10 | Maintainability | Code quality | Must | Backend and ML-service unit-test line coverage ≥ **70 %**; linters (ruff, eslint) pass in CI on every PR. |
| NFR-11 | Maintainability | API contract | Must | `docs/api/openapi.yaml` is generated from code; a CI step fails if the committed contract differs from the generated one. |
| NFR-12 | Portability | Deployment | Must | `docker compose up` on a clean Linux host with Docker installed starts the full stack in ≤ 10 minutes (excluding model download); documented in README. |
| NFR-13 | Usability | Learnability | Should | See AC-11.4; System Usability Scale (SUS) score ≥ 68 from ≥ 3 test users. |
| NFR-14 | Usability | Localisation | Must | UI and error messages in Russian and English; correct rendering of all Kazakh Cyrillic letters in UI, exports and PDFs. |
| NFR-15 | Observability | Logging and metrics | Should | Structured JSON logs with request ID; per-endpoint latency and error counters exposed at `/metrics`. |
| NFR-16 | Robustness | Informal text | Must | Model quality on the *informal* subset of the test set (slang, transliteration, typos — tagged during annotation) is reported separately; Macro-F1 drop vs. formal subset is documented (H7). |
| NFR-17 | Ethics / transparency | Model card | Must | A model card states intended use, label set, training data, per-slice metrics, known limitations (sarcasm, surprise mapping, domain shift). |

## 6.6 Constraints and assumptions

| ID | Constraint / assumption | Impact |
|---|---|---|
| CON-1 | Team of two; ≈ 8 months to final defense | Strict MoSCoW; Won't list enforced |
| CON-2 | No guaranteed GPU in production; training on a single Colab-class or university GPU | XLM-R-base, not large, as default (DOC-05 TD-4); CPU-oriented NFRs |
| CON-3 | Only open-licence datasets and anonymised own data | MLR-08 |
| CON-4 | Self-hosted, no mandatory cloud services | DD5, NFR-12 |
| AS-4, AS-5, AS-6 | Inherited from DOC-02 | FR-05, FR-06, FR-10, FR-12, FR-13, MLR-02 marked [A] until interviews confirm |

## 6.7 Traceability matrix (requirements → design → verification → work)

Test IDs are defined in DOC-09; DIP tasks are defined in DOC-10. The matrix is the single place where a reviewer can check that every Must requirement is designed, tested and planned.

| Req. | Evidence | Objective | Component (DOC-07) | Data entity | Test(s) (DOC-09) | DIP task(s) |
|---|---|---|---|---|---|---|
| FR-01 | H4 | O5, O7 | API Gateway → Analysis Service → ML Client → Inference API | analysis_log | TC-UNIT-01, TC-INT-01, TC-LOAD-01 | DIP-26, DIP-31 |
| FR-02 | H1, S19 | O4 | ML inference service (Preprocessor, Language Identifier) | prediction.language | TC-UNIT-05, TC-ML-07 | DIP-21 |
| FR-03 | H4 | O5 | ML inference service (Emotion Classifier) | prediction | TC-UNIT-02, TC-UNIT-03 | DIP-26 |
| FR-04 | — | O7 | API Gateway (validation, error handler) | — | TC-UNIT-04, TC-INT-02 | DIP-31 |
| FR-05 | H5 | O7 | Batch Service, File storage, File Parser | batch, batch_item | TC-INT-03, TC-INT-04 | DIP-32 |
| FR-06 | H5 | O7 | Batch Service (header check), File Parser | batch.column_map | TC-UNIT-06 | DIP-32 |
| FR-07 | H5, DD2 | O7 | Batch Service, Batch Processing Task, Redis broker | batch.status | TC-UNIT-07, TC-INT-05, TC-INT-09 | DIP-33 |
| FR-08 | H5 | O7 | Results & Statistics Service | prediction | TC-INT-06 | DIP-34 |
| FR-09 | H5 | O7, O9 | Aggregator (write), Results & Statistics Service (read) | batch_stats | TC-INT-07 | DIP-34 |
| FR-10 | [A] | O9 | Results & Statistics Service | batch_item.item_date | TC-INT-08 | DIP-34 |
| FR-11 | Gap 3 | O9 | Web UI (Dashboard) | — | TC-E2E-01, TC-USE-01 | DIP-37 |
| FR-12 | H5 | O9 | Report Service | — | TC-INT-10 | DIP-38 |
| FR-13 | H4 | O9 | Results & Statistics Service, Web UI | prediction.confidence | TC-INT-11 | DIP-37 |
| FR-14 | H6 | O7 | Auth Module | api_key | TC-UNIT-08, TC-INT-12 | DIP-35 |
| FR-15 | — | O9 | Auth Module, Web UI | app_user | TC-INT-13 | DIP-35 |
| FR-16 | NFR-09 | O8 | Batch Service, Scheduler | batch | TC-INT-14 | DIP-33 |
| FR-17 | — | O7 | Auth Module (admin endpoints), Web UI admin pages | api_key, app_user | TC-INT-15 | DIP-35 |
| FR-18 | DD5 | O10 | API Gateway, Inference API, Model Loader | model_version | TC-INT-16 | DIP-26, DIP-31 |
| FR-19 | — | O3 | Results & Statistics Service, Web UI | label_feedback | TC-INT-17 | DIP-41 |
| MLR-01…08 | S4, S12, S15 | O3–O5 | Training pipeline (offline, DOC-07 §7.11) | model_version | TC-ML-01…TC-ML-08 | DIP-20…DIP-25 |
| NFR-01…05 | DD2, DD8 | O10 | Whole system | — | TC-LOAD-01…03, TC-INT-09 | DIP-40 |
| NFR-07…12 | C7, DD5 | O10 | Deployment, CI | — | TC-SEC-01, TC-CI-01 | DIP-39 |

## 6.8 Requirements change control

1. A change is proposed as a YouTrack issue of type *Requirement Change* referencing the requirement ID.
2. The impact on design, tests and schedule is assessed by both team members.
3. Changes to Must requirements or acceptance criteria are discussed with the supervisor and recorded in DOC-11.
4. This document's version is incremented and the change is listed below.

| Version | Date | Change | Reason |
|---|---|---|---|
| 1.0 | 20.10.2026 | Initial specification | Pre-defense-1 |
