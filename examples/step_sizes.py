"""
Find all scales with a given number of step sizes.

Can be run as

    $ python3 step_sizes.py 3

to find all scales with three different step sizes for example.

Prints the scale name, number of notes in the scale, and the step sizes in
cents. Searches the current directory by default, else a directory can be
specified with --scale-dir.

Example output using the Scala scale archive:

    $ python3 step_sizes.py 3 | column -t | tail
    scl/turkish_41a.scl                     41          22.641        22.642    45.283
    scl/meanfifth_43.scl                    43          27.266        28.155    28.156
    scl/ennealimmal45trans.scl              45          13.399        34.905    35.767
    scl/donar46.scl                         46          22.301        26.549    31.504
    scl/compton48.scl                       48          16.597        16.776    50.029
    scl/yarman_17etx3.scl                   51          15.482        19.812    35.294
    scl/oettingen.scl                       53          19.553        21.506    29.614
    scl/oettingen2.scl                      53          19.553        21.506    29.614
    scl/chin_60.scl                         60          3.615         19.845    23.46
    scl/guiron77.scl                        77          7.547         22.641    22.642

"""

import argparse
from pathlib import Path

import tuning_library as tl


def find_scales_with_stepsize_count(count, scale_directory=None, rounding=3):
    directory = Path(scale_directory) if scale_directory is not None else Path.cwd()
    results = []
    for fn in directory.rglob("*.scl"):
        scale = tl.read_scl_file(fn)
        tuning = tl.Tuning(scale)
        xs = [1200 * tuning.log_scaled_frequency_for_midi_note(i) for i in range(128)]
        step_sizes = sorted(set(round(x - y, rounding) for x, y in zip(xs[1:], xs)))
        if len(step_sizes) == count:
            results.append((scale, step_sizes))
    return results


def get_parser():
    parser = argparse.ArgumentParser(
        description="Find scales with given number of step sizes"
    )
    parser.add_argument("steps", type=int, help="Number of steps to search for")
    parser.add_argument(
        "--scale-dir",
        "-s",
        help="Directory containing scl files to search",
    )
    return parser


def main():
    args = get_parser().parse_args()
    results = find_scales_with_stepsize_count(args.steps, args.scale_dir)
    for scale, step_sizes in sorted(results, key=lambda x: x[0].count):
        print(f"{scale.name}\t{scale.count}\t" + "\t".join(str(x) for x in step_sizes))


if __name__ == "__main__":
    main()
