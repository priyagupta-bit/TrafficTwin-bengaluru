import streamlit as st
import pandas as pd

st.title("📍 Bengaluru Risk Intelligence")

risk_df = pd.read_csv(
    "data/processed/risk_index.csv"
)

st.subheader("Top High Risk Junctions")

st.dataframe(
    risk_df.head(20),
    use_container_width=True
)

st.bar_chart(
    risk_df.head(10).set_index("junction")["risk_score"]
)
st.markdown("---")

st.caption(
    "TrafficTwin Bengaluru | AI-Powered Traffic Incident Intelligence Platform"
)