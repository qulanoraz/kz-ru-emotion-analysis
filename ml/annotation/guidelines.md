# Annotation Guidelines v0 — Emotions in Kazakh, Russian and Mixed Texts

**Issue:** DIP-18 · **Owner:** Nurgaly Ashkenov · **Version:** 0.1 (22.10.2026) · **Requirement:** MLR-02
**Used in:** pilot labelling of public reviews (DIP-6), corpus annotation v1 (DIP-22)
**Status:** draft for the pilot; disagreement cases from the pilot are collected in §8 and lead to v1.

---

## 1. Task

For every text, annotate **three** fields:

| Field | Values | Rule |
|---|---|---|
| `language` | `kk`, `ru`, `mixed` | Language of the text as written (§3) |
| `informal` | `yes`, `no` | Slang, transliteration, missing Kazakh letters, typos, CAPS, emoji-only parts |
| `emotion` | `joy`, `sadness`, `anger`, `fear`, `surprise`, `neutral` | The **dominant perceived emotion of the author** (§2) |

Annotate the emotion **expressed by the author**, not the emotion the text might cause in a reader, and not the annotator's opinion about the situation.

## 2. Emotion labels

| Label | Definition | Typical signals | Polarity (FR-03) |
|---|---|---|---|
| `joy` | Satisfaction, gratitude, delight, relief | thanks, praise, "супер", "керемет", 😊 | positive |
| `sadness` | Disappointment, regret, being upset **without** aggression | "жаль", "өкінішке қарай", "расстроен", "раньше было лучше" | negative |
| `anger` | Irritation, outrage, accusation, demand | "ужас", "безобразие", "Бұл қандай қызмет?!", "верните немедленно", CAPS, "!!!" | negative |
| `fear` | Worry, anxiety, fear of loss or harm | "боюсь", "переживаю", "қорқып отырмын", "что делать?" about money / data / safety | negative |
| `surprise` | Reaction to something unexpected, positive or negative | "ого", "не ожидал", "ойбай", "серьёзно?" | neutral |
| `neutral` | Facts, questions, instructions, no clear emotion | how-to questions, order details, "нормально" | neutral |

## 3. Language tag

| Tag | Rule | Example |
|---|---|---|
| `kk` | Only Kazakh (Cyrillic or Latin), possibly with international words (app, ok, SMS) | «Рахмет, қызмет көрсету керемет болды!» |
| `ru` | Only Russian | «Спасибо большое, оператор быстро решил проблему!» |
| `mixed` | Both Kazakh and Russian, **at least two words of each** (FR-02, AC-02.2) | «Доставка вообще кешікті, курьер телефон алмады, очень недоволен» |

Kazakh written with Russian letters (e.g. «рахмет», «жаксы» instead of «жақсы») is still `kk`, with `informal = yes`. A single Kazakh greeting in a Russian text («Сәлеметсіз бе, у меня вопрос…») is `ru`.

## 4. Decision rules

1. **Several emotions → choose the dominant one.** Prefer the emotion of the main statement or the final sentence; if a complaint ends with thanks for a solved problem, choose `joy`.
2. **Negative emotion: anger vs. sadness.** Blame, demands, insults, CAPS or "!!!" → `anger`. Resignation, regret, disappointment without blame → `sadness`.
3. **Anxiety about money, data, health or safety → `fear`**, even if phrased as a question («Деньги пропали, что делать?»).
4. **Sarcasm:** label the intended emotion («Отличный сервис, третий день жду 🙃» → `anger`), and write `sarcasm` in `notes`.
5. **Rating mismatch:** for KazSAnDRA texts the star rating is a sanity check only; label the text. A 1-star review is rarely `joy` — check it again before saving.
6. **Unclear or too short** («ок», «👍», «норм») → `neutral`, unless the emoji clearly signals an emotion (😡 → `anger`, 😢 → `sadness`).
7. **Do not guess from context outside the text** (app name, previous reviews).

## 5. Examples (3 per label per language slice)

*Examples are constructed in the style of real public reviews; Kazakh examples to be verified by a native speaker before v1.*

### joy
| kk | ru | mixed |
|---|---|---|
| Рахмет, қызмет көрсету керемет болды! | Спасибо большое, оператор быстро решил проблему! | Рахмет, курьер очень быстро привёз! |
| Тапсырыс уақытында келді, өте ризамын. | Отличное приложение, всё работает как часы. | Приложение супер, қолдануға өте ыңғайлы. |
| Жаңартудан кейін қосымша әлдеқайда ыңғайлы болды, жарайсыңдар! | Курьер вежливый, доставили раньше срока, очень доволен. | Жақсы сервис, спасибо за помощь! |

### sadness
| kk | ru | mixed |
|---|---|---|
| Өкінішке қарай, тапсырысым жоғалып кетті, көңілім түсті. | Жаль, раньше было намного лучше. | Өкінішке қарай, заказ отменили без объяснений. |
| Бұрын жақсы еді, қазір сапасы нашарлап кетті. | Очень расстроена, заказ так и не пришёл к празднику. | Расстроился, бонустар жанбады. |
| Үміттенген едім, бірақ ештеңе өзгермеді. | Грустно, что поддержка больше не отвечает. | Бұрын нормально было, қазір мүлдем нашар. |

### anger
| kk | ru | mixed |
|---|---|---|
| Үш күн күттім, ешкім жауап бермеді. Бұл қандай қызмет? | Ужасный сервис, больше никогда не закажу! | Доставка вообще кешікті, курьер телефон алмады, очень недоволен |
| Ақшамды екі рет алып қойды, дереу қайтарыңдар! | Деньги списали дважды, верните немедленно! | Бұл не деген безобразие? Третий раз пишу! |
| Ең нашар қосымша, уақытымды босқа кетірдім! | Сколько можно ждать? Поддержка просто издевается. | Ақша списали, а заказ жоқ, кошмар! |

### fear
| kk | ru | mixed |
|---|---|---|
| Картамнан белгісіз біреу ақша алды, енді не істеймін, қорқып отырмын. | С карты пропали деньги, я в панике, что делать? | Картадан деньги пропали, қорқып отырмын, помогите! |
| Деректерім ұрланып кетті ме деп алаңдаймын. | Боюсь, что мои данные попали к мошенникам. | Звонили мошенники, енді аккаунтыма кіре алмаймын, страшно. |
| Шотым бұғатталды, айлығым түспей қала ма деп уайымдаймын. | Пришло странное СМС, страшно, что взломали аккаунт. | Шотым заблокирован, айлығым қайда, переживаю. |

### surprise
| kk | ru | mixed |
|---|---|---|
| Ойбай, тапсырыс бір сағатта келді! | Ого, так быстро ещё никогда не привозили! | Ого, заказ бір сағатта келді, не ожидал! |
| Күтпеген едім, бонус өзі түсіп қалды. | Неожиданно: вернули деньги без всяких заявлений. | Серьёзно? Кешбэк бірден түсті! |
| Шынымен бе? Қосымша енді қазақша да жұмыс істейді! | Не думал, что ответят ночью, удивлён. | Вот это да, қолдау қызметі бес минутта жауап берді. |

### neutral
| kk | ru | mixed |
|---|---|---|
| Нөмірді қалай ауыстыруға болады? | Как поменять номер телефона в профиле? | Как сменить тариф, қайда басу керек? |
| Тапсырыс 15 қазанда рәсімделді. | Заказ оформлен 15 октября. | Заказ 15 қазанда оформлен. |
| Қосымшаның жаңа нұсқасы қашан шығады? | Работает нормально, без замечаний. | Қосымша норм, ничего особенного. |

## 6. Mapping of existing datasets

| Dataset | Original labels | Mapping |
|---|---|---|
| CEDR (ru) | joy, sadness, surprise, fear, anger, no emotion (multi-label) | Same names; `no emotion` → `neutral`; multi-label items: dominant label by rules §4, or excluded from the single-label set |
| KazSAnDRA (kk) | 1–5 stars | **Not mapped automatically**; texts are re-annotated with emotions; stars used only as a sanity check (§4.5) |

## 7. Process and quality control

1. **Calibration round:** both annotators label the same 100 texts, discuss all disagreements, update these guidelines.
2. **Double annotation:** ≥ 15 % of all items are labelled independently by both annotators (Nurgaly, Ulan); Cohen's κ is reported per language slice (target κ ≥ 0.60, assumption AS-6).
3. **Adjudication:** disagreements are resolved by discussion; unresolved items are marked `disputed` and excluded from the test set.
4. **Anonymisation before annotation:** names, phone numbers, IIN, e-mails, card and order numbers are replaced by `[NAME]`, `[PHONE]`, `[ID]`.
5. **Storage:** labelled texts stay in `ml/data/` (gitignored); only statistics and agreement reports go to `ml/annotation/agreement/`.

## 8. Open questions for v1 (collected during the pilot)

| # | Case | Current rule | To decide |
|---|---|---|---|
| 1 | Complaint + thanks in one text | Final sentence decides | Check agreement on such items after the pilot |
| 2 | Polite complaint without blame | `sadness` | Users may treat it as `anger`; verify with interview results |
| 3 | `disgust` (absent in CEDR) | Mapped to `anger` | Count how often annotators wanted a separate label (AS-4) |
