"""Trie-backed n-gram name generator.

This module provides a character-level n-gram model implemented on top of a
prefix trie. It can be trained on a list of names and then used to generate
new, name-like strings. 

"""
import random

class Node:
    """A node in the prefix trie.

    Attributes:
        children (dict[str, Node]): Child nodes keyed by character.
        next_counts (dict[str, int]): Successor character counts for n-gram generation.
    """
    def __init__(self):
        self.children = {}
        self.next_counts = {}

class NGramTrie:
    """An n-gram model implemented on top of a prefix trie.

    This class can build a trie from a list of training names and
    generate new names using an n-gram character model.

    Attributes:
        root (Node): Root node of the trie.
        order (int): Order of the n-gram model (e.g., 2 for bigram).
        names (set[str]): Training names.
        start_counts (dict[str, int]): Frequencies of starting contexts of length order-1.
    """

    def __init__(self, names=None, order=2, normalize_case=True) :
        """Set up a new n-gram trie.

        Args:
            names (iterable[str] or None): Training names to build the model from.
                If None, the trie starts empty.
            order (int): Size of the n-grams to use (e.g. 2 = bigram, 3 = trigram).
                Must be at least 1. Default is 2.
            normalize_case (bool): If True, normalize all inputs using casefold()
                so mixed-case datasets are handled uniformly. Default True.

        Raises:
            ValueError: If order is less than 1.
        """
        if order < 1:
            raise ValueError("Order must be >= 1")
        self.root = Node()
        self.order = order
        self.names = set()
        self.start_counts = {}
        self.normalize_case = normalize_case
        if names:
            self.fit(names)

    def norm(self, s: str) -> str:
        """Normalize a string according to case settings.

        Args:
            s (str): Input string to normalize.

        Returns:
            str: Normalized string (case-folded if enabled).
        """
        return s.casefold() if (self.normalize_case and isinstance(s, str)) else s
    
    def fit(self, names):
        """Build the trie and n-gram statistics from training names.

        Args:
            names (iterable[str]): Collection of training names.

        Raises:
            ValueError: If order exceeds the length of the longest training name.
        """
        names_norm = [self.norm(n) for n in names]
        self.names = set(names_norm)

        if self.names:
            max_len = max(len(n) for n in self.names)
            if self.order > max_len:
                raise ValueError(
                    f"order ({self.order}) cannot exceed the longest name length ({max_len})"
                )

        self.build_prefix_trie(self.names)
        self.build_ngram_counts(self.names)

    def successors(self, s):
        """Return successor character counts for a given context string.

        Args:
            s (str): Context string.

        Returns:
            dict[str, int]: Mapping of successor characters to counts.
        """
        s = self.norm(s) 
        ctx = s[-(self.order - 1):] if self.order > 1 else ""
        node = self.get_node(ctx)
        return dict(node.next_counts) if node else {}
    

    def generate(self, target_len=None, max_len=20, stop_prob=0.20, rng=None, retries=500, capitalize=True):
        """Generate a new name using the n-gram model.

        You can call this with no arguments to get a random name.  
        Extra parameters let you control length, randomness, and formatting.

        Args:
            target_len (int or None): Exact length of the name. If None, the
                generator may stop early using stop_prob.
            max_len (int): Maximum allowed length. Default is 20.
            stop_prob (float): Chance of stopping early at each step when
                target_len is None. Default is 0.20.
            rng (random.Random or None): Random generator. If None, uses Python's3
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
        if rng is None:
            rng = random

        for _ in range(retries):
            candidate = self.generate_once(target_len, max_len, stop_prob, rng)
            if candidate and candidate not in self.names:
                if target_len is None or len(candidate) == target_len:
                    return candidate.capitalize() if capitalize else candidate
        return None

    def generate_once(self, target_len, max_len, stop_prob, rng):
        """Attempt to generate a single name candidate.

        Args:
            target_len (int or None): Desired exact length of the name, or None for variable length.
            max_len (int): Maximum length of the name.
            stop_prob (float): Stop probability in variable-length mode.
            rng (random.Random): Random number generator.

        Returns:
            str: Candidate name (may be empty if generation failed).
        """
        if self.order == 1:
            if not self.root.next_counts:
                return ""
            first = sample_weighted(self.root.next_counts, rng)
            if first is None:
                return ""
            name_chars = [first]
        else:
            if not self.start_counts:
                return ""
            start_ctx = sample_weighted(self.start_counts, rng)
            if start_ctx is None:
                return ""
            name_chars = list(start_ctx)


        while len(name_chars) < max_len:
            if target_len is not None and len(name_chars) >= target_len:
                break
            if target_len is None and rng.random() < stop_prob:
                break

            if self.order == 1:
                node = self.root
            else:
                ctx = name_chars[-(self.order - 1):]
                node = self.get_node_chars(ctx)

            if not node:
                break
            succ = node.next_counts
            if not succ:
                break
            ch = sample_weighted(succ, rng)
            if ch is None:
                break
            name_chars.append(ch)

        return "".join(name_chars)

    # ----- trie -----
    def build_prefix_trie(self, names):
        """Build a prefix trie from training names."""
        self.root = Node()
        for name in names:
            node = self.root
            for ch in name:
                if ch not in node.children:
                    node.children[ch] = Node()
                node = node.children[ch]

    def build_ngram_counts(self, names):
        """Build n-gram successor counts from training names.
        
        For each training name, this method:
      - Records the frequency of starting contexts (the first order-1 characters).
      - Updates successor counts for all (order-1)-length contexts that occur
        within the name, so the model can predict the next character.
        """
        self.start_counts = {}
        if self.order == 1:
            self.root.next_counts.clear()
            for name in names:
                for ch in name:
                    self.root.next_counts[ch] = self.root.next_counts.get(ch, 0) + 1
            return

        self.clear_next_counts(self.root)
        for name in names:
            if not name:
                continue
            chars = list(name)

            if len(chars) >= self.order - 1:
                start_ctx = chars[: self.order - 1]
                skey = "".join(start_ctx)
                self.start_counts[skey] = self.start_counts.get(skey, 0) + 1

            if len(chars) >= self.order:
                for i in range(len(chars) - self.order + 1):
                    ctx = chars[i: i + self.order - 1]
                    nxt = chars[i + self.order - 1]
                    ctx_node = self.ensure_path(ctx)
                    ctx_node.next_counts[nxt] = ctx_node.next_counts.get(nxt, 0) + 1

    def ensure_path(self, chars):
        """Ensure a path exists in the trie for the given character sequence.

        Args:
            chars (list[str]): Sequence of characters.

        Returns:
            Node: Node corresponding to the end of the path.
        """
        node = self.root
        for ch in chars:
            if ch not in node.children:
                node.children[ch] = Node()
            node = node.children[ch]
        return node

    def get_node(self, s):
        """Get the trie node for a string.

        Args:
            s (str): String to look up.

        Returns:
            Node or None: Node if the path exists, otherwise None.
        """
        s = self.norm(s)                                
        return self.get_node_chars(list(s)) if s else self.root

    def get_node_chars(self, chars):
        """Get the trie node for a sequence of characters.

        Args:
            chars (list[str]): Character sequence.

        Returns:
            Node or None: Node if the path exists, otherwise None.
        """
        node = self.root
        for ch in chars:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def clear_next_counts(self, node):
        """Clear successor counts recursively for a node and its descendants."""
        node.next_counts.clear()
        for child in node.children.values():
            self.clear_next_counts(child)

def sample_weighted(weights_dict, rng):
    """Sample a key from a dictionary of weighted counts.

    Args:
        weights_dict (dict[str, int]): Mapping from keys to weights (must be non-negative).
        rng (random.Random): Random number generator.

    Returns:
        str or None: Sampled key, or None if total weight <= 0.
    """
    total = sum(weights_dict.values())
    if total <= 0:
        return None
    r = rng.random() * total
    acc = 0.0
    for k, w in weights_dict.items():
        acc += w
        if r <= acc:
            return k
    for k in weights_dict:
        return k
    return None

# ---------------- Usage ----------------
if __name__ == "__main__":
    from pathlib import Path

    PROJECT_DIR = Path(__file__).parent.parent
    DATA_FILE = PROJECT_DIR / "data" / "female.txt"

    if not DATA_FILE.exists():
        print(f"Dataset not found: {DATA_FILE}")
        exit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        names = [line.strip().lower() for line in f if line.strip()]

    print(f"Loaded {len(names)} names from {DATA_FILE}")

    try:
        order = int(input("Enter desired n-gram order (e.g. 2, 3, 4): "))
    except ValueError:
        order = 3

    try:
        target_len = int(input("Enter desired name length (e.g. 6): "))
    except ValueError:
        target_len = None

    model = NGramTrie(names, order=order)

    print(f"\nGenerating names with order={order}, target_len={target_len}...")
    for _ in range(10):
        print(" ->", model.generate(target_len=target_len))