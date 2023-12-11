class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def get_height(node):
    if node is None:
        return 0
    return 1 + max(get_height(node.left), get_height(node.right))

def left_rotate(node):
    new_root = node.right
    node.right = new_root.left
    new_root.left = node
    return new_root

def right_rotate(node):
    new_root = node.left
    node.left = new_root.right
    new_root.right = node
    return new_root

def insert(node, val):
    if node is None:
        return Node(val)

    if val > node.val:
        node.right = insert(node.right, val)
    elif val < node.val:
        node.left = insert(node.left, val)

    left_height = get_height(node.left)
    right_height = get_height(node.right)
    if abs(left_height - right_height) > 1:
        if left_height > right_height:
            node = right_rotate(node)
        else:
            node = left_rotate(node)

    return node

def display(node):
    if node is None:
        print("_", end=" ")
        return
    display(node.left)
    print(node.val, end=" ")
    display(node.right)
        

if __name__ == '__main__':
    arr = [1,5,4,3,6,8,0]

    root = None
    for x in arr:
        root = insert(root, x)

    display(root)
