"""Filter and sort course tables."""

from __future__ import annotations

import pandas as pd


def filter_courses(
    df: pd.DataFrame,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    certificate_only: bool = False,
    modes: list[str] | None = None,
) -> pd.DataFrame:
    out = df.copy()
    if category and category != "All":
        out = out[out["course_category"] == category]
    if min_price is not None:
        out = out[out["price_inr"] >= min_price]
    if max_price is not None:
        out = out[out["price_inr"] <= max_price]
    if certificate_only:
        out = out[out["certificate"] == "yes"]
    if modes:
        modes_l = [m.lower() for m in modes]
        out = out[out["mode"].isin(modes_l)]
    return out.reset_index(drop=True)


def sort_by_price(df: pd.DataFrame, ascending: bool = False) -> pd.DataFrame:
    return df.sort_values("price_inr", ascending=ascending).reset_index(drop=True)


def cheapest_and_expensive(df: pd.DataFrame) -> tuple[pd.Series | None, pd.Series | None]:
    if df.empty:
        return None, None
    idx_min = df["price_inr"].idxmin()
    idx_max = df["price_inr"].idxmax()
    return df.loc[idx_min], df.loc[idx_max]
