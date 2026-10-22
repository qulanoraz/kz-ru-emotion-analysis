# 2. Evidence of Relevance

**Document ID:** DOC-02 · **Version:** 1.0 (draft) · **Date:** 20.10.2026
**YouTrack:** DIP-4 (interviews), DIP-6 (public data analysis) · **Owner:** Ulan Orazbek, Nurgaly Ashkenov

---

## 2.1 Purpose and method

This document records the evidence on which the problem statement (DOC-01) and requirements (DOC-06) are based. Evidence is collected through three complementary methods:

| Method | Goal | Planned volume | Status |
|---|---|---|---|
| **M1. Semi-structured interviews** with representatives of target users | Validate the problem, current process, pain points and required outputs | 3–5 interviews, 30–40 min each | In progress |
| **M2. Analysis of publicly available feedback data** | Measure language mix and emotional content of real KZ/RU feedback | Sample of ≥ 300 public reviews/comments | In progress |
| **M3. Desk research** on existing tools and datasets | Confirm the language-coverage gap | Linked to DOC-03 / DOC-04 | In progress |

To meet the committee requirement, every statement below is classified as one of:

- **[V] Verified finding** — supported by a recorded interview, measured data, or a cited source.
- **[A] Assumption / hypothesis** — believed true but not yet confirmed; each has a planned validation step.

> **Rule:** a statement moves from [A] to [V] only when the referenced evidence (interview ID, data file, or citation) is committed to the repository.

## 2.2 Hypotheses to validate

| ID | Hypothesis | Validation method | Confirmation criterion |
|---|---|---|---|
| H1 | Target organisations receive a significant share of feedback in Kazakh and in mixed KZ–RU, not only in Russian | M1, M2 | ≥ 3 of 5 respondents confirm; M2 sample shows non-trivial share of kk + mixed texts |
| H2 | Feedback is currently categorised manually or with keyword rules, and this is time-consuming | M1 | ≥ 3 respondents describe manual/rule-based process and name it as a pain point |
| H3 | Existing tools used by respondents perform poorly or not at all on Kazakh text | M1, M3 | Respondents report problems; DOC-04 confirms lack of Kazakh emotion support |
| H4 | Users need emotions finer than positive/negative (at least anger vs. other negative emotions) | M1 | ≥ 3 respondents give concrete use cases for fine-grained emotions |
| H5 | Batch upload of exported files (CSV/XLSX) with an aggregated report is the most valuable primary scenario | M1 | Majority of respondents prefer batch analysis over manual one-by-one input |
| H6 | Technical teams want an API for integration with CRM/helpdesk | M1 | ≥ 1 respondent from IT/integration side confirms |
| H7 | A significant share of real messages is informal (slang, transliteration, typos) | M2 | Measured share in sample |

## 2.3 Interview programme (M1)

### 2.3.1 Planned respondents

Interviews are anonymised as `INT-01 … INT-05`; organisation names are disclosed only with written consent.

| ID | Target profile | Why relevant | Responsible | Date | Status |
|---|---|---|---|---|---|
| INT-01 | Customer-support team lead (bank / telecom / e-commerce) | Primary user of ticket triage | Ulan | ___.10.2026 | ☐ Planned |
| INT-02 | SMM / social-media monitoring specialist | Analyses comments in both languages | Nurgaly | ___.10.2026 | ☐ Planned |
| INT-03 | Employee handling citizen appeals / service-quality analyst in public sector (akimat, public service centre) | Public-sector use case | Ulan | ___.10.2026 | ☐ Planned |
| INT-04 | Data analyst / BI specialist working with customer feedback | Reporting and metrics needs | Nurgaly | ___.10.2026 | ☐ Planned |
| INT-05 | Backend / integration developer of CRM or helpdesk | API integration requirements | Ulan | ___.10.2026 | ☐ Planned |

### 2.3.2 Interview guide (summary)

Full guide: `docs/evidence/interview-guide.md`. Consent form: `docs/evidence/consent-form.md`.

1. **Context:** What is your role? What kind of textual feedback does your team process? Approximate daily/monthly volume?
2. **Languages:** What share of messages is in Kazakh, Russian, mixed? Do people write Kazakh in Latin script or with Russian letters?
3. **Current process:** How are messages read, categorised and routed today? Who does it, how long does it take?
4. **Tools:** Do you use any software for sentiment/emotion analysis? How does it handle Kazakh and mixed texts?
5. **Pain points:** What is the most time-consuming or error-prone part? Examples of missed critical messages?
6. **Emotions:** Is positive/negative enough, or do you need to distinguish anger, sadness, fear, joy, surprise? Why?
7. **Outputs:** What report or dashboard would be useful? Which charts and breakdowns (by date, channel, language)?
8. **Integration:** Would you upload files manually or integrate via API? What data formats do you export?
9. **Constraints:** Data privacy restrictions? Acceptable processing time for a file of N messages? Acceptable error level?
10. **Validation:** Would you be willing to review a prototype later or share an anonymised sample of texts?

### 2.3.3 Interview record template

Each interview is stored as `docs/evidence/interviews/INT-XX.md`:

```markdown
# INT-XX — <role, sector> (anonymised)
- Date / format: DD.MM.2026, online / offline, duration
- Interviewer(s):
- Consent obtained: yes / no (form ref)

## Key facts (verbatim or close paraphrase)
- Volume of feedback:
- Language distribution (respondent's estimate):
- Current process & tools:
- Pain points:
- Need for fine-grained emotions (examples):
- Preferred interaction (UI / API / both):
- Constraints (privacy, time, formats):

## Hypotheses affected
| Hypothesis | Supports / Refutes / Neutral | Evidence |
|---|---|---|

## Requirements derived
- FR/NFR candidate: ...
```

## 2.4 Public data analysis (M2)

**Goal:** obtain measurable evidence, independent of respondents' opinions, on language mix, informality and emotional content of real feedback.

**Sources (publicly visible content only, no personal data stored):** public reviews of Kazakhstani apps in app stores, public reviews of organisations on map/review services, public comments under posts of Kazakhstani companies and public institutions.

**Procedure:**
1. Collect a random sample of ≥ 300 texts across ≥ 3 sources (manually or with permitted export tools); remove usernames and any personal identifiers.
2. Two team members independently label each text by **language** (kk / ru / mixed), **informality** (yes/no: slang, transliteration, typos), and **dominant emotion** (six classes).
3. Compute distribution tables and Cohen's κ for the emotion label on the double-labelled subset.
4. Store the anonymised sample metadata and analysis in `docs/evidence/data-analysis/` (raw texts stay in gitignored `ml/data/raw/`).

**Results table (to be filled):**

| Metric | Value | Status |
|---|---|---|
| Sample size / sources | ___ / ___ | [A] |
| Share of Kazakh texts | ___ % | [A] |
| Share of Russian texts | ___ % | [A] |
| Share of mixed KZ–RU texts | ___ % | [A] |
| Share of informal texts | ___ % | [A] |
| Share of non-neutral emotional texts | ___ % | [A] |
| Emotion distribution (joy/sadness/anger/fear/surprise/neutral) | ___ | [A] |
| Cohen's κ (emotion, double-labelled subset) | ___ | [A] |

> This pilot also serves as a dry run of the annotation guidelines (O3) and gives a first estimate of class imbalance for the ML plan.

## 2.5 Desk research summary (M3)

Detailed analysis and full citations are given in DOC-03 (literature) and DOC-04 (existing systems). Statements here are limited to those the team will back with citations in Module 2.

| # | Statement | Status | Evidence / planned citation |
|---|---|---|---|
| D1 | Kazakhstan is a bilingual environment: Kazakh is the state language, Russian is officially used and widely spoken | [V] | Constitution of the Republic of Kazakhstan (Art. 7) |
| D2 | Kazakh is an agglutinative Turkic language, which complicates word-level NLP | [V] | Linguistic literature; cited in DOC-03 |
| D3 | Public datasets for Kazakh sentiment exist mainly at polarity level (e.g., KazSAnDRA, ISSAI, 2024) | [V] | S15 (Yeshpanov & Varol, 2024), DOC-03 §3.3.3 |
| D4 | Emotion-labelled datasets exist for Russian (e.g., CEDR, Sboev et al., 2021) | [V] | S12 (Sboev et al., 2021), DOC-03 §3.3.3 |
| D5 | Major cloud NLP services provide limited or no emotion analysis for Kazakh | [V] (checked 20.10.2026) | T1–T3, DOC-04 §4.4: Google and AWS do not support Kazakh sentiment; Azure supports Kazakh polarity only |
| D6 | Multilingual transformers (XLM-R) include Kazakh in pre-training data and enable cross-lingual transfer | [V] | S4 (Conneau et al., 2020), DOC-03 §3.3.2 |
| D7 | Code-switched KZ–RU emotion recognition is largely unaddressed in published work | [A] — supported by DOC-03 concept matrix; search in local Kazakhstani journals pending | DOC-03 §3.4, §3.7 |

## 2.6 Customer / partner agreement (optional strengthening)

If a partner organisation agrees to provide anonymised feedback data or to review the prototype, the following is recorded:

| Field | Value |
|---|---|
| Organisation | ___ (or "anonymised, sector: ___") |
| Contact role | ___ |
| Form of agreement | Letter of support / e-mail confirmation / data-sharing agreement |
| Scope | Data sample / requirements review / prototype testing |
| Date | ___ |
| File | `docs/evidence/partner-letter.pdf` (if permitted) |

## 2.7 Verified findings vs. assumptions (consolidated)

*This table is the main output of DOC-02 and is updated after each interview and after the data analysis.*

### Verified findings

| ID | Finding | Evidence |
|---|---|---|
| VF-1 | Kazakh and Russian are both officially used in Kazakhstan, so organisations must handle both | D1 |
| VF-2 | Kazakh morphology is agglutinative, requiring dedicated preprocessing/tokenisation analysis | D2 |
| VF-3 | No public human-annotated emotion dataset for Kazakh text was found; Kazakh resources are polarity-level or speech-oriented | D3, DOC-03 §3.3.3 |
| VF-4 | Major cloud NLP APIs do not offer emotion-level (only polarity or none) analysis for Kazakh | D5, DOC-04 §4.4 |
| VF-5 | The authors of the largest Kazakh sentiment dataset name code-switching and spelling errors as open problems | S15 |
| VF-… | *(added after interviews and M2)* | INT-XX / data analysis |

### Assumptions (open)

| ID | Assumption | Linked hypothesis | Validation | Deadline |
|---|---|---|---|---|
| AS-1 | Mixed KZ–RU messages form a substantial share of real feedback | H1 | M2 sample, INT-01…05 | 24.10.2026 |
| AS-2 | Manual triage is a significant time cost | H2 | Interviews | 24.10.2026 |
| AS-3 | Existing tools *used by respondents* fail on Kazakh (desk research part verified as VF-4) | H3 | Interviews | 24.10.2026 |
| AS-4 | Six emotion classes are sufficient and meaningful for users | H4 | Interviews; revisit after annotation pilot | Nov 2026 |
| AS-5 | Batch file analysis is the primary scenario | H5 | Interviews | 24.10.2026 |
| AS-6 | Reliable annotation (κ ≥ 0.6) is achievable for six classes on informal text | — | Annotation pilot | Nov 2026 |

## 2.8 Traceability to requirements

Each requirement in DOC-06 will reference its evidence source, for example:

| Requirement (draft) | Evidence |
|---|---|
| FR: detect language kk / ru / mixed per text | H1, AS-1, D1 |
| FR: batch upload of CSV/XLSX with aggregated report | H5, AS-5 |
| FR: six-class emotion output, not only polarity | H4, AS-4 |
| FR: REST API with API-key auth | H6 |
| NFR: robustness to informal text and transliteration | H7 |
| NFR: no storage of raw personal data beyond retention period | Interview constraints (privacy) |

Requirements whose evidence remains [A] at pre-defense-1 are explicitly flagged in DOC-06 as *assumption-based* and scheduled for re-validation.
