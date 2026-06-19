import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Analytics",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/train.csv")

    for col in [
        "event_cause",
        "zone",
        "junction",
        "veh_type"
    ]:
        df[col] = df[col].fillna("Unknown")

    return df

df = load_data()

st.title("📊 Bengaluru Traffic Analytics")

# ---------------------------------
# Event Causes
# ---------------------------------

st.subheader("Top Event Causes")

cause_counts = (
    df["event_cause"]
    .value_counts()
    .reset_index()
)

cause_counts.columns = [
    "event_cause",
    "count"
]

fig = px.bar(
    cause_counts.head(10),
    x="event_cause",
    y="count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------
# Zone Distribution
# ---------------------------------

st.subheader("Incidents by Zone")

zone_counts = (
    df["zone"]
    .value_counts()
    .reset_index()
)

zone_counts.columns = [
    "zone",
    "count"
]

fig = px.pie(
    zone_counts,
    names="zone",
    values="count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------
# Vehicle Types
# ---------------------------------

st.subheader("Vehicle Types")

veh_counts = (
    df["veh_type"]
    .value_counts()
    .reset_index()
)

veh_counts.columns = [
    "veh_type",
    "count"
]

fig = px.bar(
    veh_counts.head(10),
    x="veh_type",
    y="count"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")

st.caption(
    "TrafficTwin Bengaluru | AI-Powered Traffic Incident Intelligence Platform"
)