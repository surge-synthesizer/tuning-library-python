#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "Tunings.h"

namespace py = pybind11;

PYBIND11_MODULE(_tuning_library, m)
{
    m.doc() = "Wrapper for Surge Synth Team Tuning Library";

    m.attr("MIDI_0_FREQ") = Tunings::MIDI_0_FREQ;

    py::enum_<Tunings::Tone::Type>(m, "Type")
        .value("kToneCents", Tunings::Tone::Type::kToneCents)
        .value("kToneRatio", Tunings::Tone::Type::kToneRatio)
        .export_values()
    ;

    py::class_<Tunings::Tone>(m, "Tone")
        .def(py::init<>())
        .def_readonly("type", &Tunings::Tone::type)
        .def_readonly("cents", &Tunings::Tone::cents)
        .def_readonly("ratio_d", &Tunings::Tone::ratio_d)
        .def_readonly("ratio_n", &Tunings::Tone::ratio_n)
        .def_readonly("string_rep", &Tunings::Tone::stringRep)
        .def_readonly("float_value", &Tunings::Tone::floatValue)
        .def_readonly("lineno", &Tunings::Tone::lineno)
        .def("__repr__",
            [](const Tunings::Tone &t) {
                return "Tone(\"" + t.stringRep + "\")";
            }
        );
    ;

    m.def("tone_from_string", &Tunings::toneFromString, py::arg("t"), py::arg("lineno") = -1);

    py::class_<Tunings::Scale>(m, "Scale")
        .def(py::init<>())
        .def_readonly("name", &Tunings::Scale::name)
        .def_readonly("description", &Tunings::Scale::description)
        .def_readonly("raw_text", &Tunings::Scale::rawText)
        .def_readonly("count", &Tunings::Scale::count)
        .def_readonly("tones", &Tunings::Scale::tones)
        .def("__repr__", [](const Tunings::Scale &s){
            return "Scale(name=\"" + s.name + "\")";
        })
    ;

    py::class_<Tunings::KeyboardMapping>(m, "KeyboardMapping")
        .def(py::init<>())
        .def_readonly("count", &Tunings::KeyboardMapping::count)
        .def_readonly("first_midi", &Tunings::KeyboardMapping::firstMidi)
        .def_readonly("last_midi", &Tunings::KeyboardMapping::lastMidi)
        .def_readonly("middle_note", &Tunings::KeyboardMapping::middleNote)
        .def_readonly("tuning_constant_note", &Tunings::KeyboardMapping::tuningConstantNote)
        .def_readonly("tuning_frequency", &Tunings::KeyboardMapping::tuningFrequency)
        .def_readonly("tuning_pitch", &Tunings::KeyboardMapping::tuningPitch)
        .def_readonly("octave_degrees", &Tunings::KeyboardMapping::octaveDegrees)
        .def_readonly("keys", &Tunings::KeyboardMapping::keys)
        .def_readonly("raw_text", &Tunings::KeyboardMapping::rawText)
        .def_readonly("name", &Tunings::KeyboardMapping::name)
        .def("__repr__", [](const Tunings::KeyboardMapping &k){
            return "KeyboardMapping(name=\"" + k.name + "\")";
        })
    ;

    py::register_local_exception<Tunings::TuningError>(m, "TuningError", PyExc_RuntimeError);

    m.def(
        "_read_scl_file",
        &Tunings::readSCLFile,
        "readSCLFile returns a Scale from the SCL File in fname"
    );

    m.def(
        "parse_scl_data",
        &Tunings::parseSCLData,
        "parseSCLData returns a scale from the SCL file contents in memory"
    );

    m.def(
        "even_temperament_12_note_scale",
        &Tunings::evenTemperament12NoteScale,
        "evenTemperament12NoteScale provides a utility scale which is the \"standard tuning\" scale"
    );

    m.def(
        "even_division_of_span_by_m",
        &Tunings::evenDivisionOfSpanByM,
        "evenDivisionOfSpanByM provides a scale referred to as \"ED2-17\" or "
        "\"ED3-24\" by dividing the Span into M points. eventDivisionOfSpanByM(2,12) "
        "should be the evenTemperament12NoteScale"
    );

    m.def(
        "even_division_of_cents_by_m",
        &Tunings::evenDivisionOfCentsByM,
        "evenDivisionOfCentsByM provides a scale which divides Cents into M "
        "steps. It is less frequently used than evenDivisionOfSpanByM for obvious "
        "reasons. If you want the last cents label labeled differently than the cents "
        "argument, pass in the associated optional label",
        py::arg("cents"),
        py::arg("M"),
        py::arg("last_label") = ""
    );

    m.def(
        "_read_kbm_file",
        &Tunings::readKBMFile,
        "readKBMFile returns a KeyboardMapping from a KBM file name"
    );

    m.def(
        "parse_kbm_data",
        &Tunings::parseKBMData,
        "parseKBMData returns a KeyboardMapping from a KBM data in memory"
    );

    m.def(
        "tune_A69_to",
        &Tunings::tuneA69To,
        "tuneA69To creates a KeyboardMapping which keeps the midi note 69 (A4) set "
        "to a constant frequency, given"
    );

    m.def(
        "tune_note_to",
        &Tunings::tuneNoteTo,
        "tuneNoteTo creates a KeyboardMapping which keeps the midi note given is set "
        "to a constant frequency, given"
    );

    m.def(
        "start_scale_on_and_tune_note_to",
        &Tunings::startScaleOnAndTuneNoteTo,
        "startScaleOnAndTuneNoteTo generates a KBM where scaleStart is the note 0 "
        "of the scale, where midiNote is the tuned note, and where freq is the frequency"
    );

    py::class_<Tunings::Tuning>(m, "Tuning")
        .def(py::init<>())
        .def(py::init<const Tunings::Scale &>(), py::arg("scale"))
        .def(py::init<const Tunings::KeyboardMapping &>(), py::arg("keyboard_mapping"))
        .def(
            py::init<const Tunings::Scale &, const Tunings::KeyboardMapping &, bool>(),
            py::arg("scale"),
            py::arg("keyboard_mapping"),
            py::arg("allow_tuning_center_on_unmapped") = false
        )
        .def_property_readonly("N", [](const Tunings::Tuning t){return t.N;})
        .def("with_skipped_notes_interpolated", &Tunings::Tuning::withSkippedNotesInterpolated)
        .def("frequency_for_midi_note", &Tunings::Tuning::frequencyForMidiNote)
        .def("frequency_for_midi_note_scaled_by_midi_0", &Tunings::Tuning::frequencyForMidiNoteScaledByMidi0)
        .def("log_scaled_frequency_for_midi_note", &Tunings::Tuning::logScaledFrequencyForMidiNote)
        .def("retuning_from_equal_in_cents_for_midi_note", &Tunings::Tuning::retuningFromEqualInCentsForMidiNote)
        .def("retuning_from_equal_in_semitones_for_midi_note", &Tunings::Tuning::retuningFromEqualInSemitonesForMidiNote)
        .def("scale_position_for_midi_note", &Tunings::Tuning::scalePositionForMidiNote)
        .def("is_midi_note_mapped", &Tunings::Tuning::isMidiNoteMapped)
        .def_readonly("scale", &Tunings::Tuning::scale)
        .def_readonly("keyboard_mapping", &Tunings::Tuning::keyboardMapping)
        .def("__repr__",
            [](const Tunings::Tuning &t) {
                return "Tuning(scale.name=\""
                        + t.scale.name
                        + "\", keyboard_mapping.name=\""
                        + t.keyboardMapping.name
                        + "\")";
            }
        );
    ;
}
