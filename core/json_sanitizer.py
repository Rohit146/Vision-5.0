
import json

def sanitize_json(text):
    try:
        obj = json.loads(text)
    except:
        text = text[text.find("{"):text.rfind("}")+1]
        obj = json.loads(text)

    # Hard defaults
    obj.setdefault("title", "Dashboard")
    obj.setdefault("kpis", [])
    obj.setdefault("slicers", [])
    obj.setdefault("charts", [])
    return obj
