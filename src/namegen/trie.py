from collections import Counter, defaultdict

class NGramTrie:
    ""
    def __init__(self, n):
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.counts = defaultdict(Counter)


    def tokenize_with_markers(self, name):
        return ["<s>"]*(self.n-1) + list(name) + ["</s>"]
        
    def add_name(self, name):
        tokens = self.tokenize_with_markers(name)
        for i in range(self.n - 1, len(tokens)):
            context = tuple(tokens[i- (self.n - 1): i ]) if self.n > 1 else tuple()
            next_token = tokens[i]

            self.counts[context][next_token] += 1


    def candidates(self, context):
        tuple_context = tuple(context)
        if len(tuple_context) != self.n-1:
            raise ValueError("context length must be n-1")
        return self.counts.get(tuple_context, Counter())
    

    def total_successors(self, context):
        return sum(self.candidates(context).values())

trie = NGramTrie(n=3)
names = ["anna", "anne"]
for name in names:
    trie.add_name(name)

print(trie.candidates(("<s>", "<s>")))   # {'a': 2}
print(trie.candidates(("a", "n")))       # {'n': 2}
print(trie.candidates(("n", "n")))       # {'a': 1, 'e': 1}
print(trie.total_successors(("n", "n"))) # 2


