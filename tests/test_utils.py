from zprolog.lexer import *
from zprolog.parser import *
from zprolog.program import *

def lexed(s: str) -> Peekable[str]:
    return Peekable(lex(s))

def p_term(s: str) -> Term:
    return parse_term(lexed(s))

def p_rule(s: str) -> Rule:
    return parse_rule(lexed(s))

def p_program(s: str) -> Program:
    return Program([rule for rule in parse_program(lexed(s)) if isinstance(rule, Rule)])