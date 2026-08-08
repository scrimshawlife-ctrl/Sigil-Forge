# Bind-runes method (channel `bind_runes`)

## What it is

Historical Germanic craft of **binding** multiple runes into one composed figure.
Sigil-Forge uses **Elder Futhark** latin transliteration and simplified stick
geometry for a verifiable offline channel.

## What it is not

- Not Enochian seals or authority certificates (see `distinction-enochian.md`).
- Not a claim of traditional magical efficacy.
- Rune **names are not written** into public SVG/PNG (privacy).

## Pipeline

1. Take Spare-reduced latin letters (consonants, unique first-seen).
2. Map latin digraphs/letters → Elder Futhark (`th`→ᚦ, `ng`→ᛜ, …).
3. Keep unique runes (first-seen), cap at 8.
4. Place each rune’s stick strokes at canvas center with small rotational fan.
5. Emit SVG group `id="bind-runes"` as multiple polylines.

## Channel status

| Status | When |
|--------|------|
| `applied` | ≥1 rune stroke polyline produced |
| `skipped` | No mappable letters / empty spare |

## API

```python
from bind_runes import latin_to_runes, build_bind_polylines
runes = latin_to_runes("maintain")
polys, used = build_bind_polylines("mntclfs")
```
