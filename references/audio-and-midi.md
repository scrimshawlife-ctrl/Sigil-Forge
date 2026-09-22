# Audio/MIDI for Mantric Carriers (Planned)

From expansion-spine: remaining optional later.

## Status
Not implemented in v0.13.0. Current focuses on visual/stego carriers (SVG, PNG LSB, wallpaper).

## Plan Outline
- Phonetic channel already exists (see phonetic.py, --phonetic).
- Extend to audio: generate simple tones or MIDI from phonetic sequence or intent digest.
- Use stdlib or optional (no new deps for core).
- Output: .mid or .wav in run dir, bound to sigil_root.
- Integrate with wizard full path optional step.
- Safety: same refusals.
- Example: mantric alphabet to MIDI notes.

## References
- phonetic.py
- references/profiles-creative.md
- Spine: "Audio/MIDI for mantric carriers"

To implement: start with stub in scripts/audio.py using simple sine or mido if available (optional).

See also modular-synth or audio skills in broader context.
