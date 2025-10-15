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
1. Training (NGramTrie.fit): build/extend trie paths for each training name; collect successor counts per context of length (order − 1); collect start_counts for opening contexts. For n-gram order == 1, counts are kept at the root.
2. Generation (NGramGenerator.generate / generate_once): pick a start context, then iterate: look up the node for the current context (suffix length order − 1), fetch successor counts, sample the next char, append, stop by rules (target_len, stop_prob, whether name exists in training set, max_len).


## ACHIEVED TIME AND SPACE COMPLEXITIES

Let N be the total number of characters across all training names; Σ the alphabet size (distinct characters); L the maximum name length; n the n-gram order; and k the average number of successors for a context (≤ Σ).

Building (fit)
- Time: O(N). We traverse/insert each character once and update counts with O(1) amortized bookkeeping.
- Space: O(U + E) nodes/edges where U is the number of distinct prefixes (≤ N). Successor maps collectively store O(N) counts in the worst case.

Lookup
- get_node by context of length (n − 1): O(n) character steps down the trie (bounded by name length).
- successors(s): O(n) to locate the node plus O(1) to return a reference. Copying the dict would cost O(k).

Generation (per produced character)
- Context lookup: O(n).
- Weighted sampling across successors: O(k).
Therefore one name of length T costs O(T · (n + k)). With exact length T (target_len), that’s the upper bound. With early stopping, expected T is smaller.

Memory at inference
- Reuses the trained trie. Marginal memory is only the temporary candidate string O(T).
------

ChatGPT (GPT-5 Thinking) was used to help draft text, debug code, and explain concepts.