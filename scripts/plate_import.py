#!/usr/bin/env python3
"""
Plate Import (Planned / Skeleton)

Scanned unique MS plate import for scholarly vector plates.
Offline-first, no authority claims.

From references/plate-import-plan.md
Current scholarly vectorization lives in references/planetary-plate-strokes.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Optional SVG parsing (stdlib only for skeleton; recommend svgpathtools or svglib for prod)
try:
    import xml.etree.ElementTree as ET  # stdlib
    SVG_AVAILABLE = True
except Exception:
    SVG_AVAILABLE = False


def load_plate(source: str | Path) -> dict[str, Any]:
    """Load plate data from JSON or SVG source (stub)."""
    p = Path(source)
    if p.suffix.lower() == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    elif p.suffix.lower() == ".svg":
        return {"type": "svg_stub", "source": str(p), "strokes": parse_svg_strokes(p.read_text(encoding="utf-8"))}
    else:
        raise ValueError(f"Unsupported plate source: {p.suffix}")


def parse_svg_strokes(svg_text: str) -> list[dict[str, Any]]:
    """Parse <path> etc into stroke dicts (very basic skeleton using stdlib)."""
    if not SVG_AVAILABLE:
        return [{"error": "no svg parser", "raw": svg_text[:200]}]
    try:
        root = ET.fromstring(svg_text)
        strokes = []
        for elem in root.iter():
            if elem.tag.endswith("path") or elem.tag.endswith("polyline"):
                d = elem.attrib.get("d") or elem.attrib.get("points", "")
                strokes.append({"type": elem.tag.split("}")[-1], "data": d[:100]})
        return strokes or [{"type": "empty"}]
    except Exception as e:
        return [{"error": str(e)}]


def normalize_to_plate(strokes: list[dict]) -> list[dict]:
    """Normalize imported strokes to canonical plate stroke format (stub)."""
    # TODO: map to planetary-plate-strokes.json schema
    return [{"normalized": True, "original": s} for s in strokes]


def validate_plate(plate_data: dict) -> bool:
    """Basic validation (extend with forge schema)."""
    return "strokes" in plate_data or "type" in plate_data


def import_and_save(source: str | Path, out_path: str | Path | None = None) -> Path:
    """Import and write normalized plate JSON (skeleton)."""
    data = load_plate(source)
    strokes = data.get("strokes", parse_svg_strokes(str(data)) if isinstance(data, str) else [])
    normalized = normalize_to_plate(strokes)
    out = Path(out_path) if out_path else Path(source).with_suffix(".imported.json")
    out.write_text(json.dumps({"source": str(source), "normalized_strokes": normalized}, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    print("plate_import skeleton — use via import or sigil_forge wizard extension")
    print("Example: python -m scripts.plate_import  (not wired yet)")
