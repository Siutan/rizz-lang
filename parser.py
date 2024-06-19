def parse(tokens):
    it = iter(tokens)
    token = next(it, None)
    while token:
        kind, value = token
        print(f"Parsing token: {kind} -> {value}")  # Debug output
        if kind == "KEYWORD":
            if value == "nocap":
                yield parse_declaration(it, "const")
            elif value == "huh":
                yield parse_declaration(it, "let")
            elif value == "finna":
                yield parse_function(it)
            elif value == "yap":
                yield parse_print(it)
            elif value == "sigma":
                yield parse_while(it)
        elif kind == "ID":
            yield parse_function_call(it, value)
        token = next(it, None)



def parse_declaration(it, var_type):
    _, name = next(it)
    _, _ = next(it)  # Skip the '=' token
    kind, value = next(it)
    if kind == "STRING" or kind == "NUMBER":
        _, _ = next(it)  # Skip the ';' token
        return f"{var_type} {name} = {value};"
    else:
        raise SyntaxError("Invalid declaration")


def parse_function(it):
    _, name = next(it)
    _, _ = next(it)  # Skip the '(' token
    params = []
    while True:
        kind, value = next(it)
        if kind == "ID":
            params.append(value)
        elif kind == "RPAREN":
            break
        elif kind == "COMMA":
            continue
        else:
            raise SyntaxError("Invalid function declaration")
    _, _ = next(it)  # Skip the '{' token
    body = []
    while True:
        kind, value = next(it)
        if kind == "KEYWORD" and value == "yap":
            body.append(parse_print(it))
        elif kind == "RBRACE":
            break
        else:
            raise SyntaxError("Invalid function body")
    return f"function {name}({', '.join(params)}) {{\n{''.join(body)}\n}}"


def parse_print(it):
    kind, value = next(it)  # Expecting '(' token
    if kind != "LPAREN":
        raise SyntaxError(f"Expected '(', got {kind}")
    
    kind, value = next(it)  # This should be either TEMPLATE_LITERAL or ID
    if kind == "TEMPLATE_LITERAL":
        content = value
    elif kind == "ID":
        content = value
    else:
        raise SyntaxError(f"Invalid print statement: expected TEMPLATE_LITERAL or ID, got {kind}")

    kind, value = next(it)  # Expecting ')' token
    if kind != "RPAREN":
        raise SyntaxError(f"Expected ')', got {kind}")

    kind, value = next(it)  # Expecting ';' token
    if kind != "END":
        raise SyntaxError(f"Expected ';', got {kind}")

    return f"console.log({content});\n"


def parse_function_call(it, func_name):
    kind, value = next(it)
    if kind != "LPAREN":
        raise SyntaxError(f"Expected '(', got {kind} - {value}")
    args = []
    while True:
        kind, value = next(it)
        print(f"Parsing function call: {kind} -> {value}")  # Debug output
        if kind == "ID":
            args.append(value)
        elif kind == "RPAREN":
            break
        elif kind == "COMMA":
            continue
        else:
            raise SyntaxError(f"Invalid function call: unexpected {kind}")
    kind, value = next(it)
    if kind != "END":
        raise SyntaxError(f"Expected ';', got {kind}")
    return f"{func_name}({', '.join(args)});\n"



def parse_while(it):
    _, _ = next(it)  # Skip the 'sigma' keyword
    condition = []
    
    # Parse the condition
    while True:
        kind, value = next(it)
        if kind == "RPAREN":
            break
        condition.append(value)
    
    _, _ = next(it)  # Skip the '{' token
    body = []
    
    # Parse the body
    while True:
        kind, value = next(it)
        print(f"Parsing while body: {kind} -> {value}")  # Debug output
        if kind == "KEYWORD" and value == "yap":
            body.append(parse_print(it))
        elif kind == "ID":
            body.append(parse_assignment(it, value))
        elif kind == "RBRACE":
            break
        else:
            raise SyntaxError(f"Invalid while loop body {kind} - {value}")
    
    return f"while ({''.join(condition)}) {{\n{''.join(body)}\n}}"




def parse_assignment(it, name):
    kind, value = next(it)
    if kind == "ASSIGN":
        kind, value = next(it)
        if kind == "NUMBER" or kind == "ID":
            assignment = f"{name} = {value};\n"
            next(it)  # Skip the ';' token
            return assignment
    elif kind == "OP":
        op = value
        kind, value = next(it)
        if kind == "NUMBER":
            assignment = f"{name} {op} {value};\n"
            next(it)  # Skip the ';' token
            return assignment
    elif kind == "INCREMENT":
        assignment = f"{name}++;\n"
        next(it)  # Skip the ';' token
        return assignment
    elif kind == "DECREMENT":
        assignment = f"{name}--;\n"
        next(it)  # Skip the ';' token
        return assignment
    raise SyntaxError(f"Invalid assignment {kind} - {value}")
