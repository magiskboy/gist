## Simple HTTP server with asyncio and socket programming

In this demo, I use asyncio for listening and handling connections from the client and `httptools` for parsing HTTP message.

One of the most important things is routing in the web application, which is implemented in pure Python, you can see them in the following:

```python
def parse_url_pattern(pattern):
    variables = []
    matcher = r""
    stack = LifoQueue()
    stop_append = False
    for token in pattern:
        if token == '{':
            stack.put(token)
            stop_append = True
        elif token == '}':
            var_name = ""
            while True:
                char = stack.get()
                if char == '{':
                    break
                var_name = char + var_name

            name, op_type = var_name.split(":")
            variables.append((name, int if op_type == "int" else str))
            matcher += int_pattern if op_type == "int" else str_pattern
            stop_append = False
        else:
            stack.put(token)
            if not stop_append:
                matcher += token
    return variables, matcher


def parse_url(url, variables, matcher):
    gs = re.match(matcher, url)
    args = {}
    if gs:
        for i, var in enumerate(variables):
            name, type = var
            args[name] = type(gs.group(i+1))
    return args
```

When defining router, application uses to parse pattern. You will get regex of pattern for matching after.

When application received a url, it uses parsed regex to test and routing it.
