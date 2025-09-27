# app.py
from pathlib import Path
import gradio as gr
from src import NGramTrie, NGramGenerator

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"

DATASETS = {
    "Female (female.txt)": {
        "files": [DATA_DIR / "female.txt"],
        "desc": (
            "NLTK names corpus (Mark Kantrowitz).\n"
            "Source: https://www.kaggle.com/datasets/nltkdata/names"
        ),
    },
    "Male (male.txt)": {
        "files": [DATA_DIR / "male.txt"],
        "desc": (
            "NLTK names corpus (Mark Kantrowitz).\n"
            "Source: https://www.kaggle.com/datasets/nltkdata/names"
        ),
    },
    "Both (female + male)": {
        "files": [DATA_DIR / "female.txt", DATA_DIR / "male.txt"],
        "desc": (
            "Combination of male and female names from the NLTK corpus.\n"
            "Source: https://www.kaggle.com/datasets/nltkdata/names"
        ),
    },
    "Finnish Female (finnishfemale.txt)": {
        "files": [DATA_DIR / "finnishfemale.txt"],
        "desc": (
            "Finnish Population Information System (DVV).\n"
            "Source: https://www.opendata.fi/data/en_GB/dataset/"
            "none/resource/08c89936-a230-42e9-a9fc-288632e234f5"
        ),
    },
    "Finnish Male (finnishmale.txt)": {
        "files": [DATA_DIR / "finnishmale.txt"],
        "desc": (
            "Finnish Population Information System (DVV).\n"
            "Source: https://www.opendata.fi/data/en_GB/dataset/"
            "none/resource/08c89936-a230-42e9-a9fc-288632e234f5"
        ),
    },
    "Finnish Both (finnishfemale + finnishmale)": {
        "files": [DATA_DIR / "finnishfemale.txt", DATA_DIR / "finnishmale.txt"],
        "desc": (
            "Combined male and female names from the Finnish Population Information System (DVV).\n"
            "Source: https://www.opendata.fi/data/en_GB/dataset/"
            "none/resource/08c89936-a230-42e9-a9fc-288632e234f5"
        ),
    },
    "Names (names.txt)": {
        "files": [DATA_DIR / "names.txt"],
        "desc": (
            "32k most common US names from SSA.gov (2018), via makemore repo.\n"
            "Source: https://github.com/karpathy/makemore"
        ),
    },
}

def _read_txt(path: Path):
    if not path.exists():
        return []
    txt = path.read_text(encoding="utf-8", errors="ignore")
    return [line.strip() for line in txt.splitlines() if line.strip()]

def load_names_by_choice(choice: str):
    entry = DATASETS.get(choice)
    if not entry:
        return [], f"Unknown dataset choice: {choice}"

    files = [p if isinstance(p, Path) else Path(p) for p in entry["files"]]

    missing = [p for p in files if not p.exists()]
    if missing:
        miss_str = "\n".join(f"- {p}" for p in missing)
        return [], f"Missing dataset file(s):\n{miss_str}"

    names = []
    for p in files:
        txt = p.read_text(encoding="utf-8", errors="ignore")
        names.extend(line.strip() for line in txt.splitlines() if line.strip())

    seen, deduped = set(), []
    for n in names:
        if n not in seen:
            seen.add(n)
            deduped.append(n)

    info = " + ".join(str(p) for p in files)
    desc = entry.get("desc", "")
    return deduped, f"{info}\n\n{desc}"

def generate_ui(dataset_choice, order, target_len, max_len, stop_prob, count, retries, normalize, capitalize):
    names, src_info = load_names_by_choice(dataset_choice)
    if not names:
        return f"No names loaded.\n{src_info}", ""

    try:
        model = NGramTrie(names, order=int(order), normalize_case=bool(normalize))
    except ValueError as e:
        return str(e), ""

    generator = NGramGenerator(model)

    exact = int(target_len)
    exact = exact if exact > 0 else None

    results = []
    for _ in range(int(count)):
        s = generator.generate(
            target_len=exact,
            max_len=int(max_len),
            stop_prob=float(stop_prob),
            retries=int(retries),
            capitalize=bool(capitalize),
        )
        results.append(s or "")

    preview = "\n".join(names[:8])
    return (
        f"Using dataset(s): {src_info}\n"
        f"Total names: {len(names)}\n\nPreview:\n{preview}",
        "\n".join(results),
    )

def build_demo():
    with gr.Blocks(title="Trie-backed n-gram name generator") as demo:
        gr.Markdown("## Trie-backed n-gram name generator")

        with gr.Row():
            with gr.Column():
                dataset_choice = gr.Dropdown(
                    choices=list(DATASETS.keys()),
                    value="Female (female.txt)",
                    label="Dataset"
                )

                with gr.Row():
                    order = gr.Slider(1, 10, value=3, step=1, label="n-gram order")
                    target_len = gr.Slider(0, 50, value=0, step=1, label="exact length (0 = variable)")
                    max_len = gr.Slider(1, 50, value=20, step=1, label="max length")

                with gr.Row():
                    stop_prob = gr.Slider(0, 1, value=0.35, step=0.01, label="stop probability")
                    retries = gr.Slider(1, 5000, value=500, step=50, label="retries per name")
                    count = gr.Slider(1, 200, value=10, step=1, label="how many to generate")

                normalize = gr.Checkbox(True, label="case-insensitive training")
                capitalize = gr.Checkbox(True, label="capitalize output")

                btn = gr.Button("Generate")

            with gr.Column():
                src_info = gr.Textbox(label="Dataset info", lines=10, interactive=False)
                results = gr.Textbox(label="Generated names", lines=16)

        btn.click(
            fn=generate_ui,
            inputs=[dataset_choice, order, target_len, max_len, stop_prob, count, retries, normalize, capitalize],
            outputs=[src_info, results],
        )

    return demo

if __name__ == "__main__":
    demo = build_demo()
    demo.launch()