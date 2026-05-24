from typing import Iterator

from zprolog.lexer import Peekable, is_identifier, is_variable, is_string_literal, Token
from zprolog.program import CompoundTerm, Query, Rule, Term, Variable, StringLiteral

type Tokens = Peekable[Token]

def raise_unexpected_token(expected: str | list[str], token: Token):
    if isinstance(expected, list):
        expected = ", ".join([f"'{e}'" for e in expected[:-1]]) + f" or {expected[-1]}"
    else:
        expected = f"'{expected}'"
    raise Exception(f"Expected {expected}, found '{token}'")

def parse_program(tokens: Tokens) -> Iterator[Query | Rule]:
    """Main entry point into the parser. Parses rules and queries from lexed tokens."""
    while token := tokens.peek():
        if token == "?":
            check_token(tokens, "?")
            query = parse_term(tokens)
            check_token(tokens, ".")
            yield Query(query)
        else:
            yield parse_rule(tokens)

def parse_rule(tokens: Tokens):
    head = parse_term(tokens)
    body = []
    match next(tokens):
        case ".":
            pass
        case ":-":
            body = parse_non_empty_token_list(tokens)
            check_token(tokens, ".")
    return Rule(head, body)

def parse_term(tokens: Tokens) -> Term:
    if literal := tokens.peek():
        if is_string_literal(literal):
            return StringLiteral(next(tokens))

    identifier = parse_identifier(tokens)
    if is_variable(identifier):
        return identifier
    arguments = []
    if tokens.peek() == "(":
        arguments = parse_argument_list(tokens)
    return CompoundTerm(identifier, arguments)

def parse_identifier(tokens: Tokens) -> Token:
    token = next(tokens)
    if not is_identifier(token):
        raise_unexpected_token("an identifier", token)
    return token

def parse_argument_list(tokens: Tokens) -> list[Term]:
    check_token(tokens, "(")
    if tokens.peek() == ")":
        arguments = []
    else:
        arguments = parse_non_empty_token_list(tokens)
    check_token(tokens, ")", [",", ")"])
    return arguments

def parse_non_empty_token_list(tokens: Tokens) -> list[Term]:
    token_list = []
    while True:
        token_list.append(parse_term(tokens))
        if tokens.peek() == ",":
            _ = next(tokens)
        else:
            return token_list 

def check_token(tokens: Tokens, expected: Token, allowed = None):
    """Consume the next token and check that it is exactly the expected token."""
    if allowed is None:
        allowed = expected

    token = next(tokens)
    if token != expected:
        raise_unexpected_token(expected, token)
