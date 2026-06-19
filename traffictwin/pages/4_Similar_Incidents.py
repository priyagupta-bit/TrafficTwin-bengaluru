import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap

st.set_page_config(
    page_title="Similar Incidents",
    layout="wide"
)

# ------------------------------------
# Load Data
# ------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/train.csv")

    # Fill missing values
    for col in [
        "event_type",
        "event_cause",
        "zone",
        "junction",
        "veh_type"
    ]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    return df

df = load_data()

# ------------------------------------
# Page Header
# ------------------------------------

st.title("📚 Similar Historical Incidents")

st.markdown("""
Find historical incidents similar to a new traffic event.
This helps traffic authorities understand likely impact based on past cases.
""")

# ------------------------------------
# User Inputs
# ------------------------------------

col1, col2 = st.columns(2)

with col1:
    event_cause = st.selectbox(
        "Event Cause",
        sorted(df["event_cause"].unique())
    )

    zone = st.selectbox(
        "Zone",
        sorted(df["zone"].unique())
    )

with col2:
    veh_type = st.selectbox(
        "Vehicle Type",
        sorted(df["veh_type"].unique())
    )

# ------------------------------------
# Search Similar Incidents
# ------------------------------------

if st.button("Find Similar Incidents"):

    similar = df[
        (df["event_cause"] == event_cause) &
        (df["zone"] == zone)
    ]

    if veh_type != "Unknown":
        similar = similar[
            similar["veh_type"] == veh_type
        ]

    st.divider()

    st.subheader("📋 Similar Historical Cases")

    st.metric(
        "Matching Incidents",
        len(similar)
    )

    if len(similar) == 0:

        st.warning(
            "No similar incidents found."
        )

    else:

        display_cols = []

        for col in [
            "event_type",
            "event_cause",
            "zone",
            "junction",
            "veh_type",
            "priority",
            "requires_road_closure",
            "start_datetime"
        ]:
            if col in similar.columns:
                display_cols.append(col)

        st.dataframe(
            similar[display_cols].head(20),
            use_container_width=True
        )

        # ----------------------------
        # Historical Insights
        # ----------------------------

        st.subheader("📈 Historical Insights")

        colA, colB, colC = st.columns(3)

        # High Priority Rate
        if "priority" in similar.columns:

            high_rate = (
                (similar["priority"] == "High").mean()
                * 100
            )

            colA.metric(
                "High Priority %",
                f"{high_rate:.1f}%"
            )

        # Closure Rate
        if "requires_road_closure" in similar.columns:

            closure_rate = (
                similar["requires_road_closure"]
                .astype(str)
                .str.lower()
                .eq("true")
                .mean()
                * 100
            )

            colB.metric(
                "Road Closure %",
                f"{closure_rate:.1f}%"
            )

        # Junction Count
        colC.metric(
            "Affected Junctions",
            similar["junction"].nunique()
        )

        # ----------------------------
        # Top Junctions
        # ----------------------------
        

        st.subheader("🚦 Most Common Junctions")

        top_junctions = (
            similar["junction"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_junctions.columns = [
            "Junction",
            "Incident Count"
        ]

        st.dataframe(
            top_junctions,
            use_container_width=True
        )

        # ----------------------------
        # Recommendation
        # ----------------------------

        st.subheader("🧠 Operational Recommendation")

        if len(similar) >= 50:

            st.error("""
High frequency historical pattern detected.

Recommended Actions:
• Deploy traffic personnel proactively
• Monitor congestion continuously
• Keep diversion routes ready
• Alert nearby traffic control room
""")

        elif len(similar) >= 20:

            st.warning("""
Moderate historical risk detected.

Recommended Actions:
• Increase monitoring
• Keep response team on standby
• Track traffic buildup
""")

        else:

            st.success("""
Low historical impact detected.

Recommended Actions:
• Routine monitoring sufficient
• No additional deployment required
""")
st.markdown("---")

st.caption(
    "TrafficTwin Bengaluru | AI-Powered Traffic Incident Intelligence Platform"
)
    
