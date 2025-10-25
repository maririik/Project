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

def test_trie_shape_and_counts_from_example_diagram():
    words = ["to", "tea", "ted", "ten", "i", "in", "inn"]

    t2 = NGramTrie(names=words, order=2)

    root = t2.root
    assert "t" in root.children and "i" in root.children

    node_t = root.children["t"]
    node_i = root.children["i"]

    assert "o" in node_t.children
    assert "e" in node_t.children
    node_te = node_t.children["e"]
    assert "a" in node_te.children and "d" in node_te.children and "n" in node_te.children
    assert "n" in node_i.children
    node_in = node_i.children["n"]
    assert "n" in node_in.children  
    assert t2.start_counts.get("t") == 4
    assert t2.start_counts.get("i") == 3
    assert set(t2.start_counts) == {"t", "i"}
    assert t2.successors("t") == {"o": 1, "e": 3}
    assert t2.successors("i") == {"n": 2}
    assert t2.successors("e") == {}

    t3 = NGramTrie(names=words, order=3)

    assert t3.start_counts == {"to": 1, "te": 3, "in": 2}
    assert t3.successors("te") == {"a": 1, "d": 1, "n": 1}
    assert t3.successors("in") == {"n": 1}
    assert t3.successors("to") == {}

def _dump_trie_ascii(node, prefix=""):
    lines = ["(root)"]
    items = sorted(node.children.items())
    for idx, (ch, child) in enumerate(items):
        is_last = (idx == len(items) - 1)
        connector = "+-"  
        lines.append(f"{prefix}{connector} {ch}")
        next_prefix = prefix + ("   " if is_last else "|  ")
        lines.extend(_dump_trie_ascii(child, next_prefix)[1:])  
    return lines

def test_trie_dump_for_visual_comparison():
    words = ["to", "tea", "ted", "ten", "i", "in", "inn"]
    t = NGramTrie(names=words, order=2)
    lines = _dump_trie_ascii(t.root)
    print("\n".join(lines)) 

    text = "\n".join(lines)
    assert "+- t" in text and "+- i" in text
    assert "+- e" in text and "+- o" in text and "+- n" in text