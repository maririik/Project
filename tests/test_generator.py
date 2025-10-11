# tests/test_generator.py
import random
import pytest
from namegen import NGramTrie, NGramGenerator, sample_weighted
from conftest import FakeRNG

def test_generate_respects_target_len_exact_when_possible(names_mixed):
    model = NGramTrie(names_mixed, order=3)
    gen = NGramGenerator(model, rng=random.Random(0))
    out = gen.generate(target_len=4, max_len=10, capitalize=False)
    if out is not None:
        assert len(out) == 4

def test_generate_avoids_exact_training_names(monkeypatch):
    names = ["maria"]
    model = NGramTrie(names, order=2)
    gen = NGramGenerator(model, rng=random.Random(0))

    def fake_sample_weighted(weights, rng):
        return max(weights, key=weights.get)

    monkeypatch.setattr("namegen.sample_weighted", fake_sample_weighted)
    out = gen.generate(target_len=None, max_len=10, capitalize=False, retries=0)
    assert out is None

def test_generate_with_order_one_uses_root_counts_and_stops():
    names = ["ab", "aa", "ba"]
    model = NGramTrie(names, order=1)
    gen = NGramGenerator(model, rng=random.Random(42))
    s = gen.generate(target_len=2, max_len=2, capitalize=False)
    if s is not None:
        assert len(s) == 2

def test_generate_raises_when_target_len_exceeds_max_len():
    names = ["ada", "ava", "amy"]
    model = NGramTrie(names, order=2)
    gen = NGramGenerator(model, rng=random.Random(0))
    with pytest.raises(ValueError):
        gen.generate(target_len=12, max_len=10)

def test_generate_once_stops_when_no_successors():
    names = ["zx"]
    model = NGramTrie(names, order=2)
    gen = NGramGenerator(model, rng=random.Random(0))
    s = gen.generate_once(target_len=None, max_len=10, stop_prob=0.0)
    assert isinstance(s, str)
    assert s == "" or len(s) <= 3

@pytest.mark.parametrize("cap", [True, False])
def test_generate_capitalize_flag_param(names_mixed, cap):
    model = NGramTrie(names_mixed, order=3)
    gen = NGramGenerator(model, rng=random.Random(0))
    s = gen.generate(capitalize=cap, retries=100)
    if s:
        first = s[0]
        assert (first == first.upper()) if cap else (first == first.lower())

@pytest.mark.parametrize(
    ("seq", "max_len", "upper_bound"),
    [([0.0], 20, 3),   
     ([0.99], 5,  5)]  
)
def test_variable_length_behavior(names_mixed, seq, max_len, upper_bound):
    model = NGramTrie(names_mixed, order=3)
    gen = NGramGenerator(model, rng=FakeRNG(seq))
    s = gen.generate(target_len=None, max_len=max_len, capitalize=False)
    assert s is None or len(s) <= upper_bound

def test_generated_ngrams_exist_in_training_closed_corpus():
    order = 2
    names = ["abababababababa"]
    model = NGramTrie(names, order=order)
    gen = NGramGenerator(model, rng=random.Random(0))

    observed = set()
    for n in model.names:
        for i in range(len(n) - order + 1):
            observed.add(n[i:i + order])

    for _ in range(50):
        s = gen.generate(max_len=12, capitalize=False, retries=200)
        if not s or len(s) < order:
            continue
        for i in range(len(s) - order + 1):
            assert s[i:i + order] in observed, (
                f"Found unseen {order}-gram '{s[i:i+order]}' in generated name '{s}'"
            )


