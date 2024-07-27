# Tuning Library Python bindings
Python bindings for the [Surge Synth Team Tuning Library](https://github.com/surge-synthesizer/tuning-library).

## Installation

To install from PyPI:
```console
$ pip install tuning_library
```
or to clone the repo and install from source:
```console
$ git clone --recurse-submodules https://github.com/surge-synthesizer/tuning-library-python.git
$ cd tuning-library-python
$ python3 -m pip install .
```

## Examples

Read scl file and find frequency of midi note 69
```python
import tuning_library as tl

scale = tl.read_scl_file("scale.scl")
tuning = tl.Tuning(scale)
f = tuning.frequency_for_midi_note(69)
```

Read scl and kbm files and find frequency of midi note 69
```python
import tuning_library as tl

scale = tl.read_scl_file("scale.scl")
mapping = tl.read_kbm_file("mapping.kbm")
tuning = tl.Tuning(scale, mapping)
f = tuning.frequency_for_midi_note(69)
```

## Wrapper names

The names in the C++ Tuning Library and this Python wrapper correspond as follows

|   C++                                             |   Python                                                  |
| ------------------------------------------------- | --------------------------------------------------------- |
|   readSCLFile                                     |   read_scl_file                                           |
|   parseSCLData                                    |   parse_scl_data                                          |
|   evenTemperament12NoteScale                      |   even_temperament_12_note_scale                          |
|   evenDivisionOfSpanByM                           |   even_division_of_span_by_m                              |
|   evenDivisionOfCentsByM                          |   even_division_of_cents_by_m                             |
|                                                   |                                                           |
|   readKBMFile                                     |   read_kbm_file                                           |
|   parseKBMData                                    |   parse_kbm_data                                          |
|   tuneA69To                                       |   tune_A69_to                                             |
|   tuneNoteTo                                      |   tune_note_to                                            |
|   startScaleOnAndTuneNoteTo                       |   start_scale_on_and_tune_note_to                         |
|                                                   |                                                           |
|   Scale::name                                     |   Scale.name                                              |
|   Scale::description                              |   Scale.description                                       |
|   Scale::rawText                                  |   Scale.raw_text                                          |
|   Scale::count                                    |   Scale.count                                             |
|   Scale::tones                                    |   Scale.tones                                             |
|                                                   |                                                           |
|   KeyboardMapping::count                          |   KeyboardMapping.count                                   |
|   KeyboardMapping::firstMidi                      |   KeyboardMapping.first_midi                              |
|   KeyboardMapping::lastMidi                       |   KeyboardMapping.last_midi                               |
|   KeyboardMapping::middleNote                     |   KeyboardMapping.middle_note                             |
|   KeyboardMapping::tuningConstantNote             |   KeyboardMapping.tuning_constant_note                    |
|   KeyboardMapping::tuningFrequency                |   KeyboardMapping.tuning_frequency                        |
|   KeyboardMapping::tuningPitch                    |   KeyboardMapping.tuning_pitch                            |
|   KeyboardMapping::octaveDegrees                  |   KeyboardMapping.octave_degrees                          |
|   KeyboardMapping::keys                           |   KeyboardMapping.keys                                    |
|   KeyboardMapping::rawText                        |   KeyboardMapping.raw_text                                |
|   KeyboardMapping::name                           |   KeyboardMapping.name                                    |
|                                                   |                                                           |
|   Tuning::N                                       |   Tuning.N                                                |
|   Tuning::withSkippedNotesInterpolated            |   Tuning.with_skipped_notes_interpolated                  |
|   Tuning::frequencyForMidiNote                    |   Tuning.frequency_for_midi_note                          |
|   Tuning::frequencyForMidiNoteScaledByMidi0       |   Tuning.frequency_for_midi_note_scaled_by_midi_0         |
|   Tuning::logScaledFrequencyForMidiNote           |   Tuning.log_scaled_frequency_for_midi_note               |
|   Tuning::retuningFromEqualInCentsForMidiNote     |   Tuning.retuning_from_equal_in_cents_for_midi_note       |
|   Tuning::retuningFromEqualInSemitonesForMidiNote |   Tuning.retuning_from_equal_in_semitones_for_midi_note   |
|   Tuning::scalePositionForMidiNote                |   Tuning.scale_position_for_midi_note                     |
|   Tuning::isMidiNoteMapped                        |   Tuning.is_midi_note_mapped                              |
|   Tuning::scale                                   |   Tuning.scale                                            |
|   Tuning::keyboardMapping                         |   Tuning.keyboard_mapping                                 |
|                                                   |                                                           |
|   Tone::type                                      |   Tone.type                                               |
|   Tone::cents                                     |   Tone.cents                                              |
|   Tone::ratio_d                                   |   Tone.ratio_d                                            |
|   Tone::ratio_n                                   |   Tone.ratio_n                                            |
|   Tone::stringRep                                 |   Tone.string_rep                                         |
|   Tone::floatValue                                |   Tone.float_value                                        |
|                                                   |                                                           |
|   toneFromString                                  |   tone_from_string                                        |

## Extra

The `tuning_library` Python package also includes a
`scala_files_to_frequencies` convenience function which is not in the C++
library.  It can be called as
```python
import tuning_library as tl

frequencies = tl.scala_files_to_frequencies("scale.scl", "mapping.kbm")
```
or, using a default keyboard mapping,
```python
frequencies = tl.scala_files_to_frequencies("scale.scl")
```
and returns a list of 128 frequencies in Hz, one for each each midi note.
