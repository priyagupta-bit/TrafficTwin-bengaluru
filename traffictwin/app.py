import streamlit as st

st.set_page_config(
    page_title="TrafficTwin Bengaluru",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 TrafficTwin Bengaluru")

st.markdown("""
### AI-Powered Traffic Incident Intelligence Platform

TrafficTwin helps Bengaluru Traffic Police proactively manage traffic disruptions using historical incident intelligence and machine learning.

### Key Capabilities

✅ Predict Incident Severity

✅ Estimate Road Closure Risk

✅ Identify High-Risk Junctions

✅ Analyze Traffic Incident Patterns

✅ Support Resource Deployment Decisions

---

### Model Performance

| Model | Metric |
|---------|---------|
| Priority Prediction | AUC = 0.845 |
| Road Closure Prediction | AUC = 0.738 |

---

Built using Bengaluru traffic incident data and machine learning.
""")

# ===================================
# Key Features
# ===================================

st.markdown("## 🚀 Key Features")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):
        st.markdown("### 📍 Risk Mapping")
        st.write(
            "Identify congestion-prone locations and traffic hotspots using historical incident intelligence."
        )

    with st.container(border=True):
        st.markdown("### 📚 Historical Intelligence")
        st.write(
            "Retrieve similar historical incidents to understand likely impact and support decision-making."
        )

with col2:

    with st.container(border=True):
        st.markdown("### 🚨 Incident Prediction")
        st.write(
            "Predict incident severity and road closure risk using machine learning models."
        )

    with st.container(border=True):
        st.markdown("### 🚔 Command Center")
        st.write(
            "Generate actionable deployment recommendations for traffic personnel and resources."
        )

