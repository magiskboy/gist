from typing import Optional


class Node:
    def __init__(self, key: int, left: Optional["Node"] = None, right: Optional["Node"] = None):
        self.key = key
        self.left = left
        self.right = right


def insert(array: list) -> Node:
    root = Node(array[0])

    for x in array[1:]:
        push(root, Node(x))

    return root


def push(root: Node, node: Node):
    c = root
    while True:
        if node.key >= c.key:
            if c.right is None:
                c.right = node
                break
            else:
                c = c.right
        else:
            if c.left is None:
                c.left = node
                break
            else:
                c = c.left


def search(root: Node, key) -> Node | None:
    c = root
    while c:
        if c.key == key:
            return c

        if key >= c.key:
            c = c.right
        else:
            c = c.left

    return None


def travesal(root: Node, func=None):
    """In-order travesal"""
    if root.left:
        travesal(root.left, func)

    if func:
        func(root)

    if root.right:
        travesal(root.right, func)


if __name__ == '__main__':
    a = [5,4,3,2,1]
    tree = insert(a)
    travesal(tree, lambda x: print(x.key, end=" "))
