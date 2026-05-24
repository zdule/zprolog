from zprolog.program import *
from zprolog.solver import *

from tests.test_utils import *

def test_atom_in_database():
    a = CompoundTerm('a')
    assert list(solve(Program([Rule(a)]), Query([a]))) == [{}]

def test_atom_not_in_database():
    a = CompoundTerm('a')
    b = CompoundTerm('b')
    assert list(solve(Program([Rule(a)]), Query([b]))) == []

def test_transitivity():
    p = p_program("p(x, y). p(y, z). q(X, Y) :- p(X, Y). q(X, Z) :- p(X, Y), q(Y, Z).")
    q = Query([p_term("q(x, z)")])
    assert len(list(solve(p, q))) == 1
