# 9. Verification and Evaluation Plan

**Document ID:** DOC-09 · **Version:** 1.0 (draft for pre-defense-1) · **Date:** 20.10.2026
**YouTrack:** DIP-14 · **Owner:** Nurgaly Ashkenov (ML evaluation, §9.4), Ulan Orazbek (software testing, §9.3, §9.5–§9.7) · **Reviewer:** K. Tanyrbergenova
**Related:** DOC-01 §1.10 (success criteria), DOC-06 (FR / NFR / MLR and AC), DOC-07 (components), DOC-08 (API contract)

---

## 9.1 What has to be proven

The project aim (DOC-01 §1.5) is achieved when **two claims** are demonstrated with evidence:

| Claim | Proven by | Pass condition |
|---|---|---|
| **C1. The model identifies emotions in Kazakh, Russian and mixed texts better than a simple baseline.** | ML evaluation (§9.4) on a held-out, stratified test set | MLR-06: fine-tuned model Macro-F1 > TF-IDF baseline on **each** of kk, ru, mixed, with paired bootstrap p < 0.05 |
| **C2. The system makes this capability usable by organisations through an API and an analytics interface.** | Software tests (§9.3), load tests (§9.5), usability test (§9.6) | All Must acceptance criteria pass; NFR-01/02/03 met on the reference server; ≥ 2 target users complete the main scenario unaided |

Every test below has an ID that appears in the traceability matrix of DOC-06 §6.7, so a reviewer can follow any requirement to the test that verifies it and, later, to its result.

## 9.2 Strategy and test levels

| Level | Scope | Tools | Runs | Owner | Exit criterion |
|---|---|---|---|---|---|
| Static checks | Lint, types, secrets, OpenAPI drift | ruff, mypy, eslint, gitleaks, `scripts/check_openapi.py` | Every PR (CI) | Both | 0 errors |
| **Unit** | Functions and classes in isolation (no network, no DB) | pytest, vitest | Every PR (CI) | Both | 100 % pass; line coverage ≥ 70 % (NFR-10) |
| **Integration** | API + PostgreSQL + Redis + worker, ML service **mocked** or real small model | pytest, httpx, testcontainers / Docker Compose | Every PR to `develop` | Ulan | 100 % of Must AC tests pass |
| End-to-end | Browser through the full stack | Playwright | Nightly + before each milestone | Ulan | Main flows pass |
| **ML evaluation** | Models on fixed test splits | scikit-learn, Hugging Face `evaluate`, own scripts | Each experiment; final run before defense | Nurgaly | MLR-05, MLR-06 |
| **Load / performance** | Latency and throughput on the reference server | Locust | Milestones (pre-defense-2, final) | Ulan | NFR-01–NFR-05 |
| Security | Basic dynamic scan, dependency audit | OWASP ZAP baseline, pip-audit, npm audit | Milestones | Ulan | No High findings (NFR-08) |
| Usability | Real target users on the working UI | Moderated sessions, SUS questionnaire | Apr 2027 | Both | AC-11.4, NFR-13 |

**Test doubles.** A deterministic **ML-service stub** (DIP-27) implements the internal contract (DOC-07 §7.5.1) and returns fixed predictions by keyword. It allows backend and UI tests to run in CI without a GPU and to start before the real model exists.

**Test data.** Small fixture files in `backend/tests/fixtures/` (committed, no personal data):

| Fixture | Content | Used by |
|---|---|---|
| `batch_small.csv` | 30 rows, kk/ru/mixed, with known stub labels, dates, one empty row, one 2,500-char row | TC-INT-03, -05…-08, -10 |
| `batch_semicolon.csv`, `batch.xlsx`, `batch.txt` | Same rows in other formats | TC-INT-03 |
| `batch_cp1251.csv`, `report.docx` | Wrong encoding / type | TC-INT-04 |
| `batch_11mb.csv` (generated at test time) | Size limit | TC-INT-04 |
| `batch_10k.csv` (generated) | 10,000 rows, mean 150 chars | TC-LOAD-02, -03 |

## 9.3 Software test cases

### 9.3.1 Unit tests

| ID | Verifies | Test idea | Expected result |
|---|---|---|---|
| TC-UNIT-01 | FR-01 (AC-01.3, AC-01.4) | Classifier wrapper: same input twice; input of 600 tokens | Identical output; `truncated = true` for long input |
| TC-UNIT-02 | FR-03 (AC-03.1, AC-03.2) | Softmax post-processing on random logits (property-based, 1,000 cases) | 6 keys, values in [0, 1], sum = 1 ± 0.001, `emotion` = arg-max, `confidence` = max |
| TC-UNIT-03 | FR-03 (AC-03.3) | Polarity mapping for all six labels | Matches table in FR-03 |
| TC-UNIT-04 | FR-04 (AC-04.1, AC-04.2, AC-04.4) | Pydantic request models: `""`, `"   "`, 2,000 and 2,001 chars | 422 with `TEXT_EMPTY` / `TEXT_TOO_LONG`; 2,000 chars accepted; error envelope schema valid |
| TC-UNIT-05 | FR-02 (AC-02.2, AC-02.4) | Preprocessor and language identifier on hand-written examples, incl. `ә ғ қ ң ө ұ ү һ і` | Kazakh letters preserved; rule for `mixed` applied as documented |
| TC-UNIT-06 | FR-05, FR-06 (AC-05.4, AC-06.2, AC-06.3) | File Parser: auto-detect text column (`review`, `отзыв`, `пікір`), date formats, empty and long rows | Correct column; dates parsed or counted invalid; counters correct |
| TC-UNIT-07 | FR-07 (AC-07.2) | Batch state machine: every pair (from, to) | Only transitions of DOC-07 §7.7 allowed; others raise `InvalidStateTransition` |
| TC-UNIT-08 | FR-14 (AC-14.2, AC-14.4) | Key hashing and verification; token-bucket limiter | Plain key never stored; 61st request in a minute rejected |

### 9.3.2 Integration tests

Each test runs against the Compose stack (`docker compose -f docker-compose.test.yml`) with the ML stub unless stated otherwise.

| ID | Verifies | Steps | Expected result |
|---|---|---|---|
| TC-INT-01 | FR-01, AC-01.1, AC-01.2, AC-01.5 | `POST /analyze` with kk, ru and mixed texts; then query `analysis_log` | 200; response valid against `AnalyzeResponse`; `model_version` = `/model`; text **not** stored unless `store = true` |
| TC-INT-02 | FR-04, AC-04.3, AC-04.5 | No key; wrong key; stop ML stub and call `/analyze` | 401 with identical body for both key cases; 503 `MODEL_UNAVAILABLE` within 5 s |
| TC-INT-03 | FR-05, AC-05.1 | Upload `batch_small` as CSV (`,` and `;`), XLSX, TXT | 202, status `queued`; all four end `completed` with the same predictions |
| TC-INT-04 | FR-05, AC-05.2, AC-05.3 | Upload 11 MB file; `.docx`; CP-1251 CSV | 413 `BATCH_TOO_LARGE`; 415 `UNSUPPORTED_FILE` ×2; no batch row created |
| TC-INT-05 | FR-07, AC-07.1, AC-07.3 | Upload batch, poll status; in parallel call `/analyze` | Status sequence `queued → processing → completed`; `progress` monotonic, ends at 100; `/analyze` keeps working |
| TC-INT-06 | FR-08, AC-08.1–AC-08.4 | Filters `emotion`, `language`, `min_confidence`; pagination; second user requests the batch | Only matching items; page sizes correct; Σ pages = `total_count − skipped_count`; other user gets 404 |
| TC-INT-07 | FR-09, AC-09.1, AC-09.2 | Stats of `batch_small` against hand-computed expected values | Counts and percentages equal expected; percent sums 100 ± 0.1 |
| TC-INT-08 | FR-10, AC-10.1, AC-10.2 | Batch with and without `date_column`; `granularity` day/week/month | `timeline` correct when dates exist, absent otherwise |
| TC-INT-09 | FR-07 AC-07.4, **NFR-05** | During a batch, kill the ML container for 20 s, then restart | Chunks retried; batch `completed`; `COUNT(prediction) = COUNT(item)` (no duplicates, no gaps). Second variant: ML down > 3 retries → `failed` with `error_message`, partial items readable |
| TC-INT-10 | FR-12, AC-12.1, AC-12.2 | Export CSV; open with Python `csv` and check BOM; cell starting with `=` | Rows = analysed items; BOM present; Kazakh letters intact; `=` cell escaped |
| TC-INT-11 | FR-13 | Stats `top_examples` vs. items sorted by confidence | ≤ 5 per emotion, highest confidence, respect language filter |
| TC-INT-12 | FR-14, AC-14.1, AC-14.3, AC-14.4 | All endpoints without auth; revoke key and retry after 60 s; 61 requests/min | 401 (except `/health`); revoked key rejected; 429 + `Retry-After` |
| TC-INT-13 | FR-15, AC-15.1–AC-15.3 | Login, session expiry (clock shift 8 h), analyst calls admin endpoint | Session cookie flags set; expired session → 401; analyst → 403 |
| TC-INT-14 | FR-16, AC-16.2, AC-16.3 | Delete batch; set `expires_at` in the past and run retention job | File, items, predictions, stats removed; subsequent GET 404 |
| TC-INT-15 | FR-17 | Admin creates, lists, revokes keys and users | Secret shown once; list shows prefix only |
| TC-INT-16 | FR-18 | `/health` with all services up and with Redis stopped; `/model` | `ok` / `degraded` correctly; model info has label set and metrics |
| TC-INT-17 | FR-19 (Could) | Correct label, then read item and export corrections | `corrected_emotion` set; original prediction unchanged |

### 9.3.3 End-to-end, contract and other tests

| ID | Verifies | Description | Expected result |
|---|---|---|---|
| TC-E2E-01 | FR-11, AC-11.1, AC-11.2, AC-07.5 | Playwright: login → upload `batch_small.csv` → wait for completion → dashboard → click "anger" → table filtered → export | All widgets present; filter applied; file downloaded |
| TC-CI-01 | NFR-10, NFR-11, NFR-07 | CI pipeline: lint, tests with coverage, `openapi.yaml` regenerated and diffed, gitleaks | Pipeline fails on coverage < 70 %, contract drift or a committed secret |
| TC-SEC-01 | NFR-07, NFR-08 | OWASP ZAP baseline scan of the API behind Nginx; pip-audit / npm audit | No High findings; HTTPS enforced; no known critical CVEs in dependencies |

## 9.4 ML evaluation plan

### 9.4.1 Data and splits

| Element | Definition |
|---|---|
| Corpus | Re-annotated KazSAnDRA subset (kk), CEDR (ru, labels mapped: *no emotion* → `neutral`), own annotated public sample (kk / ru / mixed) — DOC-03 §3.3.3 |
| Language slices | `kk`, `ru`, `mixed`, assigned during annotation (gold), not by the model |
| Additional slices | `informal` (slang / transliteration / typos, tagged by annotators), `formal` (NFR-16); `domain=reviews` vs. `domain=social` |
| Split | 70 / 15 / 15, stratified by label × language slice, fixed seed, near-duplicates removed across splits (MLR-03) |
| Test set size | ≥ 300 items per language slice, ≥ 30 per label per slice where data permits; exact counts published (MLR-04) |
| Leakage control | CEDR has an official test split — kept as part of the ru test set; texts from the same review thread are kept in the same split |
| Freeze | Test set is frozen and hashed (SHA-256 in `ml/reports/test_set.sha256`) before the first experiment; it is not used for model selection |

### 9.4.2 Metrics

| Metric | Why | Reported for |
|---|---|---|
| **Macro-F1** (primary) | Classes are imbalanced (neutral and joy dominate in reviews; fear is rare); macro averaging gives every emotion equal weight, as in S7, S10, S12 | Each slice and overall |
| Per-class Precision, Recall, F1 | Shows which emotions are confused (e.g., anger vs. sadness) | Each slice |
| Confusion matrix (normalised by row) | Error analysis | Each slice |
| Weighted-F1 and accuracy | Comparability with other papers; secondary only | Overall |
| Polarity Macro-F1 (derived 3-class) | Comparability with KazSAnDRA-style polarity results (S15) | kk slice |
| Language-ID accuracy | AC-02.3 | kk, ru, mixed |
| Expected Calibration Error (ECE) | Confidence is shown to users; it should be meaningful | Overall |
| Inference latency p50 / p95, model size | Link to NFR-01, NFR-02 | CPU and GPU |

**Statistical testing.** Differences between the primary model and each baseline are tested with a **paired bootstrap** on the test set (10,000 resamples), reporting the 95 % confidence interval of ΔMacro-F1 and the p-value. Each fine-tuned model is trained with **3 random seeds**; mean ± standard deviation are reported.

### 9.4.3 Baselines and compared models

| Model | Type | Role | Notes |
|---|---|---|---|
| Majority class | Trivial | Sanity floor | Any model must beat it clearly |
| TF-IDF (char 2–5-grams) + Logistic Regression | Classical | **Reference baseline for MLR-06** | Char n-grams are robust to Kazakh suffixes and typos |
| mBERT (bert-base-multilingual-cased), fine-tuned | Transformer | Transformer baseline | DOC-05 TD-4 |
| RuBERT-tiny2-CEDR (off-the-shelf) | Transformer | External baseline, **ru slice only** | Labels already match; T4 |
| LLM zero-shot prompt | Generative | Reference only, on ≤ 300 test items, no personal data | Motivated by S10; prompt fixed in `ml/configs/llm_prompt.md` |
| **XLM-R-base, fine-tuned** | Transformer | **Primary model** | DOC-05 TD-4 |
| mDeBERTa-v3-base, fine-tuned | Transformer | Alternative | DOC-05 TD-4 |
| XLM-R-large, fine-tuned | Transformer | Upper bound, if GPU memory allows | — |

### 9.4.4 Measurement conditions

| Condition | Value |
|---|---|
| Training hardware | One NVIDIA GPU with ≥ 16 GB (Colab-class or university server); exact model recorded |
| Inference benchmark hardware | Reference server: 4 vCPU, 16 GB RAM, no GPU (DOC-06 §6.1.1); optional GPU run reported separately |
| Hyper-parameter search | On validation split only; same budget (≤ 12 runs) for each transformer; search space in `ml/configs/` |
| Max sequence length | 256 tokens for training (covers ≈ 99 % of reviews; to be confirmed in EDA), 512 at inference |
| Software | Versions pinned in `ml/requirements.txt`; seeds fixed; run config, git commit and data hash saved with each model (MLR-01) |
| Reporting | One table per slice in `ml/reports/eval_<model>_<date>.md`; summary in `GET /model` (FR-18) and model card (NFR-17) |

### 9.4.5 ML test cases

| ID | Verifies | Check | Pass condition |
|---|---|---|---|
| TC-ML-01 | MLR-01 | Retrain from config with same seed | ΔMacro-F1 ≤ 0.01 |
| TC-ML-02 | MLR-02 | Agreement on the double-annotated subset | Cohen's κ reported; target ≥ 0.60 (AS-6) |
| TC-ML-03 | MLR-03 | Split script: stratification and near-duplicate check | Label × slice proportions within ±2 pp; 0 cross-split duplicates |
| TC-ML-04 | MLR-04 | Test-set composition report | ≥ 300 per slice; counts per label published |
| TC-ML-05 | MLR-05 | Evaluation report generated for every model | All tables and confusion matrices present for kk, ru, mixed, overall |
| TC-ML-06 | MLR-06 | Primary vs. TF-IDF, paired bootstrap | ΔMacro-F1 > 0 with p < 0.05 on each slice |
| TC-ML-07 | FR-02, AC-02.3 | Language-ID accuracy on gold slice tags | ≥ 95 % (kk, ru), ≥ 85 % (mixed) |
| TC-ML-08 | MLR-07, MLR-08, NFR-16, NFR-17 | Exported artefact loads in ML service; model card and data README complete; informal vs. formal gap reported | Service returns predictions; documents complete |

### 9.4.6 Error analysis

After each main experiment, Nurgaly reviews ≥ 100 misclassified test items (stratified by slice) and tags the cause: *sarcasm*, *mixed emotions*, *domain term*, *transliteration*, *annotation error*, *other*. The distribution of causes is reported; annotation errors found here are fixed in train/validation only, never in the frozen test set.

### 9.4.7 Absolute quality target

MLR-06 defines a **relative** target because no published Kazakh text-emotion baseline exists to set an absolute number credibly. For orientation only: CEDR authors report Macro-F1 0.78 for Russian (S12), and the best KazSAnDRA model reaches F1 0.81 for 3-class polarity but 0.39 for 5-class scores (S15). An absolute target (e.g., Macro-F1 ≥ 0.60 on kk) will be fixed after the pilot experiment (DIP-23) and recorded in DOC-11.

## 9.5 Performance and load testing

Tool: **Locust** (`backend/tests/load/`). Environment: reference server, full Docker Compose stack, real XLM-R-base model, warm-up of 1 minute before measuring. Each scenario is run 3 times; the median run is reported.

| ID | Requirement | Scenario | Load profile | Metrics | Pass condition |
|---|---|---|---|---|---|
| TC-LOAD-01 | NFR-01 | `POST /analyze` with texts sampled from the test set (≤ 500 chars) | 5 concurrent users, no think time, 5 min | p50, p95, p99 latency; error rate; per-component timing from logs | p95 ≤ 1,000 ms; errors < 1 % |
| TC-LOAD-02 | NFR-02 | Upload `batch_10k.csv`, measure until `completed` | 1 batch | Total time; items/s; CPU and RAM of ml-service | ≤ 15 min on CPU (≈ 11 items/s) |
| TC-LOAD-03 | NFR-04, AC-07.3 | 3 × `batch_10k.csv` simultaneously + TC-LOAD-01 profile in parallel | Mixed | All batches complete; `COUNT` checks; `/analyze` p95 | No lost or duplicate items; `/analyze` p95 ≤ 1,000 ms |
| (in TC-LOAD-03) | NFR-03 | `GET /stats` and first `GET /items` page on a 50,000-item batch | 10 sequential calls | Server time | ≤ 1 s |

If TC-LOAD-01 or -02 fails, the mitigation sequence from DOC-07 §7.9.1 is applied (ONNX Runtime + INT8 quantisation → distilled model → GPU), and the test is repeated; results of every attempt are kept.

## 9.6 Usability evaluation

| ID | Verifies | Method | Pass condition |
|---|---|---|---|
| TC-USE-01 | AC-11.4, NFR-13 | Moderated sessions with ≥ 3 representatives of target users (preferably interview participants). Tasks: (T1) upload a provided CSV and map columns; (T2) find the share of negative Kazakh reviews; (T3) find three angry mixed-language examples; (T4) export the filtered list. Think-aloud; afterwards SUS questionnaire. | ≥ 2 users complete T1–T4 unaided in ≤ 5 min total; mean SUS ≥ 68; all critical issues logged as DIP tasks |

## 9.7 Entry / exit criteria and reporting

| Milestone | Required evidence |
|---|---|
| **pre-defense-1** (24.10.2026) | This plan; fixtures defined; CI skeleton with lint + empty test suites (TC-CI-01 partially) |
| **pre-defense-2** | All Must unit and integration tests implemented and passing with ML stub; baseline ML results (TF-IDF, mBERT) per slice; first TC-LOAD-01 measurement |
| **final-defense** | Full ML evaluation report (§9.4) for all models with 3 seeds; all Must AC passing with the real model; load tests TC-LOAD-01…03; TC-SEC-01; TC-USE-01 |

**Defect handling.** Every failed test produces a YouTrack issue of type *Bug* linked to the requirement ID and the test ID; severity *Critical* (Must AC fails) blocks the milestone.

**Test report.** Generated per milestone into `docs/reports/test-report-<milestone>.md`: summary per level, list of AC with pass / fail, coverage, load-test charts, ML tables, open defects.

## 9.8 Coverage check

| Requirement group | Covered by |
|---|---|
| FR-01 … FR-19 | TC-UNIT-01…08, TC-INT-01…17, TC-E2E-01 (each FR has ≥ 1 test, see DOC-06 §6.7) |
| MLR-01 … MLR-08 | TC-ML-01…08 |
| NFR-01 … NFR-05 | TC-LOAD-01…03, TC-INT-09 |
| NFR-07, NFR-08 | TC-SEC-01, TC-CI-01 |
| NFR-09 | TC-INT-01, TC-INT-14 |
| NFR-10, NFR-11 | TC-CI-01 |
| NFR-12 | Manual check: fresh VM, `docker compose up`, timed (checklist in `docs/reports/`) |
| NFR-13 | TC-USE-01 |
| NFR-14 | TC-INT-10 (export), visual check of UI and PDF (§8.7) |
| NFR-15 | TC-INT-16 + log inspection in TC-LOAD-01 |
| NFR-16, NFR-17 | TC-ML-08 |
| NFR-06 (Could) | Not tested beyond restart policy |
