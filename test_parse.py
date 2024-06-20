import re
from collections import namedtuple

# Define token structure
Token = namedtuple('Token', ['type', 'value'])

class Lexer:
    def __init__(self):
        self.token_specification = [
            ("KEYWORD", r"(nocap|huh|finna|yap|sigma|noway|unless)"),
            ("ASSIGN", r"="),
            ("END", r";"),
            ("ID", r"[A-Za-z_]\w*"),
            ("STRING", r"\".*?\""),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("LBRACE", r"{"),
            ("RBRACE", r"}"),
            ("TEMPLATE_LITERAL", r"`[^`]*`"),
            ("INCREMENT", r"\+\+"),
            ("DECREMENT", r"--"),
            ("OP", r"[+*\/-]"),
            ("NUMBER", r"\d+(\.\d*)?"),
            ("COMMA", r","),
            ("LT", r"<"),
            ("GT", r">"),
            ("EQ", r"=="),
            ("GE", r">="),
            ("LE", r"<="),
            ("NE", r"!="),
            ("AND", r"&&"),
            ("OR", r"\|\|"),
            ("NEWLINE", r"\n"),
            ("COMMENT", r"#.*"),
            ("SKIP", r"[ \t]+"),
            ("MISMATCH", r"."),
        ]

        self.tok_regex = "|".join("(?P<%s>%s)" % pair for pair in self.token_specification)
        self.get_token = re.compile(self.tok_regex).match

    def tokenize(self, code):
        line_num = 1
        pos = 0
        mo = self.get_token(code)

        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == "NEWLINE":
                line_num += 1
            elif kind != "SKIP" and kind != "COMMENT":
                yield Token(kind, value)
            elif kind == "MISMATCH":
                raise RuntimeError(f"{value} unexpected on line {line_num}")
            pos = mo.end()
            mo = self.get_token(code, pos)

        if pos != len(code):
            raise RuntimeError(f"Unexpected character {code[pos]} on line {line_num}")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise RuntimeError(f"Expected token {token_type} but got {self.current_token}")

    def parse(self):
        statements = []
        while self.current_token:
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token.type == 'KEYWORD':
            if self.current_token.value == 'nocap':
                return self.assignment()
            elif self.current_token.value == 'huh':
                return self.assignment()
            elif self.current_token.value == 'finna':
                return self.function_declaration()
            elif self.current_token.value == 'sigma':
                return self.loop()
            elif self.current_token.value == 'yap':
                return self.print_statement()
            elif self.current_token.value == 'noway':
                return self.if_statement()
        raise RuntimeError(f"Unexpected token {self.current_token}")

    def assignment(self):
        var_type = self.current_token.value
        self.advance()
        var_name = self.current_token.value
        self.consume('ID')
        self.consume('ASSIGN')
        value = self.expression()
        self.consume('END')
        return ('assignment', var_type, var_name, value)

    def expression(self):
        token = self.current_token
        if token.type in ('NUMBER', 'STRING', 'ID', 'TEMPLATE_LITERAL'):
            self.advance()
            return token
        raise RuntimeError(f"Unexpected token {token}")

    def print_statement(self):
        self.consume('KEYWORD')
        value = self.expression()
        self.consume('END')
        return ('print', value)

    def function_declaration(self):
        self.consume('KEYWORD')
        name = self.current_token.value
        self.consume('ID')
        self.consume('LPAREN')
        params = []
        while self.current_token and self.current_token.type != 'RPAREN':
            if self.current_token.type == 'ID':
                params.append(self.current_token.value)
                self.consume('ID')
            if self.current_token.type == 'COMMA':
                self.consume('COMMA')
        self.consume('RPAREN')
        self.consume('LBRACE')
        body = self.parse()
        self.consume('RBRACE')
        return ('function', name, params, body)

    def if_statement(self):
        self.consume('KEYWORD')
        condition = self.expression()
        self.consume('LBRACE')
        body = self.parse()
        self.consume('RBRACE')
        unless_blocks = []
        while self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'unless':
            self.consume('KEYWORD')
            unless_condition = self.expression()
            self.consume('LBRACE')
            unless_body = self.parse()
            self.consume('RBRACE')
            unless_blocks.append((unless_condition, unless_body))
        return ('if', condition, body, unless_blocks)

    def loop(self):
        self.consume('KEYWORD')
        condition = self.expression()
        self.consume('LBRACE')
        body = self.parse()
        self.consume('RBRACE')
        return ('loop', condition, body)

def parse_code(code):
    lexer = Lexer()
    tokens = list(lexer.tokenize(code))
    parser = Parser(tokens)
    ast = parser.parse()
    return ast

# Example usage
code = """
nocap myName = "jeff";
huh myAge = 28;

finna sayHello(name, age) {
    yap(`hello ${name}, you are ${age}`);

    noway (age < 18) {
        yap("you're a minor");
    } unless noway (age >= 18 && age < 65) {
        yap("you're an adult");
    } unless (age > 65) {
        yap("you're a senior");
    }
}

sayHello(myName, myAge);

huh i = 0;
sigma (i < 5) {
    yap(i);
    i++;
}
"""
ast = parse_code(code)
print(ast)
