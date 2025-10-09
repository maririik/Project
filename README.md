# Project: Name Generator
This project is a **name generator** developed for the *University of Helsinki* Algorithms and AI Lab

---

## Documentation
- [Specification Document](Documentation/Specification-Document.md)
- [Weekly Report 1](Documentation/Weekly-Reports/Weekly-Report-1_1.md)


## Data format

The generator expects plain text files in `data/` with **one name per line**.

- **Location:** `data/*.txt` (e.g., `data/female.txt`, `data/male.txt`)
- **One name per line:** no commas/CSV; blank lines are ignored.
- **Case:** training names are read as lowercase (`.lower()` in code).
- **Allowed characters:** letters and the hyphen `-` (safe default).  
  Recommended regex per line: `^[a-z-]+$`  
  > If you include other characters (spaces, digits, apostrophes), they’ll be treated as literal tokens. For best results, keep to `[a–z-]`.
- **Length limits:**  
  - Training data: aim for 2–40 chars per name.  
  - Generation: bounded by `max_length` (default **20**). Names longer than `max_length` cannot be produced; if your dataset has many very long names, increase `max_length`.


### Tips

- **Duplicates:** avoid duplicates; they overweight those names in the model.
- **Normalization:** keep everything lowercase and remove leading/trailing spaces.
- **Hyphenated names:** `maria-elisabet` is fine; the hyphen is modeled as a character.
- **Very short datasets:** with only a few names, the model may produce many training names; increase `retries` or add more data.

### Common pitfalls

- **Spaces in names:** `mary jane` introduces a space token and often degrades quality. Prefer `mary-jane` or `maryjane`.
- **Exotic characters:** unicode letters work, but mixing accents with plain ASCII in small datasets can hurt consistency. Consider normalizing (e.g., `á -> a`) if output quality suffers.
- **Long names not appearing:** raise `max_length` in the UI/CLI if your dataset skews long.