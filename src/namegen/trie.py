
class TrieNode:
    ""
    def __init__(self, letter):
        self.letter = letter
        self.children = {}
        self.is_end_of_name = False

class Trie:
    ""
    def __init__(self):
        self.root = TrieNode("*")
        
    def add_name(self, name):
        curr_node = self.root
        for letter in name:
            if letter not in curr_node.children:
                curr_node.children[letter] = TrieNode(letter)
            curr_node = curr_node.children[letter]
        curr_node.is_end_of_name = True

    def does_name_exist(self, name):
        if name == "":
            return True
        curr_node = self.root
        for letter in name:
            if letter not in curr_node.children:
                return False
            curr_node = curr_node.children[letter]
        return curr_node.is_end_of_name


trie = Trie()
names = ["tim", "timothy", "amogelang", "amor", "amore"]
for name in names:
    trie.add_name(name)

print(trie.does_name_exist("tim")) # True
print(trie.does_name_exist("")) # True
print(trie.does_name_exist("timo")) # False
print(trie.does_name_exist("amogelang")) # True
print(trie.does_name_exist("amorr")) # False
print(trie.does_name_exist("amore")) # True
print(trie.does_name_exist("timothy")) # True





