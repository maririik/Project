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
        
         This method  validates the order against the data, resets the trie, and for each name:
            1) Builds/extends the trie path for the name while caching the node path.
            2) Updates successor counts:
            - For order==1, increments counts on the root for each character.
            - For order>1, records the starting (order-1)-prefix in `start_counts`
            and, for each position i >= order-1, increments the count of
            `chars[i]` in `nodes_path[i].next_counts`.

        Args:
            names (iterable[str]): Collection of training names.

        Raises:
            ValueError:If no names are provided or if `order` exceeds the longest
            training name length.
        """
        names_norm = [self.norm(n) for n in names]
        self.names = set(names_norm)

        if not self.names:
            raise ValueError("No training names provided.")
        


        max_len = max(len(n) for n in self.names)
        if self.order > max_len:
            raise ValueError(
                f"order ({self.order}) cannot exceed the longest name length ({max_len})"
            )

        self.root = Node()
        self.start_counts = {}

        
        for name in self.names:
            if not name:
                continue

            node = self.root
            chars = list(name)
            nodes_path = [self.root] 

            for ch in chars:
                if ch not in node.children:
                    node.children[ch] = Node()
                node = node.children[ch]
                nodes_path.append(node)

            if self.order == 1:
                for ch in chars:
                    self.root.next_counts[ch] = self.root.next_counts.get(ch, 0) + 1
                continue

            
            if len(chars) >= self.order - 1:
                start_ctx = "".join(chars[: self.order - 1])
                self.start_counts[start_ctx] = self.start_counts.get(start_ctx, 0) + 1

            for i in range(self.order - 1, len(chars)):
                ctx_node = nodes_path[i]
                nxt = chars[i]
                ctx_node.next_counts[nxt] = ctx_node.next_counts.get(nxt, 0) + 1


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