# Expansion spine

**Current release: v0.7.0** (this file tracks shipped vs remaining).

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
| v0.7 | Host AI background provider (file + shell command), enriched prompt packages, `construct --wallpaper` one-shot |

### Craft / methods
- Encodings: `hebrew_gematria` (default), `latin_extended`, `latin_mod9_v1` (compat)
- Rose Cross: 22 Hebrew petals + markers
- Planetary: traditional seal, intelligence (odds→evens), spirit (reverse)
- Bind-runes: **modern_derivation**
- Spare family modes + phonetic JSON carrier
- Ontology + `references/source-manifest.yaml`

### Wallpapers (v0.6–0.7)
- Surfaces: `phone_lock`, `phone_home`, `tablet`, `desktop`, `desktop_ultrawide`
- Modes: stealth / ambient / focus / ritual / immersive
- Canonical glyph immutable; background = procedural (offline), operator PNG, or host AI
- Host AI: `--background` (host_file), `--provider-command` / `SIGIL_FORGE_BG_COMMAND` (host_command)
- Enriched `background-prompt-*.json` (canvas, seed, output_hint, contract)
- Spec + receipt under `wallpaper/` and `receipts/`; optional LSB digest binding
- One-shot: `construct --wallpaper` (presentation via `--wp-mode`)

### Ops
- CLI: construct, verify, wallpaper, open, learn, ledger, doctor, eval, check
- Receipts + PROPOSED ledger
- `validate_hermes_skill.py`

## Remaining / optional later
- Full manuscript-accurate intelligence/spirit *grimoire* character corpus (beyond kamea-derived reconstructions)
- Audio/MIDI for mantric carriers
- Multi-frame storyboard carriers
- Rich Orchestra/Kubrick/ComfyUI adapters beyond thin interop fields
- Deeper geometric multi-channel steganalysis
- Optional bundled ComfyUI workflow templates (skill still does not call cloud image APIs)

## Explicit non-goals
- Goetic / Enochian / authority seals in the **default** forge
- Deterministic freehand automatic drawing claimed as pure geometry
- Auto-promoting learning ledger to canon

## Compatibility rules
1. Do not break forge-packet required keys without `schema_version` bump.  
2. New channels append; unknown IDs report applied/skipped honestly.  
3. Offline path works without optional pip packages.  
4. Never mutate `references/` at run time.
