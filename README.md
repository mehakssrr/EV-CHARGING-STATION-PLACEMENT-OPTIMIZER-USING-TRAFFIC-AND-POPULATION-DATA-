<div align="center">

# ⚡ EV Charging Station Placement Helper — Chandigarh

**A simple, transparent, data-driven tool to recommend where to build new EV charging stations in Chandigarh.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-data%20wrangling-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-interactive%20app-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Status](https://img.shields.io/badge/status-active-brightgreen)]()

*No heavy GIS. No complex ML. Just clean, explainable logic — built to be easy to present in a report or viva.*

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [How It Works](#-how-it-works)
- [Sample Output](#-sample-output)
- [Project Structure](#-project-structure)
- [Setup](#-setup)
- [Usage](#-usage)
- [Data Format](#-data-format)
- [Customizing Weights](#-customizing-weights)
- [Roadmap](#-roadmap)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 🌍 Overview

Chandigarh, like most growing Indian cities, needs to plan its EV charging
infrastructure strategically — but full GIS-based, multi-criteria siting
studies are complex and data-heavy.

This project offers a **lightweight, explainable alternative**: score each
ward using a handful of easily available factors, rank them, and recommend
the top candidates for new charging stations — all in under 200 lines of
Python.

> Built as a simplified version of the multi-criteria decision-making
> (MCDM) + GIS approaches used in real EV infrastructure planning research,
> focused on the two most easily available and explainable factors.

---

## 🧮 How It Works

Each ward is scored using a simple weighted formula:

```
NeedScore = w_p · NormalizedPopulation + w_t · TrafficScore − w_e · ExistingChargerPenalty
```

| Factor | Description |
|---|---|
| 👥 **Population** | More people generally means more potential EV owners |
| 🚦 **Traffic score (1–5)** | Manually rated: how central / commercial / high-footfall a ward is (city centre, markets, bus stands, major roads) |
| 🔌 **Existing charger penalty** | Wards that already have a charger get a small score reduction, so new stations prioritize under-served areas |

Wards are ranked by `need_score`, and the **top K** are recommended as
priority locations for new charging stations.

---

## 📊 Sample Output

Running the pipeline on the included sample data produces a ranked bar
chart of the top recommended wards:

```
output/top_wards_chart.png
```

| Rank | Ward | Need Score |
|---|---|---|
| 1 | Manimajra | 0.633 |
| 2 | Sector 35 | 0.411 |
| 3 | Sector 34 | 0.402 |
| 4 | Sector 22 | 0.374 |
| 5 | Sector 45 | 0.369 |

*(Values shown are from the bundled sample dataset — your results will
differ once you plug in real ward data.)*

---

## 📁 Project Structure

```text
ev-charging-chandigarh/
├── data/
│   └── chandigarh_wards_population.csv   # ward-level input data (replace with real data)
├── src/
│   ├── 01_prepare_data.py                # load + clean + validate
│   ├── 02_compute_scores.py              # normalize + compute need_score
│   └── 03_recommend_locations.py         # select top K + generate chart
├── app/
│   └── app.py                            # optional Streamlit interactive app
├── output/                               # generated charts + recommendation CSVs
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Setup

```bash
git clone <your-repo-url>
cd ev-charging-chandigarh
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Run the pipeline scripts (in order)

```bash
python src/01_prepare_data.py
python src/02_compute_scores.py
python src/03_recommend_locations.py
```

This will:

1. ✅ Clean and validate `data/chandigarh_wards_population.csv` → `data/wards_clean.csv`
2. 📐 Compute normalized scores → `data/wards_scored.csv`
3. 🏆 Select the top K wards and save a chart + recommendations to `output/`

### 2. Run the interactive Streamlit app *(optional but recommended)*

```bash
streamlit run app/app.py
```

Adjust the number of stations (**K**) and the factor weights
(`w_p`, `w_t`, `w_e`) live with sliders — results update instantly.

---

## 🗂️ Data Format

The included `data/chandigarh_wards_population.csv` contains **sample /
placeholder values** for demonstration. For a real submission, replace it
with actual ward-level population figures (e.g. from Census of India /
Chandigarh Administration statistical abstracts) and your own traffic
importance ratings, along with any known existing charger locations.

| Column | Type | Description |
|---|---|---|
| `ward_id` | int | Ward number |
| `ward_name` | str | Ward / area name |
| `population` | int | Ward population |
| `traffic_score` | int (1–5) | Manually assigned traffic/commercial importance |
| `has_charger` | int (0/1) | Whether a charger already exists in that ward |

---

## ⚖️ Customizing Weights

Default weights (set in `src/02_compute_scores.py` and `app/app.py`):

| Weight | Default | Meaning |
|---|---|---|
| `w_p` | `0.5` | Population importance |
| `w_t` | `0.4` | Traffic / commercial importance |
| `w_e` | `0.1` | Penalty for wards that already have a charger |

Try changing these to see how the recommended wards shift — this makes a
great **sensitivity analysis** section for a report, without needing any
extra math.

---

## 🛣️ Roadmap

- [ ] Add budget-constrained selection (cost per station vs. fixed budget)
- [ ] Support real-time traffic data via an API instead of manual scoring
- [ ] Add ward boundary map visualization (folium / geopandas)
- [ ] Export recommendations as a PDF report

---

## ⚠️ Disclaimer

This is a simplified **planning helper tool** built for educational and
demonstration purposes. It is not an official government plan and should
not be used as the sole basis for real infrastructure investment
decisions.

---

## AUTHOR

MEHAK SHARMA

#CONTACT
mehak.ssrr@gmail.com

<div align="center">

Made with 🐍 + ☕ for smarter, greener cities.

</div>
