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
            elif value == "noway":
                yield parse_if_else(it)
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
    body = parse_block(it)
    return f"function {name}({', '.join(params)}) {{\n{body}\n}}"


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

def parse_assignment(it, name, kind, value):
    if kind == "ASSIGN":
        kind, value = next(it)
        if kind == "NUMBER" or kind == "ID" or kind == "STRING":
            assignment = f"{name} = {value};\n"
            next(it)  # Skip the ';' token
            return assignment
    elif kind == "INCREMENT":
        next(it)  # Skip the ';' token
        return f"{name}++;\n"
    elif kind == "DECREMENT":
        next(it)  # Skip the ';' token
        return f"{name}--;\n"
    elif kind == "OP":
        op = value
        kind, value = next(it)
        if kind == "NUMBER" or kind == "ID":
            assignment = f"{name} {op}= {value};\n"
            next(it)  # Skip the ';' token
            return assignment
    raise SyntaxError("Invalid assignment")



def parse_function_call(it, func_name):
    args = []
    while True:
        kind, value = next(it)
        if kind == "ID" or kind == "NUMBER" or kind == "STRING":
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
    body = parse_block(it)

    return f"while ({''.join(condition)}) {{\n{body}\n}}"

def parse_if_else(it):
    condition = []

    # Parse the condition for the 'noway' keyword
    while True:
        kind, value = next(it)
        if kind == "RPAREN":
            break
        condition.append(value)

    _, _ = next(it)  # Skip the '{' token
    body = parse_block(it)

    result = f"if ({''.join(condition)}) {{\n{body}\n}}"

    # Parse subsequent 'unless' blocks
    while True:
        next_token = next(it, None)
        if next_token:
            kind, value = next_token
            if kind == "KEYWORD" and value == "unless":
                kind, value = next(it)
                if kind == "KEYWORD" and value == "noway":
                    condition = []
                    while True:
                        kind, value = next(it)
                        if kind == "RPAREN":
                            break
                        condition.append(value)
                    _, _ = next(it)  # Skip the '{' token
                    body = parse_block(it)
                    result += f" else if ({''.join(condition)}) {{\n{body}\n}}"
                else:
                    condition = []
                    while True:
                        kind, value = next(it)
                        if kind == "RPAREN":
                            break
                        condition.append(value)
                    _, _ = next(it)  # Skip the '{' token
                    body = parse_block(it)
                    result += f" else {{\n{body}\n}}"
            else:
                break
        else:
            break
    return result


def parse_block(it):
    body = []
    while True:
        try:
            kind, value = next(it)
        except StopIteration:
            raise SyntaxError("Unexpected end of input while parsing block")
        
        if kind == "KEYWORD":
            if value == "yap":
                body.append(parse_print(it))
            elif value == "nocap":
                body.append(parse_declaration(it, "const"))
            elif value == "huh":
                body.append(parse_declaration(it, "let"))
            elif value == "finna":
                body.append(parse_function(it))
            elif value == "sigma":
                body.append(parse_while(it))
            elif value == "noway":
                body.append(parse_if_else(it))
            else:
                raise SyntaxError(f"Unexpected keyword {value}")
        elif kind == "ID":
            # Peek at the next token to decide whether it's a function call or an assignment
            next_token = next(it, None)
            if next_token:
                next_kind, next_value = next_token
                if next_kind == "LPAREN":
                    body.append(parse_function_call(it, value))
                else:
                    # If it's not a function call, put the token back and parse as assignment
                    body.append(parse_assignment(it, value, next_kind, next_value))
            else:
                raise SyntaxError(f"Unexpected end of input after ID {value}")
        elif kind == "RBRACE":
            break
        else:
            raise SyntaxError(f"Unexpected token {kind} {value}")
    return ''.join(body)

