"""Tests for sorting and filtering."""

import pandas as pd

from src.filters import cheapest_and_expensive, filter_courses, sort_by_price
from src.utils import ensure_dataframe, price_per_week


def _sample_df() -> pd.DataFrame:
    raw = pd.DataFrame(
        [
            {
                "course_category": "Data Analyst",
                "course_name": "A",
                "platform": "P1",
                "price_inr": 10000,
                "duration_weeks": 10,
                "certificate": "yes",
                "mode": "self-paced",
                "course_url": "https://a.example",
                "last_checked_date": "2026-11-13",
                "notes": "",
            },
            {
                "course_category": "Data Analyst",
                "course_name": "B",
                "platform": "P2",
                "price_inr": 3000,
                "duration_weeks": 6,
                "certificate": "no",
                "mode": "live",
                "course_url": "https://b.example",
                "last_checked_date": "2026-11-13",
                "notes": "SAMPLE",
            },
            {
                "course_category": "Python",
                "course_name": "C",
                "platform": "P3",
                "price_inr": 5000,
                "duration_weeks": 8,
                "certificate": "yes",
                "mode": "online",
                "course_url": "https://c.example",
                "last_checked_date": "2026-11-13",
                "notes": "",
            },
        ]
    )
    return ensure_dataframe(raw)


def test_sort_descending():
    df = sort_by_price(_sample_df(), ascending=False)
    assert list(df["price_inr"]) == [10000, 5000, 3000]


def test_sort_ascending():
    df = sort_by_price(_sample_df(), ascending=True)
    assert list(df["price_inr"]) == [3000, 5000, 10000]


def test_filter_category():
    df = filter_courses(_sample_df(), category="Data Analyst")
    assert len(df) == 2
    assert set(df["course_category"]) == {"Data Analyst"}


def test_filter_price_and_certificate():
    df = filter_courses(
        _sample_df(),
        min_price=4000,
        max_price=20000,
        certificate_only=True,
    )
    assert len(df) == 2
    assert all(df["certificate"] == "yes")


def test_filter_mode():
    df = filter_courses(_sample_df(), modes=["live"])
    assert len(df) == 1
    assert df.iloc[0]["platform"] == "P2"


def test_cheapest_expensive():
    cheap, expensive = cheapest_and_expensive(_sample_df())
    assert cheap["price_inr"] == 3000
    assert expensive["price_inr"] == 10000


def test_price_per_week():
    assert price_per_week(1000, 10) == 100.0
    assert price_per_week(1000, 0) == 1000.0
