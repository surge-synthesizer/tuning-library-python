"""
Find scales similar to a given scale.

Prints matching scale names, mode numbers, and max cent differences separated by tabs.

Can be called as

    $ python3 similar.py target_scale.scl

to find any scl files similar to target_scale.scl in the same directory.

The cent tolerance for what is 'similar' can be set as follows:

    $ python3 similar.py target_scale.scl --tolerance 20

Scales in a different directory from the target scale can be searched, e.g.

    $ python3 similar.py target_scale.scl --scale-dir ~/scala_scale_archive

On Unix the output can be formatted nicely by running

    $ python3 similar.py target_scale.scl | column -t

Example output using duodene in the Scala scl archive:

    $ python3 similar.py scl/duodene.scl | column -t
    scl/duodene.scl             0  0.00
    scl/efg33355.scl            2  0.00
    scl/euler.scl               4  0.00
    scl/mersen_s1.scl           5  0.00
    scl/de_caus.scl             9  0.00
    scl/blueji-cataclysmic.scl  0  1.66
    scl/pyth_12s.scl            0  1.95
    scl/neidhardt-s1.scl        7  1.95
    scl/duodene_t.scl           0  3.91
    scl/miller_reflections.scl  4  5.14
    scl/marveldene.scl          0  5.45
    scl/dwarf12marv.scl         3  5.78
    scl/sullivan_eagle.scl      0  6.11
    scl/duodene_w.scl           0  6.65
    scl/smithgw72i.scl          0  6.89
    scl/ji_12.scl               0  7.71
    scl/sullivan_blueji.scl     0  7.71
    scl/dwarf12_7.scl           0  7.71
    scl/parizek_7lqmtd2.scl     0  7.71
    scl/augdommean.scl          4  7.71
    scl/parizek_7lmtd1.scl      0  7.71
    scl/parizek_17lqmt.scl      2  7.71
    scl/thirteendene.scl        3  7.71
    scl/parizek_qmeb1.scl       4  8.09
    scl/bedos.scl               2  8.60
    scl/meansev2.scl            2  9.22
    scl/parizek_qmtp12.scl      4  9.77
    scl/parizek_cirot.scl       4  9.78
    scl/wiese3.scl              1  9.78
    scl/parizek_qmeb2.scl       4  9.78
    scl/sullivan_blue.scl       0  9.83
    scl/parizek_qmeb3.scl       4  9.98

"""

import argparse
from pathlib import Path

import tuning_library as tl


def find_similar_scales(target_scale_filename, tolerance, scale_directory=None):
    """
    Find scales similar to a target scale.

    Parameters
    ----------
    target_scale_filename : str or Path
        Filename of scl file containing scale to match.
    tolerance: float
        Max cent diff between scale notes to consider two scales similar.
    scale_directory : str or Path, optional
        Directory to search for similar scl files. If not provided, the parent
        directory of `target_scale_filename` is searched.

    Returns
    -------
    list of (tuning_library.Scale, int, float)
        List of similar scale, the mode number which is similar to the target scale,
        and the corresponding max abs cent diff from the target scale.
    """
    target_scale = tl.read_scl_file(target_scale_filename)
    scale_directory = (
        Path(scale_directory)
        if scale_directory is not None
        else Path(target_scale_filename).parent
    )

    target_cents = [0.0] + [t.cents for t in target_scale.tones[:-1]]
    similar_scales = []
    for fn in scale_directory.glob("*.scl"):
        scale = tl.read_scl_file(fn)
        if scale.count != target_scale.count:
            continue
        cents = [0.0] + [t.cents for t in scale.tones[:-1]]
        period = scale.tones[-1].cents
        for n in range(len(cents)):
            mode_cents = sorted((x - cents[n]) % period for x in cents)
            max_diff = max(abs(mode_cents[i] - x) for i, x in enumerate(target_cents))
            if max_diff <= tolerance:
                similar_scales.append((scale, n, max_diff))
    return similar_scales


def get_parser():
    parser = argparse.ArgumentParser(description="Find similar scales")
    parser.add_argument(
        "target_scale_filename", help="scl file containing target scale"
    )
    parser.add_argument(
        "--tolerance",
        "-t",
        type=float,
        default=10.0,
        help="Tolerance for similarity in cents",
    )
    parser.add_argument(
        "--scale-dir", "-s", help="Directory containing scl files to search"
    )
    return parser


def main():
    args = get_parser().parse_args()
    similar_scales = find_similar_scales(
        args.target_scale_filename, args.tolerance, args.scale_dir
    )
    for scale, mode, cent_diff in sorted(similar_scales, key=lambda x: x[2]):
        print(f"{scale.name}\t{mode}\t{cent_diff:.2f}")


if __name__ == "__main__":
    main()
