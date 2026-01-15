import zipfile, os, json, tempfile, shutil

BASE_TEMPLATE = "templates/base.pbit"

def build_pbit(spec, output_path):
    temp_dir = tempfile.mkdtemp()

    if not os.path.exists(BASE_TEMPLATE):
        raise FileNotFoundError("Base PBIT template missing")

    with zipfile.ZipFile(BASE_TEMPLATE, "r") as z:
        z.extractall(temp_dir)

    layout_path = os.path.join(temp_dir, "Report", "Layout")
    os.makedirs(os.path.dirname(layout_path), exist_ok=True)

    with open(layout_path, "w", encoding="utf-8") as f:
        json.dump({"ai_dashboard_spec": spec}, f, indent=2)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                p = os.path.join(root, file)
                zipf.write(p, os.path.relpath(p, temp_dir))

    shutil.rmtree(temp_dir)
