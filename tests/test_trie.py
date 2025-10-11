# tests/test_trie.py
import pytest
from namegen import NGramTrie

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
