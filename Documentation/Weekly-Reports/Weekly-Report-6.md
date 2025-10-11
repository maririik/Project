# Weekly Report 6

**Time spent:** ~ 8 hours 

## What did I do this week?
This week I improved my unit tests. I tested whether generated n-grams exist in training (closed-corpus check) I also improved my code using the good peer review feedback I received. Namely:
- Refactored the project into a proper src package layout: `src/namegen/` with `__init__.py`, `trie.py`, `namegen.py`.
- Fixed imports across the codebase so CLI/UI/tests all use `from namegen import ...`.
- Added deterministic RNG injection to `NGramGenerator` and `sample_weighted` (no global seeding; tests can fix the seed).
- Updated `pyproject.toml`: declared the package under `src`, added `gradio` dependency, cleaned pytest path hacks.
- Improved UI text (what “order” means; why high order can stall on small data) + order-too-high hint in the Dataset info panel.
- Documented data format & constraints in `README.md` (one name per line; allowed characters; length caps).


## How has the program progressed?
The app, tests, and CLI now share a **single import model** and run reliably via Poetry. The generation results are **reproducible** in tests and the UI (optional seed). Users get clearer guidance in the UI, and the app **cautions** when `order` is likely too high for the dataset.

## What did I learn this week/today?
I learned how to organize the code so modules import cleanly across the app, tests, and tooling. I also learned how to make randomized behavior reproducible by injecting a local random source instead of changing global state.

## What remains unclear or has been challenging?
Some testing aspects have been challenging. It was a little difficult to figure out which tests are comprehensive enough.
 
## What will I do next?
I will continue writing my testing and implementation documents. I would like to divide my testing files for clarity and remove unnecessary tests. I will also try to refine the UI in preparation for the demo sessions. I would also like to switch terminology to Markov convention: interpret `order = k` as “depends on k previous chars” (current n-gram order n maps to k = n−1) for clarity. 

