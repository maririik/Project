import pytest
from namegen.trie import NGramTrie

def test_add_name_and_candidates():
    trie = NGramTrie(n=3)
    trie.add_name("anna")
    trie.add_name("anne")

    # The start context <s>, <s> should always lead to 'a'
    assert trie.candidates(("<s>", "<s>")) == {"a": 2}

    # The context "n", "n" should lead to both "a" and "e"
    cand = trie.candidates(("n", "n"))
    assert cand["a"] == 1
    assert cand["e"] == 1
    assert trie.total_successors(("n", "n")) == 2


def test_invalid_context_length():
    trie = NGramTrie(n=3)
    trie.add_name("anna")

    # Context length must be n-1 = 2
    with pytest.raises(ValueError):
        trie.candidates(("a",))  # too short
    with pytest.raises(ValueError):
        trie.candidates(("a", "n", "n"))  # too long
