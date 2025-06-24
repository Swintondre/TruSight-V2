# log_dashboard.py (Streamlit app)
import streamlit as st
import os

LOG_FILE = "data/factflow.log"

st.set_page_config(page_title="FactFlow Log Viewer", layout="wide")
st.title("📊 FactFlow Log Dashboard")

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.readlines()
    
    st.text_area("📄 Log Output", value="".join(logs[-500:]), height=600)
else:
    st.warning("No log file found at 'data/factflow.log'.")
