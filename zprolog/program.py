from typing import TypeGuard

type Variable = str
type Term = CompoundTerm | Variable

class CompoundTerm:
    def __init__(self, functor: str, arguments: list[Term] = []):
        self.functor = functor
        self.arguments = arguments
    
class Rule:
    """A rule is a Horn clause. It has a head and a body.
    The head is a predicate. The body is a list of predicates.
    """
    def __init__(self, head: Term, body: list[Term] = []):
        self.head = head
        self.body = body

class Program:
    def __init__(self, rules: list[Rule] = []):
        self.rules = rules

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

class Query:
    """A query is a logical formula we need to prove.
    Extends Prolog with "Query ::= ? Term ." for interactive queries.
    """
    def __init__(self, term: Term):
        self.term = term

def is_variable(t: Term) -> TypeGuard[str]:
    return isinstance(t, str)

def is_compund_term(t: Term) -> TypeGuard[CompoundTerm]:
    return isinstance(t, CompoundTerm)