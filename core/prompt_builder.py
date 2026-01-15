import json
def build_prompt(model):
    return f"""You are a Power BI architect.
Return STRICT JSON dashboard spec only.
{json.dumps(model, indent=2)}
"""
