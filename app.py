
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype

st.set_page_config(
    page_title="AI Power BI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- UI STYLE --------------------
st.markdown("""
<style>
.stApp { background-color: #f5f6f7; font-family: Segoe UI, sans-serif; }
[data-testid="stMetric"] {
    background: white;
    padding: 14px;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

st.title("AI Power BI–Style Dashboard Generator")

# -------------------- FILE UPLOAD --------------------
file = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])
if not file:
    st.stop()

df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)
st.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")

# -------------------- SCHEMA INFERENCE --------------------
def infer_schema(df):
    measures, dimensions, dates = [], [], []
    for c in df.columns:
        if is_datetime64_any_dtype(df[c]):
            dates.append(c)
        elif is_numeric_dtype(df[c]):
            measures.append(c)
        else:
            dimensions.append(c)
    return {"measures": measures, "dimensions": dimensions, "dates": dates}

schema = infer_schema(df)

# -------------------- LLM DASHBOARD PLAN --------------------
def get_llm_plan(schema, sample):
    if "OPENAI_API_KEY" not in st.secrets:
        return {
            "theme": {"primary":"#118DFF","background":"#FFFFFF"},
            "kpis": schema["measures"][:3],
            "charts": [
                {"type":"line","x":schema["dates"][0],"y":schema["measures"][0]} if schema["dates"] else None,
                {"type":"bar","x":schema["dimensions"][0],"y":schema["measures"][0]} if schema["dimensions"] else None
            ]
        }
    try:
        from openai import OpenAI
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""You are a Power BI dashboard architect.
Schema: {json.dumps(schema)}
Sample data:
{sample.head(5).to_csv(index=False)}
Return ONLY valid JSON with theme, kpis, charts."""
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.1
        )
        return json.loads(r.choices[0].message.content)
    except Exception:
        return {
            "theme":{"primary":"#118DFF","background":"#FFFFFF"},
            "kpis":schema["measures"][:2],
            "charts":[]
        }

plan = get_llm_plan(schema, df)

# -------------------- KPIs --------------------
st.subheader("Key Metrics")
kpi_cols = st.columns(len(plan.get("kpis",[])))
for i,k in enumerate(plan.get("kpis",[])):
    kpi_cols[i].metric(k, round(df[k].sum(),2))

# -------------------- FILTERS --------------------
st.sidebar.header("Filters")
filtered_df = df.copy()
for d in schema["dimensions"]:
    vals = st.sidebar.multiselect(d, sorted(df[d].dropna().unique().tolist()))
    if vals:
        filtered_df = filtered_df[filtered_df[d].isin(vals)]

# -------------------- CHARTS --------------------
st.subheader("Insights")
for ch in plan.get("charts",[]):
    if not ch: 
        continue
    if ch["type"]=="line":
        fig = px.line(filtered_df, x=ch["x"], y=ch["y"], template="plotly_white")
    elif ch["type"]=="bar":
        agg = filtered_df.groupby(ch["x"])[ch["y"]].sum().reset_index()
        fig = px.bar(agg, x=ch["x"], y=ch["y"], template="plotly_white")
    else:
        continue
    st.plotly_chart(fig, use_container_width=True)

# -------------------- EXPORTS --------------------
st.subheader("Power BI Exports")

data_csv = filtered_df.to_csv(index=False).encode("utf-8")
schema_json = json.dumps(schema,indent=2).encode("utf-8")
theme_json = json.dumps({
    "name":"AI Generated Theme",
    "dataColors":[plan["theme"]["primary"]],
    "background":plan["theme"]["background"],
    "foreground":"#000000"
},indent=2).encode("utf-8")

c1,c2,c3 = st.columns(3)
with c1: st.download_button("Download Data",data_csv,"data.csv")
with c2: st.download_button("Download Schema",schema_json,"schema.json")
with c3: st.download_button("Download Power BI Theme",theme_json,"theme.json")

st.info("""Deployment:
- Streamlit Cloud ready
- Add OPENAI_API_KEY in secrets
- Upload → auto dashboard → export to Power BI""")
