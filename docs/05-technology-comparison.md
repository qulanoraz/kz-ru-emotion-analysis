# 5. Technology Comparison

**Document ID:** DOC-05 · **Version:** 1.0 (draft) · **Date:** 20.10.2026
**YouTrack:** DIP-8 · **Owner:** Ulan Orazbek (TD-1…TD-3, TD-5), Nurgaly Ashkenov (TD-4)

---

## 5.1 Method

For each key technical decision (TD) we compare 2–3 realistic alternatives using a **weighted decision matrix**. Criteria are derived from **decision drivers** that trace to the proposal (DOC-01) and draft requirements (formalised in DOC-06). Scores are 1 (poor) – 5 (excellent), assigned jointly by the team with a written rationale; weighted total = Σ(weight × score), maximum 5.00.

### Decision drivers

| ID | Driver | Origin |
|---|---|---|
| DD1 | ML and backend must share a language/ecosystem to minimise integration effort for a 2-person team | Team constraint, O5/O7 |
| DD2 | Batch files of thousands of texts must be processed asynchronously without blocking the API | O7, H5 |
| DD3 | Machine-readable API contract (OpenAPI) for external integrators | O7, H6 |
| DD4 | Aggregation queries for dashboards (counts by emotion, language, date) must be fast | O8, O9 |
| DD5 | Self-hosted deployment on one server via Docker; no mandatory cloud services | Scope, DOC-04 C7 |
| DD6 | Model must cover Kazakh and Russian and handle mixed text | O5, DOC-03 |
| DD7 | Training must fit available compute (single consumer/Colab-class GPU) | Feasibility |
| DD8 | Inference latency acceptable for interactive single-text analysis on CPU or modest GPU | NFR (DOC-06) |
| DD9 | Team familiarity and learning curve within the 8-month timeline | Schedule risk |

## 5.2 TD-1 — Backend framework

| Criterion (driver) | Weight | FastAPI (Python) | Django REST Framework (Python) | Spring Boot (Java) |
|---|---|---|---|---|
| Ecosystem shared with ML (DD1) | 0.25 | 5 | 5 | 2 |
| Async I/O for calls to ML service and job queue (DD2) | 0.20 | 5 | 3 | 4 |
| Automatic OpenAPI generation, typed schemas (DD3) | 0.20 | 5 | 3 | 4 |
| Built-in admin/ORM/auth batteries | 0.10 | 3 | 5 | 4 |
| Performance under concurrent requests | 0.10 | 4 | 3 | 5 |
| Team familiarity / learning curve (DD9) | 0.15 | 4 | 4 | 3 |
| **Weighted total** | 1.00 | **4.60** | 3.80 | 3.45 |

**Rationale.** FastAPI generates an OpenAPI specification directly from Pydantic models, which makes `docs/api/openapi.yaml` a by-product of the code and guarantees contract–implementation consistency. Native `async` fits the I/O-bound pattern (forwarding texts to the ML service, polling jobs). DRF's admin and ORM are attractive but its async support is less mature and OpenAPI needs extra packages. Spring Boot is robust and fast but splits the codebase across Java and Python.

**Decision:** **FastAPI** + SQLAlchemy 2.x + Alembic migrations.
**Trade-off accepted:** no built-in admin panel — admin functions are limited to API endpoints and a minimal admin page in the frontend.

## 5.3 TD-2 — Database management system

| Criterion (driver) | Weight | PostgreSQL | MySQL | MongoDB |
|---|---|---|---|---|
| Relational integrity for batches → items → predictions (DD4) | 0.20 | 5 | 5 | 2 |
| Analytical queries: GROUP BY, window functions, date bucketing (DD4) | 0.25 | 5 | 4 | 3 |
| Semi-structured fields (per-class probabilities, metadata) | 0.15 | 5 (JSONB + GIN index) | 3 (JSON, weaker indexing) | 5 |
| Unicode / Kazakh Cyrillic text handling, full-text search | 0.10 | 5 | 4 | 4 |
| Docker / self-hosted maturity (DD5) | 0.10 | 5 | 5 | 5 |
| Team familiarity (DD9) | 0.20 | 4 | 4 | 3 |
| **Weighted total** | 1.00 | **4.80** | 4.20 | 3.35 |

**Rationale.** The domain is inherently relational (user → batch → text item → prediction → aggregate report). PostgreSQL combines this with JSONB for the variable-shaped probability vectors, window functions and `date_trunc` for time-series dashboards, and materialised views for pre-computed batch statistics. MongoDB would simplify storing documents but weakens joins and aggregate consistency; MySQL is viable but offers weaker JSON indexing.

**Decision:** **PostgreSQL 16**. Redis (see TD-3) is used only as a message broker/cache, not as a system of record.

## 5.4 TD-3 — Interaction between backend and ML model

| Criterion (driver) | Weight | (a) Model embedded in backend process | (b) Separate ML inference microservice over HTTP | (c) (b) + task queue for batches (Celery/Redis) |
|---|---|---|---|---|
| Isolation of heavy inference from API request handling (DD8) | 0.20 | 1 | 4 | 5 |
| Asynchronous batch processing with progress & retries (DD2) | 0.25 | 2 | 3 | 5 |
| Independent scaling / replacement of model version | 0.15 | 1 | 5 | 5 |
| Operational simplicity (number of containers) | 0.15 | 5 | 4 | 3 |
| Clear ownership split between team members | 0.15 | 2 | 5 | 5 |
| Latency for single text (DD8) | 0.10 | 5 | 4 | 4 |
| **Weighted total** | 1.00 | 2.30 | 4.00 | **4.65** |

**Rationale.** Embedding the model makes every API worker load a large transformer, blocks the event loop during inference and couples releases of the model and the API. A separate **inference service** (FastAPI + PyTorch/ONNX Runtime) gives a clean contract between Nurgaly's and Ulan's work. For batches, the backend enqueues a job; workers split the file into chunks, call the inference service with mini-batches, write predictions and update progress — giving retries and status tracking without holding HTTP connections open.

**Decision:** **Option (c)**: synchronous `POST /analyze` → inference service directly; batch jobs via **Celery workers with Redis broker** → inference service in chunks.
**Considered but not selected:** dedicated model servers (e.g., TorchServe, Triton) — powerful but add operational complexity unjustified for one model; gRPC — faster serialisation but loses the simplicity of HTTP/JSON for debugging. Both remain upgrade paths.

## 5.5 TD-4 — Base ML model

| Criterion (driver) | Weight | XLM-RoBERTa-base | mBERT (bert-base-multilingual-cased) | mDeBERTa-v3-base |
|---|---|---|---|---|
| Kazakh & Russian in pre-training data (DD6) | 0.20 | 5 (CC-100, 100 languages) | 3 (Wikipedia; small Kazakh share) | 5 (CC-100) |
| Evidence of cross-lingual / low-resource performance (DD6) | 0.20 | 5 (S4) | 3 (outperformed by XLM-R in S4) | 4 (S5; fewer Kazakh reports) |
| Robustness to informal text (subword tokeniser, web-crawl data) | 0.15 | 5 | 3 | 5 |
| Fine-tuning compute & memory (DD7) | 0.15 | 4 | 4 | 3 (slower training, fp16 instabilities reported by practitioners) |
| Inference speed / size (DD8) | 0.10 | 3 | 4 | 3 |
| Tooling maturity, reference implementations (DD9) | 0.20 | 5 | 5 | 4 |
| **Weighted total** | 1.00 | **4.65** | 3.60 | 4.15 |

**Rationale.** XLM-R was pre-trained on large web-crawled corpora covering both target languages, reports strong cross-lingual transfer (S4), and its SentencePiece vocabulary handles agglutinative suffix chains and noisy spelling better than WordPiece vocabularies built mainly from Wikipedia. mDeBERTa-v3 is a strong challenger and is kept as **an experimental alternative**; mBERT is kept as a **baseline**.

**Decision:** **XLM-RoBERTa-base** as the primary model; XLM-R-large as an upper bound if GPU memory allows.

**Full experimental grid (planned in DOC-09):**

| Model | Role |
|---|---|
| TF-IDF (char n-grams) + Logistic Regression | Classical baseline, robust to morphology |
| mBERT | Transformer baseline |
| RuBERT-tiny2-CEDR (T4) | Off-the-shelf baseline, Russian slice only |
| LLM zero-shot prompting (small sample) | Reference baseline (S10) |
| **XLM-R-base (fine-tuned)** | **Primary model** |
| mDeBERTa-v3-base (fine-tuned) | Alternative |

## 5.6 TD-5 — Frontend (secondary decision)

| Criterion | Weight | React + TypeScript (Vite) + Recharts/ECharts | Vue 3 + TypeScript | Server-rendered templates (Jinja2 + HTMX) |
|---|---|---|---|---|
| Interactive charts and dashboards | 0.30 | 5 | 5 | 3 |
| Typed API client generated from OpenAPI (DD3) | 0.20 | 5 | 4 | 2 |
| Ecosystem / component libraries | 0.20 | 5 | 4 | 3 |
| Simplicity / time to first screen | 0.15 | 3 | 4 | 5 |
| Team familiarity (DD9) | 0.15 | 4 | 3 | 4 |
| **Weighted total** | 1.00 | **4.55** | 4.15 | 3.20 |

**Decision:** **React + TypeScript (Vite)** with a charting library; API client generated from `openapi.yaml`.

## 5.7 Resulting technology stack

| Layer | Choice | Decision |
|---|---|---|
| Backend API | Python 3.11, FastAPI, Pydantic, SQLAlchemy 2.x, Alembic | TD-1 |
| Database | PostgreSQL 16 | TD-2 |
| Async jobs | Celery + Redis | TD-3 |
| ML inference service | FastAPI + PyTorch (ONNX Runtime as optimisation option) | TD-3 |
| ML training | Hugging Face Transformers, Datasets, scikit-learn; experiment configs in YAML | TD-4 |
| Base model | XLM-RoBERTa-base (fine-tuned) | TD-4 |
| Frontend | React, TypeScript, Vite, charting library | TD-5 |
| Testing | pytest, httpx, Locust (load) | DOC-09 |
| Deployment | Docker, Docker Compose; GitHub Actions CI | DD5 |

## 5.8 Decision log

| ID | Decision | Date | Status | Revisit trigger |
|---|---|---|---|---|
| TD-1 | FastAPI | 20.10.2026 | Proposed — awaiting supervisor review | Team cannot meet async/test requirements |
| TD-2 | PostgreSQL | 20.10.2026 | Proposed | — |
| TD-3 | Inference microservice + Celery/Redis | 20.10.2026 | Proposed | Load test shows queue overhead dominates for small files |
| TD-4 | XLM-R-base primary | 20.10.2026 | Proposed | mDeBERTa or mBERT beats XLM-R on Kazakh slice in pilot experiment |
| TD-5 | React + TS | 20.10.2026 | Proposed | — |

Supervisor comments on these decisions are recorded in DOC-11.
