import zipfile, tempfile, shutil, os, json

BASE_TEMPLATE = "templates/base.pbit"

def build_pbit(spec, df, output_path):
    temp = tempfile.mkdtemp()
    with zipfile.ZipFile(BASE_TEMPLATE) as z:
        z.extractall(temp)

    layout = os.path.join(temp, "Report", "Layout")
    os.makedirs(os.path.dirname(layout), exist_ok=True)
    with open(layout, "w") as f:
        json.dump({"ai_spec": spec}, f)

    with zipfile.ZipFile(output_path, "w") as z:
        for root, _, files in os.walk(temp):
            for file in files:
                p = os.path.join(root, file)
                z.write(p, os.path.relpath(p, temp))
    shutil.rmtree(temp)
