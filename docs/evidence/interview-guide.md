# Interview Guide (DOC-02 §2.3)

**Issue:** DIP-4 · **Duration:** 20–40 min · **Format:** online or in person · **Language:** Kazakh or Russian, as the respondent prefers

## Before the interview
- Send the consent form (`consent-form.md`); confirm whether audio recording is allowed.
- Prepare 2–3 wireframes from `docs/mockups/` (SCR-02, SCR-04) to show at question 7.
- Note-taker and interviewer are different people where possible.

## Introduction (2 min)
"We are students of SE-2406 working on a diploma project: automatic detection of emotions in Kazakh, Russian and mixed texts — reviews, appeals, comments. We want to understand how your team works with such texts today. There are no right or wrong answers; we will not name you or your organisation without permission."

## Questions

| # | Topic | Question | Hypothesis |
|---|---|---|---|
| 1 | Context | What is your role? What kinds of texts does your team process (reviews, chats, appeals, comments)? Roughly how many per day / month? | — |
| 2 | Languages | What share is in Kazakh, Russian, both in one message? Do people write Kazakh in Latin letters or with Russian letters instead of ә, қ, ү…? Could you show (anonymised) examples? | H1, H7 |
| 3 | Current process | How are messages read, categorised and routed today? Who does it, and how long does it take per day or week? | H2 |
| 4 | Tools | Do you use any software for sentiment or emotion analysis? How does it handle Kazakh and mixed texts? | H3 |
| 5 | Pain points | What is the most time-consuming or error-prone part? Was there a case when an important angry or worried message was noticed too late? | H2 |
| 6 | Emotions | Is "positive / negative" enough, or would you need to distinguish anger, sadness, fear, joy, surprise? What would you do differently with that information? | H4 |
| 7 | Outputs | *(show wireframes)* Which report or dashboard would help you? Which breakdowns: by date, channel, language? What is missing or unnecessary on these screens? | H5 |
| 8 | Integration | Would you upload files manually, or should the system connect via API to your CRM / helpdesk? In which formats can you export data (CSV, Excel)? | H5, H6 |
| 9 | Constraints | Are there restrictions on sending texts outside the organisation? How quickly must a file of ~10,000 messages be processed? What error level is acceptable? | NFR-02, NFR-09 |
| 10 | Follow-up | Could we show you a prototype later (usability test, spring 2027)? Could you share an anonymised sample of texts? | DOC-02 §2.6 |

## Closing (1 min)
Thank the respondent; ask whom else we could talk to; confirm how the notes will be stored.

## After the interview (same day)
1. Write `docs/evidence/interviews/INT-XX.md` using the template in DOC-02 §2.3.3.
2. Update the hypothesis table in DOC-02 §2.7.
3. Commit: `DIP-4: add anonymised notes INT-XX (<role>)` — by the interviewer.
