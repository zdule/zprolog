from typing import TypeGuard

type Variable = str
type Term = CompoundTerm | Variable

class CompoundTerm:
    def __init__(self, functor: str, arguments: list[Term] = []):
        self.functor = functor
        self.arguments = arguments
    
    def is_variable(self):
        return False

# A rule is a Horn clause. It has a head a body.
# The head is a predicate. The body is a list of predicates.
class Rule:
    def __init__(self, head: Term, body: list[Term] = []):
        self.head = head
        self.body = body

class Program:
    def __init__(self, rules: list[Rule] = []):
        self.rules = rules

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

# A query is logical formula we need to prove.
# I extended Prolog with "Query ::= ? Term ." such that I can interactively run queries
# on rules known so far.
class Query:
    def __init__(self, term: Term):
        self.term = term

def is_variable(t: Term) -> TypeGuard[str]:
    return isinstance(t, str)

def is_compund_term(t: Term) -> TypeGuard[CompoundTerm]:
    return isinstance(t, CompoundTerm)