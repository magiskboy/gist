## Simple HTTP Parser in Python

Parser can parse multiple chunks.

### Performance

Parse can parse 80k message per second in Python 3.11 and 1.5 million message per second in PyPy3.9 7.3.11

I also implement this parser in C, you can checkout [magiskboy/http-parser](https://github.com/magiskboy/http-parser)

Implementation `feed_data` method:

```python
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
```


Run it

```bash
$ python benchmark.py
```
