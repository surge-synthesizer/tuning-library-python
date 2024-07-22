"""
Tests for tuning_library
"""

import math
from pathlib import Path

import pytest

import tuning_library as tl

DATA_DIR = Path(__file__).parent / "data"

CENT_ROUNDING = 6
DEFAULT_SCALE_NAME = "Scale from patch"


def assert_close(x, y):
    epsilon = 1e-12
    assert abs(x - y) < epsilon


def test_midi_0_freq():
    assert_close(tl.MIDI_0_FREQ, 440 * 2 ** (-69 / 12))


def test_type_enum():
    assert tl.Type.kToneCents == 0
    assert tl.Type.kToneRatio == 1


def test_tone_init():
    tone = tl.Tone()
    assert tone.type == tl.Type.kToneRatio
    assert tone.cents == 0.0
    assert tone.ratio_d == 1
    assert tone.ratio_n == 1
    assert tone.string_rep == "1/1"
    assert tone.float_value == 1.0


def test_tone_from_string_ratio():
    tone = tl.tone_from_string("8/7")
    assert tone.type == tl.Type.kToneRatio
    assert_close(tone.cents, 1200 * math.log2(8 / 7))
    assert tone.ratio_n == 8
    assert tone.ratio_d == 7
    assert tone.string_rep == "8/7"
    assert_close(tone.float_value, math.log2(8 / 7) + 1)
    assert tone.lineno == -1


def test_tone_from_string_cents():
    tone = tl.tone_from_string("150.0")
    assert tone.type == tl.Type.kToneCents
    assert tone.cents == 150.0
    assert tone.ratio_n == 1
    assert tone.ratio_d == 1
    assert tone.string_rep == "150.0"
    assert tone.float_value == 150 / 1200 + 1
    assert tone.lineno == -1


def test_tone_from_string_lineno():
    tone = tl.tone_from_string("8/7", lineno=23)
    assert tone.lineno == 23


def test_tone_repr():
    t = tl.tone_from_string("8/7")
    assert str(t) == 'Tone("8/7")'


def check_scale(scale, text):
    assert scale.description == "bar"
    assert scale.raw_text == text
    assert scale.count == 12
    assert len(scale.tones) == 12

    tone = scale.tones[0]
    assert isinstance(tone, tl.Tone)
    assert tone.ratio_n == 25
    assert tone.ratio_d == 24


@pytest.mark.parametrize("fname_func", [lambda x: x, str])
def test_read_scl_file(fname_func):
    test_file = DATA_DIR / "test.scl"
    text = test_file.read_text()
    scale = tl.read_scl_file(fname_func(test_file))
    check_scale(scale, text)
    assert Path(scale.name).name == "test.scl"


def test_tuning_error():
    with pytest.raises(tl.TuningError):
        tl.read_scl_file("")


def test_parse_scl_data():
    test_file = DATA_DIR / "test.scl"
    text = test_file.read_text()
    scale = tl.parse_scl_data(text)
    check_scale(scale, text)
    assert scale.name == DEFAULT_SCALE_NAME


def test_scale_init():
    scale = tl.Scale()
    assert scale.name == "empty scale"
    assert scale.description == ""
    assert scale.raw_text == ""
    assert scale.count == 0
    assert scale.tones == []


def test_scale_repr():
    scale = tl.Scale()
    assert str(scale) == 'Scale(name="empty scale")'


def test_even_temperament_12_note_scale():
    scale = tl.even_temperament_12_note_scale()
    assert scale.name == DEFAULT_SCALE_NAME
    assert (
        scale.description
        == "12 Tone Equal Temperament | ED2-12 - Equal division of harmonic 2 into 12 parts"
    )
    assert (
        scale.raw_text
        == """! 12 Tone Equal Temperament.scl
!
12 Tone Equal Temperament | ED2-12 - Equal division of harmonic 2 into 12 parts
 12
!
 100.00000
 200.00000
 300.00000
 400.00000
 500.00000
 600.00000
 700.00000
 800.00000
 900.00000
 1000.00000
 1100.00000
 2/1
"""
    )
    assert scale.count == 12
    for i, t in enumerate(scale.tones, 1):
        assert t.cents == 100 * i


def test_even_division_of_span_by_m():
    scale = tl.even_division_of_span_by_m(2, 19)
    assert scale.name == DEFAULT_SCALE_NAME
    assert scale.description == "Automatically generated ED2-19 scale"
    assert (
        scale.raw_text
        == """! Automatically generated ED2-19 scale
Automatically generated ED2-19 scale
19
!
63.157895
126.315789
189.473684
252.631579
315.789474
378.947368
442.105263
505.263158
568.421053
631.578947
694.736842
757.894737
821.052632
884.210526
947.368421
1010.526316
1073.684211
1136.842105
2/1
"""
    )
    assert len(scale.tones) == 19
    for i, t in enumerate(scale.tones, 1):
        assert t.cents == round(i * 1200 / 19, CENT_ROUNDING)


def test_even_division_of_cents_by_m_1():
    scale = tl.even_division_of_cents_by_m(1902, 13)
    assert scale.name == DEFAULT_SCALE_NAME
    assert (
        scale.description
        == "Automatically generated Even Division of 1902 ct into 13 scale"
    )
    assert (
        scale.raw_text
        == """! Automatically generated Even Division of 1902 ct into 13 scale
Automatically generated Even Division of 1902 ct into 13 scale
13
!
146.307692
292.615385
438.923077
585.230769
731.538462
877.846154
1024.153846
1170.461538
1316.769231
1463.076923
1609.384615
1755.692308
1902.000000
"""
    )
    assert scale.count == 13
    for i, t in enumerate(scale.tones, 1):
        assert t.cents == round(i * 1902 / 13, CENT_ROUNDING)


def test_even_division_of_cents_by_m_2():
    scale = tl.even_division_of_cents_by_m(1902, 13, last_label="3")
    assert scale.name == DEFAULT_SCALE_NAME
    assert (
        scale.description
        == "Automatically generated Even Division of 1902 ct into 13 scale"
    )
    assert (
        scale.raw_text
        == """! Automatically generated Even Division of 1902 ct into 13 scale
Automatically generated Even Division of 1902 ct into 13 scale
13
!
146.307692
292.615385
438.923077
585.230769
731.538462
877.846154
1024.153846
1170.461538
1316.769231
1463.076923
1609.384615
1755.692308
3
"""
    )
    assert scale.count == 13
    for i, t in enumerate(scale.tones[:-1], 1):
        assert t.cents == round(i * 1902 / 13, CENT_ROUNDING)
    assert_close(scale.tones[-1].cents, 1200 * math.log2(3))


def check_mapping(mapping, text):
    assert mapping.count == 12
    assert mapping.first_midi == 0
    assert mapping.last_midi == 127
    assert mapping.middle_note == 60
    assert mapping.tuning_constant_note == 69
    assert mapping.tuning_frequency == 440.0
    assert mapping.tuning_pitch == 440.0 / tl.MIDI_0_FREQ
    assert mapping.octave_degrees == 12
    assert mapping.keys == list(range(12))
    assert mapping.raw_text == text


@pytest.mark.parametrize("fname_func", [lambda x: x, str])
def test_read_kbm_file(fname_func):
    test_file = DATA_DIR / "test.kbm"
    text = test_file.read_text()
    mapping = tl.read_kbm_file(fname_func(test_file))
    check_mapping(mapping, text)
    assert Path(mapping.name).name == "test.kbm"


def test_parse_kbm_data():
    test_file = DATA_DIR / "test.kbm"
    text = test_file.read_text()
    mapping = tl.parse_kbm_data(text)
    check_mapping(mapping, text)
    assert mapping.name == "Mapping from patch"


def test_keyboard_mapping_init():
    mapping = tl.KeyboardMapping()
    assert mapping.count == 0
    assert mapping.first_midi == 0
    assert mapping.last_midi == 127
    assert mapping.middle_note == 60
    assert mapping.tuning_constant_note == 60
    assert_close(mapping.tuning_frequency, 440 * 2 ** (-9 / 12))
    assert mapping.tuning_pitch == 32
    assert mapping.octave_degrees == 0
    assert mapping.keys == []
    assert (
        mapping.raw_text
        == """! Default KBM file
0
0
127
60
60
261.626
0
"""
    )
    assert mapping.name == ""


def test_keyboard_mapping_repr():
    mapping = tl.KeyboardMapping()
    assert str(mapping) == 'KeyboardMapping(name="")'


def test_tune_A69_to():
    mapping = tl.tune_A69_to(441.0)
    assert mapping.tuning_constant_note == 69
    assert mapping.tuning_frequency == 441.0


def test_tune_note_to():
    mapping = tl.tune_note_to(68, 441.0)
    assert mapping.tuning_constant_note == 68
    assert mapping.tuning_frequency == 441.0


def test_start_scale_on_and_tune_note_to():
    mapping = tl.start_scale_on_and_tune_note_to(10, 68, 441.0)
    assert mapping.middle_note == 10
    assert mapping.tuning_constant_note == 68
    assert mapping.tuning_frequency == 441.0


def test_tuning_init_1():
    tuning = tl.Tuning()
    assert tuning.N == 512
    assert tuning.scale.name == DEFAULT_SCALE_NAME
    assert tuning.keyboard_mapping.name == ""


def test_tuning_init_2():
    scale = tl.even_temperament_12_note_scale()
    tuning = tl.Tuning(scale)
    assert tuning.scale.name == DEFAULT_SCALE_NAME
    assert tuning.keyboard_mapping.name == ""


def test_tuning_init_3():
    mapping = tl.KeyboardMapping()
    tuning = tl.Tuning(mapping)
    assert tuning.scale.name == DEFAULT_SCALE_NAME
    assert tuning.keyboard_mapping.name == ""


def test_tuning_init_4():
    scale = tl.even_temperament_12_note_scale()
    mapping = tl.KeyboardMapping()
    tuning = tl.Tuning(scale, mapping)
    assert tuning.scale.name == DEFAULT_SCALE_NAME
    assert tuning.keyboard_mapping.name == ""


def test_with_skipped_notes_interpolated():
    mapping = tl.read_kbm_file(DATA_DIR / "unmapped.kbm")
    tuning = tl.Tuning(mapping)
    unmapped_note = 3
    interpolated_frequency = tl.MIDI_0_FREQ * 2 ** (unmapped_note / 12)
    assert tuning.frequency_for_midi_note(unmapped_note) != interpolated_frequency
    interpolated_tuning = tuning.with_skipped_notes_interpolated()
    assert_close(
        interpolated_tuning.frequency_for_midi_note(unmapped_note),
        interpolated_frequency,
    )


def test_frequency_for_midi_note():
    tuning = tl.Tuning()
    assert_close(tuning.frequency_for_midi_note(69), 440)


def test_frequency_for_midi_note_scaled_by_midi_0():
    tuning = tl.Tuning()
    assert_close(
        tuning.frequency_for_midi_note_scaled_by_midi_0(69), 440.0 / tl.MIDI_0_FREQ
    )


def test_log_scaled_frequency_for_midi_note():
    tuning = tl.Tuning()
    assert_close(
        tuning.log_scaled_frequency_for_midi_note(69), math.log2(440.0 / tl.MIDI_0_FREQ)
    )


def test_retuning_from_equal_in_cents_for_midi_note():
    tuning = tl.Tuning(tl.read_scl_file(DATA_DIR / "test.scl"))
    assert_close(
        tuning.retuning_from_equal_in_cents_for_midi_note(1),
        1200 * math.log2(25 / 24) - 100,
    )


def test_retuning_from_equal_in_semitones_for_midi_note():
    tuning = tl.Tuning(tl.read_scl_file(DATA_DIR / "test.scl"))
    assert_close(
        tuning.retuning_from_equal_in_semitones_for_midi_note(1),
        12 * math.log2(25 / 24) - 1,
    )


def test_scale_position_for_midi_note():
    tuning = tl.Tuning(tl.read_scl_file(DATA_DIR / "test.scl"))
    assert tuning.scale_position_for_midi_note(12) == 0


def test_is_midi_note_mapped():
    mapping = tl.read_kbm_file(DATA_DIR / "unmapped.kbm")
    tuning = tl.Tuning(mapping)
    assert tuning.is_midi_note_mapped(0)
    assert not tuning.is_midi_note_mapped(3)


def test_tuning_scale_and_keyboard_mapping():
    scale = tl.read_scl_file(DATA_DIR / "test.scl")
    mapping = tl.read_kbm_file(DATA_DIR / "test.kbm")
    tuning = tl.Tuning(scale, mapping)
    assert Path(tuning.scale.name).name == "test.scl"
    assert Path(tuning.keyboard_mapping.name).name == "test.kbm"


def test_tuning_repr():
    tuning = tl.Tuning()
    assert (
        str(tuning) == 'Tuning(scale.name="Scale from patch", keyboard_mapping.name="")'
    )


def test_allow_tuning_center_on_unmapped_1():
    scale = tl.read_scl_file(DATA_DIR / "test.scl")
    mapping = tl.read_kbm_file(DATA_DIR / "test.kbm")
    tuning = tl.Tuning(scale, mapping, allow_tuning_center_on_unmapped=False)


def test_allow_tuning_center_on_unmapped_2():
    scale = tl.read_scl_file(DATA_DIR / "test.scl")
    mapping = tl.read_kbm_file(DATA_DIR / "test.kbm")
    tuning = tl.Tuning(scale, mapping, allow_tuning_center_on_unmapped=True)


def test_allow_tuning_center_on_unmapped_3():
    scale = tl.read_scl_file(DATA_DIR / "test.scl")
    mapping = tl.read_kbm_file(DATA_DIR / "unmapped_center.kbm")
    with pytest.raises(tl.TuningError):
        tuning = tl.Tuning(scale, mapping, allow_tuning_center_on_unmapped=False)


def test_allow_tuning_center_on_unmapped_4():
    scale = tl.read_scl_file(DATA_DIR / "test.scl")
    mapping = tl.read_kbm_file(DATA_DIR / "unmapped_center.kbm")
    tuning = tl.Tuning(scale, mapping, allow_tuning_center_on_unmapped=True)


def test_scala_files_to_frequencies_1():
    freqs = tl.scala_files_to_frequencies(DATA_DIR / "test.scl")
    assert_close(freqs[1] / freqs[0], 25 / 24)


def test_scala_files_to_frequencies_2():
    freqs = tl.scala_files_to_frequencies(DATA_DIR / "test.scl", DATA_DIR / "test.kbm")
    assert_close(freqs[1] / freqs[0], 25 / 24)
