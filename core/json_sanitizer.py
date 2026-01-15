import json
def sanitize_json(text):
    try:
        return json.loads(text)
    except:
        text = text[text.find('{'):text.rfind('}')+1]
        return json.loads(text)
