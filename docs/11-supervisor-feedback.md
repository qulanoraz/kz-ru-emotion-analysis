# 11. Supervisor Feedback Log

**Document ID:** DOC-11 · **Version:** 1.0 (draft for pre-defense-1) · **Date:** 20.10.2026
**YouTrack:** DIP-16 · **Owner:** Ulan Orazbek (maintains the log), Nurgaly Ashkenov · **Supervisor:** Kamila Tanyrbergenova

---

## 11.1 Purpose

This log shows **that the supervisor reviewed the substance of the work and that her feedback led to concrete changes**. Every comment is traced from the moment it is given to the commit that resolves it:

```text
Review session (SFB-xx) → comment SFB-xx.n → team decision → YouTrack issue DIP-yy → commit "DIP-yy: … (SFB-xx.n)" → new artefact version
```

Entries are written **only after a real review** (meeting, e-mail or comment in the repository). Wording of comments is recorded verbatim where possible; paraphrases are marked *(paraphrase)*. Each entry is confirmed by the supervisor (reply e-mail, signature on printed minutes, or approval comment on the PR).

## 11.2 Process

| Step | Who | When | Output |
|---|---|---|---|
| 1. Send review package | Ulan | ≥ 3 working days before the session | E-mail / PR link with the artefacts, their version and **specific questions** (§11.5) |
| 2. Review session | Team + supervisor | Every 2 weeks and before each milestone (§11.3) | Minutes using the template in §11.7 |
| 3. Log comments | Ulan | Same day | New rows in §11.4 with status *Open* |
| 4. Decide | Both (consulting supervisor if needed) | ≤ 2 days | Decision per comment: Accepted / Partially accepted / Rejected (with rationale) / Deferred |
| 5. Implement | Owner of the artefact | By the due date in YouTrack | Issue DIP-yy; commit message ends with `(SFB-xx.n)` |
| 6. Close | Ulan | After merge | Row updated with commit/PR, new version, status *Resolved*; supervisor confirmation recorded |

A comment may be rejected only with a written rationale; rejected comments stay in the log.

## 11.3 Review schedule

| Session | Planned date | Artefacts for review | Status |
|---|---|---|---|
| SFB-00 | 09.2026 *(exact date to be added)* | Topic, scope, roles | Held |
| SFB-01 | 21.10.2026, 10:00, in person | Status of all 11 components against the pre-defense-1 requirements (status table), repository and YouTrack project | **Held** — 2 instructions, no comments on content (§11.4) |
| SFB-02 | After pre-defense-1 *(date to agree)* | Content review of DOC-01, DOC-02, DOC-06; open questions Q1–Q9 (sent in writing); committee remarks | Planned |
| SFB-03 | ≈ 06.11.2026 | Committee remarks from pre-defense-1; interview results; annotation guidelines v1 | Planned |
| SFB-04 | ≈ 20.11.2026 | Annotation calibration round, κ; DB schema; API skeleton | Planned |
| SFB-05 | ≈ 11.12.2026 | Pilot experiment, absolute quality target (MLR-06) | Planned |
| SFB-06+ | Every 2 weeks | Sprint results | Planned |

## 11.4 Feedback log

**Legend.** Category: SCOPE (aims, scope, objectives), EVID (evidence, interviews), LIT (literature), REQ (requirements), ARCH (architecture, diagrams), ML (data, model, evaluation), UX, PM (plan, risks), DOC (form, language, structure). Severity: **Major** — changes content or plan; **Minor** — clarification or wording.

| ID | Date | Artefact (version) | Comment of the supervisor | Cat. | Sev. | Team decision and rationale | Action (issue) | Result (commit / PR, new version) | Status | Confirmed by supervisor |
|---|---|---|---|---|---|---|---|---|---|---|
| SFB-00.1 | 09.2026 *(exact date to be added)* | Topic proposal | Topic and its EN / RU / KZ wording approved *(details to be added by the team)* | SCOPE | Major | Accepted | DIP-2 | Topic fixed in DOC-01 §1.1 | Resolved | Topic assignment |
| SFB-00.2 | 09.2026 *(exact date to be added)* | Role split | Two-person team: ML/NLP (Nurgaly Ashkenov) and backend / integration (Ulan Orazbek) | SCOPE | Major | Accepted | DIP-2 | Roles in DOC-01 §1.2 | Resolved | Topic assignment |
| SFB-01.1 | 21.10.2026 | Status table of the 11 components; repository | "Create a release in the GitHub repository." *(paraphrase)* | PM | Minor | Accepted. A release on `main` marks the exact submitted version and carries the release notes required by the repository requirements (Step 8) | DIP-19 | GitHub release with tags `prob-period-1` and `pre-defense-1` on `main`, release notes (completed work, limitations, outstanding tasks) and the consolidated PDF attached | Resolved on publication of the release | Verbal, in person |
| SFB-01.2 | 21.10.2026 | Submission plan | "Fill in and submit the submission form" — by **22.10.2026** *(paraphrase)* | PM | Major | Accepted. The plan (submission 24.10) was compressed to 22.10: all documents enter the repository through reviewed pull requests on 22.10, release and form on the same day | DIP-15, DIP-19 | DOC-10 v1.1 (§10.4, §10.9.3, backlog dates); form submitted 22.10.2026 | Resolved on submission | Verbal, in person |

*At SFB-01 no comments on the content of the artefacts were given. The open questions Q1–Q9 (§11.5) are therefore still unanswered; they are sent to the supervisor in writing after the submission and discussed at SFB-02. Their answers will be logged here as SFB-02.x.*


### 11.4.1 Example of a correctly completed entry (format illustration only — not a real comment)

| ID | Date | Artefact (version) | Comment | Cat. | Sev. | Team decision | Action | Result | Status | Confirmed |
|---|---|---|---|---|---|---|---|---|---|---|
| SFB-xx.n | DD.MM.2026 | DOC-06 v1.0, NFR-02 | "Where does the figure of 15 minutes for 10,000 reviews come from? Justify it or mark it as an estimate." *(paraphrase)* | REQ | Minor | Accepted: the value is an engineering estimate; it is now labelled as such and re-baselined after the CPU benchmark | DIP-9, DIP-26 | Commit `DIP-9: mark NFR-02 as estimate pending benchmark (SFB-xx.n)`, DOC-06 v1.1 | Resolved | E-mail of DD.MM.2026 |

## 11.5 Open questions that need the supervisor's decision

These questions are sent with the review packages so that the review focuses on the decisions with the largest impact. Answers are logged in §11.4 and propagated to the referenced documents.

| # | Question | Options considered | Team proposal | Affects | For session |
|---|---|---|---|---|---|
| Q1 | Is the scope (6-class single-label emotion model **and** full web system) appropriate for a two-person diploma, or should one part be reduced? | (a) as proposed; (b) reduce UI to minimal; (c) reduce ML grid | (a), with Could items explicitly droppable | DOC-01 §1.8, DOC-06 | SFB-02 |
| Q2 | Is the label set *joy, sadness, anger, fear, surprise, neutral* acceptable (disgust excluded)? | Ekman-6 + neutral; CEDR-5 + neutral; polarity only | CEDR-aligned 6 classes (DOC-03 §3.3.1) | MLR-02, AS-4 | SFB-02 |
| Q3 | Is a **relative** quality target (beat TF-IDF on each slice, p < 0.05) acceptable until the pilot, or is an absolute number required now? | Relative now, absolute after pilot; absolute now | Relative now, absolute after DIP-23 | MLR-06, DOC-09 §9.4.7 | SFB-02 |
| Q4 | Are 3–5 interviews plus a 300-text public-data analysis sufficient evidence, or is a letter from a partner organisation expected? | Interviews + data; + partner letter | Interviews + data; partner letter if obtainable | DOC-02 §2.6 | SFB-02 |
| Q5 | Do you agree with the technology decisions TD-1…TD-5 (FastAPI, PostgreSQL, inference microservice + Celery/Redis, XLM-R-base, React)? | See DOC-05 | As in DOC-05 | DOC-05, DOC-07 | SFB-02 |
| Q6 | Is the definition of *mixed* text (≥ 2 Kazakh and ≥ 2 Russian tokens) adequate, or should a share-based rule be used? | Token count rule; share ≥ 20 %; annotator judgement | Annotator judgement as gold; token rule for the system | FR-02, AC-02.2 | SFB-02 |
| Q7 | Are the performance targets (p95 ≤ 1 s; 10,000 texts ≤ 15 min on CPU) reasonable for evaluation, given that they are estimates? | Keep; relax; measure first | Keep as estimates, re-baseline after DIP-26 | NFR-01, NFR-02 | SFB-02 |
| Q8 | Which diagram notation does the committee expect (C4 + UML in PlantUML is used)? | PlantUML; Mermaid; both | PlantUML (sources + exports) | DOC-07 | SFB-02 |
| Q9 | How should authorship of the thesis chapters be divided and presented? | Separate chapters per person; joint chapters with marked sections | Joint intro/analysis; ML chapters by Nurgaly; system chapters by Ulan | DIP-45 | SFB-03 |

## 11.6 Review checklist sent with each package

To get feedback on substance rather than formatting, each package asks the supervisor to check these points:

| Artefact | Questions for the reviewer |
|---|---|
| DOC-01 Proposal | Is the problem clearly stated? Is the scope realistic for 8 months? Is engineering complexity sufficient in both ML and backend? |
| DOC-02 Evidence | Are verified findings clearly separated from assumptions? Which assumption is most risky? |
| DOC-03 Literature | Are key works missing (especially Kazakh-language publications)? Is the gap convincingly argued? |
| DOC-04 / DOC-05 | Are claims about existing systems sufficiently supported? Are criteria weights justified? |
| DOC-06 Requirements | Can each Must requirement be tested unambiguously? Is anything Must that should be Should? |
| DOC-07 Architecture | Are requirements, components, data and use cases consistent? Is the architecture over- or under-engineered? |
| DOC-08 UX / API | Is it clear how users and external systems interact with the solution? |
| DOC-09 Verification | Will the plan prove the aim? Are baselines and metrics appropriate? |
| DOC-10 PM | Are tasks, deadlines and risks realistic? Is the workload fairly split? |

## 11.7 Meeting minutes template

Stored as `docs/supervisor/SFB-xx-YYYY-MM-DD.md` (one file per session) and summarised in §11.4.

```markdown
# SFB-xx — Supervisor review, DD.MM.YYYY

- Format: in person / online / e-mail; duration: __ min
- Participants: K. Tanyrbergenova, N. Ashkenov, U. Orazbek
- Artefacts reviewed (version / commit): DOC-0x vX.Y (commit abc1234), ...
- Questions sent in advance: Q_, Q_

## Comments
| # | Artefact / section | Comment (verbatim or *paraphrase*) | Severity |
|---|---|---|---|
| SFB-xx.1 | | | |

## Decisions
| # | Decision | Owner | Issue | Due |
|---|---|---|---|---|

## Next session
- Date:
- Artefacts:

Confirmed by supervisor: ☐ e-mail of DD.MM ☐ signature ☐ PR approval
```

## 11.8 Evidence of improvement (before → after)

Filled from resolved entries; this is the summary the committee reads to see that supervision changed the work.

| SFB ID | Artefact | Before (version, short description) | After (version, short description) | Commit |
|---|---|---|---|---|
| SFB-01.1 | Repository | No release; version for submission not marked | GitHub release on `main` with tags `prob-period-1` / `pre-defense-1`, release notes and PDF | release commit on `main` |
| SFB-01.2 | DOC-10 v1.0 → v1.1 | Submission planned for 24.10; start dates in the backlog did not reflect reality | Submission 22.10; real start dates and states; actual PR sequence (§10.9.3) | PR `DIP-15-project-management` |

## 11.9 Summary statistics (updated at milestones)

| Milestone | Sessions held | Comments | Accepted | Partially | Rejected | Deferred | Resolved |
|---|---|---|---|---|---|---|---|
| pre-defense-1 | 2 (SFB-00 topic approval, SFB-01) | 2 (SFB-01) | 2 | 0 | 0 | 0 | 2 (on release / submission) |

## Appendix A — Review request (template, Russian)

```text
Тема: Предзащита 1 — материалы на ревью (KZ-RU Emotion Analysis), SFB-01

Камила [отчество], здравствуйте!

Направляем на ревью материалы к предзащите 24.10:
— Project proposal (DOC-01), Evidence of relevance (DOC-02), Requirements (DOC-06)
Ссылка: <ссылка на PR / папку docs/ в репозитории, коммит ...>

Особенно просим вашего решения по вопросам:
1) Q1 — реалистичность объёма (модель + полноценная веб-система);
2) Q2 — набор из 6 эмоций (без «отвращения»);
3) Q3 — относительная цель качества до пилотного эксперимента;
4) Q4 — достаточно ли интервью + анализа 300 публичных отзывов.

Будем благодарны за комментарии до [дата] или на встрече [дата, время].
Все замечания фиксируем в логе (docs/11-supervisor-feedback.md) и связываем с задачами YouTrack.

С уважением,
Нургалы Ашкенов, Улан Оразбек (SE-2406)
```
