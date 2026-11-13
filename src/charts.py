"""Plotly charts for price comparison."""

from __future__ import annotations

import pandas as pd
import plotly.express as px


def price_bar_chart(df: pd.DataFrame, title: str = "Price by platform (INR)"):
    if df.empty:
        return None
    plot_df = df.copy()
    plot_df["label"] = plot_df["platform"] + " — " + plot_df["course_name"].str.slice(0, 30)
    fig = px.bar(
        plot_df.sort_values("price_inr", ascending=True),
        x="price_inr",
        y="label",
        orientation="h",
        color="platform",
        title=title,
        labels={"price_inr": "Price (INR)", "label": "Course"},
        hover_data=["duration_weeks", "mode", "certificate"],
    )
    fig.update_layout(
        height=max(320, 40 * len(plot_df)),
        showlegend=True,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig
