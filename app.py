"""
app.py

Streamlit app for the EV Charging Station Placement Helper (Chandigarh).

Run with:
    streamlit run app/app.py
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Allow importing from src/ when running via `streamlit run app/app.py`
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

DATA_FILE = BASE_DIR / "data" / "chandigarh_wards_population.csv"


def min_max_normalize(series: pd.Series) -> pd.Series:
    min_val, max_val = series.min(), series.max()
    if max_val == min_val:
        return series.apply(lambda _: 0.5)
    return (series - min_val) / (max_val - min_val)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=["ward_id", "ward_name", "population", "traffic_score"])
    df["has_charger"] = df["has_charger"].fillna(0).astype(int)
    return df


def compute_need_score(df: pd.DataFrame, w_p: float, w_t: float, w_e: float) -> pd.DataFrame:
    df = df.copy()
    df["norm_population"] = min_max_normalize(df["population"])
    df["norm_traffic"] = min_max_normalize(df["traffic_score"])
    df["need_score"] = (
        w_p * df["norm_population"] + w_t * df["norm_traffic"] - w_e * df["has_charger"]
    )
    return df


def main():
    st.set_page_config(page_title="EV Charging Placement Helper - Chandigarh", layout="wide")

    st.title("⚡ EV Charging Station Placement Helper — Chandigarh")
    st.write(
        "A simple, transparent planning tool that scores each ward using population, "
        "traffic importance, and existing charger coverage, then recommends the top "
        "wards for new EV charging stations."
    )

    df = load_data()

    st.sidebar.header("Settings")

    k = st.sidebar.slider(
        "Number of stations to recommend (K)",
        min_value=1,
        max_value=len(df),
        value=5,
    )

    st.sidebar.subheader("Weights")
    w_p = st.sidebar.slider("Population weight (w_p)", 0.0, 1.0, 0.5, 0.05)
    w_t = st.sidebar.slider("Traffic weight (w_t)", 0.0, 1.0, 0.4, 0.05)
    w_e = st.sidebar.slider("Existing charger penalty (w_e)", 0.0, 1.0, 0.1, 0.05)

    st.sidebar.caption(
        "Weights don't need to sum to 1 — they control the relative importance "
        "of each factor in the need score."
    )

    df_scored = compute_need_score(df, w_p, w_t, w_e)
    df_sorted = df_scored.sort_values("need_score", ascending=False).reset_index(drop=True)
    df_top = df_sorted.head(k)

    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader(f"Top {k} Recommended Wards")
        st.dataframe(
            df_top[
                ["ward_id", "ward_name", "population", "traffic_score", "has_charger", "need_score"]
            ].style.format({"need_score": "{:.3f}"}),
            use_container_width=True,
        )

        csv = df_top.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download recommendations as CSV",
            data=csv,
            file_name="top_wards_recommendations.csv",
            mime="text/csv",
        )

    with col2:
        st.subheader("Need Score by Ward")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df_top["ward_name"], df_top["need_score"], color="teal")
        ax.set_ylabel("Need Score")
        ax.set_xticklabels(df_top["ward_name"], rotation=45, ha="right")
        fig.tight_layout()
        st.pyplot(fig)

    st.divider()
    st.subheader("All Wards (Full Ranking)")
    st.dataframe(
        df_sorted[
            ["ward_id", "ward_name", "population", "traffic_score", "has_charger", "need_score"]
        ].style.format({"need_score": "{:.3f}"}),
        use_container_width=True,
    )

    st.caption(
        "Note: This is a simplified planning helper tool for demonstration purposes, "
        "not an official government plan."
    )


if __name__ == "__main__":
    main()
