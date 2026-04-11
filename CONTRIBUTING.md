# Contributing

Thanks for helping maintain the crowd-accidents dataset. This repo mirrors the [Zenodo record](https://doi.org/10.5281/zenodo.19483010) and adds collaborative maintenance on top of it.

## Ways to contribute

- Report a missing or incorrect accident (open an issue).
- Add a new accident with sources.
- Correct casualty figures, dates, coordinates, or typos.
- Improve the validation script or CI.

## Data changes

The authoritative files are at the repo root:

- `accident_data_raw.csv` — word-based casualty figures (e.g. `Dozens`, `Hundreds`).
- `accident_data_numeric.csv` — numeric casualty figures; `-1` means **Unknown** (see `number_conversion.csv`).
- `references/<YYYYMMDD>.txt` — source notes per event.
- `gis_data/CrowdAccidents.{shp,shx,dbf}` — shapefile for mapping.

When editing data:

1. Keep both CSVs in sync. A row added to one must exist in the other with the same `Number`.
2. Add a matching `references/<YYYYMMDD>.txt` file citing the source(s). If multiple events share a date, suffix with `_1`, `_2`, …
3. Use ISO-friendly date components (`Year`, `Month`, `Day`) and a readable `Full date`.
4. Preserve column order and existing quoting style.
5. If a field is unknown, use `-1` for numeric columns rather than leaving it blank.

## Validation

All data edits are checked in CI by `scripts/validate_data.py`. Run it locally before pushing:

```bash
python scripts/validate_data.py
```

The validator checks required columns, year/month/day/lat/lon ranges, non-negative counts (with `-1` allowed as "Unknown"), and duplicate rows.

## Pull requests

- Branch from `main`.
- Keep each PR focused (one topic: new events, a correction batch, or a script change).
- Describe the source(s) and reasoning in the PR body. Link the references you added.
- CI must be green before merge.

## Citation and license

The dataset is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). By contributing, you agree that your additions are licensed under the same terms and that you have the right to share any sources you reference. Cite the dataset via `CITATION.cff` or the DOI badge in the README.
