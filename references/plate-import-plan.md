# Scanned Unique MS Plate Import Pipeline (Planned)

From expansion-spine: remaining optional later.

## Status
Not implemented in v0.13.0. Current uses scholarly vectorization in references/planetary-plate-strokes.json

## Plan Outline
- Support importing external SVG or JSON for unique manuscript (MS) plates.
- Parse strokes, normalize to the existing plate format.
- Integrate with planetary geometry: --planetary-geometry plate-import or similar.
- Validation against schema.
- Preserve scholarly accuracy, no authority claims.
- Output: updated corpus or per-run plate data bound to sigil_root.

## References
- references/planetary-plate-strokes.json
- references/methods-planetary-characters.md
- scripts/plate_strokes.py
- scripts/planetary_seals.py

To implement: start with import script in scripts/plate_import.py using svg parsing (stdlib or optional).

See also graphify/graft for corpus analysis.
