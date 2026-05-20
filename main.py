from sys import stdin

from zprolog.lexer import lex, Peekable
from zprolog.parser import parse_program, Query, Rule
from zprolog.program import Program, Query, Rule
from zprolog.solver import solve

def main():
    program = Program()
    for command in parse_program(Peekable(lex(stdin))):
        match command:
            case Query():
                print("Answer:")
                for sol in solve(program, command):
                    print(sol)
            case Rule():
                program.add_rule(command)

if __name__ == "__main__":
    main()
