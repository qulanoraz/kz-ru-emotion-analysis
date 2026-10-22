"""Single source of truth for the YouTrack backlog (DOC-10).

Generates:
  docs/pm/backlog.csv          — import file for YouTrack (or reference for manual creation)
  docs/pm/backlog-tables.md    — tables to paste into DOC-10 §10.6 (temporary)
  docs/diagrams/src/11-roadmap.puml — Gantt roadmap (DOC-10 §10.4)

Run:  python scripts/backlog.py
"""
import csv, pathlib, sys, datetime as dt

N, U, B = "Nurgaly Ashkenov", "Ulan Orazbek", "Both"
ROOT = pathlib.Path(__file__).resolve().parents[1]

# id, title, type, owner, milestone, start, due, status, priority, depends_on, refs,
# expected result, acceptance criteria, branch suffix, commit example
T = [
# ---------------- M1: pre-defense-1 (analysis & design) ----------------
(1, "Set up Git repository, branch protection and YouTrack project", "Task", U, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "Critical", "", "README",
 "GitHub repo with main/develop, protected main, YouTrack project DIP with issue types, states and VCS integration",
 "main protected (PR + 1 review); develop exists; YouTrack shows commits linked to DIP issues; both members have access",
 "repo-setup", "DIP-1: add initial README, .gitignore and folder skeleton"),
(2, "Agree topic, scope and role split with supervisor", "Task", B, "pre-defense-1", "2026-09-15", "2026-10-01", "Done", "Critical", "", "DOC-01 §1.2",
 "Approved topic in EN/RU/KZ, roles of Nurgaly and Ulan fixed",
 "Topic and roles confirmed by supervisor (entry SFB-00 in DOC-11)",
 "", ""),
(3, "Write project proposal (DOC-01)", "Docs", B, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "Critical", "2", "O1–O10",
 "docs/01-project-proposal.md v1.0", "All proposal sections present; scope In/Out explicit; reviewed by supervisor; comments resolved in DOC-11",
 "project-proposal", "DIP-3: add project proposal draft v1"),
(4, "Conduct 3–5 interviews with target users", "Research", B, "pre-defense-1", "2026-10-20", "2026-10-31", "In Progress", "Critical", "3", "DOC-02 H1–H7",
 "Anonymised notes INT-01…INT-05 in docs/evidence/interviews/, hypotheses H1–H7 updated in DOC-02",
 "≥ 3 interviews recorded with consent; each note uses the template; DOC-02 §2.7 moves at least H1, H2, H5 to Verified or Refuted",
 "user-interviews", "DIP-4: add anonymised notes INT-01 (support team lead)"),
(5, "Literature review with concept matrix (DOC-03)", "Docs", N, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "Critical", "", "O2",
 "docs/03-literature-review.md, docs/literature/references.bib",
 "≥ 12 sources, ≥ 8 scientific; every DOI verified; concept matrix and analytical table complete; BRIGHTER language list re-checked",
 "literature-review", "DIP-5: add concept matrix and analytical summary table"),
(6, "Analyse public sample of ≥ 300 KZ/RU feedback texts", "Research", N, "pre-defense-1", "2026-10-20", "2026-10-31", "In Progress", "High", "18", "DOC-02 §2.4, H1, H7",
 "Filled results table in DOC-02 §2.4; analysis notebook in docs/evidence/data-analysis/",
 "≥ 300 texts from ≥ 3 sources; shares of kk/ru/mixed and informal reported; κ on double-labelled subset; no personal data committed",
 "public-data-analysis", "DIP-6: add language-mix analysis of 300 public reviews"),
(7, "Compare existing systems (DOC-04)", "Docs", U, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "High", "5", "C1–C10",
 "docs/04-existing-systems.md", "≥ 3 systems × 6–10 criteria; every claim backed by a source with check date",
 "existing-systems", "DIP-7: add comparison matrix of 7 existing systems"),
(8, "Compare technologies for key decisions (DOC-05)", "Docs", B, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "High", "", "TD-1…TD-5",
 "docs/05-technology-comparison.md", "≥ 3 decisions × 2–3 alternatives; weighted matrix with drivers; decision log; both members agree on scores",
 "technology-comparison", "DIP-8: add weighted decision matrix for backend framework"),
(9, "Requirements specification with MoSCoW and AC (DOC-06)", "Docs", B, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "Critical", "3", "FR, NFR, MLR",
 "docs/06-requirements.md", "Every Must requirement has measurable AC and a test ID; traceability matrix complete",
 "requirements-spec", "DIP-9: add functional requirements with acceptance criteria"),
(10, "Architecture description (DOC-07)", "Docs", U, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "Critical", "9", "§7.13",
 "docs/07-architecture.md", "C4 levels 1–3 described; consistency table (§7.13) has no gaps for Must requirements",
 "architecture", "DIP-10: add container view and internal ML contract"),
(11, "Diagram sources and exports (PlantUML)", "Docs", B, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "High", "10", "D1–D10",
 "docs/diagrams/src/*.puml + export/*.svg|png", "All diagrams render without errors; names match DOC-06/DOC-07; ML pipeline diagram reviewed by Nurgaly",
 "diagrams", "DIP-11: add system context and use case diagrams"),
(12, "UX wireframes for key scenarios (DOC-08)", "Design", U, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "High", "9", "SCR-01…06",
 "docs/08-ux-prototype.md, docs/mockups/*.png", "6 screens with requirement labels and error states; walkthrough with supervisor done",
 "ux-wireframes", "DIP-12: add dashboard and results table wireframes"),
(13, "REST API contract (OpenAPI 3.1)", "Design", U, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "High", "9", "FR-01…FR-19",
 "docs/api/openapi.yaml, scripts/check_openapi.py", "scripts/check_openapi.py passes; JSON examples for single and batch flows",
 "openapi-contract", "DIP-13: add OpenAPI contract for batch endpoints"),
(14, "Verification and evaluation plan (DOC-09)", "Docs", B, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "Critical", "9", "TC-*",
 "docs/09-verification-plan.md", "Every test ID referenced in DOC-06 defined; ML metrics per slice, baselines and conditions specified",
 "verification-plan", "DIP-14: add ML evaluation protocol per language slice"),
(15, "Project management: backlog, risks, roadmap (DOC-10)", "Docs", U, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "Critical", "", "DOC-10",
 "docs/10-project-management.md, docs/pm/backlog.csv, roadmap diagram", "All DIP tasks have owner, result, AC, deadline, branch, commit; risk matrix scored; issues created in YouTrack",
 "project-management", "DIP-15: add risk matrix and roadmap"),
(16, "Supervisor review sessions and feedback log (DOC-11)", "Task", B, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "Critical", "3", "DOC-11",
 "docs/11-supervisor-feedback.md with ≥ 1 real review entry", "Feedback recorded with date, artefact, comment, decision, resulting commit/issue",
 "supervisor-feedback", "DIP-16: log supervisor review of requirements (SFB-01)"),
(17, "Repository skeleton: folders, .env.example, compose stub, CI lint", "Task", U, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "High", "1", "NFR-10, NFR-12",
 "All folders from README tree with .gitkeep; .env.example; docker-compose.yml stub; GitHub Actions running ruff on PRs",
 "README tree matches repository; CI badge green on develop",
 "repo-skeleton", "DIP-17: add CI workflow with lint job"),
(18, "Annotation guidelines v0 for 6 emotions", "Research", N, "pre-defense-1", "2026-10-20", "2026-10-22", "Done", "High", "5", "MLR-02",
 "ml/annotation/guidelines.md v0 with ≥ 3 examples per label per slice", "Used for the DIP-6 pilot; disagreement cases listed for v1",
 "annotation-guidelines", "DIP-18: add annotation guidelines v0 with KZ/RU/mixed examples"),
(19, "Pre-defense-1 release, tag and form submission", "Task", B, "pre-defense-1", "2026-10-22", "2026-10-22", "In Progress", "Critical", "3,5,7,8,9,10,11,12,13,14,15,16,17,18", "—",
 "GitHub release with tags prob-period-1 and pre-defense-1 on main; consolidated PDF; submission form sent; slides for 24.10", "develop merged to main via reviewed PR; release published with notes and PDF; form submitted 22.10; all links open for supervisor and committee",
 "pre-defense-1-release", "DIP-19: update README status table for pre-defense-1"),
# ---------------- M2: data & baselines ----------------
(20, "Data collection and anonymisation pipeline", "Feature", N, "pre-defense-2", "2026-10-26", "2026-11-15", "To Do", "Critical", "18", "MLR-08",
 "ml/src/preprocessing/collect.py, anonymise.py; ml/data/README.md with sources and licences",
 "Unit tests remove names, phones, IIN, e-mails on fixtures; licences listed; raw data never committed",
 "data-pipeline", "DIP-20: add anonymisation of phones, IIN and e-mails"),
(21, "Kazakh text normaliser and language identifier (kk/ru/mixed)", "Feature", N, "pre-defense-2", "2026-11-02", "2026-11-29", "To Do", "Critical", "20", "FR-02, AC-02.1–02.4",
 "ml/src/preprocessing/normalize.py, langid.py", "TC-UNIT-05 passes; TC-ML-07 accuracy ≥ 95 % kk/ru, ≥ 85 % mixed on pilot set",
 "kazakh-text-normalizer", "DIP-21: normalize Kazakh-specific Cyrillic letters before tokenization"),
(22, "Annotate corpus v1 and measure agreement", "Research", N, "pre-defense-2", "2026-11-09", "2026-12-20", "To Do", "Critical", "18,20", "MLR-02",
 "Labelled corpus v1 (≥ 3,000 kk/mixed items) + κ report", "≥ 15 % double-annotated (Ulan second annotator); κ reported; guidelines v1",
 "annotation-v1", "DIP-22: add agreement report for annotation round 1"),
(23, "Pilot experiment and absolute quality target", "Research", N, "pre-defense-2", "2026-11-30", "2026-12-13", "To Do", "High", "21", "MLR-06",
 "Pilot results on the first 1,000 items annotated in DIP-22 (partial dependency); absolute Macro-F1 target proposed", "Target agreed with supervisor and logged in DOC-11; MLR-06 updated",
 "pilot-experiment", "DIP-23: add pilot TF-IDF and XLM-R results"),
(24, "Stratified splits and frozen test set", "Feature", N, "pre-defense-2", "2026-12-07", "2026-12-20", "To Do", "Critical", "22", "MLR-03, MLR-04",
 "ml/src/data/split.py; test_set.sha256", "TC-ML-03 and TC-ML-04 pass; hash committed",
 "stratified-splits", "DIP-24: add stratified split with near-duplicate check"),
(25, "Baselines and evaluation pipeline", "Feature", N, "pre-defense-2", "2026-12-14", "2027-01-17", "To Do", "Critical", "24", "MLR-05, TC-ML-05",
 "TF-IDF, mBERT, RuBERT-tiny2-CEDR, LLM zero-shot results; ml/src/evaluation/", "Per-slice tables and confusion matrices generated automatically; bootstrap implemented",
 "baselines-eval", "DIP-25: add per-slice evaluation report generator"),
(26, "ML inference service and CPU benchmark", "Feature", N, "pre-defense-2", "2027-01-04", "2027-01-31", "To Do", "Critical", "27", "FR-01–FR-03, FR-18, NFR-01",
 "ml-service/ with /predict, /model, /health; latency benchmark", "Contract identical to stub; p95 latency of 1 text measured and NFR-01 budget re-baselined in DOC-06/DOC-11",
 "ml-inference-service", "DIP-26: add /predict endpoint with batching up to 64 texts"),
(27, "ML-service stub implementing the internal contract", "Feature", U, "pre-defense-2", "2026-10-26", "2026-11-08", "To Do", "High", "13", "DOC-07 §7.5.1",
 "ml-service/stub/ Docker image with deterministic predictions", "Backend integration tests run in CI against the stub",
 "ml-service-stub", "DIP-27: add deterministic ML stub for integration tests"),
(28, "Fine-tune XLM-R-base (primary model)", "Feature", N, "pre-defense-2", "2027-01-11", "2027-02-21", "To Do", "Critical", "25", "MLR-01, MLR-06",
 "Model emotion-xlmr-kkru-v0.1.0 + config + report", "3 seeds; TC-ML-01 and TC-ML-06 pass on all slices",
 "xlmr-finetune", "DIP-28: add XLM-R fine-tuning config and training script"),
(29, "Alternative models and error analysis", "Research", N, "final-defense", "2027-02-15", "2027-03-28", "To Do", "Medium", "28", "DOC-05 TD-4, DOC-09 §9.4.6",
 "mDeBERTa-v3 (and XLM-R-large if feasible) results; error analysis of ≥ 100 items", "Comparison table with CI; error causes distribution reported",
 "alt-models", "DIP-29: add error analysis of misclassified mixed-language items"),
(30, "Database schema and migrations", "Feature", U, "pre-defense-2", "2026-10-26", "2026-11-15", "To Do", "Critical", "17", "O8, DOC-07 §7.8",
 "SQLAlchemy models + Alembic migration 0001", "Migration up/down on clean DB; ER diagram matches code",
 "db-schema", "DIP-30: add initial Alembic migration for batches and predictions"),
(31, "API skeleton: gateway, errors, /analyze, /health, /model", "Feature", U, "pre-defense-2", "2026-11-09", "2026-11-29", "To Do", "Critical", "27,30", "FR-01, FR-04, FR-18",
 "backend/app with routers and unified error handler", "TC-UNIT-04, TC-INT-01, TC-INT-02, TC-INT-16 pass against stub; OpenAPI drift check green",
 "api-skeleton", "DIP-31: add unified error envelope and /analyze endpoint"),
(32, "Batch upload and file parser", "Feature", U, "pre-defense-2", "2026-11-23", "2026-12-20", "To Do", "Critical", "31", "FR-05, FR-06",
 "POST /batches; File Parser for CSV/XLSX/TXT", "TC-UNIT-06, TC-INT-03, TC-INT-04 pass",
 "batch-upload-endpoint", "DIP-32: add POST /api/v1/batches endpoint with CSV validation"),
(33, "Celery worker, state machine, retries, retention", "Feature", U, "pre-defense-2", "2026-12-07", "2027-01-17", "To Do", "Critical", "32", "FR-07, FR-16, NFR-05",
 "Batch Processing Task, Scheduler", "TC-UNIT-07, TC-INT-05, TC-INT-09, TC-INT-14 pass",
 "batch-worker", "DIP-33: add idempotent prediction upsert and chunk retries"),
(34, "Results, statistics and timeline endpoints", "Feature", U, "pre-defense-2", "2027-01-04", "2027-01-31", "To Do", "Critical", "33", "FR-08–FR-10, FR-13",
 "/items, /stats with batch_stats aggregation", "TC-INT-06, TC-INT-07, TC-INT-08, TC-INT-11 pass; /stats ≤ 1 s on 50k items",
 "results-stats", "DIP-34: add batch_stats aggregation after completion"),
(35, "Authentication: API keys, sessions, roles, admin", "Feature", U, "pre-defense-2", "2027-01-11", "2027-02-07", "To Do", "Critical", "31", "FR-14, FR-15, FR-17",
 "Auth Module + admin endpoints", "TC-UNIT-08, TC-INT-12, TC-INT-13, TC-INT-15 pass",
 "auth-api-keys", "DIP-35: add hashed API keys with per-key rate limit"),
(36, "Web UI skeleton and screens SCR-01…SCR-03", "Feature", U, "pre-defense-2", "2027-01-18", "2027-02-21", "To Do", "Critical", "31,32", "FR-01, FR-05–FR-07",
 "frontend/ React app; typed client from openapi.yaml", "Single analysis and upload wizard work end-to-end against stub",
 "web-ui-upload", "DIP-36: add upload wizard with column mapping"),
(37, "Dashboard and records table SCR-04, SCR-05", "Feature", U, "pre-defense-2", "2027-02-08", "2027-03-14", "To Do", "Critical", "34,36", "FR-11, FR-13",
 "Dashboard with charts and filtered table", "TC-E2E-01 passes; click on chart filters table (AC-11.2)",
 "dashboard", "DIP-37: add emotion-by-language stacked chart"),
(38, "Export CSV (Must) and PDF report (Could)", "Feature", U, "final-defense", "2027-03-01", "2027-03-28", "To Do", "High", "34", "FR-12",
 "Report Service", "TC-INT-10 passes; PDF renders Kazakh letters",
 "export-reports", "DIP-38: add CSV export with BOM and formula escaping"),
(39, "Deployment: Docker Compose, Nginx, CI pipeline", "Feature", U, "pre-defense-2", "2026-11-16", "2027-03-07", "To Do", "Critical", "17", "NFR-07, NFR-10–NFR-12",
 "docker-compose.yml, nginx.conf, full CI", "TC-CI-01 passes; fresh VM start ≤ 10 min (NFR-12 checklist)",
 "deployment-ci", "DIP-39: add nginx reverse proxy with TLS to compose"),
(40, "Load and performance testing", "Test", U, "final-defense", "2027-03-15", "2027-04-11", "To Do", "Critical", "26,33,39", "NFR-01–NFR-05",
 "Locust scenarios + load-test report", "TC-LOAD-01…03 executed 3×; results and any mitigations documented",
 "load-tests", "DIP-40: add Locust scenario for concurrent batches"),
(41, "Label correction by analysts (Could)", "Feature", U, "final-defense", "2027-03-29", "2027-04-18", "To Do", "Low", "37", "FR-19",
 "PUT /items/{id}/label + UI", "TC-INT-17 passes",
 "label-correction", "DIP-41: add label correction endpoint and table edit"),
(42, "Final evaluation report and model card", "Docs", N, "final-defense", "2027-03-29", "2027-04-25", "To Do", "Critical", "28,29", "MLR-05, NFR-16, NFR-17",
 "ml/reports/final-evaluation.md, model card", "TC-ML-05, TC-ML-08 pass; informal vs. formal gap reported",
 "final-evaluation", "DIP-42: add model card with per-slice metrics"),
(43, "Usability test with target users", "Test", B, "final-defense", "2027-04-12", "2027-04-30", "To Do", "High", "37", "AC-11.4, NFR-13",
 "Usability report (TC-USE-01)", "≥ 3 sessions; task success, time, SUS; issues filed as DIP bugs",
 "usability-test", "DIP-43: add usability test protocol and results"),
(44, "Security scan and dependency audit", "Test", U, "final-defense", "2027-04-12", "2027-04-25", "To Do", "High", "39", "NFR-07, NFR-08",
 "ZAP baseline report, audit results", "TC-SEC-01: no High findings",
 "security-scan", "DIP-44: fix missing security headers found by ZAP"),
(45, "Diploma thesis writing", "Docs", B, "final-defense", "2027-02-01", "2027-05-23", "To Do", "Critical", "42", "DOC-01…DOC-11",
 "Thesis text (both parts) approved by supervisor", "All chapters reviewed; plagiarism check passed; formatting per department rules",
 "thesis", "DIP-45: add chapter 3 system design draft"),
(46, "Final defense preparation and release", "Task", B, "final-defense", "2027-05-17", "2027-06-06", "To Do", "Critical", "40,42,43,44,45", "—",
 "Presentation, demo video, tag final-defense", "Demo on clean deployment rehearsed; tag pushed",
 "final-release", "DIP-46: update README with final results and demo instructions"),
]

FIELDS = ["id", "title", "type", "owner", "milestone", "start", "due", "status", "priority",
          "depends_on", "refs", "result", "ac", "branch", "commit"]
tasks = [dict(zip(FIELDS, t)) for t in T]
for t in tasks:
    t["key"] = f"DIP-{t['id']}"
    t["branch_full"] = f"{t['key']}-{t['branch']}" if t["branch"] else "—"
    t["deps"] = ", ".join(f"DIP-{int(x)}" for x in t["depends_on"].split(",") if x) or "—"

# ---- consistency checks ----
keys = {t["key"] for t in tasks}
for t in tasks:
    for d in t["deps"].split(", "):
        assert d == "—" or d in keys, (t["key"], d)
    if t["commit"]:
        assert t["commit"].startswith(t["key"] + ": "), t["key"]
        assert len(t["commit"]) <= 72, (t["key"], len(t["commit"]))
    assert t["start"] <= t["due"], t["key"]
    for d in t["deps"].split(", "):
        if d != "—":
            dep = next(x for x in tasks if x["key"] == d)
            assert dep["due"] <= t["due"], f"{t['key']} due before its dependency {d}"

if "--check" in sys.argv:          # used by tests/CI: validate only, write nothing
    print(f"{len(tasks)} tasks; consistency checks passed")
    sys.exit(0)

# ---- CSV for YouTrack ----
pm = ROOT / "docs" / "pm"; pm.mkdir(parents=True, exist_ok=True)
with open(pm / "backlog.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Issue ID", "Summary", "Type", "Assignee", "Fix versions", "Start date", "Due date",
                "State", "Priority", "Depends on", "Requirements", "Expected result",
                "Acceptance criteria", "Branch", "Commit example"])
    for t in tasks:
        w.writerow([t["key"], t["title"], t["type"], t["owner"], t["milestone"], t["start"], t["due"],
                    t["status"], t["priority"], t["deps"], t["refs"], t["result"], t["ac"],
                    t["branch_full"], t["commit"] or "—"])

# ---- markdown tables ----
def fmt(d): return dt.date.fromisoformat(d).strftime("%d.%m.%Y")
md = []
for ms, title in [("pre-defense-1", "M1 — pre-defense-1 (analysis & design; materials submitted 22.10.2026, pre-defense 24.10.2026)"),
                  ("pre-defense-2", "M2 — pre-defense-2 (data, baselines, MVP)"),
                  ("final-defense", "M3 — final-defense (full system, evaluation, thesis)")]:
    md.append(f"#### {title}\n")
    md.append("| ID | Task | Owner | Due | State | Depends on | Expected result | Acceptance criteria | Branch / commit example |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for t in [x for x in tasks if x["milestone"] == ms]:
        bc = f"`{t['branch_full']}`<br>`{t['commit']}`" if t["commit"] else "—"
        owner = {"Nurgaly Ashkenov": "Nurgaly", "Ulan Orazbek": "Ulan", "Both": "Both"}[t["owner"]]
        md.append(f"| **{t['key']}** | {t['title']} ({t['refs']}) | {owner} | {fmt(t['due'])} | {t['status']} | "
                  f"{t['deps']} | {t['result']} | {t['ac']} | {bc} |")
    md.append("")
(pm / "backlog-tables.md").write_text("\n".join(md), encoding="utf-8")

# ---- workload summary ----
from collections import Counter
c = Counter((t["milestone"], t["owner"]) for t in tasks)
summary = {ms: {o: c[(ms, o)] for o in (N, U, B)} for ms in ("pre-defense-1", "pre-defense-2", "final-defense")}

# ---- Gantt ----
g = ["@startgantt 11-roadmap", "' DOC-10 §10.4 — generated by scripts/backlog.py; do not edit by hand",
     "title Roadmap — KZ-RU Emotion Analysis (DIP backlog)", "projectscale weekly zoom 1",
     "Project starts 2026-09-14", "saturday are closed", "sunday are closed", ""]
groups = [("pre-defense-1", "M1 · pre-defense-1"), ("pre-defense-2", "M2 · pre-defense-2"),
          ("final-defense", "M3 · final-defense")]
colors = {N: "#7FA7E8", U: "#8CCB9B", B: "#E8C27F"}
for ms, label in groups:
    g.append(f"-- {label} --")
    for t in [x for x in tasks if x["milestone"] == ms and x["id"] != 2]:
        who = {N: "N", U: "U", B: "N+U"}[t["owner"]]
        short = t["title"] if len(t["title"]) <= 46 else t["title"][:46].rsplit(" ", 1)[0].rstrip(",:;") + "…"
        g.append(f"[{t['key']} {short} ({who})] as [{t['key']}] starts {t['start']} and ends {t['due']}")
        g.append(f"[{t['key']}] is colored in {colors[t['owner']]}")
g += ["", "[materials submitted] happens 2026-10-22", "[pre-defense-1] happens 2026-10-24", "[pre-defense-2 (planned)] happens 2027-03-20",
      "[final defense (planned)] happens 2027-06-12", "2026-10-22 is colored in #FFD6D6", "@endgantt"]
(ROOT / "docs" / "diagrams" / "src" / "11-roadmap.puml").write_text("\n".join(g), encoding="utf-8")

print(f"{len(tasks)} tasks; consistency checks passed")
for ms, s in summary.items():
    print(f"  {ms}: Nurgaly {s[N]}, Ulan {s[U]}, Both {s[B]}")
