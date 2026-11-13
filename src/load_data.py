"""Load and save course price data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils import COURSES_CSV, REQUIRED_COLUMNS, ensure_dataframe


def load_courses(path: Path | None = None) -> pd.DataFrame:
    csv_path = path or COURSES_CSV
    if not csv_path.exists():
        empty = pd.DataFrame(columns=REQUIRED_COLUMNS)
        return ensure_dataframe(empty)
    df = pd.read_csv(csv_path)
    return ensure_dataframe(df)


def save_courses(df: pd.DataFrame, path: Path | None = None) -> None:
    csv_path = path or COURSES_CSV
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    cols = [c for c in REQUIRED_COLUMNS if c in df.columns]
    df[cols].to_csv(csv_path, index=False)


def append_course(row: dict, path: Path | None = None) -> pd.DataFrame:
    df = load_courses(path)
    new = pd.DataFrame([row])
    df = pd.concat([df, new], ignore_index=True)
    save_courses(df, path)
    return load_courses(path)
