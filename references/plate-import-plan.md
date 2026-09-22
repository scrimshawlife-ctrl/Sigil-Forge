# Scanned Unique MS Plate Import Pipeline (Planned)

From expansion-spine: remaining optional later.

## Status
Not implemented in v0.13.0 / v0.14. Current uses scholarly vectorization in references/planetary-plate-strokes.json

Basic skeleton added: scripts/plate_import.py (import/parse stubs only; no runtime call yet).

## Plan Outline
- Support importing external SVG or JSON for unique manuscript (MS) plates.
- Parse strokes, normalize to the existing plate format.
- Integrate with planetary geometry: --planetary-geometry plate-import or wizard extension.
- Validation against schema (use forge schemas).
- Preserve scholarly accuracy, no authority claims.
- Output: updated corpus or per-run plate data bound to sigil_root.
- Offline, stdlib + optional (e.g. svgpathtools if present).

## Skeleton Functions (in scripts/plate_import.py)
- load_plate(source: str | Path) -> dict
- parse_svg_strokes(svg_text: str) -> list[dict]
- normalize_to_plate(strokes: list) -> list[dict]
- validate_plate(plate_data: dict) -> bool
- import_and_save(source, out_path) -> Path

## References
- references/planetary-plate-strokes.json
- references/methods-planetary-characters.md
- scripts/plate_strokes.py
- scripts/planetary_seals.py
- scripts/forge_core.py (for schema)

To implement: extend with real parsing; hook into wizard or construct via interop.

See also graphify/graft for corpus analysis.

