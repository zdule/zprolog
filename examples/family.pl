ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

parent(petar, zika).
parent(petar, mara).
parent(zika, nina).
parent(zika, mika).

? ancestor(petar, nina).
? ancestor(petar, mika).
? ancestor(zika, mara).
