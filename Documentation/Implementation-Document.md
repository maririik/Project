# Implementation document


### Project scope
A character-level name generator that learns successor statistics from a dataset of names using a prefix trie and generates new, name-like strings via an n-gram model. The implementation is split into a modeling module (trie.py) and a generation module (generator.py), with a package initializer (__init__.py).

## GENERAL STRUCTURE OF THE PROGRAM

#### Modules and responsibilities
- trie.py → Model layer
  • Node: trie node holding `children` and `next_counts` (successor counts).
  • NGramTrie:
    - Configuration: order (n-gram order), normalize_case.
    - Data: root, names (training set), start_counts (frequency of starting contexts).
    - API:
      - fit(names): builds the trie and n-gram statistics; validates input and order.
      - successors(s): returns successor character counts for the current context.
      - get_node(...): internal lookup by string or list of chars.

- generator.py → Generation layer
  • sample_weighted(d, rng): samples a key proportional to its weight by a single pass over the dictionary.
  • NGramGenerator:
    - generate(...): retries until it finds a novel candidate (not in training names), with optional exact target_len. Uses the model’s start_counts and successors to extend characters.
    - generate_once(...): one attempt to produce a candidate using order-aware context lookup (get_node) and weighted sampling at each step..

- __init__.py → Package exports
  • Exposes NGramTrie, Node, NGramGenerator at package top level.

#### High-level data flow
1. Training (NGramTrie.fit): build/extend trie paths for each training name; collect successor counts per context of length (order − 1); collect start_counts for opening contexts. For n-gram order = 1, counts are kept at the root.
2. Generation (NGramGenerator.generate / generate_once): pick a start context, then iterate: look up the node for the current context (suffix length order − 1), fetch successor counts, sample the next char, append, stop by rules (target_len, stop_prob, whether name exists in training set, max_len).


## ACHIEVED TIME AND SPACE COMPLEXITIES

Let N be the total number of characters across all training names; Σ the alphabet size (distinct characters); L the maximum name length; n the n-gram order; and k the average number of successors for a context (≤ Σ).

#### Building (fit):
- Time: O(N). We traverse/insert each character once and update counts with O(1) amortized bookkeeping.
- Space: O(U + E) nodes/edges where U is the number of distinct prefixes (≤ N). Successor maps collectively store O(N) counts in the worst case.

#### Lookup:
- get_node by context of length (n − 1): O(n) character steps down the trie (bounded by name length).
- successors(s): O(n) to locate the node plus O(1) to return a reference. Copying the dict would cost O(k).

#### Generation (per produced character):
- Context lookup: O(n).
- Weighted sampling across successors: O(k).
Therefore one name of length T costs O(T · (n + k)). With exact length T (target_len), that’s the upper bound. With early stopping, expected T is smaller.

####: Memory at inference
- Reuses the trained trie. Marginal memory is only the temporary candidate string O(T).


## LIMITATIONS AND SUGGESTIONS FOR IMPROVEMENT

#### Performance limitations: 
The trie is rebuilt each time a new dataset is loaded or parameters are changed, which can be inefficient for very large datasets.
- **Improvement:**
Cache pre-trained tries for each dataset or serialize trained models to disk for faster reloads.

#### No feedback or user control:
The Gradio UI allows adjusting parameters but doesn't have features constraining name structure (e.g., starting letters, endings, or specific patterns).
- **Improvement:** Add optional filters or regular expressions that post-process generated names to match user preferences, such as “must start with A” or “must end with -a”.

#### No generation statistics:
The current system reports only the raw list of names. It does not track quality/diversity metrics (e.g., novelty, length distribution, n-gram divergence vs. training), failure/duplicate rates, or performance (time/name, retries). This makes it hard to compare settings (order, stop_prob, min_len) or detect regressions after code changes.
- **Improvement:** Add a “Stats” panel to the UI (or a CLI flag) to compute novelty, duplicates, failure rate, and length summary per batch. Extend to n-gram divergence and entropy to show fair comparisons across settings.

#### Sparse contexts at high order:
With small datasets and high n-gram order, many contexts have no successors → stalls or empty outputs.
- **Improvement:** Add backoff/interpolation (e.g., Katz or Kneser–Ney). If a context is unseen it can fall back to shorter contexts automatically.

#### Limited explainability:
Users can’t see why a given character was chosen or why an attempt failed.
- **Improvement:** Debug panel showing: chosen start context, current context, and top-k successors with probabilities.

#### Limited input format (TXT-only, one name per line)
The generator only supports plain `.txt` files with one clean name per line, assuming no headers, missing values, or irregular formatting. This restricts its use with other dataset types such as CSV or JSON.  
- **Improvement:** Add support for common formats like `.csv` and `.json` with a column selector in the UI, implement automatic text cleaning (trimming, deduplication, normalization), and include validation to detect missing or invalid entries. Clear error messages and a simple data-quality summary would make the tool more robust and user-friendly across varied data sources.

#### No backoff or smoothing implementation
Although the Specification document mentioned implementing a backoff mechanism, it was not ultimately included in the final version. As a result, the generator fails to produce output for unseen n-gram contexts, especially at higher orders or with small datasets.  
- **Improvement:** Implement backoff smoothing to fall back from higher- to lower-order n-grams when a context is missing, allowing the model to generalize better and reduce generation stalls.

## REFERENCES
- Jurafsky, D. & Martin, J. H. (2023). *Speech and Language Processing (3rd ed. draft).*  
  [https://web.stanford.edu/~jurafsky/slp3/](https://web.stanford.edu/~jurafsky/slp3/)  
  *(General background on n-gram language models and smoothing techniques.)*

- **Wikipedia. (2024).**  
  *Trie.*  Retrieved from [https://en.wikipedia.org/wiki/Trie](https://en.wikipedia.org/wiki/Trie)

- **GeeksforGeeks. (n.d.).**  
  *Markov Chain in Machine Learning.*  Retrieved from [https://www.geeksforgeeks.org/machine-learning/markov-chain/](https://www.geeksforgeeks.org/machine-learning/markov-chain/)

- **Wikipedia. (2024).**  
  *Markov Chain.*  
  Retrieved from [https://en.wikipedia.org/wiki/Markov_chain](https://en.wikipedia.org/wiki/Markov_chain)

- **Wikipedia. (2024).**  
  *Markov Decision Process.*  
  Retrieved from [https://en.wikipedia.org/wiki/Markov_decision_process](https://en.wikipedia.org/wiki/Markov_decision_process)



### Datasets
- **Kantrowitz, M. (NLTK Names Corpus).**  
  *Female (female.txt), Male (male.txt), Both (female + male).*  
  Natural Language Toolkit (NLTK) Names Corpus.  
  Source: [https://www.kaggle.com/datasets/nltkdata/names](https://www.kaggle.com/datasets/nltkdata/names)

- **Digital and Population Data Services Agency (DVV).**  
  *Finnish Female (finnishfemale.txt), Finnish Male (finnishmale.txt), Finnish Both (finnishfemale + finnishmale).*  
  Finnish Population Information System – Open Data.  
  Source: [https://www.opendata.fi/data/en_GB/dataset/none/resource/08c89936-a230-42e9-a9fc-288632e234f5](https://www.opendata.fi/data/en_GB/dataset/none/resource/08c89936-a230-42e9-a9fc-288632e234f5)

- **Karpathy, A. (2018).**  
  *US Names (US_names.txt).*  
  32k most common U.S. names from SSA.gov (via *makemore* repository).  
  Source: [https://github.com/karpathy/makemore](https://github.com/karpathy/makemore)

- **Hämäläinen, M., & Alnajjar, K. (2019).**  
  *Finnish Words (finnish_words.txt).*  
  “Let’s FACE it: Finnish Poetry Generation with Aesthetics and Framing.”  
  *Proceedings of the 12th International Conference on Natural Language Generation* (pp. 290–300).  
  Source: [https://www.kaggle.com/datasets/mikahama/finnish-words-and-their-concreteness-values](https://www.kaggle.com/datasets/mikahama/finnish-words-and-their-concreteness-values)

- **Banik, R. (2017).**  
  *Pokémon (pokemon.txt).*  
  Dataset of 802 Pokémon from all seven generations.  
  Source: [https://www.kaggle.com/datasets/rounakbanik/pokemon](https://www.kaggle.com/datasets/rounakbanik/pokemon)

### Tools

- Gradio Team. (2024). *Gradio: A Python Library for Building Machine Learning Demos and Web Apps.*  
  [https://gradio.app](https://gradio.app)  
  *(Used for the interactive user interface.)*

- Poetry Authors. (2024). *Poetry — Python Dependency Management and Packaging Made Easy.*  
  [https://python-poetry.org/](https://python-poetry.org/)  
  *(Used for dependency management and project structure.)*
--------
ChatGPT (GPT-5 Thinking) was used to help draft text, debug code, and explain concepts.