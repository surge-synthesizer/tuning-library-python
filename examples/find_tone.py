"""
Find all scales containing a given tone.

Can be run as

    $ python3 find_tone.py 15/13

to find all scales containing 15/13. Searches the current directory by default,
else a directory can be specified with --scale-dir.

Example output using the Scala scale archive:

    $ python3 find_tone.py 15/13 | column -t
    scl/neutr_pent2.scl            5
    scl/tritriad26.scl             7
    scl/chrom15.scl                7
    scl/diat_chrom.scl             7
    scl/augtetc.scl                8
    scl/octony_u.scl               8
    scl/diat15.scl                 8
    scl/harmd-lyd.scl              9
    scl/misce.scl                  9
    scl/thirteenten.scl            9
    scl/burt4.scl                  12
    scl/harmsub16.scl              12
    scl/harmjc-15.scl              12
    scl/schulter_24a.scl           24
    scl/garcia.scl                 29
    scl/erlich_bpf.scl             39
    scl/novaro15.scl               49
    scl/danielou_53.scl            53
    scl/tagawa_55.scl              55
    scl/pipedum_58a.scl            58
    scl/diamond15.scl              59
    scl/diamond17b.scl             65
    scl/ji_87.scl                  87
    scl/vaisvil_halfdiamond91.scl  91
    scl/ji_121.scl                 121
    scl/snyder.scl                 168
    scl/ji_311.scl                 311
    scl/sc311_41.scl               311
    scl/gann_wolfe.scl             579

"""

import argparse
from pathlib import Path

import tuning_library as tl


def find_tone(tone, scale_directory=None, rounding=6):
    directory = Path(scale_directory) if scale_directory is not None else Path.cwd()
    target_cents = round(tl.tone_from_string(tone).cents, rounding)
    scales = []
    for fn in directory.rglob("*.scl"):
        scale = tl.read_scl_file(fn)
        if target_cents in [round(t.cents, rounding) for t in scale.tones]:
            scales.append(scale)
    return scales


def get_parser():
    parser = argparse.ArgumentParser(description="Find scales containing given tone")
    parser.add_argument("tone", help="Tone to search for, e.g. 8/7 or 350.0")
    parser.add_argument(
        "--scale-dir",
        "-s",
        help="Directory containing scl files to search",
    )
    return parser


def main():
    args = get_parser().parse_args()
    scales = find_tone(args.tone, args.scale_dir)
    for scale in sorted(scales, key=lambda x: x.count):
        print(f"{scale.name}\t{scale.count}")


if __name__ == "__main__":
    main()
