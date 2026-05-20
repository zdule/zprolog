from functools import reduce
from typing import Iterator
from zprolog.program import *

type Substitution = dict[Variable, Term]

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

def unify(s: Substitution, a: Term, b: Term) -> Substitution | None:
    # early out
    if s is None: return None

    # Unifying X with X.
    if a.is_variable() and b.is_variable() and a.identifier == b.identifier:
        return s

    # Apply substitutions, but without recursing into compunds.
    if a.is_variable() and a.identifier in s:
        a = s[a.identifier]
    if b.is_variable() and b.identifier in s:
        b = s[b.identifier]

    if a.is_variable():
        if occurs(a.identifier, b): # occurs check
            return None
        return update_substituion(s, a.identifier, b)
    if b.is_variable():
        return unify(s, b, a)

    assert not (a.is_variable() or b.is_variable())
    if a.functor != b.functor:
        return None
    if len(a.arguments) != len(b.arguments):
        return None
    return reduce(lambda s, ab: unify(s, *ab), zip(a.arguments, b.arguments), s)

def anonymize_variables(r: Rule, variable_generator: dict[str, int]) -> tuple[Rule, dict[str, int]]:
    variables = collect_variables(r.head) | set().union(*map(collect_variables, r.body))
    new_variables = {id: variable_generator.get(id, 0) + 1 for id in variables}
    s = {id: Variable(f"@{id}_{counter}") for (id, counter) in new_variables.items()}
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

# Return a term obtained by applying substitution s to term t.
def substitute(s: Substitution, t: Term) -> Term:
    if t.is_variable():
        if t.identifier in s:
            return s[t.identifier]
        else:
            return t
    else:
        return CompoundTerm(t.functor, [substitute(s, arg) for arg in t.arguments])

# Returns true if id occurs as a variable in t:
def occurs(id: str, t: Term) -> bool:
    if t.is_variable():
        return t.identifier == id
    return any((occurs(id, arg) for arg in t.arguments))

def collect_variables(t: Term) -> set[str]:
    if t.is_variable():
        return {t.identifier}
    return set().union(*map(collect_variables, t.arguments))