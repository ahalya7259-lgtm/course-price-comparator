# Course Price Comparator

A **Python + Streamlit** web app that helps students compare **certification course fees** across learning platforms (Internshala Trainings, GeeksforGeeks, Coursera, Udemy, Simplilearn, Great Learning, and more).

Example: pick **Data Analyst** → see each platform’s price, duration, and link, sorted **highest → lowest** by default.

> **Disclaimer:** Prices are **not live**. Many rows are marked **SAMPLE** (approximate). Always verify the fee on the official course page before you pay. This project is not affiliated with any platform.

---

## Features

- Choose a course category (Data Analyst, Python, Java, Web Development, Machine Learning, SQL, Power BI, Cyber Security)
- Table with price, ₹/week, duration, certificate, mode, link, and last-checked date
- Sort by price **descending** (default) or ascending
- Bar chart of prices by platform
- Filters: price range, certificate only, mode
- Highlights **cheapest** and **most expensive** options
- Form to **add** a course row (saved to `data/courses.csv`)
- Download filtered results as CSV
- Clear warnings for SAMPLE / unverified prices

---

## How to run

```bash
git clone https://github.com/ahalya7259-lgtm/course-price-comparator.git
cd course-price-comparator

python -m venv venv
# Windows: venv\Scripts\activate
source venv/bin/activate

pip install -r requirements.txt
pytest -q
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

---

## Data sources and honesty

| Policy | Detail |
|--------|--------|
| Storage | `data/courses.csv` |
| Scraping | **Not used.** Sites often forbid scraping; fees change with coupons. |
| SAMPLE rows | Marked in the `notes` column and warned in the UI |
| Before sharing | Update prices you care about by checking official pages |

A few Data Analyst rows use fees seen on public listings around **2026-11-13** (e.g. Internshala placement course). Treat everything as **starting points**, not guarantees.

---

## Tech stack

- Python 3.10+
- Streamlit, pandas, plotly, pytest

## Limitations

- Prices are static until you update the CSV
- Not a full market map of every course

## Future work

- Power BI dashboard on the same CSV
- More categories as you expand the sheet

---

## Author

**Ahalya** — BCA Graduate | Aspiring Data Analyst  
GitHub: [ahalya7259-lgtm](https://github.com/ahalya7259-lgtm)

## License

MIT
