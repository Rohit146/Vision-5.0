
import streamlit as st
import pandas as pd
from core.profiler import profile_data
from core.semantic_model import build_semantic_model
from core.prompt_builder import build_prompt
from core.openai_client import call_llm
from core.json_sanitizer import sanitize_json
from ui.renderer import render_dashboard

st.set_page_config(layout="wide", page_title="AI Dashboard Studio")

st.title("📊 AI Dashboard Studio (Power BI–Inspired)")

file = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])

if file:
    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
    st.subheader("Data Preview")
    st.dataframe(df.head())

    if st.button("🚀 Generate Professional Dashboard"):
        profile = profile_data(df)
        semantic = build_semantic_model(profile)
        prompt = build_prompt(semantic)
        raw = call_llm(prompt)
        spec = sanitize_json(raw)

        st.session_state["spec"] = spec
        st.session_state["df"] = df

if "spec" in st.session_state:
    render_dashboard(st.session_state["df"], st.session_state["spec"])
