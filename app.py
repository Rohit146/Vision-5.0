import streamlit as st
import pandas as pd
import tempfile
import os
from core.profiler import profile_data
from core.semantic_model import build_semantic_model
from core.prompt_builder import build_prompt
from core.openai_client import call_llm
from core.json_sanitizer import sanitize_json
from core.pbit_builder import build_pbit

st.set_page_config(page_title="AI → Power BI Generator", layout="wide")
st.title("📊 AI-Powered Power BI Dashboard Generator")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    st.subheader("Preview")
    st.dataframe(df.head())

    if st.button("🚀 Generate Power BI Dashboard"):
        with st.spinner("Analyzing data..."):
            profile = profile_data(df)
            semantic = build_semantic_model(profile)

        with st.spinner("Designing dashboard with AI..."):
            prompt = build_prompt(semantic)
            raw = call_llm(prompt)
            spec = sanitize_json(raw)

        with st.spinner("Building Power BI Template..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pbit") as tmp:
                build_pbit(spec, tmp.name)

            with open(tmp.name, "rb") as f:
                st.download_button(
                    "⬇️ Download Power BI Template (.pbit)",
                    f,
                    file_name="ai_dashboard.pbit"
                )
