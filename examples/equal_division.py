"""
Write out an scl file for equal division of a given span.

Running

    $ python3 equal_division.py 17

writes out an scl file ED2-17.scl containing a scale with 17 equal divisions of
the octave.

The span to be divided can be specified as, for example,

    $ python3 equal_division.py 13 --span 3

which writes out an scl file ED3-13.scl.

"""

import argparse
from pathlib import Path

import tuning_library as tl


def write_equal_division_scl(division, span):
    filename = f"ED{span}-{division}.scl"
    Path(filename).write_text(tl.even_division_of_span_by_m(span, division).raw_text)


def get_parser():
    parser = argparse.ArgumentParser(description="Write equal division scl file")
    parser.add_argument("division", type=int, help="Number of equal divisions to use")
    parser.add_argument(
        "--span",
        "-s",
        type=int,
        default=2,
        help="Span to equally divide (defaults to the octave)",
    )
    return parser


def main():
    args = get_parser().parse_args()
    write_equal_division_scl(args.division, args.span)


if __name__ == "__main__":
    main()
