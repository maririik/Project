## Unit Testing Coverage Report

| File                      | Stmts | Miss | Branch | BrPart | Cover | Missing                                     |
|----------------------------|-------|------|--------|---------|--------|------------------------------------------|
| src\namegen\__init__.py    | 3     | 0    | 0      | 0       | 100%   | —                                        |
| src\namegen\generator.py   | 60    | 9    | 38     | 9       | 84%    | 22, 32, 92, 95, 99, 102, 108, 110, 123   |
| src\namegen\trie.py        | 64    | 1    | 28     | 2       | 97%    | 98, 116→120                              |
| **TOTAL**                  | 127   | 10   | 66     | 11      | **90%**|                                          |

**Notes on uncovered lines**  
    The uncovered lines are primarily defensive/fallback branches (e.g., sampler CDF fallback, early exits on empty counts) that are not exercised by normal inputs.

## What was tested and how?
### 1. Weighted sampling (sample_weighted)

**Empty mapping and all-zero weights**
- Test name: test_sample_weighted_empty_and_zeroes
- Intent: ensure the function returns None for no choices or when total weight is zero (no selectable item).
- Concrete assertions:
``` 
assert sample_weighted({}, rng) is None
assert sample_weighted({"a": 0, "b": 0}, rng) is None
```

**Single-positive-key dominates**
- Test name: test_sample_weighted_single_positive_wins
- Intent: if exactly one key has positive weight, it must always be chosen. Also tests repeated deterministic sampling with the same RNG.
- Concrete assertions: run 10 samples with rng = random.Random(0) and assert the result is always "x" for {"x":3,"y":0}.

**CDF boundary behavior (exact cut points)**
- Test name: test_sample_weighted_cdf_boundaries_are_respected
- Intent: confirm the CDF selection logic maps fractional RNG outputs to the correct keys (checks off-by-one and ≤ vs < boundary decisions).
- Concrete setup & assertions:
```
w = {"a": 1, "b": 3, "c": 6}   # total = 10
FakeRNG([0.05, 0.25, 0.75])   # returns fractional values in sequence
# The function multiplies random() * total -> [0.5, 2.5, 7.5]
# cumulative thresholds: a:1, b:1+3=4, c:10
# therefore results -> "a", "b", "c"
```

### 2. NGramTrie.build() / prefix trie internals
**Model validation**
- Tests: test_rejects_invalid_order, test_fit_rejects_empty_training
- Intent: Verify the NGramTrie validates constructor and training inputs (invalid n-gram order and empty training are rejected).
- How: Attempt to construct/fit with invalid inputs (NGramTrie(..., order=0) and NGramTrie().fit([])) and assert a ValueError is raised.

**Argument validation**
- Tests: test_generate_raises_when_target_len_exceeds_max_len
- Intent: Ensure NGramGenerator.generate() validates its parameters (specifically target_len must not exceed max_len).
- How: Call gen.generate(target_len=12, max_len=10) and assert it raises ValueError.

**Length & stopping behavior**
- Tests: test_generate_respects_target_len_exact_when_possible, test_generate_with_order_one_uses_root_counts_and_stops, test_variable_length_behavior, test_generate_once_stops_when_no_successors
- Intent: Verify how the generator handles length and termination: respecting target_len when possible, the special-case order==1 path, probabilistic early stops, and graceful termination when no successors exist.
- How: Run the listed subtests using small deterministic RNG (FakeRNG) and assert produced lengths or None behavior as appropriate (e.g., len(out)==target_len when non-None; bounds on variable-length output; short/empty output when successors absent).

**Generation constraints & corpus integrity**
- Tests: test_generate_avoids_exact_training_names, test_generated_ngrams_exist_in_training_closed_corpus
- Intent: Confirm generator output respects corpus constraints: it should not return exact training names and should only emit n-grams observed in training.
- How: (1) Train on ["maria"], monkeypatch sample_weighted to force reconstruction and assert generate(..., retries=0) returns None. (2) Train on a closed repetitive corpus (e.g., ["abab..."]), collect observed n-grams, generate many samples and assert every generated n-gram is in the observed set.