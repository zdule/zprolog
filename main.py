from dataclasses import dataclass
from sys import stdin
from zprolog.lexer import InputStream, lex

# A database is a collection of rules.
class Database:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

# A rule is a Horn clause. It has a head a body.
# The head is a predicate. The body is a list of predicates.
class Rule:
    def __init__(self, head, body):
        self.head = head
        self.body = body

# A name -- sequence of letters, digits, and underscores, starting with a letter or underscore.
@dataclass
class Identifier:
    name: str

# Left parenthesis.
@dataclass
class LParen:
    pass

# Right parenthesis.
@dataclass
class RParen:
    pass

# Period.
@dataclass
class Period:
    pass

def main():
    print("Hello from zprolog!")
    for x in lex(InputStream(stdin)):
        print(x)


if __name__ == "__main__":
    main()
