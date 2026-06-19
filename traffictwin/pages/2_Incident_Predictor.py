import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Incident Predictor", layout="wide")

# -----------------------------
# Load Data
# -----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/train.csv")

    for col in [
        "event_type",
        "event_cause",
        "zone",
        "junction",
        "veh_type"
    ]:
        df[col] = df[col].fillna("Unknown")

    return df

df = load_data()

# -----------------------------
# Load Models
# -----------------------------

priority_model = joblib.load(
    "models/priority_model.pkl"
)

closure_model = joblib.load(
    "models/closure_model.pkl"
)

# -----------------------------
# UI
# -----------------------------

st.title("🚨 Incident Impact Predictor")

st.markdown(
    "Predict incident severity and road closure risk."
)

col1, col2 = st.columns(2)

with col1:

    event_type = st.selectbox(
        "Event Type",
        sorted(df["event_type"].unique())
    )

    event_cause = st.selectbox(
        "Event Cause",
        sorted(df["event_cause"].unique())
    )

    zone = st.selectbox(
        "Zone",
        sorted(df["zone"].unique())
    )

    junction = st.selectbox(
        "Junction",
        sorted(df["junction"].unique())
    )

with col2:

    veh_type = st.selectbox(
        "Vehicle Type",
        sorted(df["veh_type"].unique())
    )

    hour = st.slider(
        "Hour",
        0,
        23,
        12
    )

    weekday = st.selectbox(
        "Weekday",
        [
            ("Monday",0),
            ("Tuesday",1),
            ("Wednesday",2),
            ("Thursday",3),
            ("Friday",4),
            ("Saturday",5),
            ("Sunday",6)
        ],
        format_func=lambda x: x[0]
    )

    month = st.selectbox(
        "Month",
        list(range(1,13))
    )

# -----------------------------
# Predict
# -----------------------------

if st.button("Predict Impact"):

    input_df = pd.DataFrame([{
        "event_type": event_type,
        "event_cause": event_cause,
        "zone": zone,
        "junction": junction,
        "veh_type": veh_type,
        "hour": hour,
        "weekday": weekday[1],
        "month": month
    }])

    priority_prob = (
        priority_model.predict_proba(input_df)[0][1]
    )

    closure_prob = (
        closure_model.predict_proba(input_df)[0][1]
    )
    st.divider()

    st.subheader("🧠 Recommended Actions")

    if priority_prob > 0.8:

        st.warning("""
        • Deploy additional traffic personnel

        • Monitor congestion continuously

        • Alert nearby traffic control room
        """)

    elif priority_prob > 0.5:

        st.info("""
        • Monitor traffic conditions

        • Keep response unit on standby
        """)

    else:

        st.success("""
        • Routine monitoring sufficient
        """)

        st.divider()

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "🚨 Priority Risk",
            f"{priority_prob*100:.1f}%"
        )

    with c2:
        st.metric(
            "🚧 Road Closure Risk",
            f"{closure_prob*100:.1f}%"
        )

    # Impact Category

    impact_score = (
        0.7 * priority_prob +
        0.3 * closure_prob
    )

    if impact_score > 0.75:
        st.error("🔴 HIGH IMPACT INCIDENT")
    elif impact_score > 0.45:
        st.warning("🟠 MEDIUM IMPACT INCIDENT")
    else:
        st.success("🟢 LOW IMPACT INCIDENT")
st.markdown("---")

st.caption(
    "TrafficTwin Bengaluru | AI-Powered Traffic Incident Intelligence Platform"
)