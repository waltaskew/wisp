"""The wisp REPL."""

import parsec  # type: ignore

import wisp.parser as parser
import wisp.prelude as prelude
import wisp.wtypes as wtypes


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
                expr = parser.parse_expr.parse(line)
            except parsec.ParseError as e:
                print(e)
            else:
                try:
                    result = expr.eval(env)
                    print(result)
                except wtypes.WispException as e:
                    print(e)
