from zprolog.lexer import lex

def test_only_whitespace():
    assert not list(lex(" \t\n\r\n  "))

def test_identifiers():
    text = "  one Two Three Forty2 with_an_underscore "
    assert list(lex(text)) == text.split()