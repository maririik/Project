## Unit Testing Coverage Report

| File                      | Stmts | Miss | Branch | BrPart | Cover | Missing                                     |
|----------------------------|-------|------|--------|---------|--------|------------------------------------------|
| src\namegen\__init__.py    | 3     | 0    | 0      | 0       | 100%   | —                                        |
| src\namegen\generator.py   | 60    | 9    | 38     | 9       | 84%    | 22, 32, 92, 95, 99, 102, 108, 110, 123   |
| src\namegen\trie.py        | 64    | 1    | 28     | 2       | 97%    | 98, 116→120                              |
| **TOTAL**                  | 127   | 10   | 66     | 11      | **90%**|                                          |

**Notes on uncovered lines**  
    The uncovered lines are primarily defensive/fallback branches (e.g., sampler CDF fallback, early exits on empty counts) that are not exercised by normal inputs.

##What was tested and how?
# 1. Weighted sampling (sample_weighted)

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