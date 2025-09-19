import io
from datetime import date
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ---------- Page Config ----------
st.set_page_config(page_title="Power-style Case Dashboard", layout="wide")

# ---------- CSS Styling ----------
st.markdown("""
    <style>
    /* KPI Card Styling */
    .kpi-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #ffffff;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .kpi-label {
        font-size: 14px;
        color: #555;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: bold;
        color: #2c3e50;
    }
    .kpi-sub {
        font-size: 12px;
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Manager Map ----------
manager_map = {
    "Tiya Singh": "Rohit Beniwal", "Vidita Sharma": "Nakul Kumar", "Ankita Mishra": "Varsanye tikoo",
    "Preeti Lnu": "Nakul Kumar", "Karan Malhotra": "Nakul Kumar", "Naina Bansal": "Prashant Singh",
    "Mayank Aggarwal": "Rohit Beniwal", "Khushboo Narula": "Nakul Kumar", "Sahil Verma": "Amita Pal",
    "Nikhil Gera": "Prashant Singh", "Vishwas Dhariwal": "Amita Pal", "Geetanjali LNU": "Amita Pal",
    "Mohit Kalra": "Prashant Singh", "Shivani Chanchal": "Nakul Kumar", "Ritika Raj": "Amita Pal",
    "Anmol Gupta": "Rohit Beniwal", "Sania Mirza": "Varsanye tikoo", "Vikas Bhandari": "Varsanye tikoo",
    "Vinamrata Sharma": "Rohit Beniwal", "Bharat Kapoor": "Varsanye tikoo", "Ayush Ojha": "Rohit Beniwal",
    "Manish Taheem": "Amita Pal", "Kartik Gaba": "Rohit Beniwal", "Amrit Rai": "Amita Pal",
    "Tanish Sadh": "Rohit Beniwal", "Himanshi Bisht": "Amita Pal", "Raghav Kochhar": "Prashant Singh",
    "Rishabh Gululi": "Nakul Kumar", "Rishabh Gulati": "Nakul Kumar",
    "Sanjana Sharma": "Varsanye tikoo", "Muskan Malhotra": "Prashant Singh",
    "Gursimran Singh": "Nakul Kumar", "Amrita Rai": "Prashant Singh", "Vani Juneja": "Prashant Singh",
    "Vansh Bhatia": "Prashant Singh", "Pawan Bora": "Rohit Beniwal", "Ayush Latwal": "Nakul Kumar",
    "Nimmi Singh": "Amita Pal", "Sunaina Kohli": "Amita Pal", "Shruti Bhaskar":"Varsanye tikoo"
}

# ---------- Helpers ----------
def categorize_level_to_ecr(level):
    ecr_names = {
        "customer relations escalation",
        "vr partner executive escalation",
        "vr traveler executive escalation",
        "partner consultation",
        "social media",
        "social media escalation",
        "traveler consultation",
        "customer reviews"
    }
    if pd.isna(level) or str(level).strip() == "":
        return "Reimbursement"
    if str(level).strip().lower() in ecr_names:
        return "ECR"
    return "Reimbursement"

def normalize_input_df(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()
    df2["Case Number"] = df2["Case Number"].astype(str)
    df2["Level"] = df2["Level"].fillna("Unknown").astype(str)
    df2["Full Name"] = df2["Full Name"].fillna("Unknown").astype(str)
    df2["Primary Category"] = df2["Primary Category"].fillna("Unknown").astype(str)
    df2["Secondary Category"] = df2["Secondary Category"].fillna("").astype(str)
    df2["Current Status"] = df2["Current Status"].fillna("").astype(str)
    df2["Status"] = df2["Status"].fillna("Unknown").astype(str)

    df2["Date/Time Opened"] = pd.to_datetime(df2["Date/Time Opened"], errors="coerce")
    df2["Date/Time Closed"] = pd.to_datetime(df2["Date/Time Closed"], errors="coerce")

    df2["Manager"] = df2["Full Name"].map(manager_map).fillna("Unassigned").astype(str)
    df2["ECR_Category"] = df2["Level"].apply(categorize_level_to_ecr)
    df2["YearMonth"] = df2["Date/Time Closed"].dt.to_period("M").dt.to_timestamp()

    return df2

# ---------- UI ----------
st.title("📊 Power-style Case Dashboard")

uploaded_file = st.file_uploader("📂 Upload Excel file", type=["xlsx"])
if uploaded_file:
    df_raw = pd.read_excel(uploaded_file)
    df = normalize_input_df(df_raw)

    # filters, KPIs, charts, trend, table, export
    # (keep the same as your version)
    # ...
else:
    st.info("Please upload an Excel file to get started.")
