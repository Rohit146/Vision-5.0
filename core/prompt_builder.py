
import json
def build_prompt(model):
    return f"""
You are a senior BI architect inspired by Power BI.

RULES:
- Use only valid pandas aggregations: sum, mean, min, max, count
- Do NOT invent column names
- Output STRICT JSON only

Schema:
{json.dumps(model, indent=2)}

Return:
{{
 "title": "Dashboard title",
 "kpis": [{{"field":"<measure>","agg":"sum|mean"}}],
 "slicers": ["<dimension>"],
 "charts": [
   {{"type":"line","x":"<date>","y":"<measure>"}},
   {{"type":"bar","x":"<dimension>","y":"<measure>"}},
   {{"type":"pie","names":"<dimension>","values":"<measure>"}}
 ]
}}
"""
