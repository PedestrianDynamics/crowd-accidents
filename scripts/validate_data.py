#!/usr/bin/env python3
"""Validate the crowd-accidents CSV data file.

Checks:
- Required columns are present
- Year is an integer in [1900, current year]; the dataset covers 1900–2024
  but the upper bound tracks the current year to allow ongoing maintenance
- Month, if present, is an integer between 1 and 12
- Day, if present, is an integer between 1 and 31
- Dead is a non-negative integer
- Injured, if present, is a non-negative integer
- No completely empty rows
- No duplicate rows
"""

import csv
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_COLUMNS = {"Year", "Country", "City", "Location", "Event", "Dead", "Cause", "Source"}
OPTIONAL_INT_COLUMNS = {"Month": (1, 12), "Day": (1, 31), "Injured": (0, 10**6)}
CURRENT_YEAR = datetime.now().year
DATA_FILE = Path(__file__).parent.parent / "data" / "crowd-accidents.csv"


def error(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def warn(msg: str) -> None:
    print(f"WARNING: {msg}")


def validate(path: Path) -> bool:
    """Return True if data is valid, False otherwise."""
    ok = True

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            error("CSV file is empty or has no header row.")
            return False

        columns = set(reader.fieldnames)
        missing = REQUIRED_COLUMNS - columns
        if missing:
            error(f"Missing required columns: {missing}")
            ok = False

        seen_rows: list[dict[str, str]] = []
        for line_num, row in enumerate(reader, start=2):
            # Skip completely empty rows
            if not any(row.values()):
                warn(f"Line {line_num}: empty row skipped.")
                continue

            # Validate Year
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

            # Validate optional integer columns
            for col, (lo, hi) in OPTIONAL_INT_COLUMNS.items():
                val_str = (row.get(col) or "").strip()
                if val_str:
                    try:
                        val = int(val_str)
                        if not (lo <= val <= hi):
                            error(f"Line {line_num}: '{col}' value {val} is out of range [{lo}, {hi}].")
                            ok = False
                    except ValueError:
                        error(f"Line {line_num}: '{col}' must be an integer, got {val_str!r}.")
                        ok = False

            # Validate Dead (required non-negative integer)
            dead_str = (row.get("Dead") or "").strip()
            if not dead_str:
                error(f"Line {line_num}: 'Dead' is required.")
                ok = False
            else:
                try:
                    dead = int(dead_str)
                    if dead < 0:
                        error(f"Line {line_num}: 'Dead' must be non-negative, got {dead}.")
                        ok = False
                except ValueError:
                    error(f"Line {line_num}: 'Dead' must be an integer, got {dead_str!r}.")
                    ok = False

            # Warn on missing required string fields
            for col in ("Country", "City", "Location", "Event", "Cause"):
                if not (row.get(col) or "").strip():
                    warn(f"Line {line_num}: '{col}' is empty.")

            seen_rows.append(dict(row))

        # Check for duplicate rows (normalise None → "")
        def _row_key(r: dict[str, str]) -> tuple[tuple[str, str], ...]:
            return tuple(sorted((k or "", v or "") for k, v in r.items()))

        seen_keys = [_row_key(r) for r in seen_rows]
        n_dups = len(seen_keys) - len(set(seen_keys))
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
    else:
        print("Validation FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
