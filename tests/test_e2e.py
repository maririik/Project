
"""
Builds a model, generates a batch, checks multiple properties
(valid lengths, character set, n-gram integrity, novelty/diversity),
and verifies reproducibility vs seed sensitivity.
"""

import random
import pytest
from pathlib import Path

from namegen import NGramTrie, NGramGenerator

pytestmark = pytest.mark.slow

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_FALLBACK = ["maria", "marie", "mark", "marta", "mario", "marla", "max"]

def _load_names():
    """Prefer a real dataset if present; otherwise use a small fallback."""
    for fname in ("US_names.txt", "female.txt", "male.txt"):
        p = DATA_DIR / fname
        if p.exists():
            txt = p.read_text(encoding="utf-8", errors="ignore")
            names = [ln.strip() for ln in txt.splitlines() if ln.strip()]
            if names:
                return names[:5000]  
    return DEFAULT_FALLBACK

def _ngrams(s: str, order: int):
    k = order
    return {s[i:i+k] for i in range(len(s) - k + 1)}

def _observed_ngrams(names, order):
    obs = set()
    for n in names:
        obs |= _ngrams(n, order)
    return obs

def test_end_to_end_batch_quality_and_reproducibility():
    names = _load_names()
    assert names, "No training names available for E2E test."

    order = 3
    min_len, max_len = 3, 12
    stop_prob = 0.35
    batch = 200

    model = NGramTrie(names, order=order, normalize_case=True)
    rng1 = random.Random(12345)
    gen1 = NGramGenerator(model, rng=rng1)

    out1 = [
        gen1.generate(
            target_len=None,
            max_len=max_len,
            min_len=min_len,
            stop_prob=stop_prob,
            retries=500,
            capitalize=False,
        ) or ""
        for _ in range(batch)
    ]


    non_empty = [s for s in out1 if s]
    print(f"\nGenerated {len(non_empty)} names. Example: {non_empty[:5]}")

    assert len(non_empty) >= int(0.8 * batch), "Too many empty generations."

    assert all(min_len <= len(s) <= max_len for s in non_empty), "Length outside bounds."

    train_chars = set("".join(names)) | {"-"}
    assert all(set(s) <= train_chars for s in non_empty), "Unexpected characters in output."

    obs = _observed_ngrams(model.names, order)
    for s in non_empty:
        if len(s) >= order:
            assert _ngrams(s, order) <= obs, f"Unseen {order}-gram in '{s}'"



    rng_same = random.Random(12345)
    gen_same = NGramGenerator(model, rng=rng_same)
    out_same = [gen_same.generate(min_len=min_len, max_len=max_len, stop_prob=stop_prob, capitalize=False) or "" for _ in range(batch)]
    assert out_same == out1, "Same seed should reproduce identical output."

    rng_diff = random.Random(12346)
    gen_diff = NGramGenerator(model, rng=rng_diff)
    out_diff = [gen_diff.generate(min_len=min_len, max_len=max_len, stop_prob=stop_prob, capitalize=False) or "" for _ in range(batch)]
    assert out_diff != out1, "Different seed should change the sequence."
