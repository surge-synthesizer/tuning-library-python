from ._tuning_library import *
from ._tuning_library import _read_scl_file, _read_kbm_file

# Allow calling read_scl_file and read_kbm_file with Path arguments


def read_scl_file(fname):
    return _read_scl_file(str(fname))


def read_kbm_file(fname):
    return _read_kbm_file(str(fname))


def scala_files_to_frequencies(scl_filename, kbm_filename=None):
    """
    Find midi note frequencies from scala files.

    Convenience function taking filenames and producing a list of frequencies.

    Parameters
    ----------
    scl_filename : str or Path
        Filename for scl file.
    kbm_filename : str or Path, optional
        Filename for kbm file. If no `kbm_filename` is passed, a default keyboard
        mapping is used.

    Returns
    -------
    List of float
        Frequency for each of the 128 midi notes.
    """
    scale = read_scl_file(scl_filename)
    if kbm_filename is None:
        tuning = Tuning(scale)
    else:
        mapping = read_kbm_file(kbm_filename)
        tuning = Tuning(scale, mapping)
    return [tuning.frequency_for_midi_note(i) for i in range(128)]
