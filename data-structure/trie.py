class Node:
    def __init__(self, key, children: list["Node"] | None = None, is_word = False):
        self.key = key
        self.children = children or []
        self.is_word = is_word


def build(words: list[str]) -> Node:
    trie = Node(None)
    for word in words:
        push(trie, word)

    return trie


def push(trie: Node, word: str):
    c = trie

    for char in word:
        node = None
        for child in c.children:
            if child.key == char:
                node = child
                break

        if node is None:
            node = Node(char)
            c.children.append(node)

        c = node
    c.is_word = True
