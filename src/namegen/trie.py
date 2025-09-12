from collections import Counter, defaultdict

class NGramTrie:
    """An n-gram trie that stores successor counts for name generation.

    This data structure records how often each token follows a given
    context of length n-1. It is used as the backbone of an n-gram model for generating names.
    """
    def __init__(self, n):
        """Initialize an n-gram trie.

        Args:
            n (int): Order of the n-gram model. Must be >= 1.

        Raises:
            ValueError: If n is less than 1.
        """
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.counts = defaultdict(Counter)


    def tokenize_with_markers(self, name):
        """Convert a name into tokens with start and end markers.

        Args:
            name (str): The raw name string.

        Returns:
            list[str]: List of tokens, including n-1 start markers and
            a single end marker.
        """
        return ["<s>"]*(self.n-1) + list(name) + ["</s>"]
        
    def add_name(self, name):
        """Add a name to the trie by updating successor counts.

        Args:
            name (str): A cleaned name string to insert into the model.
        """
        tokens = self.tokenize_with_markers(name)
        for i in range(self.n - 1, len(tokens)):
            context = tuple(tokens[i- (self.n - 1): i ]) if self.n > 1 else tuple()
            next_token = tokens[i]

            self.counts[context][next_token] += 1


    def candidates(self, context):
        """Get all possible successor tokens for a given context.

        Args:
            context (tuple[str]): The context of length n-1 tokens.

        Returns:
            collections.Counter: A Counter mapping successor tokens to their frequencies.

        Raises:
            ValueError: If the context length is not n-1.
        """
        tuple_context = tuple(context)
        if len(tuple_context) != self.n-1:
            raise ValueError("context length must be n-1")
        return self.counts.get(tuple_context, Counter())
    

    def total_successors(self, context):
        """Count the total number of successors for a given context.

        Args:
            context (tuple[str]): The context of length n-1 tokens.

        Returns:
            int: The sum of all successor counts for the context.
        """
        return sum(self.candidates(context).values())



# Example usage
trie = NGramTrie(n=3)
names = ["anna", "anne"]
for name in names:
    trie.add_name(name)

print(trie.candidates(("<s>", "<s>")))   # {'a': 2}
print(trie.candidates(("a", "n")))       # {'n': 2}
print(trie.candidates(("n", "n")))       # {'a': 1, 'e': 1}
print(trie.total_successors(("n", "n"))) # 2


