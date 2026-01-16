
import streamlit as st
import plotly.express as px

AGG_MAP = {
    "sum": "sum",
    "avg": "mean",
    "average": "mean",
    "mean": "mean",
    "count": "count",
    "min": "min",
    "max": "max"
}

def render_dashboard(df, spec):
    st.markdown(f"## {spec.get('title','Dashboard')}")

    # Slicers
    for col in spec.get("slicers", []):
        if col in df.columns:
            df = df[df[col].isin(
                st.multiselect(col, df[col].unique(), df[col].unique())
            )]

    # KPIs
    kpis = spec.get("kpis", [])
    if kpis:
        cols = st.columns(len(kpis))
        for i, k in enumerate(kpis):
            field = k.get("field")
            agg = AGG_MAP.get(k.get("agg","sum"), "sum")
            if field in df.columns:
                try:
                    val = getattr(df[field], agg)()
                    cols[i].metric(field, f"{val:,.2f}")
                except:
                    cols[i].metric(field, "N/A")

    # Charts
    for c in spec.get("charts", []):
        try:
            if c["type"] == "line" and c["x"] in df.columns and c["y"] in df.columns:
                st.plotly_chart(px.line(df, x=c["x"], y=c["y"]), use_container_width=True)
            elif c["type"] == "bar" and c["x"] in df.columns and c["y"] in df.columns:
                st.plotly_chart(px.bar(df, x=c["x"], y=c["y"]), use_container_width=True)
            elif c["type"] == "pie" and c["names"] in df.columns and c["values"] in df.columns:
                st.plotly_chart(px.pie(df, names=c["names"], values=c["values"]), use_container_width=True)
        except:
            st.warning("One chart could not be rendered due to invalid config.")
