---
name: sigil-forge
description: >
  Use when forging sigils, intent glyphs, kamea/Spare stego, or forge packets.
  Offline multi-channel construction; dual creative/practice framing; no efficacy claims.
version: 0.6.0
author: Applied Alchemy Labs / scrimshawlife-ctrl
license: MIT
platforms: [linux, macos, windows]
dependencies: []
metadata:
  hermes:
    tags:
      - Creative
      - Sigil
      - Intent
      - Steganography
      - SymbolicDesign
    category: creative
    related_skills: []
triggers:
  - sigil
  - sigil forge
  - intent glyph
  - kamea
  - spare monogram
  - steganography
  - forge packet
  - chaos magic sigil
---

# Sigil-Forge

Standalone Hermes skill. Hermes loads this directory; `SKILL.md` is the behavior
contract. Deterministic construction lives under `scripts/`; the agent owns
intake, mode framing, safety judgment, and optional host image polish.

## Overview

Sigil-Forge turns a statement of intent into:

1. A **procedural master glyph** (SVG + offline PNG) fusing Spare monogram geometry
   with a classical kamea path.
2. A **local forge packet** with channel status, methods, crypto policy, and verify command.
3. **Steganographic carriers** (digest/channel bits — not plaintext intent by default).

Default framing is a **creative / focus tool**. Optional **`practice`** mode changes
tone only. Methods are craft + encoding — never proof of metaphysics.

**Authority:** proposal-only. Never claim the sigil “works,” causes external events,
or replaces professional help.

## When to Use

- User wants a **sigil**, **intent glyph**, **forge packet**, or multi-encoded symbol
- User mentions **Spare**, **kamea** / magic squares, or **steganography** of intent
- User wants offline, verifiable construction (no image API required)
- User chooses creative journaling/habit cue **or** personal practice framing

### When not to use

- General image gen, cinema, or Kubrick-style production (use kubrick)
- **Enochian seals** / authority placement (see `references/distinction-enochian.md`)
- Full ritual liturgy, banishing systems, or results-magic engines
- Harmful intents — refuse before any encode
- Requests to invent geometry or claim stego success without `verify`

## Prerequisites

- Python 3.10+ with stdlib (no required pip packages for core path)
- Optional: `jsonschema` for stricter packet validation; external SVG raster if desired
- Honor `HERMES_SKILL_DIR` when set; write under `--out` or `out/sigil-forge/<run-id>/`
- **Never mutate `references/` during ordinary runs**

## Procedure

Each step ends with a checkable completion criterion.

1. **Intake** — Capture present-tense intent, mode (`creative`|`practice`), optional
   passphrase / `SIGIL_FORGE_PASSPHRASE`, optional kamea square, style for polish.
   **Done when:** intent string non-empty after strip; mode valid.
2. **Safety / align** — Refuse violence, self-harm, non-consensual control, exploitation
   (`scripts/safety.py` + agent judgment). Empty noise → rewrite request.
   **Done when:** `check_intent` ok **or** clear refusal with no artifacts.
3. **Construct via engine** — Do not hand-draw paths:

   ```bash
   python3 scripts/sigil_forge.py construct \
     --intent "I maintain calm focus" \
     --mode creative \
     --kamea-encoding hebrew_gematria \
     --out out/sigil-forge
   ```

   Optional: `--kamea-encoding latin_mod9_v1|latin_extended|hebrew_gematria`,
   `--spare-mode letter_monogram|pictorial|…`, `--planetary-seal`,
   `--seal-packet`, `--polish`, `--square venus`.
   **Done when:** run dir contains `glyph.svg`, `forge-packet.json` with
   `ontology` + kamea `encoding_system` provenance, and every channel
   `applied` or `skipped(reason)`.
4. **Dual-mode notes** — Apply profile tone only to narrative / `framing_notes`.
   Construction is identical across modes.
   **Done when:** framing matches mode; no efficacy language.
5. **Deliver** — Paths + channel summary. Public media must not contain plaintext intent.
   **Done when:** operator has packet path and SVG path; privacy holds.
6. **Optional polish** — Geometry-locked host image tools only after master exists.
   Prefer construct `--polish` or `prompt_polish.build_prompt`. Master remains verify source.
   **Done when:** if polish used, `polish_prompt.json` exists and `gen_seed` is `applied`.
7. **Verify** — Before claiming integrity:

   ```bash
   python3 scripts/sigil_forge.py verify path/to/glyph.svg
   python3 scripts/sigil_forge.py verify path/to/glyph.png  # when png_lsb applied
   ```

   **Done when:** `ok: true` and digest matches packet (or honest failure detail).
8. **Open sealed intent** (if sealed):

   ```bash
   export SIGIL_FORGE_PASSPHRASE='…'
   python3 scripts/sigil_forge.py open path/to/forge-packet.json
   ```

   **Done when:** plaintext recovered or auth failure reported.

## Modes

| Mode | Default | Emphasis |
|------|---------|----------|
| `creative` | Yes | Focus externalization, journaling/habit cue, art |
| `practice` | Opt-in | Same engine; optional personal use notes; still no efficacy claims |

## Channels (fixed set)

Every successful forge **attempts** all IDs below. Capacity failures skip — never
claim full embed.

| ID | Role |
|----|------|
| `spare_monogram` | Spare letter reduction → monogram silhouette |
| `kamea_path` | Magic-square path |
| `kamea_square_choice` | Operator override or digest-derived square |
| `bind_runes` | Elder Futhark stick bind (**modern_derivation**) |
| `rose_cross_path` | Hebrew 22-petal Rose Cross name path |
| `planetary_seal` | Agrippan traditional seal (opt-in; ≠ kamea path) |
| `intent_digest` | SHA-256 of normalized intent |
| `optional_ciphertext` | AES-GCM seal when passphrase provided (local packet) |
| `svg_metadata` | SVG metadata digest / method bits |
| `path_epsilon` | Coordinate parity bits from digest |
| `path_order` | Construction-order binding (monogram before kamea) |
| `metric_quantize` | `data-sf-metric` digest nibble attributes |
| `png_lsb` | Offline layout raster + LSB (digest-only payload) |
| `gen_seed` | Digest-derived seed when `--polish` / write_polish |

Details: `references/channels-and-steganography.md`.

## CLI

```bash
python3 scripts/sigil_forge.py help
python3 scripts/sigil_forge.py doctor
python3 scripts/sigil_forge.py eval
python3 scripts/sigil_forge.py check
python3 scripts/sigil_forge.py construct --intent "…" --out out/sigil-forge
python3 scripts/sigil_forge.py construct --intent "…" --phonetic --interop --out out/sf
python3 scripts/sigil_forge.py construct --intent "…" --polish --out out/sigil-forge
python3 scripts/sigil_forge.py verify out/sigil-forge/<run-id>/glyph.svg
python3 scripts/sigil_forge.py wallpaper --run out/sigil-forge/<run-id> \
  --surface phone_lock --mode focus --theme mercurial
python3 scripts/sigil_forge.py open out/sigil-forge/<run-id>/forge-packet.json
python3 scripts/sigil_forge.py learn --class channel_preference \
  --summary "bind_runes + rose_cross_path coherent" --channels bind_runes,rose_cross_path
python3 scripts/sigil_forge.py ledger --limit 20
python3 scripts/validate_hermes_skill.py   # frontmatter / Hermes hygiene
```

Env: `HERMES_SKILL_DIR`, `SIGIL_FORGE_PASSPHRASE`. Prefer env over `--passphrase`
(argv is visible in process lists). Construct uses atomic staging then promote.

## One-Shot Recipes

### Offline creative forge + verify

```bash
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus while shipping" \
  --out out/sigil-forge
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.svg
```

**Done when:** verify `ok: true`; SVG and PNG present; `png_lsb` applied.

### Practice seal without argv passphrase

```bash
export SIGIL_FORGE_PASSPHRASE='operator-secret'
python3 scripts/sigil_forge.py construct \
  --intent "I speak clearly and keep my word" \
  --mode practice --seal-packet --out out/sigil-forge
python3 scripts/sigil_forge.py open out/sigil-forge/*/forge-packet.json
```

**Done when:** packet omits `normalized_intent`; `open` recovers the original intent.

### Polish prompt for host image tools

```bash
python3 scripts/sigil_forge.py construct \
  --intent "I build durable systems under pressure" \
  --polish --polish-style "ink on parchment" \
  --out out/sigil-forge
```

**Done when:** `polish_prompt.json` exists; `gen_seed` is `applied`; master still verifies.

## Common Pitfalls

1. **Inventing geometry** — monogram/kamea points come only from `scripts/`.
2. **Claiming stego success** when `verify` fails or channel is `skipped`.
3. **Leaking plaintext intent** into public SVG/PNG (default policy forbids).
4. **Treating PNG as full ciphertext** — public PNG LSB is digest-only; seal is packet-local.
5. **All-vowel intents** — raise `NOT_COMPUTABLE:`; rewrite with consonants.
6. **`--passphrase` on argv** — prefer `SIGIL_FORGE_PASSPHRASE`.
7. **Collapsing Enochian seals** into Spare intent glyphs.
8. **Mutating `references/`** or auto-promoting artifacts to canon.
9. **Premature completion** — deliver without verify when integrity was claimed.

## Verification Checklist

- [ ] Safety gate passed (or refusal with no artifacts)
- [ ] `forge-packet.json` has `schema_version`, `mode`, `intent_digest`, `channels[]`,
      `methods`, `artifacts`, `crypto`, `verify`, `framing_notes`
- [ ] Every fixed channel is `applied` or `skipped` with reason
- [ ] `glyph.svg` present; `glyph.png` when `png_lsb` applied
- [ ] `verify` recovers matching digest (SVG and PNG when present)
- [ ] Public media has no default plaintext intent
- [ ] Framing matches mode; **no efficacy claims**
- [ ] If polished: `polish_prompt.json` + `gen_seed` applied; master still verifies
- [ ] `python3 scripts/sigil_forge.py check` → `ok: true`
- [ ] `python3 scripts/validate_hermes_skill.py` → `ok: true` (dev/release)

## References

| Doc | Topic |
|-----|--------|
| [methods-spare.md](references/methods-spare.md) | Spare reduction |
| [methods-kamea.md](references/methods-kamea.md) | Kamea tables and path |
| [methods-bind-runes.md](references/methods-bind-runes.md) | Bind-runes (modern_derivation) |
| [methods-rose-cross.md](references/methods-rose-cross.md) | Hebrew 22-petal Rose Cross |
| [sigil-ontology.md](references/sigil-ontology.md) | Method taxonomy / families |
| [source-manifest.yaml](references/source-manifest.yaml) | Method → source citations |
| [wallpaper-framework.md](references/wallpaper-framework.md) | Wallpaper carrier pipeline |
| [wallpaper-prompt-contract.md](references/wallpaper-prompt-contract.md) | Background-only AI prompts |
| [receipts-and-ledger.md](references/receipts-and-ledger.md) | Run receipts + PROPOSED ledger |
| [channels-and-steganography.md](references/channels-and-steganography.md) | Channel IDs / capacity |
| [profiles-creative.md](references/profiles-creative.md) | Creative tone |
| [profiles-practice.md](references/profiles-practice.md) | Practice tone |
| [safety-and-framing.md](references/safety-and-framing.md) | Refusals / no-efficacy |
| [hermes-runtime-contract.md](references/hermes-runtime-contract.md) | Agent vs engine |
| [expansion-spine.md](references/expansion-spine.md) | Future growth |
| [distinction-enochian.md](references/distinction-enochian.md) | Intent ≠ Enochian seals |

Design: [docs/superpowers/specs/2026-08-07-sigil-forge-design.md](docs/superpowers/specs/2026-08-07-sigil-forge-design.md).
