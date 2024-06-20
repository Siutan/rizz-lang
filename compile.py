from lexer import tokenize
from rizz_parser import parse
import os

with open("test.rizz", "r") as f:
    code = f.read()
    tokens = list(tokenize(code))
    result = "\n".join(parse(tokens))
    filename = "./dist/index.js"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(result)
        
    print("Code written to", filename)
