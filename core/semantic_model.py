
def build_semantic_model(profile):
    measures, dimensions, dates = [], [], []
    for c in profile["columns"]:
        n = c["name"].lower()
        t = c["dtype"]
        if "date" in n:
            dates.append(c["name"])
        elif t.startswith(("int","float")):
            measures.append(c["name"])
        else:
            dimensions.append(c["name"])
    return {
        "measures": measures,
        "dimensions": dimensions,
        "dates": dates
    }
