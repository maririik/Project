import pytest
import random
from namegen import NGramTrie, Node, sample_weighted

@pytest.fixture
def names_small():
    return ["Anna", "Anne", "amy"]

@pytest.fixture
def names_mixed():
    return ["chris", "christopher", "christine", "chloe", "charlie"]

@pytest.fixture
def rng_seed0():
    return random.Random(0)

# ---------- Basic structure / construction ---------- 

def test_init_empty_ok():
    m = NGramTrie() 
    assert isinstance(m.root, Node)
    assert m.order == 2
    assert m.names == set()
    assert m.start_counts == {}

def test_get_node_empty_returns_root(names_small):
    m = NGramTrie(names_small, order=2)
    assert m.get_node("") is m.root

def test_init_order_validation():
    with pytest.raises(ValueError):
        NGramTrie(order=0) 

def test_fit_raises_if_order_exceeds_longest(names_small):
    m = NGramTrie(order=10)
    with pytest.raises(ValueError):
        m.fit(names_small)

def test_fit_builds_trie_and_counts_bigram(names_small):
    m = NGramTrie(names_small, order=2)
    first_letters = set(m.root.children.keys())
    assert {"a"} <= first_letters
    assert m.start_counts.get("a", 0) == 3

def test_successors_order1_empty_context(names_small):
    m = NGramTrie(names_small, order=1)
    assert m.successors("") == m.root.next_counts

def test_refit_clears_previous_counts(names_small):
    m = NGramTrie(["ZZZ"], order=2)
    assert "z" in (k.casefold() for k in m.root.children.keys())  
    m.fit(names_small)
    assert "a" in m.root.children
    assert "z" not in m.root.children


# ---------- Trie traversal helpers ----------

def test_get_node_and_get_node_chars(names_small):
    m = NGramTrie(names_small, order=2)
    node_a = m.get_node("a")
    assert node_a is not None
    node_ann = m.get_node_chars(list("ann"))
    assert node_ann is not None
    node_missing = m.get_node("zzz")
    assert node_missing is None

def test_ensure_path(names_small):
    m = NGramTrie(names_small, order=3)
    ctx = list("an")  
    node = m.ensure_path(ctx)
    assert node is not None
    node2 = m.get_node_chars(ctx)
    assert node2 is node


# ---------- N-gram counts & successors ----------

def test_build_ngram_counts_order1(names_small):
    m = NGramTrie(names_small, order=1)
    assert sum(m.root.next_counts.values()) == sum(len(n) for n in names_small)
    assert m.root.next_counts.get("a", 0) >= 3  # at least first chars

def test_successors_bigram(names_small):
    m = NGramTrie(names_small, order=2)
    succ = m.successors("a")
    assert isinstance(succ, dict)
    assert "n" in succ or "m" in succ 
    assert m.successors("z") == {}

def test_successors_trigram(names_small):
    m = NGramTrie(names_small, order=3)
    succ = m.successors("an")
    assert isinstance(succ, dict)
    assert "n" in succ


# ---------- sample_weighted ----------

def test_sample_weighted_basic(rng_seed0):
    w = {"a": 1, "b": 0, "c": 2}
    picks = [sample_weighted(w, rng_seed0) for _ in range(20)]
    assert "b" not in picks
    assert "c" in picks

def test_sample_weighted_empty_total(rng_seed0):
    assert sample_weighted({}, rng_seed0) is None
    assert sample_weighted({"x": 0, "y": 0}, rng_seed0) is None


# ---------- Generation behavior ----------

def test_generate_returns_none_when_no_training_data(rng_seed0):
    m = NGramTrie(order=2)
    assert m.generate(rng=rng_seed0) is None

def test_generate_length_constraint_fixed(names_small, rng_seed0):
    m = NGramTrie(names_small, order=3)
    target_len = 4
    s = m.generate(target_len=target_len, max_len=10, rng=rng_seed0, retries=200, capitalize=False)
    if s is not None:
        assert len(s) == target_len

def test_generate_never_returns_exact_training_name(names_small, rng_seed0):
    m = NGramTrie(names_small, order=3)
    for _ in range(10):
        s = m.generate(rng=rng_seed0, retries=300, capitalize=False)
        if s is not None:
            assert s not in m.names

def test_generate_capitalize_flag(names_mixed, rng_seed0):
    m = NGramTrie(names_mixed, order=3)
    s1 = m.generate(rng=rng_seed0, capitalize=True, retries=300)
    s2 = m.generate(rng=rng_seed0, capitalize=False, retries=300)
    if s1 is not None:
        assert s1[:1] == s1[:1].upper()
    if s2 is not None:
        assert s2[:1] == s2[:1].lower()


def test_generate_respects_max_len(names_mixed, rng_seed0):
    m = NGramTrie(names_mixed, order=3)
    s = m.generate(target_len=None, max_len=5, rng=rng_seed0, retries=400, capitalize=False)
    if s is not None:
        assert len(s) <= 5

def test_generate_handles_impossible_fixed_length(names_small, rng_seed0):
    m = NGramTrie(names_small, order=4) 
    out = m.generate(target_len=3, max_len=3, rng=rng_seed0, retries=50, capitalize=False)
    assert out is None or len(out) == 3

# ---------- Case handling behavior ----------

def test_case_normalization_treats_variants_as_same(rng_seed0):
    names = ["Anna", "ANNA", "anna", "Anne"]
    m = NGramTrie(names, order=2, normalize_case=True)
    assert m.names == {"anna", "anne"}
    assert m.successors("A") == m.successors("a")

