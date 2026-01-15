
import json
def build_prompt(model):
    return f"""
You are a senior BI architect inspired by Power BI.

Design a PROFESSIONAL dashboard spec in STRICT JSON:
- KPI cards
- Line charts
- Bar charts
- Pie charts
- Slicers

Schema:
{json.dumps(model, indent=2)}

Return JSON only:
{{
 "title": "...",
 "kpis": [{{"field":"", "agg":"sum"}}],
 "slicers": ["column"],
 "charts": [
   {{"type":"line","x":"","y":""}},
   {{"type":"bar","x":"","y":""}},
   {{"type":"pie","names":"","values":""}}
 ]
}}
"""
