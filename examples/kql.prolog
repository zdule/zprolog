parent(Parent, Child) :- kql("Parent | project parent_name, trim('\\s+', child_name)", Parent, Child).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

? ancestor("petar", "nina").
? ancestor("petar", "mika").
? ancestor("zika", "mara").
? ancestor("petar", X).
? ancestor(X, "nina").
