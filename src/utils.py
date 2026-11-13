"""Shared helpers and validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
COURSES_CSV = DATA_DIR / "courses.csv"

REQUIRED_COLUMNS = [
    "course_category",
    "course_name",
    "platform",
    "price_inr",
    "duration_weeks",
    "certificate",
    "mode",
    "course_url",
    "last_checked_date",
    "notes",
]

CATEGORIES = [
    "Data Analyst",
    "Python",
    "Java",
    "Web Development",
    "Machine Learning",
    "SQL",
    "Power BI",
    "Cyber Security",
]

MODES = ["online", "live", "self-paced"]


def price_per_week(price: float, weeks: float) -> float:
    weeks = max(float(weeks), 1.0)
    return round(float(price) / weeks, 2)


def is_sample_row(notes: str) -> bool:
    return "SAMPLE" in str(notes).upper()


def validate_new_row(data: dict) -> list[str]:
    errors = []
    if not str(data.get("course_category", "")).strip():
        errors.append("Category is required.")
    if not str(data.get("course_name", "")).strip():
        errors.append("Course name is required.")
    if not str(data.get("platform", "")).strip():
        errors.append("Platform is required.")
    try:
        price = float(data.get("price_inr", -1))
        if price < 0:
            errors.append("Price must be 0 or greater.")
    except (TypeError, ValueError):
        errors.append("Price must be a number.")
    try:
        weeks = int(data.get("duration_weeks", 0))
        if weeks < 1:
            errors.append("Duration must be at least 1 week.")
    except (TypeError, ValueError):
        errors.append("Duration must be a whole number of weeks.")
    cert = str(data.get("certificate", "")).lower()
    if cert not in {"yes", "no"}:
        errors.append("Certificate must be yes or no.")
    mode = str(data.get("mode", "")).lower()
    if mode not in MODES:
        errors.append(f"Mode must be one of: {', '.join(MODES)}.")
    url = str(data.get("course_url", "")).strip()
    if url and not (url.startswith("http://") or url.startswith("https://")):
        errors.append("Course URL should start with http:// or https://.")
    return errors


def ensure_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in REQUIRED_COLUMNS:
        if col not in out.columns:
            out[col] = "" if col not in ("price_inr", "duration_weeks") else 0
    out["price_inr"] = pd.to_numeric(out["price_inr"], errors="coerce").fillna(0)
    out["duration_weeks"] = pd.to_numeric(out["duration_weeks"], errors="coerce").fillna(1)
    out["certificate"] = out["certificate"].astype(str).str.lower()
    out["mode"] = out["mode"].astype(str).str.lower()
    out["notes"] = out["notes"].fillna("").astype(str)
    out["price_per_week"] = out.apply(
        lambda r: price_per_week(r["price_inr"], r["duration_weeks"]), axis=1
    )
    out["is_sample"] = out["notes"].map(is_sample_row)
    return out
