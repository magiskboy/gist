from typing import Any
import bidirect_linked_list as ll


class Queue:
    def __init__(self, capacity: int | None = None):
        self.capacity = capacity
        self.size = 0
        self.head: ll.Node | None = None
        self.pre_tail: ll.Node | None = None

    def push(self, val: Any):
        if self.is_full():
            raise ValueError("Queue is full")

        if self.head is None:
            self.head = ll.Node(val)
            self.tail = self.head

        else:
            node = ll.Node(val)
            self.head = ll.insert(self.head, 0, node)

        self.size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise ValueError("Queue is empty")

        ret = self.tail
        self.tail = ret.previous
        self.size -= 1
        return ret

    def is_empty(self) -> bool:
        return self.size == 0

    def is_full(self) -> bool:
        if self.capacity is None:
            return False
        return self.size == self.capacity
