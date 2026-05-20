from collections.abc import Iterator
import itertools
from io import TextIOBase
from typing import Callable

type Char = str
type Token = str
type Chars = Peekable[Char]

class Peekable[T]:
    """Utility class for consuming an iterator.
    Importantly has peek and put_back.
    """
    def __init__(self, iter: Iterator[T]):
        self.iter = iter
        self.peeked = None

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self.peeked != None:
            c = self.peeked
            self.peeked = None
            return c
        return next(self.iter)

    def put_back(self, c: T):
        assert(self.peeked is None)
        self.peeked = c

    def peek(self) -> T | None:
        try:
            c = next(self)
            self.put_back(c)
            return c
        except StopIteration:
            return None

def is_identifier(token: Token) -> bool:
    """Returns true if token is a valid identifier."""
    return token.isidentifier()

def is_variable(token: Token) -> bool:
    """Returns true if token is a variable.
    Variables are identifiers that start with an uppercase character.
    """
    return is_identifier(token) and token[0].isupper()

def read_while(peekable: Chars, predicate: Callable[[Char], bool]) -> Token:
    result = []
    for c in peekable:
        if predicate(c):
            result.append(c)
        else:
            peekable.put_back(c)
            break
    return ''.join(result)

def read_implication_symbol(input: Chars) -> Token:
    assert next(input) == ":"
    if c := next(input) != "-":
        raise Exception(f"Expected '-' after ':' but found {c}")
    return ":-"

def lex_chars(input: Chars) -> Iterator[Token]:
    while c := input.peek():
        if c in '(),.?': # single character tokens
            yield next(input)
        elif c == ":": 
            yield read_implication_symbol(input)
        elif c.isalpha() or c == '_': # identifiers
            yield read_while(input, lambda c: c.isalnum() or c == '_')
        elif c.isspace(): # skip whitespace
            _ = read_while(input, lambda c: c.isspace())
        else:
            raise Exception(f"Unknown character '{c}'")

def lex(input: str | TextIOBase | Iterator[str]) -> Iterator[Token]:
    """Produces an iterator of lexical elements from the input."""
    stream = None
    match input:
        case str():
            stream = Peekable(iter(input))
        case TextIOBase():
            stream = Peekable(itertools.chain.from_iterable(input))
        case _:
            stream = Peekable(input)
    return lex_chars(stream)