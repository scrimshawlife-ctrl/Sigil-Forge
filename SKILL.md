---
name: sigil-forge
description: >
  Use when forging sigils, intent glyphs, kamea/Spare stego, forge packets, or when
  the user asks to be guided/wizard through sigil creation. Offline multi-channel
  construction; dual creative/practice framing; no efficacy claims. Prefer wizard
  --next step runner for new users.
version: 0.10.0
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
  - wizard
  - guide me
  - walk me through
  - help me forge
---

# Sigil-Forge

Standalone Hermes skill. Hermes loads this directory; `SKILL.md` is the behavior
contract. Deterministic construction lives under `scripts/`; the agent owns
intake, mode framing, safety judgment, and optional host image polish.

## Overview

Sigil-Forge turns a statement of intent into:

1. A **procedural master glyph** (SVG + offline PNG) fusing Spare monogram geometry
   with kamea / rose / bind-runes (and optional planetary seals).
2. A **local forge packet** with method ontology, channels, crypto policy, and verify command.
3. **Steganographic carriers** (digest/channel bits — not plaintext intent by default).
4. Optional **wallpapers**: device-aware composition of the **immutable** glyph over
   atmosphere (procedural, operator PNG, or host AI via file/command). The model never
   redraws canonical geometry.

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

**Prefer the wizard** when the user is new, asks to be guided, or says “wizard” /
“guide me” / “walk me through”. Use the **step runner** (one question per turn):

```bash
# Quick path for most users (intent + optional wallpaper)
python3 scripts/sigil_forge.py wizard --session-new --path quick
# Each turn after the user answers:
python3 scripts/sigil_forge.py wizard --next --session <id> \
  --answers-json '{"intent":"I maintain calm focus"}'
# When next.done is true:
python3 scripts/sigil_forge.py wizard --apply answers.json --path quick --out out/sigil-forge
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.svg
```

Load [references/wizard.md](references/wizard.md) only while guiding (progressive
disclosure). Expert operators may skip to construct.

1. **Intake / wizard** — Run `--next` until done; ask **only** the current step.
   Use `step.help` if needed. Prefer `--path quick` unless craft options requested.
   **Done when:** `next.done` true or expert construct args complete; safety ok.
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
   `--seal-packet`, `--polish`, `--square venus`, `--wallpaper` (one-shot compose).
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
8. **Optional wallpapers** — Only after master verify (or via `construct --wallpaper`):

   ```bash
   python3 scripts/sigil_forge.py wallpaper \
     --run out/sigil-forge/<run-id> \
     --surface phone_lock --mode focus --theme mercurial
   # Host AI atmosphere (never redraw glyph):
   # --background-method ai_generated --background /path/ai-bg.png --provider host_file
   # or SIGIL_FORGE_BG_COMMAND with {prompt_path} {out_path} {width} {height} {seed}
   ```

   **Done when:** `wallpaper/` + `receipts/wallpaper-receipt-*.json` exist;
   receipt `geometry_preserved: true`; `glyph.svg` digest unchanged;
   if AI requested, prompt package present and method/provider recorded honestly.
9. **Open sealed intent** (if sealed):

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
| `planetary_seal` | Agrippan traditional / intelligence / spirit (opt-in; plate strokes default) |
| `intent_digest` | SHA-256 of normalized intent |
| `optional_ciphertext` | AES-GCM seal when passphrase provided (local packet) |
| `svg_metadata` | SVG metadata digest / method bits |
| `path_epsilon` | Coordinate parity bits from digest |
| `path_order` | Construction-order binding (monogram before kamea) |
| `metric_quantize` | `data-sf-metric` digest nibble attributes |
| `png_lsb` | Offline layout raster + LSB (digest-only payload) |
| `gen_seed` | Digest-derived seed when `--polish` / write_polish |
| `phonetic_sigil` | Optional phoneme-sequence JSON (`--phonetic`) |

Details: `references/channels-and-steganography.md`. Wallpapers are a
**presentation layer**, not an additional forge channel.

## CLI

```bash
python3 scripts/sigil_forge.py help
python3 scripts/sigil_forge.py doctor
python3 scripts/sigil_forge.py eval
python3 scripts/sigil_forge.py check
python3 scripts/sigil_forge.py construct --intent "…" --out out/sigil-forge
python3 scripts/sigil_forge.py construct --intent "…" --phonetic --interop --out out/sf
python3 scripts/sigil_forge.py construct --intent "…" --polish --out out/sigil-forge
python3 scripts/sigil_forge.py construct --intent "…" --wallpaper --surface phone_lock \
  --wp-mode focus --out out/sigil-forge
python3 scripts/sigil_forge.py wizard --script --path quick
python3 scripts/sigil_forge.py wizard --session-new --path quick
python3 scripts/sigil_forge.py wizard --next --session <id> --answers-json '{…}'
python3 scripts/sigil_forge.py wizard --apply answers.json --path quick --out out/sigil-forge
python3 scripts/sigil_forge.py wizard --list-corpus
python3 scripts/sigil_forge.py verify out/sigil-forge/<run-id>/glyph.svg
python3 scripts/sigil_forge.py wallpaper --run out/sigil-forge/<run-id> \
  --surface phone_lock --mode focus --theme mercurial
python3 scripts/sigil_forge.py wallpaper --run out/sigil-forge/<run-id> \
  --surface phone_lock --background-method ai_generated --background /path/ai-bg.png
python3 scripts/sigil_forge.py open out/sigil-forge/<run-id>/forge-packet.json
python3 scripts/sigil_forge.py learn --class channel_preference \
  --summary "bind_runes + rose_cross_path coherent" --channels bind_runes,rose_cross_path
python3 scripts/sigil_forge.py ledger --limit 20
python3 scripts/validate_hermes_skill.py   # frontmatter / Hermes hygiene
```

Env: `HERMES_SKILL_DIR`, `SIGIL_FORGE_PASSPHRASE`, optional `SIGIL_FORGE_BG_COMMAND`
(host AI background shell template). Prefer env over `--passphrase` (argv is
visible in process lists). Construct uses atomic staging then promote.

## One-Shot Recipes

### Wizard-guided forge (recommended for Hermes)

```bash
python3 scripts/sigil_forge.py wizard --session-new --path quick
# Loop: ask only next.step; merge answer; call --next again until done
python3 scripts/sigil_forge.py wizard --next --session <id> \
  --answers-json '{"intent":"I maintain calm focus"}'
# Save final answers and apply
python3 scripts/sigil_forge.py wizard --apply answers.json --path quick --out out/sigil-forge
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.svg
```

**Done when:** apply `ok: true`; verify recovers digest; no efficacy claims.
**Agent must:** one question per turn; refuse on `refused: true`; never invent geometry.

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

### Phone/desktop wallpaper

```bash
python3 scripts/sigil_forge.py construct --intent "I maintain calm focus" --out out/sigil-forge
RUN=$(ls -d out/sigil-forge/*/ | head -1)
python3 scripts/sigil_forge.py verify "${RUN}glyph.svg"
python3 scripts/sigil_forge.py wallpaper --run "$RUN" --surfaces phone_lock,phone_home,desktop
```

**Done when:** wallpapers under `wallpaper/`; receipts `status: verified`;
`glyph.svg` hash unchanged.

### Host AI wallpaper background (two-phase)

```bash
# Phase 1: prompt package (+ procedural stand-in offline)
python3 scripts/sigil_forge.py wallpaper --run "$RUN" --surface phone_lock \
  --background-method ai_generated --theme mercurial
# Phase 2: after host generates PNG from wallpaper/background-prompt-phone_lock.json
python3 scripts/sigil_forge.py wallpaper --run "$RUN" --surface phone_lock \
  --background-method ai_generated --background /path/to/ai-bg.png \
  --provider host_file --model "local-sd"
```

**Done when:** `generation.background_method` is `ai_generated`; provider recorded;
receipt `geometry_preserved: true`; prompt package forbids glyph invention.

## Common Pitfalls

1. **Inventing geometry** — monogram/kamea points come only from `scripts/`.
2. **Claiming stego success** when `verify` fails or channel is `skipped`.
3. **Leaking plaintext intent** into public SVG/PNG/wallpapers (default policy forbids).
4. **Treating PNG as full ciphertext** — public PNG LSB is digest-only; seal is packet-local.
5. **All-vowel intents** — raise `NOT_COMPUTABLE:`; rewrite with consonants.
6. **`--passphrase` on argv** — prefer `SIGIL_FORGE_PASSPHRASE`.
7. **Collapsing Enochian seals** into Spare intent glyphs.
8. **Mutating `references/`** or auto-promoting artifacts to canon.
9. **Premature completion** — deliver without verify when integrity was claimed.
10. **AI-redrawing the sigil for wallpaper** — generate atmosphere only; composite the master SVG.

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
- [ ] If wallpaper: receipts `geometry_preserved: true`; no plaintext intent; glyph digest unchanged
- [ ] If AI wallpaper: prompt package present; method/provider honest (no silent fake AI)
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
| [wizard.md](references/wizard.md) | Hermes guided forge interview |
| [methods-planetary-characters.md](references/methods-planetary-characters.md) | Seals / intelligence / spirit corpus |
| [planetary-character-corpus.json](references/planetary-character-corpus.json) | Agrippan names + construction flags |
| [planetary-plate-strokes.json](references/planetary-plate-strokes.json) | Multi-stroke plate digitizations |
| [receipts-and-ledger.md](references/receipts-and-ledger.md) | Run receipts + PROPOSED ledger |
| [channels-and-steganography.md](references/channels-and-steganography.md) | Channel IDs / capacity |
| [profiles-creative.md](references/profiles-creative.md) | Creative tone |
| [profiles-practice.md](references/profiles-practice.md) | Practice tone |
| [safety-and-framing.md](references/safety-and-framing.md) | Refusals / no-efficacy |
| [hermes-runtime-contract.md](references/hermes-runtime-contract.md) | Agent vs engine |
| [expansion-spine.md](references/expansion-spine.md) | Future growth |
| [distinction-enochian.md](references/distinction-enochian.md) | Intent ≠ Enochian seals |

Design: [docs/superpowers/specs/2026-08-07-sigil-forge-design.md](docs/superpowers/specs/2026-08-07-sigil-forge-design.md).
