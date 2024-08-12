# Examples

The examples directory contains some scripts using `tuning_library`. Each
script contains a docstring at the top showing how to run it and some example
output. Below is a summary of what each script does.

## show.py

Draws step, interval, and mode diagrams for the scale in a given scl file.
Useful for getting a quick overview of a scale.

## similar.py

Search a directory of scl files for scales similar to a given scale. Useful to
find if a scale is similar to a particular mode of a scale in the Scala scale
archive.

## step_sizes.py

Finds all scales in a directory with only a given number of step sizes.
Interesting to see how many scales have a small number of step sizes.

## find_tone.py

Search a directory for all scales containing a given tone. Useful for finding
scales containing some unusual interval.

## equal_division.py

Write out an scl file for an equal division of the octave (or other span).
Mainly an example of using the `raw_text` attribute.

## map.py

Map a scale from an scl file to be played on a Launchpad (a grid midi
controller). This one uses MTS-ESP through the `mtsespy` wrapper. Shows
generating a `KeyboardMapping` and building a `Tuning`.
