from collections.abc import Mapping
from functools import reduce
from typing import Iterator
from zprolog.program import *

type Substitution = Mapping[Variable, Term]

# The current solve does not know anything about variables.
# For every solution it finds it emits one empty Bindings.
def solve(program: Program, query: Query) -> Iterator[Substitution]:
    return solve_goal(program, [query.term], {}, {})

def solve_goal(program: Program, goal: list[Term], s: Substitution, variable_generator) -> Iterator[Substitution]:
    if not goal:
        yield s
    else:
        first_term = goal[0]
        for rule in program.rules:
            rule, upd_variable_generator = anonymize_variables(rule, variable_generator)
            upd_s = unify(s, first_term, rule.head)
            if upd_s is not None:
                yield from solve_goal(program, rule.body + goal[1:], upd_s, upd_variable_generator)

# Attemps to unify two terms a and b while respecting substitution s.
# If one of the terms has variables that need to unify with particular terms, these
# are added to the resulting substituion which is returned.
# s is the substitution that we lazily apply to a and b. We do not eagerly apply them
# before calling unify for performance reasons.
#
# None is returned if substitution fails.
def unify(s: Substitution, a: Term, b: Term) -> Substitution | None:
    # Unifying X with X.
    if is_variable(a) and is_variable(b) and a == b:
        return s

    # Apply substitutions, but without recursing into compunds.
    if is_variable(a) and a in s:
        a = s[a]
    if is_variable(b) and b in s:
        b = s[b]

    if is_variable(a):
        if occurs(a, b): # occurs check
            return None
        return update_substituion(s, a, b)
    if is_variable(b):
        return unify(s, b, a)

    assert is_compund_term(a) and is_compund_term(b)
    if a.functor != b.functor:
        return None
    if len(a.arguments) != len(b.arguments):
        return None
    return reduce(lambda s, ab: None if s is None else unify(s, *ab), zip(a.arguments, b.arguments), s)

def anonymize_variables(r: Rule, variable_generator: dict[str, int]) -> tuple[Rule, dict[str, int]]:
    variables = collect_variables(r.head) | {v for t in r.body for v in collect_variables(t)} 
    new_variables = {id: variable_generator.get(id, 0) + 1 for id in variables}
    s = {id: f"@{id}_{counter}" for (id, counter) in new_variables.items()}
    variable_generator = variable_generator | new_variables
    r = Rule(substitute(s, r.head), list(map(lambda t: substitute(s, t), r.body)))
    return (r, variable_generator)

# Return the result of updating the substitution s with id -> t.
# s is also applied on t.
def update_substituion(s: Substitution, id: str, t: Term) -> Substitution:
    assert id not in s
    t = substitute(s, t)
    upd_s = {k: substitute({id: t}, v) for (k,v) in s.items()}
    upd_s[id] = t
    return upd_s

def substitute(s: Substitution, t: Term) -> Term:
    """Apply substitution to a term."""
    if is_variable(t):
        if t in s:
            return s[t]
        else:
            return t
    else:
        assert is_compund_term(t)
        return CompoundTerm(t.functor, [substitute(s, arg) for arg in t.arguments])

# Returns true if id occurs as a variable in t:
def occurs(id: str, t: Term) -> bool:
    if is_variable(t):
        return t == id
    assert is_compund_term(t)
    return any((occurs(id, arg) for arg in t.arguments))

def collect_variables(t: Term) -> set[str]:
    if is_variable(t):
        return {t}
    assert is_compund_term(t)
    return set().union(*map(collect_variables, t.arguments))