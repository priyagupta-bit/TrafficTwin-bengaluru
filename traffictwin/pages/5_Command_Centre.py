import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Traffic Command Centre",
    layout="wide"
)

# -----------------------------------
# Load Data
# -----------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/raw/train.csv"
    )

    risk_df = pd.read_csv(
        "data/processed/risk_index.csv"
    )

    return df, risk_df


df, risk_df = load_data()

# -----------------------------------
# Header
# -----------------------------------

st.title("🚔 Bengaluru Traffic Command Centre")

st.markdown(
    "Operational intelligence for proactive traffic management."
)

# -----------------------------------
# KPIs
# -----------------------------------

total_incidents = len(df)

high_priority_rate = (
    (df["priority"] == "High").mean() * 100
)

closure_rate = (
    df["requires_road_closure"]
    .astype(str)
    .str.lower()
    .eq("true")
    .mean() * 100
)

unique_junctions = (
    df["junction"].nunique()
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Incidents",
    f"{total_incidents:,}"
)

c2.metric(
    "High Priority %",
    f"{high_priority_rate:.1f}%"
)

c3.metric(
    "Road Closure %",
    f"{closure_rate:.1f}%"
)

c4.metric(
    "Junctions Monitored",
    unique_junctions
)

st.divider()

# -----------------------------------
# Top Risk Junctions
# -----------------------------------

st.subheader("⚠️ Top Risk Junctions")

top_risk = (
    risk_df
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_risk,
    use_container_width=True
)

st.divider()

# -----------------------------------
# Resource Recommendations
# -----------------------------------

st.subheader(
    "🚦 Resource Allocation Recommendations"
)

for _, row in top_risk.head(5).iterrows():

    risk = row["risk_score"]

    st.markdown(
        f"### {row['junction']}"
    )

    st.write(
        f"Risk Score: {risk:.3f}"
    )

    if risk > 0.65:

        st.error("""
Recommended Actions

• Deploy 2 Traffic Officers

• Continuous Monitoring

• Prepare Diversion Plan

• Keep Tow Vehicle Available
""")

    elif risk > 0.55:

        st.warning("""
Recommended Actions

• Increase Patrol Frequency

• Monitor Peak Hours

• Prepare Response Team
""")

    else:

        st.success("""
Recommended Actions

• Routine Monitoring
""")
st.markdown("---")

st.caption(
    "TrafficTwin Bengaluru | AI-Powered Traffic Incident Intelligence Platform"
)