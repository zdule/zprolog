from zprolog.program import *
from zprolog.solver import *

def test_unify_atom_with_self():
    a = CompoundTerm('a')
    assert unify({}, a, a) == {}

def test_unify_atom_with_different_attom():
    a = CompoundTerm('a')
    assert unify({}, a, a) == {}

def test_unify_variable_with_self():
    a = Variable('A')
    assert unify({}, a, a) == {}

def test_unify_variable_with_self():
    a = Variable('A')
    assert unify({}, a, a) == {}