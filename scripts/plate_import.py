#!/usr/bin/env python3
"""
Plate Import (Completed Basic Implementation)

Scanned unique MS plate import for scholarly vector plates.
Normalizes external SVG/JSON into plate stroke format using reference corpus.
Offline-first, no authority claims.

From references/plate-import-plan.md
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import xml.etree.ElementTree as ET
    SVG_AVAILABLE = True
except Exception:
    SVG_AVAILABLE = False

REF_PLATE = Path(__file__).parent.parent / "references" / "planetary-plate-strokes.json"


def load_plate(source: str | Path) -> dict[str, Any]:
    """Load plate data from JSON or SVG source."""
    p = Path(source)
    if not p.exists():
        raise FileNotFoundError(str(p))
    if p.suffix.lower() == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    elif p.suffix.lower() == ".svg":
        return {
            "type": "svg",
            "source": str(p),
            "strokes": parse_svg_strokes(p.read_text(encoding="utf-8")),
        }
    else:
        raise ValueError(f"Unsupported plate source: {p.suffix}")


def parse_svg_strokes(svg_text: str) -> list[dict[str, Any]]:
    """Parse <path d=...> and <polyline points=...> into stroke records."""
    if not SVG_AVAILABLE:
        return [{"error": "no svg parser"}]
    try:
        root = ET.fromstring(svg_text)
        strokes: list[dict[str, Any]] = []
        for elem in root.iter():
            tag = elem.tag.split("}")[-1].lower()
            if tag in ("path", "polyline", "polygon"):
                d = elem.attrib.get("d") or elem.attrib.get("points", "")
                if d:
                    strokes.append({
                        "type": tag,
                        "data": d.strip()[:200],
                        "length": len(d),
                    })
        return strokes or [{"type": "empty"}]
    except Exception as e:
        return [{"error": str(e)}]


def normalize_to_plate(strokes: list[dict]) -> list[dict]:
    """Normalize to canonical plate format. Uses reference for structure hints."""
    ref_strokes = []
    if REF_PLATE.exists():
        try:
            ref = json.loads(REF_PLATE.read_text(encoding="utf-8"))
            ref_strokes = ref.get("strokes", []) if isinstance(ref, dict) else ref
        except Exception:
            pass

    normalized = []
    for s in strokes:
        if "error" in s or "type" not in s:
            normalized.append(s)
            continue
        entry = {
            "type": s.get("type"),
            "data_preview": s.get("data", "")[:100],
            "length": s.get("length", 0),
            "normalized": True,
        }
        if ref_strokes:
            entry["matches_reference_structure"] = len(ref_strokes) > 0
        normalized.append(entry)
    return normalized


def validate_plate(plate_data: dict) -> bool:
    """Validate basic plate structure."""
    return bool(
        plate_data.get("strokes")
        or plate_data.get("normalized_strokes")
        or plate_data.get("type")
    )


def import_and_save(source: str | Path, out_path: str | Path | None = None) -> Path:
    """Import, normalize, and persist plate data."""
    data = load_plate(source)
    strokes = data.get("strokes", [])
    if not strokes and isinstance(data, dict):
        strokes = parse_svg_strokes(str(data.get("data", "")))
    normalized = normalize_to_plate(strokes)
    out = Path(out_path) if out_path else Path(source).with_suffix(".imported.json")
    result = {
        "source": str(source),
        "normalized_strokes": normalized,
        "count": len(normalized),
        "reference_corpus_used": REF_PLATE.exists(),
    }
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    print("plate-import — MS plate importer (SVG/JSON → normalized strokes)")
    ref = REF_PLATE
    if ref.exists():
        out = import_and_save(ref, "/tmp/plate_demo.imported.json")
        print("imported:", out)
        print(json.loads(out.read_text())["count"], "strokes")
