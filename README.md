# Project: Name Generator
This project is a **name generator** developed for the *University of Helsinki* Algorithms and AI Lab

---

## Documentation
- [Specification Document](Documentation/Specification-Document.md)
- [Implementation Document](Documentation/Implementation-Document.md.md)
- [Specification Document](Documentation/Specification-Document.md.md)
- [Weekly Report 1](Documentation/Weekly-Reports/Weekly-Report-2.md)
- [Weekly Report 2](Documentation/Weekly-Reports/Weekly-Report-2.md)
- [Weekly Report 3](Documentation/Weekly-Reports/Weekly-Report-3.md)
- [Weekly Report 4](Documentation/Weekly-Reports/Weekly-Report-4.md)
- [Weekly Report 5](Documentation/Weekly-Reports/Weekly-Report-5.md)
- [Weekly Report 6](Documentation/Weekly-Reports/Weekly-Report-6.md)


## How to Run the Project

You can launch the Gradio web app either with **Poetry** or a plain Python environment.
```
poetry install
poetry run python app.py
```
Once the app starts, open your browser and visit http://127.0.0.1:7860 to use the interactive name generator.
Make sure your training datasets are in the data/ folder (one name per line).



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

### Common pitfalls

- **Spaces in names:** `mary jane` introduces a space token and often degrades quality. Prefer `mary-jane` or `maryjane`.
- **Exotic characters:** unicode letters work, but mixing accents with plain ASCII in small datasets can hurt consistency. Consider normalizing (e.g., `á -> a`) if output quality suffers.
- **Long names not appearing:** raise `max_length` in the UI/CLI if your dataset skews long.

## Running the Test Suite (pytest)

All tests live in the `tests/` folder and cover trie construction and validation, weighted sampling, and generation behavior (including edge cases and reproducibility helpers). No manual seeding is needed to run the suite.

### Quick start
```bash
# With Poetry
poetry run pytest -q

# With a plain virtualenv
pytest -q

# Coverage report
pytest -q --cov=src --cov-report=term-missing
