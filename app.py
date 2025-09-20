# app.py
from pathlib import Path
import gradio as gr
from namegen import NGramTrie

PROJECT_DIR = Path(__file__).parent
DEFAULT_DATA = PROJECT_DIR / "data" / "female.txt"

def load_default_names():
    if DEFAULT_DATA.exists():
        txt = DEFAULT_DATA.read_text(encoding="utf-8", errors="ignore")
        return [line.strip() for line in txt.splitlines() if line.strip()]
    return []

def generate_ui(order, target_len, max_len, stop_prob, count, retries, normalize, capitalize):
    names = load_default_names()
    if not names:
        return f"Built-in file not found or empty: {DEFAULT_DATA}", ""

    try:
        model = NGramTrie(names, order=int(order), normalize_case=bool(normalize))
    except ValueError as e:
        return str(e), ""

    exact = int(target_len) if int(target_len) > 0 else None
    results = []
    for _ in range(int(count)):
        s = model.generate(
            target_len=exact,
            max_len=int(max_len),
            stop_prob=float(stop_prob),
            retries=int(retries),
            capitalize=bool(capitalize),
        )
        results.append(s or "")

    preview = "\n".join(names[:8])
    return (
        f"Using built-in dataset: {DEFAULT_DATA}\n"
        f"Total names: {len(names)}\n\nPreview:\n{preview}",
        "\n".join(results),
    )

def build_demo():
    with gr.Blocks(title="Trie-backed n-gram name generator") as demo:
        gr.Markdown(
            f"## Trie-backed n-gram name generator\n"
            f"**Using built-in dataset:** `{DEFAULT_DATA}` (one name per line)")

        with gr.Row():
            with gr.Column():
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
            inputs=[order, target_len, max_len, stop_prob, count, retries, normalize, capitalize],
            outputs=[src_info, results],)

    return demo

if __name__ == "__main__":
    demo = build_demo()
    demo.launch()
