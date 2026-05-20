from argparse import ArgumentParser
from sys import stdin
from typing import IO

from zprolog.lexer import lex, Peekable
from zprolog.parser import parse_program, Query, Rule
from zprolog.program import Program, Query, Rule
from zprolog.solver import solve

def process_file(program: Program, f: IO[str]):
    for command in parse_program(Peekable(lex(f))):
        match command:
            case Query():
                print(f"?- {command.term}")
                for sol in solve(program, command):
                    print(sol)
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
    process_file(program, stdin)

if __name__ == "__main__":
    main()
