from os import environ
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from collections.abc import Iterator

from zprolog.solver import Substitution, substitute, builtins, update_substituion
from zprolog.program import StringLiteral, Term, is_compund_term, is_string_literal, is_variable

kusto_client = None
db = None

def init_kql():
    global kusto_client, db
    cluster = environ["KUSTO_CLUSTER"]
    db = environ["KUSTO_DB"]
    if kusto_client:
        return
    kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster)
    kusto_client = KustoClient(kcsb)

def built_in_kql(s: Substitution, a: Term) -> Iterator[Substitution]:
    assert is_compund_term(a)
    assert a.functor == 'kql'

    # The first argument is required. It is the query string.
    if len(a.arguments) < 1:
        raise Exception("kql usage: kql(query_string, <qeury_results...>)")        

    # We must know the query string to execute the query.
    # It can be either a StringLiteral or a variable that is already bound to a string.
    query_string = substitute(s, a.arguments[0])
    if not is_string_literal(query_string):
        raise Exception("kql usage: At the call the first argument must be resolved to a string literal")
    query_string = query_string.literal

    init_kql()
    columns = get_column_names(query_string + "| getschema ")
    if len(columns) != len(a.arguments[1:]):
        raise Exception("kql usage: number of columns returned by the kusto query must be equal to the \
            number of arguments provided to kql after the query string.")
        
    resolved_args = [substitute(s, arg) for arg in a.arguments[1:]]
    variables = set()
    for arg in resolved_args:
        if not (is_string_literal(arg) or is_variable(arg)):
            raise Exception(f"kql usage: parameters may be only string literals or unbound variables. Found {arg}")
        if is_variable(arg):
            if arg in variables:
                raise Exception(f"kql usage: a variable must not appear twice as an argument: {arg}")
            variables.add(arg)

    query_with_filters = [query_string]
    for arg, column_name in zip(resolved_args, columns):
        if is_string_literal(arg):
            query_with_filters.append(f"| where {column_name} == '{arg.literal}'") # no string escaping for now.
    query_with_filters.append("| distinct *")
    query_with_filters = "\n".join(query_with_filters)

    global kusto_client
    assert kusto_client is not None
    for row in kusto_client.execute(db, query_with_filters).primary_results[0]:
        upd_s = s
        for arg, cell in zip(resolved_args, row):
            if is_variable(arg):
                assert arg not in upd_s
                upd_s = update_substituion(upd_s, arg, StringLiteral(f'"{cell}"'))
        yield upd_s
    return

def get_column_names(query: str) -> list[str]:
    '''Get column names of the results of the query'''
    global kusto_client
    assert kusto_client is not None
    return [row[0] for row in kusto_client.execute(db, query).primary_results[0]]
    

builtins['kql'] = built_in_kql