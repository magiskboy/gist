import socket
import asyncio
from urllib.parse import unquote
import httptools


class Protocol:
    def __init__(self, app):
        self.environment = {
            "url": b"",
            "url.path": b"",
            "url.port": None,
            "url.host": b"",
            "url.schema": b"",
            "url.query": b"",
            "headers": [],
            "body": b"",
            "method": b"",
            "http_version": b"",
            "http_keep_alive": False,
            "http_upgrade": False
        }
        self._content_length = -1
        self.parser = httptools.HttpRequestParser(self)
        self.app = app
        self.read_done = False

    def on_message_complete(self):
        self.environment["method"] = self.parser.get_method()
        self.environment["http_version"] = self.parser.get_http_version()\
            .encode("utf-8")
        self.environment["http_keep_alive"] = self.parser.should_keep_alive()
        self.environment["http_upgrade"] = self.parser.should_upgrade()
        self.read_done = True
        self.t = asyncio.get_running_loop().create_task(self.on_request_done())

    def on_url(self, url: bytes):
        self.environment["url"] += url

    def on_headers_complete(self):
        url = unquote(self.environment["url"].decode("utf-8"))
        o = httptools.parse_url(url.encode("utf-8"))
        self.environment["url.schema"] = o.schema or b"http"
        self.environment["url.host"] = o.host or b""
        self.environment["url.port"] = o.port or 80
        self.environment["url.path"] = o.path or b""
        self.environment["url.query"] = o.query or b""

        for k, v in self.environment["headers"]:
            if k.lower() == b"content-length":
                self._content_length = int(v.decode("utf-8"))
                break

    def on_header(self, name: bytes, value: bytes):
        self.environment["headers"].append((name, value))

    def on_body(self, body: bytes):
        self.environment["body"] += body

    def on_data(self, data: bytes):
        self.parser.feed_data(data)

    async def on_request_done(self):
        response = await self.app(self.environment)
        return response

    async def process(self):
        data = await self.t
        return data


class Server:
    def __init__(self, app):
        self.app = app
        self.loop = asyncio.get_event_loop()

    async def run(self, host = "127.0.0.1", port = 5000):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(False)
        s.bind((host, port))
        s.listen(1000)
        print(f"Start server at {host}:{port}")
        while True:
            client, address = await self.loop.sock_accept(s)
            self.loop.create_task(self.handle_client(client))

    async def handle_client(self, client: socket.socket):
        protocol = Protocol(self.app)
        with client:
            while not protocol.read_done:
                data = await self.loop.sock_recv(client, 64)
                protocol.on_data(data)

            data = await protocol.process()
            await self.loop.sock_sendall(client, data.encode("utf-8"))

            client.close()
