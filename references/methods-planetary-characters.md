# Planetary characters (seals, intelligences, spirits)

Opt-in via `--planetary-seal` / wizard `planetary_seal`. Distinct from
`kamea_path(intent)`.

## Geometry preference (`--planetary-geometry`)

| Mode | Behavior |
|------|----------|
| `auto` (default) | **plate** → name_on_kamea → reconstruction |
| `plate` | Multi-stroke plate digitizations only |
| `name_on_kamea` | Corpus name path on planetary square |
| `reconstruction` | Successive / odds-evens / reverse |

## Plate strokes (v0.9)

Data: [`planetary-plate-strokes.json`](planetary-plate-strokes.json)

| Kind | Plate construction | Status |
|------|-------------------|--------|
| `traditional_seal` | successive 1→n² + kamea frame + start/end ticks | `stroke_digitization_plate_v1` |
| `intelligence_character` | multi-stroke unit_box digitization per planet | `stroke_digitization_plate_v1` |
| `spirit_character` | multi-stroke unit_box digitization per planet | `stroke_digitization_plate_v1` |

Plate geometry is a **scholarly vectorization** of the Western ceremonial plate
vocabulary (Agrippa / Barrett Magus lineage) — not a unique manuscript scan and
not Goetic/Enochian authority seals.

## Name corpus

Data: [`planetary-character-corpus.json`](planetary-character-corpus.json)

| Kind | Construction | Status label |
|------|----------------|--------------|
| `intelligence_character` | **name_on_kamea** of corpus intelligence name | corpus_name_path_agrippan |
| `spirit_character` | **name_on_kamea** of corpus spirit name | corpus_name_path_agrippan |

Fallback: odds→evens (intelligence) or reverse successive (spirit), labeled
`engine_reconstruction_documented`.

## Names (summary)

| Planet | Intelligence | # | Spirit | # |
|--------|--------------|---|--------|---|
| Saturn | Agiel | 45 | Zazel | 45 |
| Jupiter | Iophiel | 136 | Hismael | 136 |
| Mars | Graphiel | 325 | Bartzabel | 325 |
| Sol | Nakhiel | 111 | Sorath | 666 |
| Venus | Hagiel | 49 | Kedemel | 175 |
| Mercury | Tiriel | 260 | Taphthartharath | 2080 |
| Luna | Malkah (short form) | 3321 | Schad Barschemoth (short form) | 3321 |

Numbers and names are **provenance metadata** for craft honesty. Not Goetic or
Enochian authority seals (those remain excluded from the default forge).

## CLI

```bash
python3 scripts/sigil_forge.py wizard --list-corpus
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --square jupiter \
  --planetary-seal \
  --planetary-seal-kind intelligence_character \
  --planetary-geometry plate \
  --out out/sigil-forge
```
