from interpreter import Interpreter
from lexer import Lexer
from parser import Parser

def main():
    while True:
        line = input(">>> ")
        if (line == "exit"):
            break
        lexer = Lexer('<console>', line)
        tokens, error = lexer.make_tokens()
        
        if error:
            print(error.as_string())
            continue
        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error:
            print(ast.error.as_string())
            continue

        interpreter = Interpreter()
        
        result = interpreter.visit(ast.node)
        if result.error:
            print(result.error.as_string())
            continue
        print(result.value)

if __name__ == '__main__':
    main()