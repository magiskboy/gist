import logging
from sys import stdout
from socket import socket, SOCK_STREAM, AF_INET
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


logging.basicConfig(stream=stdout, level=logging.INFO)


class Server:
    def __init__(self, host, port, buf_size=64):
        self.addr = (host, port)
        self.poll = DefaultSelector()
        self.m = {}
        self.buf_size = buf_size

    def handle_read(self, sock):  # make isolated environment for each connection
        buffer_size = self.buf_size
        handle_write = self.handle_write

        def _can_read():
            chunks = []
            while 1:
                chunk = sock.recv(buffer_size)
                if chunk.endswith(b'\n\n'):
                    chunks.append(chunk[:-2])
                    break
                else:
                    chunks.append(chunk)
                    yield

            handle_write(sock, b''.join(chunks))

        handler = _can_read()
        self.m[sock] = handler
        self.poll.register(sock, EVENT_READ, handler)

    def handle_write(self, sock, data):     # make isolated environment for each connection
        poll = self.poll
        m = self.m
        buffer_size = self.buf_size

        def _can_write():
            nonlocal data, sock
            start_, end_ = 0, 0
            data = b'Hello ' + data
            len_data = len(data)

            while 1:
                end_ = min(start_ + buffer_size, len_data)
                if start_ >= end_:
                    break
                sock.send(data[start_:end_])
                start_ += buffer_size
                yield

            # clear handler of connection and close conection
            poll.unregister(sock)
            del m[sock]
            sock.close()
            del sock

        handler = _can_write()
        m[sock] = handler
        poll.modify(sock, EVENT_WRITE, handler)

    def handle_accept(self, sock):
        while 1:
            s, addr = sock.accept()
            logging.debug(f'Accept the connection from {addr}')
            self.handle_read(s)
            yield

    def mainloop(self):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.bind(self.addr)
            sock.setblocking(0)
            sock.listen(1024)

            self.m[sock] = self.handle_accept(sock)
            self.poll.register(sock, EVENT_READ, self.m[sock])

            logging.info(f'Server is running at {self.addr}')
            while 1:
                events = self.poll.select()
                for event, _ in events:
                    try:
                        cb = event.data
                        next(cb)
                    except StopIteration:
                        pass
        except Exception as e:
            sock.close()
            self.poll.close()
            raise e


if __name__ == '__main__':
    server = Server('127.0.0.1', 5000)
    server.mainloop()
