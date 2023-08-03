from typing import Any

class Node:
    def __init__(self, val=None, previous=None, next=None):
        self.val = val
        self.next = next
        self.previous = previous


def insert(head: Node, pos: int, node: Node) -> Node | None:
    if pos == 0:
        node.next = head
        head.previous = node
        return node

    c = head
    for i in range(1, pos):
        if c is None:
            return

        c = c.next

    # link to behind node
    node.next = c.next
    if c.next:
        c.next.previous = node

    # link to front node
    c.next = node
    node.previous = c

    return head


def delete(head: Node, pos: int) -> Node | None:
    if pos == 0:
        deleted_node = head

        head = head.next
        if head.next:
            head.next.previous = head

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
        if deleted_node.next:
            deleted_node.next.previous = c

    del deleted_node
    return head


def get(head: Node, pos: int) -> Any | None:
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
