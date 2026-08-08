# Planetary characters (seals, intelligences, spirits)

Opt-in via `--planetary-seal` / wizard `planetary_seal`. Distinct from
`kamea_path(intent)`.

## Corpus

Data: [`planetary-character-corpus.json`](planetary-character-corpus.json)

| Kind | Construction | Status label |
|------|----------------|--------------|
| `traditional_seal` | successive 1→n² on planetary kamea | historically_aligned_agrippan_character |
| `intelligence_character` | **name_on_kamea** of corpus intelligence name (Hebrew preferred) | corpus_name_path_agrippan |
| `spirit_character` | **name_on_kamea** of corpus spirit name | corpus_name_path_agrippan |

Fallback if name path fails: odds→evens (intelligence) or reverse successive
(spirit), labeled `engine_reconstruction_documented`.

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
  --out out/sigil-forge
```
