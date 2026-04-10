# crowd-accidents

[![Validate data](https://github.com/PedestrianDynamics/crowd-accidents/actions/workflows/validate.yml/badge.svg)](https://github.com/PedestrianDynamics/crowd-accidents/actions/workflows/validate.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19483010.svg)](https://doi.org/10.5281/zenodo.19483010)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A curated, open dataset of crowd accidents (crushes, stampedes, and related
incidents) from **1900 to 2024**.

The dataset is maintained here on GitHub and archived on Zenodo:
[https://doi.org/10.5281/zenodo.19483010](https://doi.org/10.5281/zenodo.19483010)

---

## Data

The main data file is [`data/crowd-accidents.csv`](data/crowd-accidents.csv).

### Columns

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `Year` | integer | ✅ | Year the accident occurred (1900–2024) |
| `Month` | integer | | Month (1–12); leave blank if unknown |
| `Day` | integer | | Day of month (1–31); leave blank if unknown |
| `Country` | string | ✅ | Country where the accident occurred |
| `City` | string | ✅ | City or region |
| `Location` | string | ✅ | Venue or specific location (stadium, bridge, temple, …) |
| `Event` | string | ✅ | Short description of the accident |
| `Dead` | integer | ✅ | Number of fatalities (0 if none confirmed) |
| `Injured` | integer | | Number of injured; leave blank if unknown |
| `Cause` | string | ✅ | Primary cause (e.g. Crush, Stampede, Fire, Panic, Structural collapse) |
| `Source` | string | ✅ | URL or bibliographic reference for the data point |

---

## Contributing

Corrections and additions are welcome via pull requests.

1. Fork the repository and create a new branch.
2. Edit `data/crowd-accidents.csv` following the column schema above.
3. Run the local validator to check your changes:

   ```bash
   python scripts/validate_data.py
   ```

4. Open a pull request — the validator runs automatically in CI.

Please provide a source URL for every entry.

---

## Citation

If you use this dataset, please cite it as follows:

```
Chraibi, Mohcine (2025). List of crowd accidents from 1900 to 2024.
Zenodo. https://doi.org/10.5281/zenodo.19483010
```

A `CITATION.cff` file is also provided for automated citation tools.

---

## License

The dataset is released under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE) licence.
