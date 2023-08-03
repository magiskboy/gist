import link_list as ll


class Stack:
    def __init__(self, capacity: int | None = None):
        self.head: ll.Node | None = None
        self.capacity = capacity
        self.size = 0

    def is_empty(self) -> bool:
        return self.head is None

    def is_full(self) -> bool:
        if self.capacity is None:
            return False
        return self.size == self.capacity

    def pop(self):
        if self.is_empty():
            raise ValueError("Stack is empty")

        ret = self.head
        self.head = self.head.next
        self.size -= 1
        return ret.val

    def push(self, val):
        if self.is_full():
            raise ValueError("Stack is full")

        if self.head is None:
            self.head = ll.Node(val)
        else:
            self.head = ll.insert(self.head, ll.Node(val), 0)
        self.size += 1
