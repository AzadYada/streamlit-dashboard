##import io
##from datetime import date
##import pandas as pd
##import numpy as np
##import streamlit as st
##import plotly.express as px
##
### ---------- Page Config ----------
##st.set_page_config(page_title="Case Dashboard", layout="wide")
##
### ---------- CSS Styling ----------
##st.markdown("""
##    <style>
##    /* KPI Card Styling */
##    .kpi-card {
##        padding: 15px;
##        border-radius: 10px;
##        background-color: #ffffff;
##        text-align: center;
##        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
##    }
##    .kpi-label {
##        font-size: 14px;
##        color: #555;
##        margin-bottom: 5px;
##    }
##    .kpi-value {
##        font-size: 26px;
##        font-weight: bold;
##        color: #2c3e50;
##    }
##    .kpi-sub {
##        font-size: 12px;
##        color: #888;
##    }
##    </style>
##""", unsafe_allow_html=True)
##
### ---------- Manager Map ----------
##manager_map = {
##    "Tiya Singh": "Rohit Beniwal", "Vidita Sharma": "Nakul Kumar", "Ankita Mishra": "Varsanye tikoo",
##    "Preeti Lnu": "Nakul Kumar", "Karan Malhotra": "Nakul Kumar", "Naina Bansal": "Prashant Singh",
##    "Mayank Aggarwal": "Rohit Beniwal", "Khushboo Narula": "Nakul Kumar", "Sahil Verma": "Amita Pal",
##    "Nikhil Gera": "Prashant Singh", "Vishwas Dhariwal": "Amita Pal", "Geetanjali LNU": "Amita Pal",
##    "Mohit Kalra": "Prashant Singh", "Shivani Chanchal": "Nakul Kumar", "Ritika Raj": "Amita Pal",
##    "Anmol Gupta": "Rohit Beniwal", "Sania Mirza": "Varsanye tikoo", "Vikas Bhandari": "Varsanye tikoo",
##    "Vinamrata Sharma": "Rohit Beniwal", "Bharat Kapoor": "Varsanye tikoo", "Ayush Ojha": "Rohit Beniwal",
##    "Manish Taheem": "Amita Pal", "Kartik Gaba": "Rohit Beniwal", "Amrit Rai": "Amita Pal",
##    "Tanish Sadh": "Rohit Beniwal", "Himanshi Bisht": "Amita Pal", "Raghav Kochhar": "Prashant Singh",
##    "Rishabh Gululi": "Nakul Kumar", "Rishabh Gulati": "Nakul Kumar",
##    "Sanjana Sharma": "Varsanye tikoo", "Muskan Malhotra": "Prashant Singh",
##    "Gursimran Singh": "Nakul Kumar", "Amrita Rai": "Prashant Singh", "Vani Juneja": "Prashant Singh",
##    "Vansh Bhatia": "Prashant Singh", "Pawan Bora": "Rohit Beniwal", "Ayush Latwal": "Nakul Kumar",
##    "Nimmi Singh": "Amita Pal", "Sunaina Kohli": "Amita Pal", "Shruti Bhaskar": "Varsanye tikoo"
##}
##
##
##
##def try_parse_dates(series: pd.Series) -> pd.Series:
##    # Force month/day/year with or without time
##    parsed = pd.to_datetime(series, format="%m/%d/%Y %I:%M %p", errors="coerce")
##    
##    # Fallback: try plain date (no time)
##    if parsed.isna().any():
##        parsed2 = pd.to_datetime(series, format="%m/%d/%Y", errors="coerce")
##        parsed = parsed.fillna(parsed2)
##
##    # Final fallback: generic parse, but FORCE monthfirst
##    if parsed.isna().any():
##        parsed2 = pd.to_datetime(series, errors="coerce")
##        parsed = parsed.fillna(parsed2)
##
##    return parsed
##
##
##
##
### ---------- Helpers ----------
##def categorize_level_to_ecr(level):
##    ecr_names = {
##        "customer relations escalation",
##        "vr partner executive escalation",
##        "vr traveler executive escalation",
##        "partner consultation",
##        "social media",
##        "social media escalation",
##        "customer reviews",
##        "traveler consultation"
##    }
##
##    billing_names = {
##        "accounting details",
##        "fraud payment",
##        "payment vendor",
##        "payment escalation",
##        "regional billing"
##    }
##
##    if pd.isna(level) or str(level).strip() == "":
##        return "Reimbursement"
##
##    level_clean = str(level).strip().lower()
##
##    if level_clean in ecr_names:
##        return "ECR"
##    elif level_clean in billing_names:
##        return "Billing"
##    else:
##        return "Reimbursement"
##
##
##def try_parse_dates(series):
##    # Try common date formats; fallback to pandas inference
##    parsed = pd.to_datetime(series, dayfirst=True, errors="coerce", format="%d/%m/%Y")
##    if parsed.isna().all():
##        parsed = pd.to_datetime(series, dayfirst=True, errors="coerce", infer_datetime_format=True)
##    return parsed
##
##
##def normalize_input_df(df: pd.DataFrame) -> pd.DataFrame:
##    df2 = df.copy()
##
##    # normalize column names (strip spaces)
##    df2.columns = df2.columns.str.strip()
##
##    # Ensure expected columns exist; if not, create them safely
##    expected = ["Case Number", "Level", "Full Name", "Primary Category", "Secondary Category",
##                "Current Status", "Status", "Date/Time Opened", "Date/Time Closed"]
##    for col in expected:
##        if col not in df2.columns:
##            df2[col] = np.nan
##
##    # Cast types and fillna
##    df2["Case Number"] = df2["Case Number"].astype(str).fillna("").replace("nan", "")
##    df2["Level"] = df2["Level"].fillna("Unknown").astype(str)
##    df2["Full Name"] = df2["Full Name"].fillna("Unknown").astype(str)
##    df2["Primary Category"] = df2["Primary Category"].fillna("Unknown").astype(str)
##    df2["Secondary Category"] = df2["Secondary Category"].fillna("").astype(str)
##    df2["Current Status"] = df2["Current Status"].fillna("").astype(str)
##    df2["Status"] = df2["Status"].fillna("Unknown").astype(str)
##
##    # parse dates more flexibly
##    df2["Date/Time Opened"] = pd.to_datetime(df2["Date/Time Opened"], format="%m/%d/%Y %I:%M %p", errors="coerce")
##    df2["Date/Time Closed"] = pd.to_datetime(df2["Date/Time Closed"], format="%m/%d/%Y %I:%M %p", errors="coerce")
##
##
##    # Manager mapping and ECR category
##    df2["Manager"] = df2["Full Name"].map(manager_map).fillna("Unassigned").astype(str)
##    df2["ECR_Category"] = df2["Level"].apply(categorize_level_to_ecr)
##    df2["YearMonth"] = df2["Date/Time Closed"].dt.to_period("M").dt.to_timestamp()
##
##    return df2
##
### ---------- UI ----------
##st.title("📊 Power-style Case Dashboard")
##
##uploaded_file = st.file_uploader("📂 Upload Excel file", type=["xlsx"])
##if uploaded_file:
##    try:
##        df_raw = pd.read_excel(uploaded_file)
##    except Exception as e:
##        st.error(f"Failed to read uploaded file: {e}")
##        st.stop()
##
##    df = normalize_input_df(df_raw)
##
##    # Ensure CloseDate exists and filter out rows without close date
##    if "Date/Time Closed" in df.columns:
##        df["CloseDate"] = df["Date/Time Closed"].dt.normalize()
##        df = df[df["CloseDate"].notna()].copy()
##        if df.empty:
##            st.warning("Uploaded file has no valid 'Date/Time Closed' values after parsing.")
##    else:
##        st.error("Uploaded file is missing 'Date/Time Closed' column.")
##        st.stop()
##
##    # Sidebar filters
##    with st.sidebar.expander("🔎 Filters", expanded=True):
##        min_date = df["Date/Time Closed"].min()
##        max_date = df["Date/Time Closed"].max()
##
##        default_start = min_date.date() if not pd.isna(min_date) else date.today()
##        default_end = max_date.date() if not pd.isna(max_date) else date.today()
##
##        date_range = st.date_input(
##            "Closed Date Range",
##            [default_start, default_end] if default_start and default_end else [date.today(), date.today()]
##        )
##        if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
##            start_date, end_date = date_range
##        else:
##            start_date = end_date = date_range
##
##        start_date = pd.to_datetime(start_date).normalize()
##        end_date = pd.to_datetime(end_date).normalize()
##
##        status_values = st.multiselect("Status", options=df["Status"].unique().tolist())
##        sel_primary_cat = st.selectbox("Primary Category", ["All"] + sorted(df["Primary Category"].unique().tolist()))
##        sel_agent = st.selectbox("Agent", ["All"] + sorted(df["Full Name"].unique().tolist()))
##        sel_manager = st.selectbox("Manager", ["All"] + sorted(df["Manager"].unique().tolist()))
##        sel_ecr = st.selectbox("ECR Category", ["All", "ECR", "Reimbursement", "Billing"])
##
##    # Apply filters
##    df = df[df["CloseDate"].between(start_date, end_date)]
##    if status_values:
##        df = df[df["Status"].isin(status_values)]
##    if sel_primary_cat != "All":
##        df = df[df["Primary Category"] == sel_primary_cat]
##    if sel_agent != "All":
##        df = df[df["Full Name"] == sel_agent]
##    if sel_manager != "All":
##        df = df[df["Manager"] == sel_manager]
##    if sel_ecr != "All":
##        df = df[df["ECR_Category"] == sel_ecr]
##
##    # KPIs
##    total_cases = len(df)
##    managers = int(df["Manager"].nunique())
##    agents = int(df["Full Name"].nunique())
##    avg_days = (df["Date/Time Closed"] - df["Date/Time Opened"]).dt.days.mean()
##    avg_days_val = f"{avg_days:.1f}" if not np.isnan(avg_days) else "N/A"
##
##    st.subheader("Key Metrics")
##    k1, k2, k3, k4 = st.columns(4)
##    with k1:
##        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Cases</div><div class='kpi-value'>{total_cases:,}</div><div class='kpi-sub'>Records</div></div>", unsafe_allow_html=True)
##    with k2:
##        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Managers</div><div class='kpi-value'>{managers}</div><div class='kpi-sub'>Unique</div></div>", unsafe_allow_html=True)
##    with k3:
##        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Agents</div><div class='kpi-value'>{agents}</div><div class='kpi-sub'>Unique</div></div>", unsafe_allow_html=True)
##    with k4:
##        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Avg Days to Close</div><div class='kpi-value'>{avg_days_val}</div><div class='kpi-sub'>Mean days</div></div>", unsafe_allow_html=True)
##
##    # ---------- Tabs ----------
##    st.subheader("Visual Insights")
##    tab1, tab2, tab3, tab4, tab5 = st.tabs(["By Manager", "By Category", "By Agent", "ECR Split", "Avg per Day by Agent"])
##
##    with tab1:
##        mgr_counts = df.groupby("Manager")["Case Number"].count().reset_index(name="Count")
##        fig_mgr = px.bar(mgr_counts, x="Count", y="Manager", orientation="h", color="Count", color_continuous_scale="Blues")
##        st.plotly_chart(fig_mgr, width=True)
##
##    with tab2:
##        cat_counts = df.groupby("Primary Category")["Case Number"].count().reset_index(name="Count")
##        fig_cat = px.bar(cat_counts, x="Count", y="Primary Category", orientation="h", color="Count", color_continuous_scale="Teal")
##        st.plotly_chart(fig_cat, width=True)
##
##    with tab3:
##        agent_counts = df.groupby("Full Name")["Case Number"].count().reset_index(name="Count").sort_values("Count", ascending=False).head(20)
##        fig_agent = px.bar(agent_counts, x="Count", y="Full Name", orientation="h", color="Count", color_continuous_scale="Viridis")
##        st.plotly_chart(fig_agent, width=True)
##
##    with tab4:
##        ecr_counts = df["ECR_Category"].value_counts().reset_index()
##        ecr_counts.columns = ["Category", "Count"]
##        fig_ecr = px.pie(
##            ecr_counts, names="Category", values="Count", hole=0.4,
##            color_discrete_map={"ECR":"#ff7f0e","Reimbursement":"#1f77b4","Billing":"#2ca02c"}
##        )
##        st.plotly_chart(fig_ecr, width=True)
##
##        agent_split = (
##            df.groupby(["Full Name", "ECR_Category"])["Case Number"]
##            .count()
##            .unstack(fill_value=0)
##            .reset_index()
##        )
##
##        # normalize possible column names and ensure canonical names
##        col_map = {}
##        for c in agent_split.columns:
##            if str(c).strip().lower() in {"reimb", "reimbursement"}:
##                col_map[c] = "Reimbursement"
##            elif str(c).strip().lower() in {"bill", "billing"}:
##                col_map[c] = "Billing"
##            elif str(c).strip().lower() in {"ecr"}:
##                col_map[c] = "ECR"
##        agent_split = agent_split.rename(columns=col_map)
##
##        for col in ["ECR", "Reimbursement", "Billing"]:
##            if col not in agent_split.columns:
##                agent_split[col] = 0
##
##        agent_split["Total_Cases"] = agent_split[["ECR", "Reimbursement", "Billing"]].sum(axis=1)
##
##        def format_count_percent(row, col):
##            if row["Total_Cases"] == 0:
##                return "0 (0.00%)"
##            pct = round(row[col] / row["Total_Cases"] * 100, 2)
##            return f"{int(row[col])} ({pct:.2f}%)"
##
##        for col in ["ECR", "Reimbursement", "Billing"]:
##            agent_split[col] = agent_split.apply(lambda r: format_count_percent(r, col), axis=1)
##
##        st.subheader("🔹 Agent-wise Split (Count + %)")
##        st.dataframe(
##            agent_split[["Full Name", "ECR", "Reimbursement", "Billing", "Total_Cases"]]
##            .sort_values("Total_Cases", ascending=False)
##            .reset_index(drop=True),
##            width=True
##        )
##
##
##
####    with tab5:
####        st.subheader("📊 Avg per Day by Agent (single table, live recalc)")
####
####        # ---- Build base agent_stats ----
####        agent_cases = df.groupby("Full Name")["Case Number"].count().reset_index(name="Cases")
####
####        agent_split = (
####            df.groupby(["Full Name", "ECR_Category"])["Case Number"]
####              .count()
####              .unstack(fill_value=0)
####              .reset_index()
####        )
####        # canonicalize agent_split columns
####        col_map = {}
####        for c in agent_split.columns:
####            if str(c).strip().lower() == "full name":
####                col_map[c] = "Full Name"
####            elif str(c).strip().lower() == "ecr":
####                col_map[c] = "ECR"
####            elif str(c).strip().lower() in {"reimb", "reimbursement"}:
####                col_map[c] = "Reimbursement"
####            elif str(c).strip().lower() in {"bill", "billing"}:
####                col_map[c] = "Billing"
####        agent_split = agent_split.rename(columns=col_map)
####        for col in ["ECR", "Reimbursement", "Billing"]:
####            if col not in agent_split.columns:
####                agent_split[col] = 0
####
####        agent_stats = pd.merge(agent_cases, agent_split, on="Full Name", how="left")
####
####        # ---- Days worked (calculated) ----
####        default_days = df.groupby("Full Name")["CloseDate"].nunique().reset_index(name="Days")
####        default_days["Src"] = "Calculated"
####        agent_stats = pd.merge(agent_stats, default_days, on="Full Name", how="left")
####
####        # ---- Optional uploaded days ----
####        days_file = st.file_uploader("Upload Agent Days Worked file (optional)", type=["xlsx", "csv"], key="days_upload")
####        if days_file is not None:
####            try:
####                if days_file.name.endswith(".xlsx"):
####                    custom_days = pd.read_excel(days_file)
####                else:
####                    custom_days = pd.read_csv(days_file)
####                custom_days.columns = custom_days.columns.str.strip()
####                if "Full Name" in custom_days.columns and "Days" in custom_days.columns:
####                    custom_days = custom_days[["Full Name", "Days"]].copy()
####                    custom_days["Src"] = "Uploaded"
####                    custom_days["Days"] = pd.to_numeric(custom_days["Days"], errors="coerce")
####
####                    # Normalize names for safer match
####                    agent_stats["Full Name_norm"] = agent_stats["Full Name"].str.strip().str.lower()
####                    custom_days["Full Name_norm"] = custom_days["Full Name"].str.strip().str.lower()
####
####                    agent_stats = agent_stats.merge(
####                        custom_days[["Full Name_norm", "Days", "Src"]],
####                        on="Full Name_norm", how="left", suffixes=("", "_Uploaded")
####                    )
####
####                    # Prefer uploaded values if present, otherwise keep calculated
####                    agent_stats["Days"] = agent_stats["Days_Uploaded"].combine_first(agent_stats["Days"])
####                    agent_stats["Src"] = agent_stats["Src_Uploaded"].combine_first(agent_stats["Src"])
####
####                    # Clean temp columns
####                    agent_stats = agent_stats.drop(
####                        columns=[c for c in ["Full Name_norm", "Days_Uploaded", "Src_Uploaded"] if c in agent_stats.columns]
####                    )
####            except Exception as e:
####                st.warning(f"Could not read uploaded days file: {e}")
####
####        # ---- Fill defaults and ensure numeric types ----
####        agent_stats["Days"] = pd.to_numeric(agent_stats["Days"], errors="coerce").fillna(0)
####        agent_stats["Remaining Days"] = 10
####        agent_stats["Target"] = 8
####
####        # rename for display
####        base_df = agent_stats.rename(columns={"Full Name": "Agent"}).copy()
####
####        # ---- Calculation function ----
####        def recalc_df(dfin):
####            d = dfin.copy()
####            d["Days"] = pd.to_numeric(d["Days"], errors="coerce").fillna(0)
####            d["Remaining Days"] = pd.to_numeric(d["Remaining Days"], errors="coerce").fillna(0)
####            d["Target"] = pd.to_numeric(d["Target"], errors="coerce").fillna(0)
####            d["Cases"] = pd.to_numeric(d["Cases"], errors="coerce").fillna(0)
####
####            # ✅ make sure Current_Avg always exists
####            d["Current_Avg"] = (d["Cases"] / d["Days"].replace(0, np.nan)).round(2).fillna(0)
####
####            d["Target_Cases"] = ((d["Days"] + d["Remaining Days"]) * d["Target"]).round(0)
####            d["Cases_Required"] = (d["Target_Cases"] - d["Cases"]).clip(lower=0).astype(int)
####            d["CPD"] = (d["Cases_Required"] / d["Remaining Days"].replace(0, np.nan)).round(2).fillna(0)
####
####            d["Cases"] = d["Cases"].astype(int, errors="ignore")
####            return d
####
####        # ---- Reset session state when new file ----
####        source_key = (getattr(uploaded_file, "name", "") or "") + f"_{df.shape}"
####        if st.session_state.get("tab5_source_key") != source_key:
####            st.session_state["tab5_source_key"] = source_key
####            st.session_state["tab5_df"] = recalc_df(base_df.reset_index(drop=True))
####
####        # ---- Always recalc before display ----
####        st.session_state["tab5_df"] = recalc_df(st.session_state["tab5_df"])
####
####        # ✅ Now Current_Avg exists here
####                # ✅ Define columns to show
####        display_cols = [
####            "Agent", "Cases", "ECR", "Reimbursement", "Billing", "Days", "Src",
####            "Current_Avg", "Remaining Days", "Target",
####            "Target_Cases", "Cases_Required", "CPD"
####        ]
####
####        # ---- Editable + live recalc table ----
####        edited = st.data_editor(
####            st.session_state["tab5_df"][display_cols]
####            .sort_values("CPD", ascending=False)
####            .reset_index(drop=True),
####            key="tab5_editor_single",
####            width=True,
####            column_config={
####                "Remaining Days": st.column_config.NumberColumn("Remaining Days", min_value=0),
####                "Target": st.column_config.NumberColumn("Target Avg", min_value=0),
####            },
####            disabled=[  # keep derived fields locked
####                "Agent", "Cases", "ECR", "Reimbursement", "Billing", "Days", "Src",
####                "Current_Avg", "Target_Cases", "Cases_Required", "CPD"
####            ]
####        )
####
####        # ---- Save edits and recalc live ----
####        st.session_state["tab5_df"] = recalc_df(edited)
####
####        # ✅ No second st.dataframe → only one interactive table
##
####
####    with tab5:
####        st.subheader("📊 Avg per Day by Agent (single table, live recalc)")
####
####        # ---- Build base agent_stats with Manager ----
####        agent_cases = (
####            df.groupby(["Manager", "Full Name"])["Case Number"]
####              .count()
####              .reset_index(name="Cases")
####        )
####
####        agent_split = (
####            df.groupby(["Manager", "Full Name", "ECR_Category"])["Case Number"]
####              .count()
####              .unstack(fill_value=0)
####              .reset_index()
####        )
####
####        # Canonicalize agent_split columns
####        col_map = {}
####        for c in agent_split.columns:
####            if str(c).strip().lower() == "full name":
####                col_map[c] = "Full Name"
####            elif str(c).strip().lower() == "manager":
####                col_map[c] = "Manager"
####            elif str(c).strip().lower() == "ecr":
####                col_map[c] = "ECR"
####            elif str(c).strip().lower() in {"reimb", "reimbursement"}:
####                col_map[c] = "Reimbursement"
####            elif str(c).strip().lower() in {"bill", "billing"}:
####                col_map[c] = "Billing"
####        agent_split = agent_split.rename(columns=col_map)
####
####        for col in ["ECR", "Reimbursement", "Billing"]:
####            if col not in agent_split.columns:
####                agent_split[col] = 0
####
####        agent_stats = pd.merge(agent_cases, agent_split, on=["Manager", "Full Name"], how="left")
####
####        # ---- Calculate percentages for categories ----
####        agent_stats["ECR_pct"] = (agent_stats["ECR"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
####        agent_stats["Reimb_pct"] = (agent_stats["Reimbursement"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
####        agent_stats["Bill_pct"] = (agent_stats["Billing"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
####
####        # ---- Combine Case + % for display ----
####        agent_stats["ECR_Display"] = agent_stats["ECR"].astype(int).astype(str) + " (" + agent_stats["ECR_pct"].astype(str) + "%)"
####        agent_stats["Reimb_Display"] = agent_stats["Reimbursement"].astype(int).astype(str) + " (" + agent_stats["Reimb_pct"].astype(str) + "%)"
####        agent_stats["Bill_Display"] = agent_stats["Billing"].astype(int).astype(str) + " (" + agent_stats["Bill_pct"].astype(str) + "%)"
####
####        # ---- Days worked (calculated) ----
####        default_days = df.groupby("Full Name")["CloseDate"].nunique().reset_index(name="Days")
####        default_days["Src"] = "Calculated"
####        agent_stats = pd.merge(agent_stats, default_days, on="Full Name", how="left")
####
####        # ---- Calculation function (your logic) ----
####        def recalc_df(d):
####            d = d.copy()
####            d["Days"] = pd.to_numeric(d["Days"], errors="coerce").fillna(0)
####            d["Remaining Days"] = pd.to_numeric(d.get("Remaining Days", 0), errors="coerce").fillna(0)
####            d["Target"] = pd.to_numeric(d.get("Target", 0), errors="coerce").fillna(0)
####            d["Cases"] = pd.to_numeric(d["Cases"], errors="coerce").fillna(0)
####
####            d["Current_Avg"] = (d["Cases"] / d["Days"].replace(0, np.nan)).round(2).fillna(0)
####            d["Target_Cases"] = ((d["Days"] + d["Remaining Days"]) * d["Target"]).round(0)
####            d["Cases_Required"] = (d["Target_Cases"] - d["Cases"]).clip(lower=0).astype(int)
####            d["CPD"] = (d["Cases_Required"] / d["Remaining Days"].replace(0, np.nan)).round(2).fillna(0)
####
####            d["Cases"] = d["Cases"].astype(int, errors="ignore")
####            return d
####
####        # ---- Initialize session state ONCE ----
####        if "tab5_df" not in st.session_state:
####            agent_stats["Remaining Days"] = 10
####            agent_stats["Target"] = 8
####            st.session_state["tab5_df"] = agent_stats.rename(columns={"Full Name": "Agent"}).copy()
####            st.session_state["tab5_original_order"] = agent_stats["Full Name"].tolist()
####
####        if "tab5_original_order" not in st.session_state:
####            st.session_state["tab5_original_order"] = st.session_state["tab5_df"]["Agent"].tolist()
####
####        display_cols = [
####            "Manager", "Agent", "Cases", 
####            "ECR_Display", "Reimb_Display", "Bill_Display",
####            "Days", "Src", "Current_Avg", 
####            "Remaining Days", "Target", 
####            "Target_Cases", "Cases_Required", "CPD"
####        ]
####
####        # ---- Build recalculated view ----
####        calc_df = recalc_df(st.session_state["tab5_df"]).copy()
####        calc_df['sort_order'] = calc_df['Agent'].map(
####            {agent: i for i, agent in enumerate(st.session_state["tab5_original_order"])}
####        )
####        show_df = calc_df.sort_values('sort_order').drop('sort_order', axis=1)
####        show_df = show_df[display_cols].reset_index(drop=True)
####
####        # ---- CSS to avoid horizontal scroll ----
####        st.markdown("""
####            <style>
####            .stDataEditor {
####                width: 100% !important;
####            }
####            table {
####                table-layout: fixed;
####                width: 100% !important;
####            }
####            th, td {
####                text-align: center !important;
####                font-size: 12px !important;
####                padding: 4px !important;
####            }
####            </style>
####        """, unsafe_allow_html=True)
####
####        # ---- Editable table ----
####        edited_df = st.data_editor(
####            show_df,
####            key="tab5_editor_single",
####            column_config={
####                "Remaining Days": st.column_config.NumberColumn("Remain", min_value=0),
####                "Target": st.column_config.NumberColumn("Tgt", min_value=0),
####                "ECR_Display": st.column_config.TextColumn("ECR"),
####                "Reimb_Display": st.column_config.TextColumn("Reimb"),
####                "Bill_Display": st.column_config.TextColumn("Bill"),
####                "Current_Avg": st.column_config.NumberColumn("Curr Avg", format="%.2f"),
####                "Target_Cases": st.column_config.NumberColumn("Tgt Cases", format="%d"),
####                "Cases_Required": st.column_config.NumberColumn("Cases Req", format="%d"),
####                "CPD": st.column_config.NumberColumn("CPD", format="%.2f"),
####            },
####            disabled=[
####                "Manager", "Agent", "Cases",
####                "ECR_Display", "Reimb_Display", "Bill_Display",
####                "Days", "Src", "Current_Avg", 
####                "Target_Cases", "Cases_Required", "CPD"
####            ],
####            width="stretch"
####        )
####
####        # ---- Persist edits ----
####        if edited_df is not None:
####            if "Agent" not in edited_df.columns:
####                st.error("Editor must include the 'Agent' column to map edits back.")
####            else:
####                edited_map = edited_df.set_index("Agent")[["Remaining Days", "Target"]].copy()
####                edited_map["Remaining Days"] = pd.to_numeric(edited_map["Remaining Days"], errors="coerce").fillna(0)
####                edited_map["Target"] = pd.to_numeric(edited_map["Target"], errors="coerce").fillna(0)
####
####                ss = st.session_state["tab5_df"].copy()
####                if "Agent" not in ss.columns:
####                    st.error("session_state['tab5_df'] must have an 'Agent' column.")
####                else:
####                    ss = ss.set_index("Agent")
####                    updated = False
####
####                    for agent in edited_map.index:
####                        if agent in ss.index:
####                            new_rem = edited_map.at[agent, "Remaining Days"]
####                            new_tgt = edited_map.at[agent, "Target"]
####
####                            old_rem = pd.to_numeric(ss.at[agent, "Remaining Days"], errors="coerce")
####                            old_tgt = pd.to_numeric(ss.at[agent, "Target"], errors="coerce")
####
####                            if pd.isna(old_rem): old_rem = 0
####                            if pd.isna(old_tgt): old_tgt = 0
####
####                            if (old_rem != new_rem) or (old_tgt != new_tgt):
####                                ss.at[agent, "Remaining Days"] = new_rem
####                                ss.at[agent, "Target"] = new_tgt
####                                updated = True
####                    
####                    if updated:
####                        st.session_state["tab5_df"] = ss.reset_index()
####                        st.rerun()
##
##
####    with tab5:
####        st.subheader("📊 Avg per Day by Agent (single table, live recalc)")
####
####        # ---- Build base agent_stats with Manager ----
####        agent_cases = (
####            df.groupby(["Manager", "Full Name"])["Case Number"]
####              .count()
####              .reset_index(name="Cases")
####        )
####
####        agent_split = (
####            df.groupby(["Manager", "Full Name", "ECR_Category"])["Case Number"]
####              .count()
####              .unstack(fill_value=0)
####              .reset_index()
####        )
####
####        # Canonicalize agent_split columns
####        col_map = {}
####        for c in agent_split.columns:
####            if str(c).strip().lower() == "full name":
####                col_map[c] = "Full Name"
####            elif str(c).strip().lower() == "manager":
####                col_map[c] = "Manager"
####            elif str(c).strip().lower() == "ecr":
####                col_map[c] = "ECR"
####            elif str(c).strip().lower() in {"reimb", "reimbursement"}:
####                col_map[c] = "Reimbursement"
####            elif str(c).strip().lower() in {"bill", "billing"}:
####                col_map[c] = "Billing"
####        agent_split = agent_split.rename(columns=col_map)
####
####        for col in ["ECR", "Reimbursement", "Billing"]:
####            if col not in agent_split.columns:
####                agent_split[col] = 0
####
####        agent_stats = pd.merge(agent_cases, agent_split, on=["Manager", "Full Name"], how="left")
####
####        # ---- Calculate percentages for categories ----
####        agent_stats["ECR_pct"] = (agent_stats["ECR"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
####        agent_stats["Reimb_pct"] = (agent_stats["Reimbursement"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
####        agent_stats["Bill_pct"] = (agent_stats["Billing"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
####
####        # ---- Combine Case + % for display ----
####        agent_stats["ECR_Display"] = agent_stats["ECR"].astype(int).astype(str) + " (" + agent_stats["ECR_pct"].astype(str) + "%)"
####        agent_stats["Reimb_Display"] = agent_stats["Reimbursement"].astype(int).astype(str) + " (" + agent_stats["Reimb_pct"].astype(str) + "%)"
####        agent_stats["Bill_Display"] = agent_stats["Billing"].astype(int).astype(str) + " (" + agent_stats["Bill_pct"].astype(str) + "%)"
####
####        # ---- Days worked (calculated) ----
####        default_days = df.groupby("Full Name")["CloseDate"].nunique().reset_index(name="Days")
####        default_days["Src"] = "Calculated"
####        agent_stats = pd.merge(agent_stats, default_days, on="Full Name", how="left")
####
####        # ---- Calculation function ----
####        def recalc_df(d):
####            d = d.copy()
####            d["Days"] = pd.to_numeric(d["Days"], errors="coerce").fillna(0)
####            d["Remaining Days"] = pd.to_numeric(d.get("Remaining Days", 0), errors="coerce").fillna(0)
####            d["Target"] = pd.to_numeric(d.get("Target", 0), errors="coerce").fillna(0)
####            d["Cases"] = pd.to_numeric(d["Cases"], errors="coerce").fillna(0)
####
####            d["Current_Avg"] = (d["Cases"] / d["Days"].replace(0, np.nan)).round(2).fillna(0)
####            d["Target_Cases"] = ((d["Days"] + d["Remaining Days"]) * d["Target"]).round(0)
####            d["Cases_Required"] = (d["Target_Cases"] - d["Cases"]).clip(lower=0).astype(int)
####            d["CPD"] = (d["Cases_Required"] / d["Remaining Days"].replace(0, np.nan)).round(2).fillna(0)
####
####            d["Cases"] = d["Cases"].astype(int, errors="ignore")
####            return d
####
####        # ---- Always rebuild from filtered df, but preserve edits ----
####        agent_stats["Remaining Days"] = 10
####        agent_stats["Target"] = 8
####        fresh_df = agent_stats.rename(columns={"Full Name": "Agent"}).copy()
####
####        if "tab5_df" in st.session_state:
####            edited_map = st.session_state["tab5_df"].set_index("Agent")[["Remaining Days", "Target"]]
####            fresh_df = fresh_df.set_index("Agent")
####            for agent in edited_map.index:
####                if agent in fresh_df.index:
####                    fresh_df.at[agent, "Remaining Days"] = edited_map.at[agent, "Remaining Days"]
####                    fresh_df.at[agent, "Target"] = edited_map.at[agent, "Target"]
####            fresh_df = fresh_df.reset_index()
####
####        st.session_state["tab5_df"] = fresh_df
####        st.session_state["tab5_original_order"] = fresh_df["Agent"].tolist()
####
####        display_cols = [
####            "Manager", "Agent", "Cases", 
####            "ECR_Display", "Reimb_Display", "Bill_Display",
####            "Days", "Src", "Current_Avg", 
####            "Remaining Days", "Target", 
####            "Target_Cases", "Cases_Required", "CPD"
####        ]
####
####        # ---- Build recalculated view ----
####        calc_df = recalc_df(st.session_state["tab5_df"]).copy()
####        calc_df['sort_order'] = calc_df['Agent'].map(
####            {agent: i for i, agent in enumerate(st.session_state["tab5_original_order"])}
####        )
####        show_df = calc_df.sort_values('sort_order').drop('sort_order', axis=1)
####        show_df = show_df[display_cols].reset_index(drop=True)
####
####        # ---- CSS to avoid horizontal scroll ----
####        st.markdown("""
####            <style>
####            .stDataEditor {
####                width: 100% !important;
####            }
####            table {
####                table-layout: fixed;
####                width: 100% !important;
####            }
####            th, td {
####                text-align: center !important;
####                font-size: 12px !important;
####                padding: 4px !important;
####            }
####            </style>
####        """, unsafe_allow_html=True)
####
####        # ---- Editable table ----
####        edited_df = st.data_editor(
####            show_df,
####            key="tab5_editor_single",
####            column_config={
####                "Remaining Days": st.column_config.NumberColumn("Remain", min_value=0),
####                "Target": st.column_config.NumberColumn("Tgt", min_value=0),
####                "ECR_Display": st.column_config.TextColumn("ECR"),
####                "Reimb_Display": st.column_config.TextColumn("Reimb"),
####                "Bill_Display": st.column_config.TextColumn("Bill"),
####                "Current_Avg": st.column_config.NumberColumn("Curr Avg", format="%.2f"),
####                "Target_Cases": st.column_config.NumberColumn("Tgt Cases", format="%d"),
####                "Cases_Required": st.column_config.NumberColumn("Cases Req", format="%d"),
####                "CPD": st.column_config.NumberColumn("CPD", format="%.2f"),
####            },
####            disabled=[
####                "Manager", "Agent", "Cases",
####                "ECR_Display", "Reimb_Display", "Bill_Display",
####                "Days", "Src", "Current_Avg", 
####                "Target_Cases", "Cases_Required", "CPD"
####            ],
####            width="stretch"
####        )
####
####        # ---- Persist edits ----
####        if edited_df is not None:
####            if "Agent" not in edited_df.columns:
####                st.error("Editor must include the 'Agent' column to map edits back.")
####            else:
####                edited_map = edited_df.set_index("Agent")[["Remaining Days", "Target"]].copy()
####                edited_map["Remaining Days"] = pd.to_numeric(edited_map["Remaining Days"], errors="coerce").fillna(0)
####                edited_map["Target"] = pd.to_numeric(edited_map["Target"], errors="coerce").fillna(0)
####
####                ss = st.session_state["tab5_df"].copy().set_index("Agent")
####                updated = False
####
####                for agent in edited_map.index:
####                    if agent in ss.index:
####                        new_rem = edited_map.at[agent, "Remaining Days"]
####                        new_tgt = edited_map.at[agent, "Target"]
####
####                        old_rem = pd.to_numeric(ss.at[agent, "Remaining Days"], errors="coerce")
####                        old_tgt = pd.to_numeric(ss.at[agent, "Target"], errors="coerce")
####
####                        if pd.isna(old_rem): old_rem = 0
####                        if pd.isna(old_tgt): old_tgt = 0
####
####                        if (old_rem != new_rem) or (old_tgt != new_tgt):
####                            ss.at[agent, "Remaining Days"] = new_rem
####                            ss.at[agent, "Target"] = new_tgt
####                            updated = True
####                
####                if updated:
####                    st.session_state["tab5_df"] = ss.reset_index()
####                    st.rerun()
##
##
##    with tab5:
##        st.subheader("📊 Avg per Day by Agent (live recalc)")
##
##        # ---- Build base agent_stats with Manager ----
##        agent_cases = (
##            df.groupby(["Manager", "Full Name"])["Case Number"]
##              .count()
##              .reset_index(name="Cases")
##        )
##
##        agent_split = (
##            df.groupby(["Manager", "Full Name", "ECR_Category"])["Case Number"]
##              .count()
##              .unstack(fill_value=0)
##              .reset_index()
##        )
##
##        # Canonicalize agent_split columns
##        col_map = {}
##        for c in agent_split.columns:
##            if str(c).strip().lower() == "full name":
##                col_map[c] = "Full Name"
##            elif str(c).strip().lower() == "manager":
##                col_map[c] = "Manager"
##            elif str(c).strip().lower() == "ecr":
##                col_map[c] = "ECR"
##            elif str(c).strip().lower() in {"reimb", "reimbursement"}:
##                col_map[c] = "Reimbursement"
##            elif str(c).strip().lower() in {"bill", "billing"}:
##                col_map[c] = "Billing"
##        agent_split = agent_split.rename(columns=col_map)
##
##        for col in ["ECR", "Reimbursement", "Billing"]:
##            if col not in agent_split.columns:
##                agent_split[col] = 0
##
##        agent_stats = pd.merge(agent_cases, agent_split, on=["Manager", "Full Name"], how="left")
##
##        # ---- Calculate percentages for categories ----
##        agent_stats["ECR_pct"] = (agent_stats["ECR"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
##        agent_stats["Reimb_pct"] = (agent_stats["Reimbursement"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
##        agent_stats["Bill_pct"] = (agent_stats["Billing"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
##
##        # ---- Combine Case + % for display ----
##        agent_stats["ECR_Display"] = agent_stats["ECR"].astype(int).astype(str) + " (" + agent_stats["ECR_pct"].astype(str) + "%)"
##        agent_stats["Reimb_Display"] = agent_stats["Reimbursement"].astype(int).astype(str) + " (" + agent_stats["Reimb_pct"].astype(str) + "%)"
##        agent_stats["Bill_Display"] = agent_stats["Billing"].astype(int).astype(str) + " (" + agent_stats["Bill_pct"].astype(str) + "%)"
##
##        # ---- Days worked (calculated by default) ----
##        default_days = df.groupby("Full Name")["CloseDate"].nunique().reset_index(name="Days")
##        default_days["Src"] = "Calculated"
##        agent_stats = pd.merge(agent_stats, default_days, on="Full Name", how="left")
##
##        # ---- Optional uploaded days override ----
##        days_file = st.file_uploader("📂 Upload Agent Days Worked file (optional)", type=["xlsx", "csv"], key="days_upload")
##        if days_file is not None:
##            try:
##                if days_file.name.endswith(".xlsx"):
##                    custom_days = pd.read_excel(days_file)
##                else:
##                    custom_days = pd.read_csv(days_file)
##
##                custom_days.columns = custom_days.columns.str.strip()
##
##                if "Full Name" in custom_days.columns and "Days" in custom_days.columns:
##                    custom_days = custom_days[["Full Name", "Days"]].copy()
##                    custom_days["Src"] = "Uploaded"
##                    custom_days["Days"] = pd.to_numeric(custom_days["Days"], errors="coerce")
##
##                    # Normalize names for safer match
##                    agent_stats["Full Name_norm"] = agent_stats["Full Name"].str.strip().str.lower()
##                    custom_days["Full Name_norm"] = custom_days["Full Name"].str.strip().str.lower()
##
##                    agent_stats = agent_stats.merge(
##                        custom_days[["Full Name_norm", "Days", "Src"]],
##                        on="Full Name_norm", how="left", suffixes=("", "_Uploaded")
##                    )
##
##                    # Prefer uploaded values if present, otherwise keep calculated
##                    agent_stats["Days"] = agent_stats["Days_Uploaded"].combine_first(agent_stats["Days"])
##                    agent_stats["Src"] = agent_stats["Src_Uploaded"].combine_first(agent_stats["Src"])
##
##                    # Clean temp columns
##                    agent_stats = agent_stats.drop(
##                        columns=[c for c in ["Full Name_norm", "Days_Uploaded", "Src_Uploaded"] if c in agent_stats.columns]
##                    )
##            except Exception as e:
##                st.warning(f"⚠️ Could not read uploaded days file: {e}")
##
##        # ---- Calculation function ----
##        def recalc_df(d):
##            d = d.copy()
##            d["Days"] = pd.to_numeric(d["Days"], errors="coerce").fillna(0)
##            d["Remaining Days"] = pd.to_numeric(d.get("Remaining Days", 0), errors="coerce").fillna(0)
##            d["Target"] = pd.to_numeric(d.get("Target", 0), errors="coerce").fillna(0)
##            d["Cases"] = pd.to_numeric(d["Cases"], errors="coerce").fillna(0)
##
##            d["Current_Avg"] = (d["Cases"] / d["Days"].replace(0, np.nan)).round(2).fillna(0)
##            d["Target_Cases"] = ((d["Days"] + d["Remaining Days"]) * d["Target"]).round(0)
##            d["Cases_Required"] = (d["Target_Cases"] - d["Cases"]).clip(lower=0).astype(int)
##            d["CPD"] = (d["Cases_Required"] / d["Remaining Days"].replace(0, np.nan)).round(2).fillna(0)
##
##            d["Cases"] = d["Cases"].astype(int, errors="ignore")
##            return d
##
##        # ---- Always rebuild from filtered df, but preserve edits ----
##        agent_stats["Remaining Days"] = 10
##        agent_stats["Target"] = 8
##        fresh_df = agent_stats.rename(columns={"Full Name": "Agent"}).copy()
##
##        if "tab5_df" in st.session_state:
##            edited_map = st.session_state["tab5_df"].set_index("Agent")[["Remaining Days", "Target"]]
##            fresh_df = fresh_df.set_index("Agent")
##            for agent in edited_map.index:
##                if agent in fresh_df.index:
##                    fresh_df.at[agent, "Remaining Days"] = edited_map.at[agent, "Remaining Days"]
##                    fresh_df.at[agent, "Target"] = edited_map.at[agent, "Target"]
##            fresh_df = fresh_df.reset_index()
##
##        st.session_state["tab5_df"] = fresh_df
##        st.session_state["tab5_original_order"] = fresh_df["Agent"].tolist()
##
##        display_cols = [
##            "Manager", "Agent", "Cases", 
##            "ECR_Display", "Reimb_Display", "Bill_Display",
##            "Days", "Src", "Current_Avg", 
##            "Remaining Days", "Target", 
##            "Target_Cases", "Cases_Required", "CPD"
##        ]
##
##        # ---- Build recalculated view ----
##        calc_df = recalc_df(st.session_state["tab5_df"]).copy()
##        calc_df['sort_order'] = calc_df['Agent'].map(
##            {agent: i for i, agent in enumerate(st.session_state["tab5_original_order"])}
##        )
##        show_df = calc_df.sort_values('sort_order').drop('sort_order', axis=1)
##        show_df = show_df[display_cols].reset_index(drop=True)
##
##        # ---- CSS to avoid horizontal scroll ----
##        st.markdown("""
##            <style>
##            .stDataEditor {
##                width: 100% !important;
##            }
##            table {
##                table-layout: fixed;
##                width: 100% !important;
##            }
##            th, td {
##                text-align: center !important;
##                font-size: 12px !important;
##                padding: 4px !important;
##            }
##            </style>
##        """, unsafe_allow_html=True)
##
##        # ---- Editable table ----
##        edited_df = st.data_editor(
##            show_df,
##            key="tab5_editor_single",
##            column_config={
##                "Remaining Days": st.column_config.NumberColumn("Remain", min_value=0),
##                "Target": st.column_config.NumberColumn("Tgt", min_value=0),
##                "ECR_Display": st.column_config.TextColumn("ECR"),
##                "Reimb_Display": st.column_config.TextColumn("Reimb"),
##                "Bill_Display": st.column_config.TextColumn("Bill"),
##                "Current_Avg": st.column_config.NumberColumn("Curr Avg", format="%.2f"),
##                "Target_Cases": st.column_config.NumberColumn("Tgt Cases", format="%d"),
##                "Cases_Required": st.column_config.NumberColumn("Cases Req", format="%d"),
##                "CPD": st.column_config.NumberColumn("CPD", format="%.2f"),
##            },
##            disabled=[
##                "Manager", "Agent", "Cases",
##                "ECR_Display", "Reimb_Display", "Bill_Display",
##                "Days", "Src", "Current_Avg", 
##                "Target_Cases", "Cases_Required", "CPD"
##            ],
##            width="stretch"
##        )
##
##        # ---- Persist edits ----
##        if edited_df is not None:
##            if "Agent" not in edited_df.columns:
##                st.error("Editor must include the 'Agent' column to map edits back.")
##            else:
##                edited_map = edited_df.set_index("Agent")[["Remaining Days", "Target"]].copy()
##                edited_map["Remaining Days"] = pd.to_numeric(edited_map["Remaining Days"], errors="coerce").fillna(0)
##                edited_map["Target"] = pd.to_numeric(edited_map["Target"], errors="coerce").fillna(0)
##
##                ss = st.session_state["tab5_df"].copy().set_index("Agent")
##                updated = False
##
##                for agent in edited_map.index:
##                    if agent in ss.index:
##                        new_rem = edited_map.at[agent, "Remaining Days"]
##                        new_tgt = edited_map.at[agent, "Target"]
##
##                        old_rem = pd.to_numeric(ss.at[agent, "Remaining Days"], errors="coerce")
##                        old_tgt = pd.to_numeric(ss.at[agent, "Target"], errors="coerce")
##
##                        if pd.isna(old_rem): old_rem = 0
##                        if pd.isna(old_tgt): old_tgt = 0
##
##                        if (old_rem != new_rem) or (old_tgt != new_tgt):
##                            ss.at[agent, "Remaining Days"] = new_rem
##                            ss.at[agent, "Target"] = new_tgt
##                            updated = True
##                
##                if updated:
##                    st.session_state["tab5_df"] = ss.reset_index()
##                    st.rerun()
##
##
##
##
##
##    # Trend
##    st.subheader("📈 Trend Over Time (Daily)")
##    trend_df = df.groupby("CloseDate")["Case Number"].count().reset_index(name="Count").sort_values("CloseDate")
##    if trend_df.empty:
##        st.info("No closed-case data in the selected date range.")
##    else:
##        fig_trend = px.line(trend_df, x="CloseDate", y="Count", markers=True)
##        fig_trend.update_xaxes(tickformat="%d-%b-%Y", tickangle=-45)
##        st.plotly_chart(fig_trend, width=True)
##
##    # Table
##    st.subheader("📋 Case Explorer")
##    explorer_cols = ["Level", "Full Name", "Case Number", "Primary Category",
##                     "Secondary Category", "Current Status", "Status",
##                     "Date/Time Opened", "Date/Time Closed", "Manager", "ECR_Category"]
##
##    # filter only columns that exist
##    explorer_cols = [c for c in explorer_cols if c in df.columns]
##
##    if df.empty:
##        st.warning("⚠️ No cases found with the current filters.")
##    elif not explorer_cols:
##        st.warning("⚠️ None of the expected Case Explorer columns are available in the uploaded file.")
##        st.write("Available columns in dataframe:", df.columns.tolist())
##    else:
##        st.dataframe(df[explorer_cols].reset_index(drop=True), use_container_width=True)
##
##
##    # Export
##    csv = df.to_csv(index=False).encode("utf-8")
##    st.download_button("⬇️ Download Filtered Data", data=csv, file_name="filtered_cases.csv", mime="text/csv")
##
##else:
##    st.info("Please upload an Excel file to get started.")


import io
import os
from datetime import date
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# ---------- Page Config ----------
st.set_page_config(page_title="Case Dashboard", layout="wide")

# ---------- Constants ----------
STORED_FILE = "stored_df.pkl"

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

def try_parse_dates(series: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(series, format="%m/%d/%Y %I:%M %p", errors="coerce")
    if parsed.isna().any():
        parsed2 = pd.to_datetime(series, format="%m/%d/%Y", errors="coerce")
        parsed = parsed.fillna(parsed2)
    if parsed.isna().any():
        parsed2 = pd.to_datetime(series, errors="coerce")
        parsed = parsed.fillna(parsed2)
    return parsed

# ---------- Helpers ----------
def categorize_level_to_ecr(level):
    ecr_names = {
        "customer relations escalation",
        "vr partner executive escalation",
        "vr traveler executive escalation",
        "partner consultation",
        "social media",
        "social media escalation",
        "customer reviews",
        "traveler consultation"
    }

    billing_names = {
        "accounting details",
        "fraud payment",
        "payment vendor",
        "payment escalation",
        "regional billing",
        "refund research"
    }

    if pd.isna(level) or str(level).strip() == "":
        return "Reimbursement"

    level_clean = str(level).strip().lower()

    if level_clean in ecr_names:
        return "ECR"
    elif level_clean in billing_names:
        return "Billing"
    else:
        return "Reimbursement"


def normalize_input_df(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()

    # normalize column names (strip spaces)
    df2.columns = df2.columns.str.strip()

    # Ensure expected columns exist; if not, create them safely
    expected = ["Case Number", "Level", "Full Name", "Primary Category", "Secondary Category",
                "Current Status", "Status", "Date/Time Opened", "Date/Time Closed"]
    for col in expected:
        if col not in df2.columns:
            df2[col] = np.nan

    # Cast types and fillna
    df2["Case Number"] = df2["Case Number"].astype(str).fillna("").replace("nan", "")
    df2["Level"] = df2["Level"].fillna("Unknown").astype(str)
    df2["Full Name"] = df2["Full Name"].fillna("Unknown").astype(str)
    df2["Primary Category"] = df2["Primary Category"].fillna("Unknown").astype(str)
    df2["Secondary Category"] = df2["Secondary Category"].fillna("").astype(str)
    df2["Current Status"] = df2["Current Status"].fillna("").astype(str)
    df2["Status"] = df2["Status"].fillna("Unknown").astype(str)

    # parse dates more flexibly
    df2["Date/Time Opened"] = pd.to_datetime(df2["Date/Time Opened"], format="%m/%d/%Y %I:%M %p", errors="coerce")
    df2["Date/Time Closed"] = pd.to_datetime(df2["Date/Time Closed"], format="%m/%d/%Y %I:%M %p", errors="coerce")


    # Manager mapping and ECR category
    df2["Manager"] = df2["Full Name"].map(manager_map).fillna("Unassigned").astype(str)
    df2["ECR_Category"] = df2["Level"].apply(categorize_level_to_ecr)
    df2["YearMonth"] = df2["Date/Time Closed"].dt.to_period("M").dt.to_timestamp()

    return df2

# ---------- UI ----------
st.title("📊 Power-style Case Dashboard")

# preload stored file into session_state (safe, non-invasive)
if os.path.exists(STORED_FILE) and "stored_df" not in st.session_state:
    try:
        st.session_state["stored_df"] = pd.read_pickle(STORED_FILE)
        # don't show message here to avoid interfering with upload flow
    except Exception as e:
        st.warning(f"Could not load stored snapshot from disk: {e}")

uploaded_file = st.file_uploader("📂 Upload Excel file", type=["xlsx"])

# Determine data source:
df_source = None
uploaded_flag = False  # True when user has uploaded a file this run

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read uploaded file: {e}")
        st.stop()

    df_source = normalize_input_df(df_raw)

    # Ensure CloseDate exists and filter out rows without close date
    if "Date/Time Closed" in df_source.columns:
        df_source["CloseDate"] = df_source["Date/Time Closed"].dt.normalize()
        df_source = df_source[df_source["CloseDate"].notna()].copy()
        if df_source.empty:
            st.warning("Uploaded file has no valid 'Date/Time Closed' values after parsing.")
    else:
        st.error("Uploaded file is missing 'Date/Time Closed' column.")
        st.stop()

    uploaded_flag = True

elif "stored_df" in st.session_state:
    # No upload, but we have previously stored data loaded in session_state
    df_source = st.session_state["stored_df"]
    st.info("Showing stored data (no upload). Upload a file to view live data, or press Clear Stored Data to remove snapshot.")

else:
    st.info("Please upload an Excel file to get started.")
    st.stop()

# At this point df_source exists (either uploaded+normalized or stored snapshot)
df = df_source.copy()  # work on a copy

# Sidebar filters (same logic as your original app)
with st.sidebar.expander("🔎 Filters", expanded=True):
    min_date = df["Date/Time Closed"].min()
    max_date = df["Date/Time Closed"].max()

    default_start = min_date.date() if not pd.isna(min_date) else date.today()
    default_end = max_date.date() if not pd.isna(max_date) else date.today()

    date_range = st.date_input(
        "Closed Date Range",
        [default_start, default_end] if default_start and default_end else [date.today(), date.today()]
    )
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

    start_date = pd.to_datetime(start_date).normalize()
    end_date = pd.to_datetime(end_date).normalize()

    status_values = st.multiselect("Status", options=df["Status"].unique().tolist())
    sel_primary_cat = st.selectbox("Primary Category", ["All"] + sorted(df["Primary Category"].unique().tolist()))
    sel_agent = st.selectbox("Agent", ["All"] + sorted(df["Full Name"].unique().tolist()))
    sel_manager = st.selectbox("Manager", ["All"] + sorted(df["Manager"].unique().tolist()))
    sel_ecr = st.selectbox("ECR Category", ["All", "ECR", "Reimbursement", "Billing"])

# Apply filters (same as before)
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

# --- Buttons: Store / Clear (non-invasive) ---
# These buttons operate on the CURRENT filtered df, but they DO NOT override the view when a user uploads a file.
c1, c2 = st.columns([1,1])
with c1:
    if st.button("💾 Store Current Data"):
        try:
            st.session_state["stored_df"] = df.copy()
            st.session_state["stored_df"].to_pickle(STORED_FILE)
            st.success("✅ Data stored successfully (saved to disk).")
        except Exception as e:
            st.error(f"Could not store data: {e}")
with c2:
    if st.button("🗑️ Clear Stored Data"):
        if "stored_df" in st.session_state:
            del st.session_state["stored_df"]
        if os.path.exists(STORED_FILE):
            try:
                os.remove(STORED_FILE)
            except Exception as e:
                st.warning(f"Could not remove stored file: {e}")
        st.info("🧹 Stored data cleared from memory and disk (if present).")

# NOTE: We DO NOT automatically override user's uploaded view with stored snapshot.
# The stored snapshot only becomes the source when there is NO upload (see logic above).

# KPIs
total_cases = len(df)
managers = int(df["Manager"].nunique())
agents = int(df["Full Name"].nunique())
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
    mgr_counts = df.groupby("Manager")["Case Number"].count().reset_index(name="Count")
    fig_mgr = px.bar(mgr_counts, x="Count", y="Manager", orientation="h", color="Count", color_continuous_scale="Blues")
    st.plotly_chart(fig_mgr, width=True)

with tab2:
    cat_counts = df.groupby("Primary Category")["Case Number"].count().reset_index(name="Count")
    fig_cat = px.bar(cat_counts, x="Count", y="Primary Category", orientation="h", color="Count", color_continuous_scale="Teal")
    st.plotly_chart(fig_cat, width=True)

with tab3:
    agent_counts = df.groupby("Full Name")["Case Number"].count().reset_index(name="Count").sort_values("Count", ascending=False).head(20)
    fig_agent = px.bar(agent_counts, x="Count", y="Full Name", orientation="h", color="Count", color_continuous_scale="Viridis")
    st.plotly_chart(fig_agent, width=True)

with tab4:
    ecr_counts = df["ECR_Category"].value_counts().reset_index()
    ecr_counts.columns = ["Category", "Count"]
    fig_ecr = px.pie(
        ecr_counts, names="Category", values="Count", hole=0.4,
        color_discrete_map={"ECR":"#ff7f0e","Reimbursement":"#1f77b4","Billing":"#2ca02c"}
    )
    st.plotly_chart(fig_ecr, width=True)

    agent_split = (
        df.groupby(["Full Name", "ECR_Category"])["Case Number"]
        .count()
        .unstack(fill_value=0)
        .reset_index()
    )

    # normalize possible column names and ensure canonical names
    col_map = {}
    for c in agent_split.columns:
        if str(c).strip().lower() in {"reimb", "reimbursement"}:
            col_map[c] = "Reimbursement"
        elif str(c).strip().lower() in {"bill", "billing"}:
            col_map[c] = "Billing"
        elif str(c).strip().lower() in {"ecr"}:
            col_map[c] = "ECR"
    agent_split = agent_split.rename(columns=col_map)

    for col in ["ECR", "Reimbursement", "Billing"]:
        if col not in agent_split.columns:
            agent_split[col] = 0

    agent_split["Total_Cases"] = agent_split[["ECR", "Reimbursement", "Billing"]].sum(axis=1)

    def format_count_percent(row, col):
        if row["Total_Cases"] == 0:
            return "0 (0.00%)"
        pct = round(row[col] / row["Total_Cases"] * 100, 2)
        return f"{int(row[col])} ({pct:.2f}%)"

    for col in ["ECR", "Reimbursement", "Billing"]:
        agent_split[col] = agent_split.apply(lambda r: format_count_percent(r, col), axis=1)

    st.subheader("🔹 Agent-wise Split (Count + %)")
    if "Full Name" in agent_split.columns:
        display_df = agent_split[["Full Name", "ECR", "Reimbursement", "Billing", "Total_Cases"]].copy()
        display_df = display_df.sort_values("Total_Cases", ascending=False).reset_index(drop=True)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("⚠️ No 'Full Name' column found in agent split table.")


with tab5:
    st.subheader("📊 Avg per Day by Agent (live recalc)")

    # ---- Build base agent_stats with Manager ----
    agent_cases = (
        df.groupby(["Manager", "Full Name"])["Case Number"]
          .count()
          .reset_index(name="Cases")
    )

    agent_split = (
        df.groupby(["Manager", "Full Name", "ECR_Category"])["Case Number"]
          .count()
          .unstack(fill_value=0)
          .reset_index()
    )

    # Canonicalize agent_split columns
    col_map = {}
    for c in agent_split.columns:
        if str(c).strip().lower() == "full name":
            col_map[c] = "Full Name"
        elif str(c).strip().lower() == "manager":
            col_map[c] = "Manager"
        elif str(c).strip().lower() == "ecr":
            col_map[c] = "ECR"
        elif str(c).strip().lower() in {"reimb", "reimbursement"}:
            col_map[c] = "Reimbursement"
        elif str(c).strip().lower() in {"bill", "billing"}:
            col_map[c] = "Billing"
    agent_split = agent_split.rename(columns=col_map)

    for col in ["ECR", "Reimbursement", "Billing"]:
        if col not in agent_split.columns:
            agent_split[col] = 0

    agent_stats = pd.merge(agent_cases, agent_split, on=["Manager", "Full Name"], how="left")

    # ---- Calculate percentages for categories ----
    agent_stats["ECR_pct"] = (agent_stats["ECR"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
    agent_stats["Reimb_pct"] = (agent_stats["Reimbursement"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)
    agent_stats["Bill_pct"] = (agent_stats["Billing"] / agent_stats["Cases"].replace(0, np.nan) * 100).round(1).fillna(0)

    # ---- Combine Case + % for display ----
    agent_stats["ECR_Display"] = agent_stats["ECR"].astype(int).astype(str) + " (" + agent_stats["ECR_pct"].astype(str) + "%)"
    agent_stats["Reimb_Display"] = agent_stats["Reimbursement"].astype(int).astype(str) + " (" + agent_stats["Reimb_pct"].astype(str) + "%)"
    agent_stats["Bill_Display"] = agent_stats["Billing"].astype(int).astype(str) + " (" + agent_stats["Bill_pct"].astype(str) + "%)"

    # ---- Days worked (calculated by default) ----
    default_days = df.groupby("Full Name")["CloseDate"].nunique().reset_index(name="Days")
    default_days["Src"] = "Calculated"
    agent_stats = pd.merge(agent_stats, default_days, on="Full Name", how="left")

    # ---- Optional uploaded days override ----
    days_file = st.file_uploader("📂 Upload Agent Days Worked file (optional)", type=["xlsx", "csv"], key="days_upload")
    if days_file is not None:
        try:
            if days_file.name.endswith(".xlsx"):
                custom_days = pd.read_excel(days_file)
            else:
                custom_days = pd.read_csv(days_file)

            custom_days.columns = custom_days.columns.str.strip()

            if "Full Name" in custom_days.columns and "Days" in custom_days.columns:
                custom_days = custom_days[["Full Name", "Days"]].copy()
                custom_days["Src"] = "Uploaded"
                custom_days["Days"] = pd.to_numeric(custom_days["Days"], errors="coerce")

                # Normalize names for safer match
                agent_stats["Full Name_norm"] = agent_stats["Full Name"].str.strip().str.lower()
                custom_days["Full Name_norm"] = custom_days["Full Name"].str.strip().str.lower()

                agent_stats = agent_stats.merge(
                    custom_days[["Full Name_norm", "Days", "Src"]],
                    on="Full Name_norm", how="left", suffixes=("", "_Uploaded")
                )

                # Prefer uploaded values if present, otherwise keep calculated
                agent_stats["Days"] = agent_stats["Days_Uploaded"].combine_first(agent_stats["Days"])
                agent_stats["Src"] = agent_stats["Src_Uploaded"].combine_first(agent_stats["Src"])

                # Clean temp columns
                agent_stats = agent_stats.drop(
                    columns=[c for c in ["Full Name_norm", "Days_Uploaded", "Src_Uploaded"] if c in agent_stats.columns]
                )
        except Exception as e:
            st.warning(f"⚠️ Could not read uploaded days file: {e}")

    # ---- Calculation function ----
    def recalc_df(d):
        d = d.copy()
        d["Days"] = pd.to_numeric(d["Days"], errors="coerce").fillna(0)
        d["Remaining Days"] = pd.to_numeric(d.get("Remaining Days", 0), errors="coerce").fillna(0)
        d["Target"] = pd.to_numeric(d.get("Target", 0), errors="coerce").fillna(0)
        d["Cases"] = pd.to_numeric(d["Cases"], errors="coerce").fillna(0)

        d["Current_Avg"] = (d["Cases"] / d["Days"].replace(0, np.nan)).round(2).fillna(0)
        d["Target_Cases"] = ((d["Days"] + d["Remaining Days"]) * d["Target"]).round(0)
        d["Cases_Required"] = (d["Target_Cases"] - d["Cases"]).clip(lower=0).astype(int)
        d["CPD"] = (d["Cases_Required"] / d["Remaining Days"].replace(0, np.nan)).round(2).fillna(0)

        d["Cases"] = d["Cases"].astype(int, errors="ignore")
        return d

    # ---- Always rebuild from filtered df, but preserve edits ----
    agent_stats["Remaining Days"] = 3
    agent_stats["Target"] = 8
    fresh_df = agent_stats.rename(columns={"Full Name": "Agent"}).copy()

    if "tab5_df" in st.session_state:
        edited_map = st.session_state["tab5_df"].set_index("Agent")[["Remaining Days", "Target"]]
        fresh_df = fresh_df.set_index("Agent")
        for agent in edited_map.index:
            if agent in fresh_df.index:
                fresh_df.at[agent, "Remaining Days"] = edited_map.at[agent, "Remaining Days"]
                fresh_df.at[agent, "Target"] = edited_map.at[agent, "Target"]
        fresh_df = fresh_df.reset_index()

    st.session_state["tab5_df"] = fresh_df
    st.session_state["tab5_original_order"] = fresh_df["Agent"].tolist()

    display_cols = [
        "Manager", "Agent", "Cases",
        "ECR_Display", "Reimb_Display", "Bill_Display",
        "Days", "Src", "Current_Avg",
        "Remaining Days", "Target",
        "Target_Cases", "Cases_Required", "CPD"
    ]

    

    # ---- Build recalculated view ----
    calc_df = recalc_df(st.session_state["tab5_df"]).copy()
    calc_df['sort_order'] = calc_df['Agent'].map(
        {agent: i for i, agent in enumerate(st.session_state["tab5_original_order"])}
    )
    show_df = calc_df.sort_values('sort_order').drop('sort_order', axis=1)
    show_df = show_df[display_cols].reset_index(drop=True)

        # ---- Chart: Average Cases per Day by Agent ----
    avg_chart_df = calc_df[["Agent", "Current_Avg"]].copy()
    avg_chart_df = avg_chart_df.sort_values("Current_Avg", ascending=False).head(20)  # top 20 agents

    st.subheader("📊 Average Cases per Day (Top 20 Agents)")
    fig_avg = px.bar(
        avg_chart_df,
        x="Current_Avg",
        y="Agent",
        orientation="h",
        color="Current_Avg",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_avg, use_container_width=True)


    # ---- CSS to avoid horizontal scroll ----
    st.markdown("""
        <style>
        .stDataEditor {
            width: 100% !important;
        }
        table {
            table-layout: fixed;
            width: 100% !important;
        }
        th, td {
            text-align: center !important;
            font-size: 12px !important;
            padding: 4px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---- Editable table ----
    edited_df = st.data_editor(
        show_df,
        key="tab5_editor_single",
        column_config={
            "Remaining Days": st.column_config.NumberColumn("Remain", min_value=0),
            "Target": st.column_config.NumberColumn("Tgt", min_value=0),
            "ECR_Display": st.column_config.TextColumn("ECR"),
            "Reimb_Display": st.column_config.TextColumn("Reimb"),
            "Bill_Display": st.column_config.TextColumn("Bill"),
            "Current_Avg": st.column_config.NumberColumn("Curr Avg", format="%.2f"),
            "Target_Cases": st.column_config.NumberColumn("Tgt Cases", format="%d"),
            "Cases_Required": st.column_config.NumberColumn("Cases Req", format="%d"),
            "CPD": st.column_config.NumberColumn("CPD", format="%.2f"),
        },
        disabled=[
            "Manager", "Agent", "Cases",
            "ECR_Display", "Reimb_Display", "Bill_Display",
            "Days", "Src", "Current_Avg",
            "Target_Cases", "Cases_Required", "CPD"
        ],
        width="stretch"
    )

    # ---- Persist edits ----
    if edited_df is not None:
        if "Agent" not in edited_df.columns:
            st.error("Editor must include the 'Agent' column to map edits back.")
        else:
            edited_map = edited_df.set_index("Agent")[["Remaining Days", "Target"]].copy()
            edited_map["Remaining Days"] = pd.to_numeric(edited_map["Remaining Days"], errors="coerce").fillna(0)
            edited_map["Target"] = pd.to_numeric(edited_map["Target"], errors="coerce").fillna(0)

            ss = st.session_state["tab5_df"].copy().set_index("Agent")
            updated = False

            for agent in edited_map.index:
                if agent in ss.index:
                    new_rem = edited_map.at[agent, "Remaining Days"]
                    new_tgt = edited_map.at[agent, "Target"]

                    old_rem = pd.to_numeric(ss.at[agent, "Remaining Days"], errors="coerce")
                    old_tgt = pd.to_numeric(ss.at[agent, "Target"], errors="coerce")

                    if pd.isna(old_rem): old_rem = 0
                    if pd.isna(old_tgt): old_tgt = 0

                    if (old_rem != new_rem) or (old_tgt != new_tgt):
                        ss.at[agent, "Remaining Days"] = new_rem
                        ss.at[agent, "Target"] = new_tgt
                        updated = True

            if updated:
                st.session_state["tab5_df"] = ss.reset_index()
                st.rerun()




# Trend
st.subheader("📈 Trend Over Time (Daily)")
trend_df = df.groupby("CloseDate")["Case Number"].count().reset_index(name="Count").sort_values("CloseDate")
if trend_df.empty:
    st.info("No closed-case data in the selected date range.")
else:
    fig_trend = px.line(trend_df, x="CloseDate", y="Count", markers=True)
    fig_trend.update_xaxes(tickformat="%d-%b-%Y", tickangle=-45)
    st.plotly_chart(fig_trend, width=True)

# Table
st.subheader("📋 Case Explorer")
explorer_cols = ["Level", "Full Name", "Case Number", "Primary Category",
                 "Secondary Category", "Current Status", "Status",
                 "Date/Time Opened", "Date/Time Closed", "Manager", "ECR_Category"]

# filter only columns that exist
explorer_cols = [c for c in explorer_cols if c in df.columns]

if df.empty:
    st.warning("⚠️ No cases found with the current filters.")
elif not explorer_cols:
    st.warning("⚠️ None of the expected Case Explorer columns are available in the uploaded file.")
    st.write("Available columns in dataframe:", df.columns.tolist())
else:
    st.dataframe(df[explorer_cols].reset_index(drop=True), use_container_width=True)

# Export
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data", data=csv, file_name="filtered_cases.csv", mime="text/csv")

