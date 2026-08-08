# Sigil ontology

Schema: `schemas/sigil-method.schema.json`  
Packet field: `ontology` (+ detailed `provenance`)

## Families

| Family | Examples | Default forge |
|--------|----------|---------------|
| `intent_compression` | Spare letter_monogram | yes |
| `name_path` | Kamea path, Rose Cross | yes |
| `planetary_character` | Agrippan planetary seal | opt-in `--planetary-seal` |
| `alphabetic_ligature` | Bind-runes (modern_derivation) | yes |
| `encoded_carrier` | Stego channels | yes |
| `entity_identifier` / Enochian / Goetic | Authority seals | **excluded** |

## Required method fields

`family`, `method_id`, `construction_type`, `determinism`, `claimed_historical_status`, `verification_method`

These prevent collapsing intent sigils, name paths, planetary characters, and entity seals.
