"""
Map a scale to be played on a Launchpad (a grid midi controller).

Uses MTS-ESP through the mtsespy wrapper.

Can be run as

    $ python3 map.py scale.scl

The number of scale steps moved when going one column across and one row up can
be set with the options -x and -y, for example

    $ python3 map.py scale.scl -x 1 -y 3

The full set of command line options is shown by running

    $ python3 map.py --help

The script prints the notes mapped to each Launchpad key - example output:

    $ python3 map.py scale.scl

     15/13   4/3     3/2     5/3     26/15   1/1     10/9    15/13   4/3
     1/1     10/9    15/13   4/3     3/2     5/3     26/15   1/1     10/9
     5/3     26/15   1/1     10/9    15/13   4/3     3/2     5/3     26/15
     4/3     3/2     5/3     26/15   1/1     10/9    15/13   4/3     3/2
     10/9    15/13   4/3     3/2     5/3     26/15   1/1     10/9    15/13
     26/15   1/1     10/9    15/13   4/3     3/2     5/3     26/15   1/1
     3/2     5/3     26/15   1/1     10/9    15/13   4/3     3/2     5/3
     15/13   4/3     3/2     5/3     26/15   1/1     10/9    15/13   4/3
     1/1     10/9    15/13   4/3     3/2     5/3     26/15   1/1     10/9


"""

import argparse
import signal

import tuning_library as tl
import mtsespy as mts


def map_scale(scale, x, y, t, base_freq):
    mapping = tl.start_scale_on_and_tune_note_to(0, 0, base_freq)
    tuning = tl.Tuning(scale, mapping)

    frequencies = []
    degrees = {}
    for n in range(128):
        # With t=0, bottom left key (midi note 11) should map to degree 0
        j, i = divmod(n, 10)
        d = (i - 1) * x + (j - 1) * y + t
        frequencies.append(tuning.frequency_for_midi_note(d))
        degrees[i, j] = d % scale.count

    labels = [" 1/1"] + [t.string_rep for t in scale.tones]
    print()
    for j in range(9, 0, -1):
        print("\t".join(labels[degrees[i, j]] for i in range(1, 10)))
    print()

    with mts.Master():
        mts.set_note_tunings(frequencies)
        signal.pause()


def get_parser():
    parser = argparse.ArgumentParser(description="Map a scale to a Launchpad")
    parser.add_argument("scl_filename", help="")
    parser.add_argument(
        "-x", type=int, default=1, help="Scale steps going one column across"
    )
    parser.add_argument("-y", type=int, default=2, help="Scale steps going one row up")
    parser.add_argument("-t", type=int, default=0, help="Scale steps to transpose by")
    parser.add_argument(
        "-f",
        "--freq",
        type=float,
        default=440 * 2 ** (-(12 + 9) / 12),
        help="Frequency for bottom left key on the Launchpad",
    )
    return parser


def main():
    args = get_parser().parse_args()
    scale = tl.read_scl_file(args.scl_filename)
    map_scale(scale, args.x, args.y, args.t, args.freq)


if __name__ == "__main__":
    main()
