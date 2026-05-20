from zprolog.lexer import *

def test_only_whitespace():
    assert not list(lex(" \t\n\r\n  "))

def test_identifiers():
    text = "  one Two Three Forty2 with_an_underscore "
    assert list(lex(text)) == text.split()

def test_single_character_tokens():
    text = "(()).,."
    assert list(lex(text)) == list(text)

def test_is_identifier():
    assert is_identifier("abcd")
    assert is_identifier("ab1cd2")
    assert is_identifier("a_bcd_")
    assert is_identifier("_abcd")

    assert not is_identifier(" abcd")
    assert not is_identifier("abcd ")
    assert not is_identifier("1abcd")
    assert not is_identifier("")