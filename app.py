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
    "Nimmi Singh": "Amita Pal", "Sunaina Kohli": "Amita Pal", "Shruti Bhaskar": "Varsanye tikoo"
}

# ---------- Helpers ----------
def categorize_level_to_ecr(level):
    ecr_names = {
        "customer relations escalation",
        "vr partner executive escalation",
        "vr traveler executive escalation",
        "partner consultation",
        "social media",
        "social media escalation"
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

    # ✅ Safely create CloseDate column
    if "Date/Time Closed" in df.columns:
        df["CloseDate"] = df["Date/Time Closed"].dt.normalize()
        df = df[df["CloseDate"].notna()]
    else:
        st.error("Uploaded file is missing 'Date/Time Closed' column.")
        st.stop()

    # Sidebar filters
    with st.sidebar.expander("🔎 Filters", expanded=True):
        min_date = df["Date/Time Closed"].min()
        max_date = df["Date/Time Closed"].max()

        date_range = st.date_input(
            "Closed Date Range",
            [min_date.date(), max_date.date()] if not pd.isna(min_date) else [date.today(), date.today()]
        )
        if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range

        start_date = pd.to_datetime(start_date).normalize()
        end_date = pd.to_datetime(end_date).normalize()

        status_values = st.multiselect("Status", df["Status"].unique())
        sel_primary_cat = st.selectbox("Primary Category", ["All"] + df["Primary Category"].unique().tolist())
        sel_agent = st.selectbox("Agent", ["All"] + df["Full Name"].unique().tolist())
        sel_manager = st.selectbox("Manager", ["All"] + df["Manager"].unique().tolist())
        sel_ecr = st.selectbox("ECR Category", ["All", "ECR", "Reimbursement"])

    # Apply filters
    df = df[df["CloseDate"].between(start_date, end_date)]
    if status_values:
        df = df[df["Status"].isin(status_values)]
    if sel_primary_cat != "All":
        df = df[df["Primary Category"] == sel_primary_cat]
    if sel_agent != "All":
        df = df[df["Full Name"] == sel_agent]
    if sel_manager != "All":
        df = df[df["Manager"] == sel_manager]
    if sel_ecr != "All":
        df = df[df["ECR_Category"] == sel_ecr]

    # KPIs
    total_cases = len(df)
    managers = df["Manager"].nunique()
    agents = df["Full Name"].nunique()
    avg_days = (df["Date/Time Closed"] - df["Date/Time Opened"]).dt.days.mean()
    avg_days_val = f"{avg_days:.1f}" if not np.isnan(avg_days) else "N/A"

    st.subheader("Key Metrics")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Cases</div><div class='kpi-value'>{total_cases:,}</div><div class='kpi-sub'>Records</div></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Managers</div><div class='kpi-value'>{managers}</div><div class='kpi-sub'>Unique</div></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Agents</div><div class='kpi-value'>{agents}</div><div class='kpi-sub'>Unique</div></div>", unsafe_allow_html=True)
    with k4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Avg Days to Close</div><div class='kpi-value'>{avg_days_val}</div><div class='kpi-sub'>Mean days</div></div>", unsafe_allow_html=True)

    # ---------- Tabs ----------
    st.subheader("Visual Insights")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["By Manager", "By Category", "By Agent", "ECR Split", "Avg per Day by Agent"])

    with tab1:
        mgr_counts = df.groupby("Manager")["Case Number"].count().reset_index()
        fig_mgr = px.bar(mgr_counts, x="Case Number", y="Manager", orientation="h", color="Case Number", color_continuous_scale="Blues")
        st.plotly_chart(fig_mgr, use_container_width=True)

    with tab2:
        cat_counts = df.groupby("Primary Category")["Case Number"].count().reset_index()
        fig_cat = px.bar(cat_counts, x="Case Number", y="Primary Category", orientation="h", color="Case Number", color_continuous_scale="Teal")
        st.plotly_chart(fig_cat, use_container_width=True)

    with tab3:
        agent_counts = df.groupby("Full Name")["Case Number"].count().reset_index().sort_values("Case Number", ascending=False).head(20)
        fig_agent = px.bar(agent_counts, x="Case Number", y="Full Name", orientation="h", color="Case Number", color_continuous_scale="Viridis")
        st.plotly_chart(fig_agent, use_container_width=True)

    with tab4:
        ecr_counts = df["ECR_Category"].value_counts().reset_index()
        ecr_counts.columns = ["Category","Count"]
        fig_ecr = px.pie(ecr_counts, names="Category", values="Count", hole=0.4,
                         color_discrete_map={"ECR":"#ff7f0e","Reimbursement":"#1f77b4"})
        st.plotly_chart(fig_ecr, use_container_width=True)

    with tab5:
        agent_days = df.groupby("Full Name")["CloseDate"].nunique().reset_index()
        agent_days.columns = ["Full Name", "Days_Worked"]

        agent_cases = df.groupby("Full Name")["Case Number"].count().reset_index()
        agent_cases.columns = ["Full Name", "Total_Cases"]

        agent_stats = pd.merge(agent_cases, agent_days, on="Full Name", how="left")
        agent_stats["Avg_Cases_Per_Day"] = agent_stats["Total_Cases"] / agent_stats["Days_Worked"]
        agent_stats = agent_stats.replace([np.inf, -np.inf], np.nan).fillna(0)

        fig_avg = px.bar(agent_stats.sort_values("Avg_Cases_Per_Day", ascending=False).head(20),
                         x="Avg_Cases_Per_Day", y="Full Name", orientation="h",
                         text="Avg_Cases_Per_Day", color="Avg_Cases_Per_Day",
                         color_continuous_scale="Blues")
        fig_avg.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        st.plotly_chart(fig_avg, use_container_width=True)
        st.dataframe(agent_stats.sort_values("Avg_Cases_Per_Day", ascending=False).reset_index(drop=True))

    # Trend
    st.subheader("📈 Trend Over Time (Daily)")
    trend_df = df.groupby("CloseDate")["Case Number"].count().reset_index().sort_values("CloseDate")
    if trend_df.empty:
        st.info("No closed-case data in the selected date range.")
    else:
        fig_trend = px.line(trend_df, x="CloseDate", y="Case Number", markers=True)
        fig_trend.update_xaxes(tickformat="%d-%b-%Y", tickangle=-45)
        st.plotly_chart(fig_trend, use_container_width=True)

    # Table
    st.subheader("📋 Case Explorer")
    st.dataframe(df[["Level", "Full Name", "Case Number", "Primary Category",
                     "Secondary Category", "Current Status", "Status",
                     "Date/Time Opened", "Date/Time Closed", "Manager", "ECR_Category"]])

    # Export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered Data", data=csv, file_name="filtered_cases.csv", mime="text/csv")

else:
    st.info("Please upload an Excel file to get started.")
