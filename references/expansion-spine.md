# Expansion spine

**Current release: v0.5.0** (this file tracks shipped vs remaining).

Sigil-Forge is a standalone Hermes skill with a lean install tree, additive
channels, and an explicit method ontology so “sigil” never collapses intent
compression, name paths, planetary characters, and entity seals.

## Shipped

| Version | Highlights |
|---------|------------|
| v0.1–0.2 | Construct/verify/check, Spare monogram, kamea, stego, offline PNG, polish prompt, open |
| v0.3 | `bind_runes`, `rose_cross_path`, run receipts, learning ledger |
| v0.4 | Kamea multi-encoding + provenance, ontology, Spare family, Hebrew Rose Cross, planetary traditional seals |
| v0.5 | Transliteration upgrade, kamea goldens, intelligence/spirit reconstructions, phonetic channel, doctor/eval, optional Argon2id, interop fields, source manifest |
| v0.6 | Wallpaper framework: immutable glyph + atmosphere composite, device profiles, wallpaper-spec/receipt, CLI `wallpaper` |

### Craft / methods
- Encodings: `hebrew_gematria` (default), `latin_extended`, `latin_mod9_v1` (compat)
- Rose Cross: 22 Hebrew petals + markers
- Planetary: traditional seal, intelligence (odds→evens), spirit (reverse)
- Bind-runes: **modern_derivation**
- Spare family modes + phonetic JSON carrier
- Ontology + `references/source-manifest.yaml`

### Ops
- CLI: construct, verify, open, learn, ledger, doctor, eval, check
- Receipts + PROPOSED ledger
- `validate_hermes_skill.py`

## Remaining / optional later
- Full manuscript-accurate intelligence/spirit *grimoire* character corpus (beyond kamea-derived reconstructions)
- Audio/MIDI for mantric carriers
- Multi-frame storyboard carriers
- Rich Orchestra/Kubrick/ComfyUI adapters beyond thin interop fields
- Deeper geometric multi-channel steganalysis

## Explicit non-goals
- Goetic / Enochian / authority seals in the **default** forge
- Deterministic freehand automatic drawing claimed as pure geometry
- Auto-promoting learning ledger to canon

## Compatibility rules
1. Do not break forge-packet required keys without `schema_version` bump.  
2. New channels append; unknown IDs report applied/skipped honestly.  
3. Offline path works without optional pip packages.  
4. Never mutate `references/` at run time.
