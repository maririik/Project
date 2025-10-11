"""Trie-backed n-gram name generator.

This module provides a character-level n-gram model implemented on top of a
prefix trie. It can be trained on a list of names and then used to generate
new, name-like strings. 

"""
import random
from .trie import NGramTrie

def sample_weighted(weights, rng=None):
    """Sample a key from a dictionary of weighted counts.

    Args:
        weights_dict (dict[str, int]): Mapping from keys to weights (must be non-negative).
        rng: random.Random or None.

    Returns:
        str or None: Sampled key, or None if total weight <= 0.
    """
    if rng is None:
        rng = random.Random()  
    total = sum(weights.values())
    if total <= 0:
        return None
    r = rng.random() * total
    acc = 0.0
    for k, w in weights.items():
        acc += w
        if r <= acc:
            return k
    return next(iter(weights), None) 



class NGramGenerator:
    """Generates names from a previously built NGramTrie."""

    def __init__(self, model, rng=None):
       self.model = model
       self._rng = rng if rng is not None else random.Random()  
    
    def generate(self, target_len=None, max_len=20, stop_prob=0.20, retries=500, capitalize=True):
        """Generate a new name using the n-gram model.

        You can call this with no arguments to get a random name.  
        Extra parameters let you control length, randomness, and formatting.

        Args:
            target_len (int or None): Exact length of the name. If None, the
                generator may stop early using stop_prob.
            max_len (int): Maximum allowed length. Default is 20.
            stop_prob (float): Chance of stopping early at each step when
                target_len is None. Default is 0.20.
            rng (random.Random or None): Random generator. If None, uses Python's
                built-in random. Useful for reproducibility.
            retries (int): How many times to try generating a valid name before
                giving up. Default is 500.
            capitalize (bool): If True, capitalize the first letter of the
                result. Default is True.

        Returns:
            str or None: A generated name, or None if no valid name could
            be created after retries.
        """
        if target_len is not None and target_len > max_len:
            raise ValueError("target_len cannot exceed max_len")

        for _ in range(retries):
            candidate = self.generate_once(target_len, max_len, stop_prob)
            if candidate and candidate not in self.model.names:
                if target_len is None or len(candidate) == target_len:
                    return candidate.capitalize() if capitalize else candidate
        return None

    def generate_once(self, target_len, max_len, stop_prob):
        """Attempt to generate a single name candidate.

        Args:
            target_len (int or None): Desired exact length of the name, or None for variable length.
            max_len (int): Maximum length of the name.
            stop_prob (float): Stop probability in variable-length mode.
            rng (random.Random): Random number generator.

        Returns:
            str: Candidate name (may be empty if generation failed).
        """
        m = self.model 

        if m.order == 1:
            if not m.root.next_counts:
                return ""
            first = sample_weighted(m.root.next_counts, self._rng)
            if first is None:
                return ""
            name_chars = [first]
        else:
            if not m.start_counts:
                return ""
            start_ctx =  sample_weighted(m.start_counts, self._rng)
            if start_ctx is None:
                return ""
            name_chars = list(start_ctx)


        while len(name_chars) < max_len:
            if target_len is not None and len(name_chars) >= target_len:
                break
            if target_len is None and self._rng.random() < stop_prob and "".join(name_chars) in m.names:
                break

            if m.order == 1:
                succ = m.root.next_counts
            else:
                ctx = "".join(name_chars[-(m.order - 1):])
                node = m.get_node(ctx)
                succ = node.next_counts if node else {}

            if not succ:
                break
            ch = sample_weighted(succ, self._rng)
            if ch is None:
                break
            name_chars.append(ch)

        return "".join(name_chars)


