class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right


def build(arr: list) -> Node:
    root = Node(arr[0])
    for x in arr[1:]:
        root = insert(root, Node(x))
    return root


def insert(tree: Node, node: Node) -> Node:
    if tree.key >= node.key:
        if tree.left is None:
            tree.left = node
        elif tree.right is None:
            tree.right = node
        else:
            tree.left = insert(tree.left, node)

        return tree

    node.left = tree.left
    node.right = tree.right
    tree.left = None
    tree.right = None
    if node.left is None:
        node.left = tree
    elif node.right is None:
        node.right = tree
    else:
        node.left = insert(node.left, tree)
    return node
        

def pop(tree: Node) -> Node:
    voted = tree.left

    if tree.right and voted and voted.key < tree.right.key:
        voted = tree.right
    else:
        voted = tree.right

    if voted is None:
        return None

    if voted is tree.left:
        voted.right = tree.right
        voted.left = pop(voted)
    else:
        voted.left = tree.left
        voted.right = pop(voted)

    return voted


def get_max(tree: Node):
    return tree.key


def travesal(root: Node):
    print(root.key, end=" ")
    if root.left:
        travesal(root.left)

    if root.right:
        travesal(root.right)


if __name__ == '__main__':
    arr = [1,2,3,1,2,4,3,2,7]
    tree = build(arr)
    travesal(tree)
    print("")
    tree = pop(tree)
    travesal(tree)
