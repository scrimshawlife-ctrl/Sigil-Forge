---
name: sigil-forge
description: >-
  Use when: sigil, intent, kamea, Spare, stego forge needed.
  Builds multi-channel forge packets and procedural glyphs with
  optional steganography. Creative or practice framing; offline-first.
  Never invents geometry or claims supernatural efficacy.
version: 0.1.0
license: MIT
metadata:
  hermes:
    tags:
      - Creative
      - Sigil
      - Intent
      - Steganography
    category: creative
---

# Sigil-Forge

Hermes skill contract for multi-channel intent sigils. The agent owns intake,
mode, safety, narrative, and optional host image polish. Deterministic Python
under `scripts/` owns normalize → digest → fuse → stego → packet → verify.

## Overview

Sigil-Forge turns a statement of intent into:

1. A **procedural master glyph** (SVG, optional PNG) fusing Spare-style monogram
   geometry with a classical kamea path.
2. A **local forge packet** (`forge-packet.json` + Markdown summary) with channel
   status, methods, artifacts, crypto policy, and verify command.
3. **Steganographic carriers** on public media (digest / channel bits — not
   plaintext intent by default).

Default framing is a **creative / focus tool** (clarify, compress, externalize).
Optional **`practice`** mode uses practitioner-oriented language without efficacy
claims. Methods are craft history, symbolic compression, and data embedding —
not proof of metaphysics.

**Authority:** all creative outputs are proposal-only. Never claim the sigil
“works,” causes external events, or replaces professional help.

## When to Use / Not

### Use when

- User wants a **sigil**, **intent glyph**, **forge packet**, or multi-encoded symbol.
- User mentions **Spare**, **kamea** / magic squares, or **steganography** of intent.
- User wants offline, verifiable construction (no image API required).
- User chooses creative journaling/habit cue **or** personal practice framing.

### Do not use when

- General image generation, cinema, or Kubrick-style production pipelines.
- **Enochian seals**, authority/placement seals, or Orchestra dual-naming as
  primary product (see [references/distinction-enochian.md](references/distinction-enochian.md)).
- Full ritual liturgy, banishing systems, or results-magic / outcome engines.
- Harmful intents (violence, self-harm, non-consensual control, exploitation) —
  refuse before any encode or stego.
- User asks you to invent glyph geometry or report stego success without `verify`.

## Prerequisites

- Python 3 with stdlib (skill root = install dir or clone).
- Optional: `jsonschema` for stricter packet validation; raster backend for PNG LSB.
- Honor `HERMES_SKILL_DIR` when set; otherwise resolve skill root from this tree.
- Write artifacts under user `--out` or default `out/sigil-forge/<run-id>/`.
  **Never mutate `references/` during ordinary runs.**

## Procedure

Mirror the construction engine. Do not skip safety or invent intermediate geometry.

1. **Intake** — Collect present-tense statement of intent; mode
   (`creative` default | `practice`); optional passphrase; optional kamea square
   override (`saturn`…`luna`); cultural exclusions if stated.
2. **Safety / align** — Run refusal heuristics (and agent judgment). Empty or
   pure-noise intent → request rewrite. Harmful intent → refuse; do not soft-build.
   Details: [references/safety-and-framing.md](references/safety-and-framing.md).
3. **Normalize** — Engine: NFKC, strip, lowercase, collapse whitespace
   (`scripts/normalize.py`). Digest = SHA-256 hex of normalized intent.
4. **Construct via scripts** — Prefer CLI or equivalent library call; do not
   hand-draw paths:

   ```bash
   python3 scripts/sigil_forge.py construct \
     --intent "I maintain calm focus" \
     --mode creative \
     --out out/sigil-forge
   ```

   Pipeline inside `construct`: safety → normalize → digest → optional AES-GCM
   seal → Spare monogram + kamea path fuse → SVG + SVG stego → optional PNG LSB
   → forge packet. Method detail:
   [methods-spare.md](references/methods-spare.md),
   [methods-kamea.md](references/methods-kamea.md),
   [channels-and-steganography.md](references/channels-and-steganography.md).
5. **Dual-mode notes** — Apply profile tone only to narrative / `framing_notes`.
   Construction is identical across modes.
   [profiles-creative.md](references/profiles-creative.md),
   [profiles-practice.md](references/profiles-practice.md).
6. **Deliver** — Paths to `glyph.svg`, optional `glyph.png`, `forge-packet.json`,
   `forge-packet.md`; channel summary (`applied` / `skipped` with reason).
7. **Optional AI polish (geometry-locked)** — Only after master glyph exists.
   May change style, medium, lighting, texture under geometry locks derived from
   the procedural master. Never replace construction. If polish breaks PNG stego:
   re-apply stego to a fresh procedural raster, or treat polished art as
   presentation-only and keep master SVG/PNG as the verifiable carrier.
   `gen_seed` channel is reserved for digest-derived seed when polish is used.
   **Agent-only prompt builder** (no image API in this skill):

   ```bash
   # library: scripts/prompt_polish.py
   # build_prompt(layout_summary, style) -> {prompt, negative, seed, geometry_lock}
   # seed = int(intent_digest[:8], 16); geometry_lock from stroke_count / path bbox
   ```

   Pass a layout summary (at least `intent_digest`, prefer `stroke_count` and
   `bbox` from the master). Write the returned package to the run dir if useful
   and record `artifacts.polish_prompt_path` on the packet. Use host image tools
   only with that package; never invent geometry or call a required remote API.
8. **Verify** — Always before claiming integrity:

   ```bash
   python3 scripts/sigil_forge.py verify path/to/glyph.svg
   # or glyph.png when png_lsb was applied
   ```

9. **Never claim efficacy** — Describe craft, encoding, and verify results only.

## Modes

| Mode | Default | Emphasis |
|------|---------|----------|
| `creative` | Yes | Focus externalization, journaling/habit cue, art; no charge language |
| `practice` | Opt-in | Same engine; optional short personal use notes (gaze, place, discard); still no efficacy claims |

## Channels (v1)

Every successful forge **attempts** the fixed set. Each row is `applied` or
`skipped` with reason in the packet. Capacity failures skip remainder — never
claim full embed.

| ID | Role |
|----|------|
| `spare_monogram` | Spare letter reduction → monogram silhouette |
| `kamea_path` | Magic-square path on selected planet square |
| `kamea_square_choice` | Operator override or digest-derived square |
| `intent_digest` | SHA-256 of normalized intent |
| `optional_ciphertext` | AES-GCM seal when passphrase provided (local packet) |
| `svg_metadata` | Namespaced SVG metadata (digest / method bits) |
| `path_epsilon` | Sub-visual coordinate perturbations from digest bits |
| `path_order` | Stroke/segment order residual encoding |
| `metric_quantize` | Quantized metrics encoding residual digits |
| `png_lsb` | Raster LSB when PNG available (digest-only payload in v1) |
| `gen_seed` | AI polish seed channel (skipped until polish used) |

Full capacity notes: [references/channels-and-steganography.md](references/channels-and-steganography.md).

## CLI

```bash
# Smoke-check skill tree
python3 scripts/sigil_forge.py check

# Construct (creative default)
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus while shipping" \
  --mode creative \
  --out out/sigil-forge

# Practice mode + passphrase seal (omit plaintext intent with --seal-packet)
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --mode practice \
  --passphrase 'operator-secret' \
  --seal-packet \
  --out out/sigil-forge

# Kamea square override
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --square venus \
  --out out/sigil-forge

# Full JSON packet on stdout
python3 scripts/sigil_forge.py construct --intent "..." --json --out out/sigil-forge

# Verify public artifact
python3 scripts/sigil_forge.py verify out/sigil-forge/<run-id>/glyph.svg
```

Env: `HERMES_SKILL_DIR` overrides skill root. Run ids are timestamp + digest
prefix (paths avoid full intent text).

## Pitfalls

- **Do not invent geometry** — monogram and kamea points come from `scripts/` only.
- **Do not claim stego success** if `verify` fails or channel is `skipped`.
- **Public SVG/PNG must not contain plaintext intent** under default policy.
- **Passphrase ciphertext** lives in the local packet; v1 public PNG LSB is
  digest-only — do not imply full intent is stego’d into the PNG.
- **PNG may be skipped** (`no_raster_backend`, filter/capacity errors) — still a
  successful forge if SVG + packet exist.
- **Empty Spare reduction** can still produce digest + kamea path; if craft
  channels fail entirely, surface rewrite guidance rather than a fake glyph.
- **Do not collapse Enochian / authority seals** into Spare-style intent glyphs.
- **Never mutate `references/`** or promote artifacts to “canon” without the human.
- **Stego is for operator sovereignty**, not assisting covert harm — safety first.

## Verification

Checklist before declaring a forge complete:

- [ ] Safety gate passed (or refusal delivered without artifacts).
- [ ] `forge-packet.json` present with `schema_version`, `mode`, `intent_digest`,
      `channels[]`, `methods`, `artifacts`, `crypto`, `verify`, `framing_notes`.
- [ ] `glyph.svg` written under run dir; channels reported honestly.
- [ ] `python3 scripts/sigil_forge.py verify <artifact>` recovers matching digest
      (or clear failure report — no fake integrity).
- [ ] Public media privacy: no default plaintext intent in SVG/PNG.
- [ ] Framing matches mode; **no efficacy claims**.
- [ ] Optional polish (if any) geometry-locked; master remains verifiable carrier.

Smoke:

```bash
python3 scripts/sigil_forge.py check
python3 -m pytest -v   # from skill root when developing
```

## References

| Doc | Topic |
|-----|--------|
| [methods-spare.md](references/methods-spare.md) | Spare reduction and monogram |
| [methods-kamea.md](references/methods-kamea.md) | Kamea tables, cipher, path |
| [channels-and-steganography.md](references/channels-and-steganography.md) | Channel IDs, capacity, failure |
| [profiles-creative.md](references/profiles-creative.md) | Creative mode tone |
| [profiles-practice.md](references/profiles-practice.md) | Practice mode tone |
| [safety-and-framing.md](references/safety-and-framing.md) | Refusals and no-efficacy rules |
| [hermes-runtime-contract.md](references/hermes-runtime-contract.md) | Agent vs engine ownership |
| [expansion-spine.md](references/expansion-spine.md) | Future CLI / receipts / interop |
| [distinction-enochian.md](references/distinction-enochian.md) | Intent sigils ≠ Enochian seals |

Runtime contract: [references/hermes-runtime-contract.md](references/hermes-runtime-contract.md).
Design: [docs/superpowers/specs/2026-08-07-sigil-forge-design.md](docs/superpowers/specs/2026-08-07-sigil-forge-design.md).
