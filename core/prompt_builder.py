import json
def build_prompt(model):
    return f"Design a Power BI dashboard as JSON only.\n{json.dumps(model, indent=2)}"
