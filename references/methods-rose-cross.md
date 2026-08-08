# Rose path method (channel `rose_cross_path`)

## What it is

A **22-slot rose** letter path inspired by published Rose Cross talisman
geometry (petal count matches the traditional Hebrew-letter rose). Latin
consonants map into slots via a stable reduction; the path connects successive
slots on a circle.

## What it is not

- Not a full Golden Dawn initiation curriculum or Hebrew lettering system.
- Not Enochian seals / Watchtower authority markers.
- Not a claim of supernatural efficacy.
- Slot indices stay private in the forge packet; public SVG has geometry only.

## Pipeline

1. Prefer Spare-style consonant set from the intent.
2. Map each letter → slot `(ord(ch)-a) % 22`.
3. Place slots on a circle (radius ~32 on the 0..100 canvas), start at top.
4. Polyline through points; soft-close when ≥3 points.
5. Emit SVG group `id="rose-cross-path"`.

## Channel status

| Status | When |
|--------|------|
| `applied` | Path has ≥2 points |
| `skipped` | No letter material for a path |

## API

```python
from rose_cross import build_rose_path, letter_to_slot
pts, slots = build_rose_path("mntclfs")
```
