from antlr4 import InputStream, StdinStream, CommonTokenStream
from schemeLexer import schemeLexer
from schemeParser import schemeParser
from EvalVisitor import EvalVisitor
from exceptions import Nothing
import sys


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], 'r', encoding='utf-8') as file:
                # S'executa el main de la funció sempre
                content = file.read()
                content += "\n(main)"
                input_stream = InputStream(content)
        else:
            input_stream = StdinStream(encoding='utf-8')
    except FileNotFoundError:
        print("Error: Arxiu no trobat.")
        sys.exit(1)
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

try:
    lexer = schemeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)
    tree = parser.root()

    visitor = EvalVisitor()
    visitor.visit(tree)
except Nothing as n:
    print(n)
except Exception:
    print("Aplicació no vàlida")