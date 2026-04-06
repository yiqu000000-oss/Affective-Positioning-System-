import streamlit as st

st.set_page_config(page_title="APS Demo", layout="wide")

st.title("Affective Positioning System (APS)")

st.markdown("### Plane 1: Internal State")

need = st.slider("Perceived Need", 0, 10, 5)
stability = st.slider("Emotional Stability", 0, 10, 5)

if st.button("Analyze"):
    if need >= 7 and stability >= 7:
        result = "Secure & Fulfilled"
    elif need >= 7 and stability < 4:
        result = "Anxious Dependency"
    elif need < 4 and stability >= 7:
        result = "Detached Stability"
    else:
        result = "Low Need & Low Stability"

    st.success(f"State: {result}")