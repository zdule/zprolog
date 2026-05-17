from io import StringIO
from typing import IO, Callable

# Utility class for consuming an file.
# Importantly has peek and put_back.
class InputStream:
    def __init__(self, io: IO[str]):
        self.io = io
        self.peeked = None

    def read(self) -> str:
        if self.peeked != None:
            c = self.peeked
            self.peeked = None
            return c
        return self.io.read(1)

    def put_back(self, c: str):
        assert(self.peeked is None)
        self.peeked = c

    def peek(self) -> str:
        c = self.read()
        self.put_back(c)
        return c

    def read_while(self, predicate: Callable[[str], bool]) -> str:
        result = []
        while c := self.read():
            if predicate(c):
                result.append(c)
            else:
                self.put_back(c)
                break
        return ''.join(result)

def lex_input_stream(input: InputStream):
    while c := input.peek():
        print(c)
        if c.isspace():
            _ = input.read_while(lambda c: c.isspace())
        elif c.isalpha() or c == '_':
            yield input.read_while(lambda c: c.isalnum() or c == '_')
        else:
            raise Exception(f"Unknown character '{c}'")

# Produces an iterator of lexical elements from the input.
def lex(input: IO[str] | InputStream | str):
    stream = None
    match input:
        case InputStream():
            stream = input
        case str():
            stream = InputStream(StringIO(input))
        case _:
            stream = input
    return lex_input_stream(stream)