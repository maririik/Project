# User Guide

## How to Run the Project
1. Clone the repository 
```git clone https://github.com/maririik/namegen-algoai.git```
2. Move to the cloned project directory
```bash
cd namegen-algoai
```

You can launch the Gradio web app with **Poetry**.
```
poetry install
poetry run python app.py
```
Once the app starts, open your browser and visit http://127.0.0.1:7860 to use the interactive name generator.
Make sure your training datasets are in the data/ folder (one name per line).

## How it works
1. Training
      - Builds a prefix trie where each node represents a prefix of the training names.
      - Each node stores successor counts (next_counts) and starting contexts (start_counts) for order > 1.

2. Generation
    - Starts from a random start context sampled from start_counts.
    - Iteratively samples next characters weighted by next_counts of the current context node.
    - Stops when reaching target_len, max_len, or with probability stop_prob.

3. Output filtering
    - Rejects names that exactly match training names.
    - Retries until reaching the requested number or retries limit.

## Using the UI (controls explained)

- Dataset: pick one of the preloaded text files (or your custom one).
- n-gram order: context size = order − 1.
    - Higher = more local structure; too high on small data may stall or overfit.
    - Note: n-gram order n ≈ Markov order n−1 (same idea, different numbering).

- exact length (0 = variable):
    - if > 0 → force exact length.
    - 0 → variable length with early stopping (see stop probability).

- max length: hard cap on any generated name.

- min length: lower bound when using variable length (ignored when exact length > 0).

- stop probability: in variable mode, once the current string already exists in training, this per-step probability lets the model stop early. Lower values → longer names.

- retries per name: how many attempts are allowed to find a valid, novel name.

- how many to generate: batch size.

- case-insensitive training: fold to lowercase before training (recommended).

- capitalize output: capitalize the first letter of each result.

#### Typical starting settings
Order 3, exact length 0, max 20, min 3, stop prob 0.30–0.40, retries 500, count 10.

## Data format

The generator expects plain text files in `data/` with **one name per line**.

- **Location:** `data/*.txt` (e.g., `data/female.txt`, `data/male.txt`)
- **One name per line:** no commas/CSV, blank lines are ignored.
- **Case:** training names are read as lowercase (`.lower()` in code).
- **Allowed characters:** letters and the hyphen `-` (safe default).  
  Recommended regex per line: `^[a-z-]+$`  
  > If you include other characters (spaces, digits, apostrophes), they’ll be treated as literal tokens. For best results, keep to `[a–z-]`.
- **Length limits:**  
  - Training data: aim for 2–40 chars per name.  
  - Generation: bounded by `max_length` (default **20**). Names longer than `max_length` cannot be produced. If your dataset has many very long names, increase `max_length`.

### Tips

- **Duplicates:** avoid duplicates, they overweight those names in the model.
- **Normalization:** keep everything lowercase and remove leading/trailing spaces.
- **Hyphenated names:** `maria-elisabet` is fine, the hyphen is modeled as a character.
- **Very short datasets:** with only a few names, the model may produce many training names. Increase `retries` or add more data.
- You can also add your own date set:
    1. Put my_names.txt in data/ (one name per line).
    2. Add an entry to DATASETS in app.py:
    ```bash
    "My names (my_names.txt)": {
    "files": [DATA_DIR / "my_names.txt"],
    "desc": "Short description / source"
    }
    ```
    3. Restart the app and choose it from the Dataset dropdown.


### Common pitfalls

- **Spaces in names:** `mary jane` introduces a space token and often degrades quality. Prefer `mary-jane` or `maryjane`.
- **Exotic characters:** unicode letters work, but mixing accents with plain ASCII in small datasets can hurt consistency. Consider normalizing (e.g., `á -> a`) if output quality suffers.
- **Long names not appearing:** raise `max_length` in the UI/CLI if your dataset skews long.



## Running the Test Suite (pytest)

All tests live in the `tests/` folder and cover trie construction and validation, weighted sampling, and generation behavior (including edge cases and reproducibility helpers). No manual seeding is needed to run the suite.

### How to run the tests & coverage

```bash
# Install dev deps (pytest, pytest-cov)
poetry install --with dev

# Run tests with terminal coverage (and show missing lines)
poetry run pytest --cov=namegen --cov-report=term-missing
```