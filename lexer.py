import re


def tokenize(code):
    token_specification = [
        ("KEYWORD", r"(nocap|huh|finna|yap|sigma|noway|unless)"),  # Keywords
        ("ASSIGN", r"="),  # Assignment operator
        ("END", r";"),  # End of statement
        ("ID", r"[A-Za-z_]\w*"),  # Identifiers
        ("STRING", r"\".*?\""),  # String literals
        ("LPAREN", r"\("),  # Left parenthesis
        ("RPAREN", r"\)"),  # Right parenthesis
        ("LBRACE", r"{"),  # Left curly brace
        ("RBRACE", r"}"),  # Right curly brace
        ("TEMPLATE_LITERAL", r"`[^`]*`"),  # Template literals
        ("INCREMENT", r"\+\+"),  # Increment operator
        ("DECREMENT", r"--"),  # Decrement operator
        ("OP", r"[+*\/-]"),  # Arithmetic operators
        ("NUMBER", r"\d+(\.\d*)?"),  # Numbers
        ("COMMA", r","),  # Comma
        ("LT", r"<"),  # Less than
        ("GT", r">"),  # Greater than
        ("EQ", r"=="),  # Equal to
        ("GE", r">="),  # Greater than or equal to
        ("LE", r"<="),  # Less than or equal to
        ("NE", r"!="),  # Not equal to
        ("AND", r"&&"),  # Logical and
        ("OR", r"\|\|"),  # Logical or
        ("NEWLINE", r"\n"),  # Line endings
        ("COMMENT", r"#.*"),  # Single-line comments
        ("SKIP", r"[ \t]+"),  # Skip over spaces and tabs
        ("MISMATCH", r"."),  # Any other character
    ]

    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    line_num = 1
    mo = get_token(code)
    pos = 0

    while mo is not None:
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == "NEWLINE":
            line_num += 1
        elif kind != "SKIP" and kind != "MISMATCH":
            yield kind, value
        elif kind == "COMMENT":
            pass
        elif kind == "MISMATCH":
            raise RuntimeError(f"{value} unexpected on line {line_num}")
        pos = mo.end()
        mo = get_token(code, pos)

    if pos != len(code):
        raise RuntimeError(f"Unexpected character {code[pos]} on line {line_num}")
