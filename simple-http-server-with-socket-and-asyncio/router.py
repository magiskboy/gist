import re
from queue import LifoQueue


int_pattern = "([\d]+)"
str_pattern = "([\w]+)"


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


if __name__ == "__main__":
    path = "/users/{id:int}/info/{field_name:str}"
    variables, matcher = parse_url_pattern(path)
    url = "/users/1/info/username"
    args = parse_url(url, variables, matcher) 
    print(args)
