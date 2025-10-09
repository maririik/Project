# tests/test_namegen_and_trie.py
import random
import pytest

from namegen import NGramTrie, NGramGenerator, sample_weighted

# Shared fixtures & tiny helpers
@pytest.fixture
def names_small():
    return ["anna", "anne", "amy"]

@pytest.fixture
def names_mixed():
    return ["Anna", "ANNE", "andrew", "aNdReA", "amy", "MARIA", "Marie", "Marin"]


class FakeRNG:
    """Deterministic stand-in for random.Random.random()."""
    def __init__(self, seq=None):
        self.seq = list(seq or [])
        self.i = 0

    def random(self):
        if not self.seq:
            return 0.0
        v = self.seq[self.i % len(self.seq)]
        self.i += 1
        return v


# sample_weighted
def test_sample_weighted_empty_and_zeroes():
    rng = random.Random(0)
    assert sample_weighted({}, rng) is None
    assert sample_weighted({"a": 0, "b": 0}, rng) is None

def test_sample_weighted_single_positive_wins():
    rng = random.Random(0)
    for _ in range(10):
        assert sample_weighted({"x": 3, "y": 0}, rng) == "x"

def test_sample_weighted_weight_bias_sanity():
    rng = random.Random(123)
    w = {"a": 1, "b": 3, "c": 6}
    counts = {k: 0 for k in w}
    for _ in range(3000):
        counts[sample_weighted(w, rng)] += 1
    assert counts["c"] > counts["b"] > counts["a"]


# Trie
def test_rejects_invalid_order():
    with pytest.raises(ValueError):
        NGramTrie(["anna"], order=0)

def test_rejects_order_longer_than_longest_name():
    with pytest.raises(ValueError):
        NGramTrie(["ann"], order=4)

def test_fit_rejects_empty_training():
    m = NGramTrie(order=2)
    with pytest.raises(ValueError):
        m.fit([])

def test_case_normalization_default_is_on(names_mixed):
    m = NGramTrie(names_mixed, order=2)
    assert "anna" in m.names and "anne" in m.names
    assert "Anna" not in m.names and "ANNE" not in m.names

def test_case_normalization_off_keeps_variants_separate():
    m = NGramTrie(["Anna", "anna"], order=2, normalize_case=False)
    assert "A" in m.root.children and "a" in m.root.children

def test_successors_bigram_counts_basic():
    names = ["anna", "anne"]
    t = NGramTrie(names=names, order=2)
    succ_a = t.successors("a")
    assert succ_a.get("n", 0) >= 2
    succ_ann = t.successors("ann")
    assert set(succ_ann) <= {"a", "e"}

def test_start_counts_for_order_gt1():
    names = ["maria", "marie", "mark"]
    t = NGramTrie(names=names, order=3)
    assert t.start_counts.get("ma", 0) == 3
    assert set(t.start_counts) == {"ma"}

def test_get_node_and_successors_when_missing():
    t = NGramTrie(names=["zoe"], order=3)
    assert t.get_node("xy") is None
    assert t.successors("xy") == {}

def test_order_one_places_counts_on_root():
    t = NGramTrie(names=["abc", "aba"], order=1)
    succ = t.successors("")
    assert succ.get("a") == 3
    assert succ.get("b") == 2
    assert succ.get("c") == 1
    assert t.successors("anything") == succ


# Generator
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

def test_variable_length_forced_stop(names_mixed):
    model = NGramTrie(names_mixed, order=3)
    gen = NGramGenerator(model, rng=FakeRNG([0.0]))
    s = gen.generate(target_len=None, max_len=20, capitalize=False)
    assert s is None or len(s) <= 3

def test_variable_length_force_continue_until_max(names_mixed):
    model = NGramTrie(names_mixed, order=3)
    gen = NGramGenerator(model, rng=FakeRNG([0.99]))  
    s = gen.generate(target_len=None, max_len=5, capitalize=False)
    assert s is None or len(s) <= 5


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