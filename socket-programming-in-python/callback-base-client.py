import time
import socket
from selectors import (
    DefaultSelector,
    EVENT_READ,
    EVENT_WRITE,
)

selector = DefaultSelector()
n_tasks = 0


def readable(s, chunks):
    global n_tasks
    # s is readable
    selector.unregister(s.fileno())
    chunk = s.recv(100)
    if chunk:
        chunks.append(chunk)
        callback = lambda: readable(s, chunks)
        selector.register(s.fileno(), EVENT_READ, data=callback)
    else:
        body = (b''.join(chunks)).decode()
        print(body.split('\n')[0])
        n_tasks -= 1


def connected(s, request):
    # s is writable
    selector.unregister(s.fileno())
    s.send(request.encode())
    chunks = []
    callback = lambda: readable(s, chunks)
    selector.register(s.fileno(), EVENT_READ, data=callback)


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

    callback = lambda: connected(s, request)
    selector.register(s.fileno(), EVENT_WRITE, data=callback)


def main():
    a = time.time()
    get('/')
    get('/')
    get('/')
    get('/')
    get('/')
    get('/')
    get('/')

    while n_tasks:
        events = selector.select()
        for event, mask in events:
            cb = event.data
            cb()

    print('Took time %f' % (time.time() - a))

if __name__ == '__main__':
    main()
