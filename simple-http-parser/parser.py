STATE_METHOD = 0
STATE_PATH = 1
STATE_HTTP_VERSION = 2
STATE_HEADER = 3
STATE_BODY = 4


class Parser:
    def __init__(self, protocol):
        self.protocol = protocol
        self.current_state = STATE_METHOD
        self.current_token = b""

    def feed_data(self, data: bytes):
        idx = 0
        len_data = len(data)
        while idx < len_data:
            if self.current_state == STATE_METHOD:
                i = data.find(b" ", idx)
                if i == -1:
                    self.current_token += data[idx:]
                    break
                else:
                    self.current_token += data[idx:i]
                    self.protocol.on_method(self.current_token)
                    self.current_token = b""
                    idx = i + 1
                    self.current_state = STATE_PATH
                    continue

            if self.current_state == STATE_PATH:
                i = data.find(b" ", idx)
                if i == -1:
                    self.current_token += data[idx:]
                    break
                else:
                    self.current_token += data[idx:i]
                    self.protocol.on_path(self.current_token)
                    self.current_token = b""
                    idx = i + 1
                    self.current_state = STATE_HTTP_VERSION
                    continue

            if self.current_state == STATE_HTTP_VERSION:
                i = data.find(b"\n", idx)
                if i == -1:
                    self.current_token += data[idx:]
                    break
                else:
                    self.current_token += data[idx:i]
                    self.protocol.on_http_version(self.current_token[:-1])
                    self.current_token = b""
                    idx = i + 1
                    self.current_state = STATE_HEADER
                    continue

            if self.current_state == STATE_HEADER:
                i = data.find(b"\n", idx)
                if i == -1:
                    self.current_token += data[idx:]
                    break
                else:
                    self.current_token += data[idx:i]
                    if self.current_token == b"\r\n":
                        self.current_state = STATE_BODY
                        self.protocol.on_headers_completed()
                    else:
                        header = self.current_token[:-1]
                        if header:
                            self.protocol.on_header(*self.parse_header(header))
                            self.current_token = b""
                    idx = i + 1

            if self.current_state == STATE_BODY:
                self.protocol.on_body(data[idx:])
                break

    def parse_header(self, header: bytes) -> (bytes, bytes):
        idx = header.find(b":")
        if idx < 0:
            raise ValueError(f"Header {header} is invalid")
        name, value = header[:idx], header[idx+1:]
        return name.strip(), value.strip()


