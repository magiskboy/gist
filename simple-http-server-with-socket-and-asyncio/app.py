from urllib.parse import parse_qs
import json


class Headers(dict):
    def __setitem__(self, k, v):
        super().__setitem__(k.lower(), v)

    def __getitem__(self, k):
        return super().__getitem__(k.lower())

    def get(self, key):
        return super().get(key.lower())

    @classmethod
    def from_list(cls, headers) -> "Headers":
        h = cls()
        for k, v in headers:
            h.__setitem__(k, v)
        return h


class Request:
    def __init__(self):
        self.url = ""
        self.schema = ""
        self.host = ""
        self.port = 80
        self.path = ""
        self.args = {}
        self.headers = Headers()
        self.body = b""
        self.method = ""
        self._environments = {}

    @classmethod
    def from_environments(cls, environments: dict) -> "Request":
        headers = Headers.from_list(environments.get("headers", []))

        request = cls()

        request.url = environments.get("url").decode("utf-8")

        request.schema = environments.get("url.schema", b"http").decode("utf-8")

        request.host = environments.get("url.host") or headers.get("host")
        if isinstance(request.host, bytes):
            request.host = request.host.decode("utf-8")

        request.port = environments.get("url.port") or 80

        request.path = environments.get("url.path").decode("utf-8")

        request.args = parse_qs(environments.get("url.query", ""))

        request.headers = Headers()
        for k, v in headers.items():
            request.headers[k.decode("utf-8")] = v.decode("utf-8")

        request.body = environments.get("body")

        request.method = environments.get("method", "get").upper().decode("utf-8")

        request._environments = environments

        return request

    @property
    def text(self) -> str:
        return self.body.decode("utf-8")

    @property
    def json(self) -> dict:
        if self.headers.get("content-type") == "application/json":
            try:
                return json.loads(self.body)
            except Exception:
                return {}

        raise ValueError("content-type of response must be application/json")

    def __str__(self):
        return f"<Request: {self.method} {self.path}>"


class Response:
    def __init__(
        self, 
        content: str | dict | list = "",
        status_code: int = 200, 
        headers: Headers = None
    ):
        if isinstance(content, str):
            self.content = content
        elif isinstance(content, (dict, list)):
            self.content = json.dumps(content)
        else:
            self.content = ""
        self.status_code = status_code
        self.headers = headers

    def __str__(self):
        return f"<Response {self.status_code}>"


class Application:
    def __init__(self):
        self._endpoints = {}

    def add_endpoint(self, url: str, method: str, handler):
        self._endpoints[(url, method.lower())] = handler

    def get(self, url: str):
        def deco(func):
            self.add_endpoint(url, "GET", func)
        return deco

    def post(self, url: str):
        def deco(func):
            self.add_endpoint(url, "POST", func)
        return deco

    def put(self, url: str):
        def deco(func):
            self.add_endpoint(url, "PUT", func)
        return deco

    def patch(self, url: str):
        def deco(func):
            self.add_endpoint(url, "PATCH", func)
        return deco

    def delete(self, url: str):
        def deco(func):
            self.add_endpoint(url, "DELETE", func)
        return deco

    def get_handler_for(self, path: str, method: str):
        return self._endpoints.get((path, method.lower()))

    async def __call__(self, environment):
        request = Request.from_environments(environment)
        # routing
        handler = self.get_handler_for(request.path, request.method)
        if handler:
            response = await handler(request)
        else:
            response = Response("Not Found", 404)

        return self.make_http_response_message(response)

    def make_http_response_message(self, response: Response) -> bytes:
        lines = []
        
        lines.append(f"HTTP/1.1 {response.status_code} OK\r\n")
        if response.headers:
            for k, v in response.headers.items():
                lines.append(f"{k}:{v}\r\n")
        lines.append("\r\n")
        if response.content:
            lines.append(response.content)
            lines.append("\r\n")
        lines.append("\r\n")
        return "".join(lines)
