
import streamlit as st
import plotly.express as px

def render_dashboard(df, spec):
    st.markdown(f"## {spec.get('title','Dashboard')}")

    # Slicers
    for col in spec.get("slicers", []):
        df = df[df[col].isin(st.multiselect(col, df[col].unique(), df[col].unique()))]

    # KPIs
    cols = st.columns(len(spec.get("kpis", [])))
    for i,k in enumerate(spec.get("kpis", [])):
        val = getattr(df[k["field"]], k["agg"])()
        cols[i].metric(k["field"], f"{val:,.2f}")

    # Charts
    for c in spec.get("charts", []):
        if c["type"] == "line":
            st.plotly_chart(px.line(df, x=c["x"], y=c["y"]), use_container_width=True)
        elif c["type"] == "bar":
            st.plotly_chart(px.bar(df, x=c["x"], y=c["y"]), use_container_width=True)
        elif c["type"] == "pie":
            st.plotly_chart(px.pie(df, names=c["names"], values=c["values"]), use_container_width=True)
