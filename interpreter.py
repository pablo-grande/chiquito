from lark import Lark, Transformer, Token, v_args

parser = Lark.open("chiquito.lark", rel_to=__file__, parser="lalr")


class ASTBuilder(Transformer):
    def start(self, items):
        return items

    def block(self, items):
        return items

    def output(self, items):
        return ("say", items[0])

    def while_(self, items):
        return ("while", items[0], items[1])

    def if_(self, items):
        return ("if", items[0], items[1])

    def op_(self, item):
        return ("op", item)

    def assign_(self, items):
        return ("set", items[0])

    @v_args(inline=True)
    def number(self, n):
        return ("num", int(str(n)))

    def true(self, _):
        return ("bool", True)

    def false(self, _):
        return ("bool", False)

    @v_args(inline=True)
    def string(self, s):
        return ("str", s[1:-1])

    @v_args(inline=True)
    def var(self):
        return ("var",)


class Interpreter:
    def __init__(self):
        self.var = None
        self.operators = {
            "POR LA GLORIA DE MI MADRE": lambda x: x + 1,
            "COBARDE": lambda x: x - 1,
        }

    def run(self, program):
        for stmt in program:
            self.exec(stmt)

    def exec(self, stmt):
        tag = stmt[0]
        if tag == "say":
            print(self.eval(stmt[1]))
        elif tag == "while":
            _, cond, body = stmt
            while self.eval(cond):
                self.run(body)
        elif tag == "if":
            _, cond, body = stmt
            if self.eval(cond):
                self.run(body)
        elif tag == "set":
            _, val = stmt
            self.var = int(val.value)
        elif tag == "op":
            _, operator = stmt
            self.eval(operator)
        else:
            raise RuntimeError(f"Unknown stmt: {stmt}")

    def eval(self, node):
        tag = node[0]
        if isinstance(tag, Token):
            operator = tag.value
            if operator in self.operators:
                self.var = self.operators[operator](self.var)
                return
        elif tag in ["num", "str", "bool"]:
            return node[1]
        elif tag == "var":
            return self.var
        raise RuntimeError(f"Unknown expr: {node}")


def run_source(src: str):
    tree = parser.parse(src)
    program = ASTBuilder().transform(tree)
    Interpreter().run(program)


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()
    run_source(code)
