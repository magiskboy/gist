import time
import socket
from selectors import (
    DefaultSelector,
    EVENT_READ,
    EVENT_WRITE,
)


selector = DefaultSelector()
n_tasks = 0


class Future:
    def __init__(self):
        self.callbacks = []

    def resolve(self):
        for c in self.callbacks:
            c()

class Task:
    def __init__(self, gen):
        self.gen = gen
        self.step()

    def step(self):
        try:
            f = next(self.gen)
        except StopIteration:
            return
        f.callbacks.append(self.step)


def get(path):
    global n_tasks
    n_tasks += 1
    request = 'GET %s HTTP/1.0\n\r\n\r' % path
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    f = Future()
    selector.register(s.fileno(), EVENT_WRITE, data=f)
    yield f
    # s is writable
    selector.unregister(s.fileno())
    s.send(request.encode())

    # s is readable
    chunks = []
    while True:
        f = Future()
        selector.register(s.fileno(), EVENT_READ, data=f)
        yield f
        selector.unregister(s.fileno())
        chunk = s.recv(100)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body.split('\n')[0])
            n_tasks -= 1
            return


def main():
    a = time.time()
    Task(get('/'))
    Task(get('/'))

    while n_tasks:
        events = selector.select()
        for event, mask in events:
            f = event.data
            f.resolve()

    print('Took time %f' % (time.time() - a))


if __name__ == '__main__':
    main()
