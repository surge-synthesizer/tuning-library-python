"""
Show step, interval, and mode diagrams for a scale.

Can be run as

    $ python3 show.py scale.scl

By default prints diagrams showing
- the steps in the scale
- the grid of intervals between each note in the scale
- the modes of the scale

By default both ratios and cents are shown. There are command line flags to
choose a specific diagram or only ratios or cents; all flags are shown in the
help message shown by running

    $ python3 show.py -h

Example output:

    $ python3 show.py --steps scale.scl

    1               15/13           4/3             3/2             26/15           2
    0               248             498             702             952             1200
            15/13           52/45           9/8             52/45           15/13
            248             250             204             250             248

"""

import argparse
import math
from fractions import Fraction

import tuning_library as tl


def freq_mult(tone):
    if tone.type == tl.Type.kToneRatio:
        return Fraction(tone.ratio_n, tone.ratio_d)
    return 2 ** (tone.cents / 1200)


def get_freq_mults(scale):
    return [Fraction(1)] + [freq_mult(t) for t in scale.tones]


def ratio_str(x):
    return str(x) if isinstance(x, Fraction) else "."


def cents_str(x):
    return str(int(round(1200 * math.log2(x))))


FORMATTERS = (ratio_str, cents_str)

SEP = "\t"


def print_steps(freq_mults, formatters=FORMATTERS):
    print()
    steps = [x / y for x, y in zip(freq_mults[1:], freq_mults)]
    for f in formatters:
        print((2 * SEP).join(map(f, freq_mults)))
    for f in formatters:
        print(SEP + (2 * SEP).join(f(x) for x in steps))
    print()


def print_interval_table(freq_mults, formatters=FORMATTERS):
    print()
    for x in freq_mults:
        intervals = [y / x for y in freq_mults]
        for f in formatters:
            print(SEP.join(map(f, intervals)))
        print()


def rotate(freq_mults, n):
    period = freq_mults[-1]
    new_freq_mults = freq_mults[n:-1] + [period * x for x in freq_mults[:n]]
    return [x / new_freq_mults[0] for x in new_freq_mults] + [period]


def print_modes(freq_mults, formatters=FORMATTERS):
    print()
    for i in range(len(freq_mults) - 1):
        mode = rotate(freq_mults, i)
        for f in formatters:
            print(SEP.join(map(f, mode)))
        print()


def get_parser():
    parser = argparse.ArgumentParser(
        description="Show step, interval, and mode diagrams for a scale"
    )
    parser.add_argument(
        "scl_filename", help="Filename of scl file to show diagrams for"
    )
    parser.add_argument(
        "-s", "--steps", action="store_true", help="Show only the steps diagram"
    )
    parser.add_argument(
        "-i", "--intervals", action="store_true", help="Show only the intervals diagram"
    )
    parser.add_argument(
        "-m", "--modes", action="store_true", help="Show only the modes diagram"
    )
    parser.add_argument(
        "-c", "--cents-only", action="store_true", help="Only print cents"
    )
    parser.add_argument(
        "-r", "--ratios-only", action="store_true", help="Only print ratios"
    )
    return parser


def main():
    args = get_parser().parse_args()
    scale = tl.read_scl_file(args.scl_filename)
    freq_mults = get_freq_mults(scale)

    if args.ratios_only:
        formatters = (ratio_str,)
    elif args.cents_only:
        formatters = (cents_str,)
    else:
        formatters = (ratio_str, cents_str)

    if args.steps:
        printers = (print_steps,)
    elif args.intervals:
        printers = (print_interval_table,)
    elif args.modes:
        printers = (print_modes,)
    else:
        printers = (print_steps, print_interval_table, print_modes)

    for p in printers:
        p(freq_mults, formatters)


if __name__ == "__main__":
    main()
