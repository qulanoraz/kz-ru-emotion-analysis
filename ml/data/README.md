# Data sources and handling (MLR-08)

Raw, interim and processed data are **not committed** (see `.gitignore`). This file documents where the data comes from and how to reproduce it.

| Source | Content | Licence | Use | Status |
|---|---|---|---|---|
| KazSAnDRA (ISSAI, Yeshpanov & Varol, 2024) | 180,064 Kazakh reviews with 1–5 ratings | CC BY 4.0 | Pool of Kazakh texts for emotion re-annotation; polarity as sanity check | Planned (DIP-20) |
| CEDR (Sboev et al., 2021) | 9,410 Russian sentences, 5 emotions + no emotion | See dataset card | Russian emotion training data; `no emotion` → `neutral` | Planned (DIP-20) |
| Own public sample | Public reviews / comments (app stores, review services) in kk / ru / mixed | Public content; anonymised | Evidence (DIP-06) and annotation (DIP-22) | In progress |

## Anonymisation (before annotation)
Remove or mask: person names, phone numbers, IIN (12-digit national ID), e-mail addresses, account / card numbers, user handles. Implemented in `ml/src/preprocessing/anonymise.py` (DIP-20).

## Folder layout
- `raw/` — original downloads and exports (local only)
- `interim/` — cleaned, anonymised, deduplicated JSONL
- `processed/` — labelled train / validation / test splits; `ml/reports/test_set.sha256` stores the frozen test-set hash
