
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
from streamlit_elements import elements, dashboard, mui

st.set_page_config(page_title="AI Power BI Authoring", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp { background:#f3f4f6; font-family:Segoe UI,sans-serif; }
.visual-tile { border:1px solid #ddd; border-radius:6px; padding:6px; cursor:pointer; }
</style>
""", unsafe_allow_html=True)

st.title("AI Power BI–Style Authoring Tool")

# ---------------- DATA ----------------
file = st.file_uploader("Upload CSV / Excel", ["csv","xlsx"])
if not file: st.stop()
df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)

# ---------------- SCHEMA ----------------
def infer_schema(df):
    m,d,dt = [],[],[]
    for c in df.columns:
        if is_datetime64_any_dtype(df[c]): dt.append(c)
        elif is_numeric_dtype(df[c]): m.append(c)
        else: d.append(c)
    return {"measures":m,"dimensions":d,"dates":dt}

schema = infer_schema(df)

# ---------------- SESSION STATE ----------------
if "layout" not in st.session_state:
    st.session_state.layout = []

if "visuals" not in st.session_state:
    st.session_state.visuals = []

# ---------------- ICON PALETTE ----------------
st.sidebar.header("Visuals")
icons = {
    "kpi":"📊 KPI",
    "line":"📈 Line",
    "bar":"📊 Bar"
}

selected = st.sidebar.radio("Add visual", list(icons.keys()), format_func=lambda x: icons[x])

if st.sidebar.button("Add Visual"):
    vid = f"v{len(st.session_state.visuals)+1}"
    st.session_state.visuals.append({
        "id":vid,
        "type":selected,
        "x": schema["dates"][0] if schema["dates"] else schema["dimensions"][0],
        "y": schema["measures"][0],
        "xpos":0,"ypos":0,"w":3,"h":2
    })

# ---------------- SAVE / LOAD ----------------
st.sidebar.divider()
if st.sidebar.button("Save Layout"):
    config = {"visuals":st.session_state.visuals}
    st.download_button("Download dashboard.json", json.dumps(config,indent=2), "dashboard.json")

uploaded_layout = st.sidebar.file_uploader("Load dashboard.json", type=["json"])
if uploaded_layout:
    loaded = json.load(uploaded_layout)
    st.session_state.visuals = loaded["visuals"]

# ---------------- CANVAS ----------------
with elements("canvas"):
    with dashboard.Grid(cols=12, rowHeight=80):
        for v in st.session_state.visuals:
            with dashboard.Item(v["id"], x=v["xpos"], y=v["ypos"], w=v["w"], h=v["h"]):
                with mui.Paper(elevation=2, sx={"p":1}):
                    if v["type"]=="kpi":
                        mui.Typography(v["y"], variant="subtitle2")
                        mui.Typography(round(df[v["y"]].sum(),2), variant="h4")
                    elif v["type"]=="line":
                        fig = px.line(df, x=v["x"], y=v["y"])
                        st.plotly_chart(fig, use_container_width=True)
                    elif v["type"]=="bar":
                        agg = df.groupby(v["x"])[v["y"]].sum().reset_index()
                        fig = px.bar(agg, x=v["x"], y=v["y"])
                        st.plotly_chart(fig, use_container_width=True)
