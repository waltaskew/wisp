"""The wisp REPL."""

import parsec  # type: ignore

import wisp.exceptions as exceptions
import wisp.parser as parser
import wisp.prelude as prelude


def main():
    """Implement the read-eval-print loop."""
    env = prelude.env()
    while True:
        try:
            line = input('wisp => ')
        except EOFError:
            print('bye!')
            exit(0)
        else:
            try:
                expr = parser.parse_expr.parse_strict(line)
            except parsec.ParseError as e:
                print(e)
            else:
                try:
                    result = expr.eval(env)
                    print(result)
                except exceptions.WispException as e:
                    print(e)
