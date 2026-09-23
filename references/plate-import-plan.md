# Plate Import Shipped (v0.14.0 + deeper)


From expansion-spine: completed in v0.14.0 + deeper wizard integration.

## Status
Shipped in v0.14.0 with wizard post-apply execution. Functional importer with SVG/JSON parsing, normalization against planetary-plate-strokes.json reference.

Module: scripts/plate_import.py (load, parse, normalize, validate, import_and_save)

## Plan Outline
- Support importing external SVG or JSON for unique manuscript (MS) plates.
- Parse strokes, normalize to the existing plate format.
- Integrate with planetary geometry: --planetary-geometry plate-import or wizard extension.
- Validation against schema (use forge schemas).
- Preserve scholarly accuracy, no authority claims.
- Output: updated corpus or per-run plate data bound to sigil_root.
- Offline, stdlib + optional (e.g. svgpathtools if present).
