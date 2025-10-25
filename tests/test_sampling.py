# tests/test_sampling.py
import random
from namegen import sample_weighted

def test_sample_weighted_empty_and_zeroes():
    rng = random.Random(0)
    assert sample_weighted({}, rng) is None
    assert sample_weighted({"a": 0, "b": 0}, rng) is None

def test_sample_weighted_single_positive_wins():
    rng = random.Random(0)
    for _ in range(10):
        assert sample_weighted({"x": 3, "y": 0}, rng) == "x"

def test_sample_weighted_cdf_boundaries_are_respected():
    w = {"a": 1, "b": 3, "c": 6} 
    class FakeRNG:
        def __init__(self, seq): self.seq, self.i = seq, 0
        def random(self): v = self.seq[self.i % len(self.seq)]; self.i += 1; return v
    rng = FakeRNG([0.05, 0.25, 0.75])  
    assert sample_weighted(w, rng) == "a"
    assert sample_weighted(w, rng) == "b"
    assert sample_weighted(w, rng) == "c"

def test_sample_weighted_default_rng_returns_key():
    assert sample_weighted({"a": 1, "b": 1}) in {"a", "b"}