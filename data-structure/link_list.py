class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


def insert(head: Node, pos: int, node: Node) -> Node | None:
    if pos == 0:
        node.next = head
        return node

    c = head
    for i in range(1, pos):
        if c is None:
            return

        c = c.next

    node.next = c.next
    c.next = node
    return head


def delete(head: Node, pos: int) -> Node | None:
    if pos == 0:
        deleted_node = head
        head = head.next
        del deleted_node
        return head

    c = head
    for i in range(1, pos):
        if c is None:
            return
        c = c.next

    deleted_node = c.next
    if deleted_node:
        c.next = deleted_node.next

    del deleted_node
    return head


def get(head: Node, pos: int) -> Node | None:
    c = head
    for i in range(pos):
        if c is None:
            return
        c = c.next
    return c


def display(head: Node):
    c = head
    while c:
        print(c.val, end=" ")
        c = c.next


if __name__ == '__main__':
    head = Node(1)
    head.next = Node(2)
    head.next.next = Node(3)
    head.next.next.next = Node(4)
    head.next.next.next.next = Node(5)


    head = delete(head, 3)
    display(head)
