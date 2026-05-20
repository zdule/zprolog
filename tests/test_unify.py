from zprolog.program import *
from zprolog.solver import *

from tests.test_utils import *

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

def test_unify_variable_with_atom():
    a = 'A'
    b = CompoundTerm('b')
    assert unify({}, a, b) == {'A': b}
    assert unify({}, b, a) == {'A': b}

def test_unify_variable_with_compound_term():
    a = 'A'
    t = p_term('a(p, q)')
    assert unify({}, a, t) == {'A': t}
    assert unify({}, t, a) == {'A': t}

def test_unify_occurs_check():
    a = 'A'
    b = 'B'
    t = p_term('a(p, b(c, A))')
    assert unify({}, a, t) is None
    assert unify({}, b, t) == {'B': t}