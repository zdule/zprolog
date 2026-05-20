from zprolog.program import *
from zprolog.solver import *

def test_unify_atom_with_self():
    a = CompoundTerm('a')
    assert unify({}, a, a) == {}

def test_unify_atom_with_different_attom():
    a = CompoundTerm('a')
    b = CompoundTerm('b')
    assert unify({}, a, b) is None

def test_unify_variable_with_self():
    a = 'A'
    assert unify({}, a, a) == {}

def test_unify_variable_with_other_variable():
    a = 'A'
    b = 'B'
    assert unify({}, a, b) == {'A': b}