import pytest

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