"""
Course Price Comparator — Streamlit app
Run: streamlit run app.py
"""

from __future__ import annotations

import io
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.charts import price_bar_chart
from src.filters import cheapest_and_expensive, filter_courses, sort_by_price
from src.load_data import append_course, load_courses
from src.utils import CATEGORIES, MODES, validate_new_row

st.set_page_config(
    page_title="Course Price Comparator",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Course Price Comparator")
st.caption(
    "Compare certification course fees across platforms. "
    "**Prices are not live** — always verify on the official site before paying."
)

try:
    df_all = load_courses()
except Exception as exc:
    st.error(f"Could not load data: {exc}")
    st.stop()

sample_count = int(df_all["is_sample"].sum()) if "is_sample" in df_all.columns else 0
if sample_count:
    st.warning(
        f"{sample_count} row(s) are marked **SAMPLE** (approximate or unverified). "
        "Update `data/courses.csv` with prices you check yourself."
    )

st.sidebar.header("Filters")
categories = ["All"] + sorted(df_all["course_category"].dropna().unique().tolist())
category = st.sidebar.selectbox("Course category", categories)

max_price_data = int(df_all["price_inr"].max()) if not df_all.empty else 100000
min_p, max_p = st.sidebar.slider(
    "Price range (INR)",
    min_value=0,
    max_value=max(max_price_data, 1000),
    value=(0, max(max_price_data, 1000)),
    step=500,
)
certificate_only = st.sidebar.checkbox("Certificate only", value=False)
mode_options = sorted(df_all["mode"].dropna().unique().tolist()) or MODES
selected_modes = st.sidebar.multiselect("Mode", mode_options, default=mode_options)
sort_asc = st.sidebar.radio("Sort by price", ["Highest first", "Lowest first"]) == "Lowest first"

filtered = filter_courses(
    df_all,
    category=category,
    min_price=min_p,
    max_price=max_p,
    certificate_only=certificate_only,
    modes=selected_modes or None,
)
filtered = sort_by_price(filtered, ascending=sort_asc)

st.subheader(f"Results ({len(filtered)} courses)")

if filtered.empty:
    st.info("No courses match these filters. Try widening the price range or category.")
else:
    cheap, expensive = cheapest_and_expensive(filtered)
    c1, c2, c3 = st.columns(3)
    if cheap is not None:
        c1.success(
            f"**Cheapest:** {cheap['platform']} — ₹{cheap['price_inr']:,.0f}\n\n"
            f"{cheap['course_name']}"
        )
    if expensive is not None:
        c2.error(
            f"**Most expensive:** {expensive['platform']} — ₹{expensive['price_inr']:,.0f}\n\n"
            f"{expensive['course_name']}"
        )
    c3.metric("Options shown", len(filtered))

    display = filtered[
        [
            "course_category",
            "course_name",
            "platform",
            "price_inr",
            "price_per_week",
            "duration_weeks",
            "certificate",
            "mode",
            "course_url",
            "last_checked_date",
            "notes",
        ]
    ].copy()
    display = display.rename(
        columns={
            "price_inr": "Price (INR)",
            "price_per_week": "₹ / week",
            "duration_weeks": "Weeks",
            "last_checked_date": "Last checked",
        }
    )
    st.dataframe(
        display,
        use_container_width=True,
        column_config={"course_url": st.column_config.LinkColumn("Link")},
    )

    fig = price_bar_chart(filtered, title=f"Price comparison — {category}")
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

    csv_buf = io.StringIO()
    filtered.drop(
        columns=[c for c in ["price_per_week", "is_sample"] if c in filtered.columns]
    ).to_csv(csv_buf, index=False)
    st.download_button(
        "Download filtered CSV",
        data=csv_buf.getvalue(),
        file_name="course_prices_filtered.csv",
        mime="text/csv",
    )

st.markdown("---")
st.subheader("Add a course (saves to data/courses.csv)")
with st.form("add_course"):
    a1, a2 = st.columns(2)
    with a1:
        new_cat = st.selectbox("Category", CATEGORIES)
        new_name = st.text_input("Course name")
        new_platform = st.text_input("Platform")
        new_price = st.number_input("Price (INR)", min_value=0.0, value=0.0, step=100.0)
        new_weeks = st.number_input("Duration (weeks)", min_value=1, value=8, step=1)
    with a2:
        new_cert = st.selectbox("Certificate", ["yes", "no"])
        new_mode = st.selectbox("Mode", MODES)
        new_url = st.text_input("Course URL", placeholder="https://...")
        new_notes = st.text_input("Notes", value="SAMPLE — verify before relying on this price")
        new_date = st.date_input("Last checked", value=date.today())
    submitted = st.form_submit_button("Save course")
    if submitted:
        row = {
            "course_category": new_cat,
            "course_name": new_name,
            "platform": new_platform,
            "price_inr": new_price,
            "duration_weeks": int(new_weeks),
            "certificate": new_cert,
            "mode": new_mode,
            "course_url": new_url,
            "last_checked_date": str(new_date),
            "notes": new_notes,
        }
        errors = validate_new_row(row)
        if errors:
            for e in errors:
                st.error(e)
        else:
            try:
                append_course(row)
                st.success("Saved. Refresh or change a filter to reload the table.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not save: {exc}")

st.markdown("---")
st.caption(
    "Educational project · Not affiliated with any course platform · "
    "Always confirm fees on the official website."
)
