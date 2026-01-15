def build_semantic_model(profile):
    measures, dimensions, dates = [], [], []
    for c in profile["columns"]:
        name = c["name"].lower()
        if "date" in name:
            dates.append(c["name"])
        elif c["dtype"].startswith(("int", "float")):
            measures.append(c["name"])
        else:
            dimensions.append(c["name"])
    return {"measures": measures, "dimensions": dimensions, "dates": dates}
