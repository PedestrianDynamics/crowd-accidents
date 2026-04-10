#!/usr/bin/env python3
"""Validate the crowd-accidents CSV data file.

Checks:
- Required columns are present
- Year is an integer in [1900, current year]
- Month, if present, is an integer between 1 and 12
- Day, if present, is an integer between 1 and 31
- Fatalities is a non-negative integer (or -1 for "Unknown")
- Injured, if present, is a non-negative integer (or -1 for "Unknown")
- Latitude/Longitude, if present, are valid floats in range
- No completely empty rows
- No duplicate rows
"""

import csv
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_COLUMNS = {
    "Number",
    "Full date",
    "Day",
    "Month",
    "Year",
    "Country name",
    "Country code",
    "Latitude",
    "Longitude",
    "Purpose of gathering",
    "Fatalities",
    "Injured",
    "Crowd size",
    "Description",
    "References",
}
OPTIONAL_INT_COLUMNS = {"Month": (1, 12), "Day": (1, 31)}
OPTIONAL_FLOAT_COLUMNS = {"Latitude": (-90.0, 90.0), "Longitude": (-180.0, 180.0)}
CURRENT_YEAR = datetime.now().year
DATA_FILE = Path(__file__).parent.parent / "accident_data_numeric.csv"


def error(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def warn(msg: str) -> None:
    print(f"WARNING: {msg}")


def _check_int(row: dict, col: str, line_num: int, lo: int, hi: int) -> bool:
    val_str = (row.get(col) or "").strip()
    if not val_str:
        return True
    try:
        val = int(val_str)
    except ValueError:
        error(f"Line {line_num}: '{col}' must be an integer, got {val_str!r}.")
        return False
    if not (lo <= val <= hi):
        error(f"Line {line_num}: '{col}' value {val} is out of range [{lo}, {hi}].")
        return False
    return True


def _check_float(row: dict, col: str, line_num: int, lo: float, hi: float) -> bool:
    val_str = (row.get(col) or "").strip()
    if not val_str:
        return True
    try:
        val = float(val_str)
    except ValueError:
        error(f"Line {line_num}: '{col}' must be a number, got {val_str!r}.")
        return False
    if not (lo <= val <= hi):
        error(f"Line {line_num}: '{col}' value {val} is out of range [{lo}, {hi}].")
        return False
    return True


def _check_count_int(row: dict, col: str, line_num: int, required: bool) -> bool:
    """Validate a count column. -1 is an allowed sentinel for 'Unknown'."""
    val_str = (row.get(col) or "").strip()
    if not val_str:
        if required:
            error(f"Line {line_num}: '{col}' is required.")
            return False
        return True
    try:
        val = int(val_str)
    except ValueError:
        error(f"Line {line_num}: '{col}' must be an integer, got {val_str!r}.")
        return False
    if val < -1:
        error(f"Line {line_num}: '{col}' must be >= -1, got {val}.")
        return False
    return True


def validate(path: Path) -> bool:
    ok = True

    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            error("CSV file is empty or has no header row.")
            return False

        columns = set(reader.fieldnames)
        missing = REQUIRED_COLUMNS - columns
        if missing:
            error(f"Missing required columns: {missing}")
            ok = False

        seen_keys: set = set()
        n_dups = 0
        for line_num, row in enumerate(reader, start=2):
            if not any(row.values()):
                warn(f"Line {line_num}: empty row skipped.")
                continue

            year_str = (row.get("Year") or "").strip()
            if not year_str:
                error(f"Line {line_num}: 'Year' is required.")
                ok = False
            else:
                try:
                    year = int(year_str)
                    if not (1900 <= year <= CURRENT_YEAR):
                        error(f"Line {line_num}: 'Year' {year} is out of range [1900, {CURRENT_YEAR}].")
                        ok = False
                except ValueError:
                    error(f"Line {line_num}: 'Year' must be an integer, got {year_str!r}.")
                    ok = False

            for col, (lo, hi) in OPTIONAL_INT_COLUMNS.items():
                if not _check_int(row, col, line_num, lo, hi):
                    ok = False

            for col, (lo, hi) in OPTIONAL_FLOAT_COLUMNS.items():
                if not _check_float(row, col, line_num, lo, hi):
                    ok = False

            if not _check_count_int(row, "Fatalities", line_num, required=True):
                ok = False
            if not _check_count_int(row, "Injured", line_num, required=False):
                ok = False
            if not _check_count_int(row, "Crowd size", line_num, required=False):
                ok = False

            key = tuple(sorted((k or "", v or "") for k, v in row.items()))
            if key in seen_keys:
                n_dups += 1
            else:
                seen_keys.add(key)

        if n_dups > 0:
            warn(f"{n_dups} duplicate row(s) found.")

    return ok


def main() -> int:
    if not DATA_FILE.exists():
        error(f"Data file not found: {DATA_FILE}")
        return 1

    print(f"Validating {DATA_FILE} …")
    if validate(DATA_FILE):
        print("Validation passed.")
        return 0
    print("Validation FAILED.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
