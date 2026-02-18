class Node:
    def __init__(self):
        self.children = dict()
        self.is_end_of_word = False 

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        current = self.root 
        for char in word:
            if char not in current.children:
                current.children[char] = Node()
            current = current.children[char]
        current.is_end_of_word = True 
        return f"{word} inserted to trie"

    def delete(self, word):
        def _delete(node, word, depth):
            if len(word) == depth:
                node.is_end_of_word = False 
                return len(node.children) == 0 
            char = word[depth]
            delete_child = _delete(node.children[char], word, depth + 1)
            if delete_child:
                del node.children[char]
                return (not node.is_end_of_word) and (len(node.children) == 0)
            return False
        _delete(self.root, word, 0)
        return 

    def prefix(self, prefix):
        current = self.root 
        for char in prefix:
            if char not in current.children:
                return None 
            current = current.children[char]
        words = []
        def dfs(node, path):
            if node.is_end_of_word is True:
                words.append(path)
            for char, child in node.children.items():
                dfs(child, path + char)
        dfs(current, prefix)
        return words