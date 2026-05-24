try: # importing readline for the side effect on input()
    import readline
except ImportError:
    import pyreadline3

from argparse import ArgumentParser
from collections.abc import Iterator
from typing import IO

from zprolog.lexer import lex, Peekable
from zprolog.parser import parse_program, Query, Rule
from zprolog.program import Program, Query, Rule
from zprolog.solver import solve, Substitution
import zprolog.kql # imported to initialize the kql built in

def from_readline() -> Iterator[str]:
    while True:
        try:
            print("Ready")
            yield from input()
        except EOFError:
            return

def print_sol(sol: Substitution):
    print({k: v for k, v in sol.items() if "@" not in k})

def process_file(program: Program, f: IO[str] | Iterator[str]):
    for command in parse_program(Peekable(lex(f))):
        match command:
            case Query():
                print(command)
                for sol in solve(program, command):
                    print_sol(sol)
            case Rule():
                program.add_rule(command)

def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Load program from file")
    args = parser.parse_args()

    program = Program()

    if args.file:
        with open(args.file) as f:
            process_file(program, f)
    process_file(program, from_readline())

if __name__ == "__main__":
    main()
