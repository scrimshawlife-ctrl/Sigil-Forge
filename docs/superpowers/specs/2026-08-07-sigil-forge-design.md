# Sigil-Forge Design

**Date:** 2026-08-07  
**Repo:** [scrimshawlife-ctrl/Sigil-Forge](https://github.com/scrimshawlife-ctrl/Sigil-Forge)  
**Status:** Ready for user review (implementation planning after approval)  
**License:** MIT  

## 1. Summary

Sigil-Forge is a **standalone Hermes skill** that turns a user’s statement of intent into a **method-faithful, multi-channel sigil**: a forge packet plus a procedural master glyph (SVG, optional PNG) in which the intent is **compressed, fused across ancient and modern craft, and steganographically embedded**. Optional AI image polish may improve aesthetics only after the master glyph exists; it never replaces construction.

Default framing is a **creative / focus tool** (clarify, compress, externalize intent). An optional **`practice` profile** uses practitioner-oriented language and optional charge/use notes without claiming supernatural efficacy.

## 2. Goals and non-goals

### Goals (v1)

- Help the user amplify intent by **making it durable, multi-encoded, and verifiable** as a symbol.
- Fuse **modern Spare-style** monogram construction with **classical kamea (magic square)** path construction into **one coherent glyph**.
- Embed the intent in **as many independent channels as the v1 channel set defines**, including steganography.
- Remain useful **offline**: procedural glyph + packet without any image API.
- Install as a lean Hermes skill under `~/.hermes/skills/sigil-forge`, with an **expansion spine** (schemas, thin CLI, future receipts) so growth does not require a rewrite.
- Stay **standalone** (no hard dependency on Kubrick, Orchestra, or ComfyUI), with thin optional interop fields for later handoff.

### Non-goals (v1)

- Full ritual liturgy, banishing systems, or a results-magic / outcome engine.
- Bind-runes, Rose Cross, Enochian seals (Enochian seals remain Orchestra’s authority/placement domain and must not be collapsed into Spare-style intent glyphs).
- Required ComfyUI, paid APIs, or multi-provider adapter matrix on day one.
- Claims that the sigil “works,” causes external events, or replaces professional help.
- Unlimited channel sprawl: “as many ways as possible” means **the fixed v1 channel set**, each reported as applied or skipped with reason—not an unbounded research project per run.

## 3. Decisions (locked)

| Topic | Decision |
|-------|----------|
| Primary deliverable | Forge packet + multi-channel master glyph |
| Methods | Spare + kamea **fused** (not pick-one-only) |
| Image path | Always procedural SVG (+ optional PNG); AI polish optional |
| Steganography | Structural + SVG + PNG LSB + seed; default **no plaintext intent** in public artifacts |
| Packaging | Hybrid: lean skill first; schemas/CLI spine for expansion |
| Framing | Dual-mode: `creative` (default) / `practice` |
| Integration | Standalone; optional interop fields empty-ok |
| Architecture | Construction engine + Hermes agent contract (Approach 2) |

## 4. Architecture

### 4.1 Identity

Hermes loads the skill directory. `SKILL.md` is the behavior contract. Python scripts provide deterministic construction, stego embed/extract, and verify. The agent owns conversation, intake, mode selection, safety refusals, packet narrative, and optional host image-tool calls.

### 4.2 Two layers

| Layer | Owns | Does not own |
|-------|------|----------------|
| **Agent contract** (`SKILL.md`, `references/`) | Intake, mode, safety, packet prose, when to invoke scripts / image tools | Inventing glyph geometry or fake stego success |
| **Construction engine** (`scripts/`) | Normalize, digest, optional encrypt, Spare, kamea, fusion layout, SVG/PNG, stego embed/extract/verify | Mystical guarantees, external image APIs, mutating skill references |

### 4.3 Authority

- All creative outputs are **proposal-only**.
- The skill may craft symbols, embed data, and write local artifacts.
- The skill may not claim efficacy, contact third parties, spend money, or promote artifacts to “canon” without the human operator.

### 4.4 Artifact rule

Write outputs under a user-chosen directory or skill `out/`. Never mutate `references/` during ordinary runs. Prefer **hash-based run paths** so filesystem listings do not leak full intent text by default.

## 5. Multi-channel intent encoding

### 5.1 Principle

A forged sigil is a **carrier**. The statement of intent is re-encoded through **independent channels** fused into one form. No single channel is the whole secret.

“Encrypt” means:

1. **Symbolic / structural encoding** via historical and modern craft methods, and  
2. **Optional real cryptography** of a payload (ciphertext of the intent under a user or run key), plus  
3. **Steganography** so public-facing media carry digest/ciphertext and channel bits without exposing plaintext by default.

### 5.2 v1 channel set

Every successful forge **attempts all channels** below. Each is recorded in the channel manifest as `applied` or `skipped` with reason.

#### A. Ancient / classical craft (visible structure)

| ID | Channel | Description |
|----|---------|-------------|
| `spare_monogram` | Spare-style letter reduction | Normalize intent → strip vowels/spaces → collapse duplicate letters → monogram join-graph as primary silhouette |
| `kamea_path` | Magic-square path | Map letters → numbers (documented cipher) → continuous path on a magic square |
| `kamea_square_choice` | Square / planetary selection | Operator pick or intent-digest-derived choice among Saturn 3×3 … Luna 9×9 (standard Western kamea sizes) |

#### B. Modern cryptographic / digital craft

| ID | Channel | Description |
|----|---------|-------------|
| `intent_digest` | Cryptographic digest | SHA-256 of normalized intent; drives seeds, stego keys, and verify |
| `optional_ciphertext` | Sealed payload | AES-GCM (or equivalent) of full intent under key derived from operator passphrase or ephemeral run key; ciphertext may be stego’d, never required in public metadata as plaintext |

#### C. Steganography

| ID | Channel | Description |
|----|---------|-------------|
| `svg_metadata` | SVG container | Namespaced private metadata: receipt id, digest, method bitmap; **not** plaintext intent by default |
| `path_epsilon` | Geometry LSB-analogue | Sub-visual coordinate perturbations of path points keyed by digest bits |
| `path_order` | Stroke order | Segment / stroke order encodes residual nibbles after monogram collapse |
| `metric_quantize` | Angles / lengths / node counts | Quantized metrics encode cipher digits while preserving one coherent glyph |
| `png_lsb` | Raster stego | When PNG exists: LSB (or similar) payload = digest + optional ciphertext + channel bitmap |
| `gen_seed` | Generation seed | When AI polish is used: seed derived from digest so regeneration is intent-locked |

### 5.3 Fusion composition rule

Produce **one master glyph**, not disconnected doodles:

- Spare monogram defines the **primary silhouette**.
- Kamea path supplies an **internal, orbital, or interwoven stroke** consistent with the same composition bounds.
- Metric / order stego operate on that fused geometry without destroying recognizability.

### 5.4 Privacy defaults

| Asset | Default content |
|-------|-----------------|
| Public SVG / PNG | Digest, stego payload, channel bitmap — **no plaintext intent** |
| Local forge packet | Plaintext intent (or passphrase-sealed packet only) + full channel report + paths + verify instructions |
| Run directory name | Timestamp + short digest prefix (not full intent string) |

Operator may opt into stronger sealing (passphrase required to read intent from packet) or, explicitly, weaker local debug modes. Debug modes must be labeled and not the default.

### 5.5 AI polish constraint

AI polish may change **style, medium, lighting, texture** only under geometry locks derived from the procedural master. If polish breaks PNG stego, either:

- re-apply stego to a fresh procedural raster, or  
- treat polished art as **presentation-only** and keep the master SVG/PNG as the verifiable carrier.

The skill must never report stego success on an artifact that fails `verify`.

## 6. Data flow

```text
USER INTENT
  → INTAKE (mode: creative|practice, constraints, optional passphrase)
  → SAFETY / ALIGN (refuse empty or harmful; request rewrite)
  → NORMALIZE
  → digest = H(normalized_intent)
  → optional ciphertext = Enc(intent, K)
  → FUSE CONSTRUCT
       spare_monogram + kamea_path + square_choice
       + path_order + metric_quantize + path_epsilon
  → WRITE SVG (+ svg_metadata stego)
  → optional RASTER PNG (+ png_lsb)
  → ASSEMBLE forge packet (local)
  → optional AI polish (geometry-locked) + re-stego policy
  → DELIVER summary + paths
  → VERIFY (extract digest / channels; integrity report)
```

Later spine (documented, not required for v1 completeness): run receipts, learning ledger (proposal-only), richer CLI jobs.

## 7. Components

### 7.1 Agent-side

1. **Intake / align** — Intent, mode, style constraints, cultural “do not use X” boundaries, passphrase optional.  
2. **Safety gate** — Refuse violence, self-harm, harming others, non-consensual control; do not soft-build the harmful form.  
3. **Packet assembler** — Human narrative + machine JSON matching schemas.  
4. **Optional image polish** — Host tools (e.g. Grok Imagine) or ComfyUI if present; never required.  
5. **Mode profiles** — `creative` vs `practice` tone without changing the engine.

### 7.2 Engine-side (`scripts/`)

| Module | Responsibility |
|--------|----------------|
| `sigil_forge.py` | Thin CLI entry: `construct`, `verify`, `check`/`help` (expandable to `doctor`, `forge` later) |
| `normalize.py` | Intent normalization rules (documented, stable) |
| `spare.py` | Letter reduction + monogram graph |
| `kamea.py` | Ciphers, square tables, path plotting |
| `fuse.py` | Compose monogram + kamea into one layout |
| `stego_svg.py` | Metadata + path epsilon + order/metric embed/extract |
| `stego_png.py` | LSB embed/extract when raster available |
| `crypto_payload.py` | Digest + optional AES-GCM seal |
| `svg_export.py` / raster helpers | Emit master SVG; optional PNG |
| `paths.py` | Skill root / out resolution |

### 7.3 References (progressive disclosure)

- `methods-spare.md`, `methods-kamea.md` — doctrine and parameters  
- `channels-and-steganography.md` — channel IDs, capacity, failure modes  
- `profiles-creative.md`, `profiles-practice.md`  
- `safety-and-framing.md`  
- `hermes-runtime-contract.md`  
- `expansion-spine.md` — how CLI/receipts/interop grow  
- `distinction-enochian.md` — do not collapse Enochian seals into intent sigils  

## 8. Repo / install layout

```text
Sigil-Forge/
  SKILL.md
  README.md
  QUICKSTART.md
  LICENSE
  VERSION
  install.sh                    # default → ~/.hermes/skills/sigil-forge
  references/
  scripts/
  schemas/
    construction-result.schema.json
    forge-packet.schema.json
    channel-manifest.schema.json
  examples/
    intents/                    # golden statements + expected reductions
  docs/
    superpowers/
      specs/
        2026-08-07-sigil-forge-design.md
  out/                          # gitignored
  tests/
```

### Runtime resolution

- Skill root = install dir or clone; honor `HERMES_SKILL_DIR` when set.  
- Default out: `out/sigil-forge/<run-id>/` or `--out`.  
- `run-id` = timestamp + digest prefix.

## 9. Forge packet (v1 fields)

Machine-readable packet (JSON) plus optional Markdown summary for humans.

Required concepts:

- `schema_version`
- `mode`: `creative` | `practice`
- `normalized_intent` (local only; omit or seal per privacy policy)
- `intent_digest` (hex)
- `channels[]`: `{ id, status: applied|skipped, detail }`
- `methods`: spare params, kamea planet/size, cipher id
- `artifacts`: paths to SVG, PNG, polished image if any
- `crypto`: algorithm, key policy (`none` | `ephemeral_run` | `passphrase`), ciphertext present boolean
- `verify`: exact command to re-check integrity
- `framing_notes`: mode-appropriate, no efficacy claims
- `interop` (optional, empty-ok): e.g. `intent_token`, `related_skills`

Schemas live under `schemas/` and are validated on construct when jsonschema is available; without jsonschema, structural checks in pure Python still run for required keys.

## 10. Modes

| Mode | Default | Packet emphasis |
|------|---------|-----------------|
| `creative` | Yes | Focus externalization, journaling/habit cue, art; no charge language |
| `practice` | Opt-in | Same construction; optional short personal use notes (gaze, place, discard); still no efficacy claims |

## 11. Error handling (fail-closed)

| Condition | Behavior |
|-----------|----------|
| Empty / pure-noise intent | Refuse; ask for clear present-tense desire or statement of intent |
| No letters left after Spare reduction | Construction may still proceed via digest + kamea from alternate mapping; if both craft channels fail, `NOT_COMPUTABLE` with rewrite guidance |
| Unknown method / invalid square | Error with allowed set; do not invent squares |
| Harmful intent | Refuse before any encode/stego |
| Image backend missing | Success with procedural artifacts + prompt packet for later |
| Stego capacity exceeded | Apply max channels that fit; mark remainder `skipped(capacity)`; never claim full embed |
| Verify mismatch | Report failure; do not claim forged integrity |
| Cultural / closed-practice exclusion | Honor operator boundary; skip channels that would violate it |

## 12. Safety and framing

- No supernatural efficacy claims in either mode.  
- Methods are craft history, symbolic compression, and data embedding—not proof of metaphysics.  
- Distinguish **Chaos/Spare intent sigils** from **Enochian seals** (authority/placement).  
- Intent text is sensitive: hash in paths; no telemetry; no default plaintext in public media.  
- Steganography is for **operator sovereignty and multi-encoding**, not for assisting covert harm. Safety refusal runs before embed.

## 13. Testing

### v1 bar

1. **Unit tests** — Spare fixtures, kamea maps, fusion bounds, digest stability.  
2. **Stego round-trip** — embed → extract → digest match; optional ciphertext decrypt with key.  
3. **Privacy tests** — public SVG/PNG must not contain plaintext intent under default policy.  
4. **Golden examples** — 3–5 intents with expected reduced strings and channel-applied checks.  
5. **`check` / smoke** — tree present, schemas load, one construct writes packet + SVG under `out/`, verify passes.  
6. **Lightweight agent evals** — refuse-harmful; creative vs practice tone; offline success without image gen.

### Explicit non-tests for v1

- Pixel-identical AI polish.  
- Adversarial steganalysis hardness certification.  
- Full ritual efficacy studies.

## 14. Expansion spine

Documented extension points (implement after v1 forge loop is solid):

- Full CLI: `do forge|doctor|eval|receipt`  
- Append-only learning ledger (method preference observations, proposal-only)  
- Provider prompt adapters (Kubrick-style) and ComfyUI workflow export  
- Additional craft channels: bind-runes, Rose Cross paths, multi-frame carriers  
- Stronger KDF (e.g. Argon2id) for passphrase sealing  
- Optional Orchestra dual-naming export (`intent_token` / `sigil_glyph`)

## 15. End-to-end user journey

**Intent example:** “I maintain calm focus while shipping Sigil-Forge.”

1. Intake with mode and optional passphrase.  
2. Safety/align.  
3. Digest (+ optional seal).  
4. Fuse construct + all applicable stego channels.  
5. Write master SVG/PNG + local forge packet.  
6. Optional AI polish under geometry lock.  
7. Deliver paths and channel summary.  
8. `verify` confirms digest/channel integrity on public artifacts.

**Success criterion:** One coherent multi-encoded sigil; offline-complete; verifiable; expandable channel list later without breaking the packet spine.

## 16. Hermes skill surface (implementation target)

`SKILL.md` frontmatter targets Hermes conventions:

- `name: sigil-forge`  
- Description front-loaded with triggers: sigil, intent, kamea, Spare, steganography, forge packet  
- Tags: Creative, Sigil, Intent, Steganography, SymbolicDesign  
- Category: creative  
- When to use / when not to use (not general image gen; not Enochian seals; not Kubrick cinema)  
- Procedure mirroring §6  
- Pitfalls and verification checklist  

## 17. Implementation phases (planning preview)

Not a full plan—ordering for `writing-plans`:

1. Repo skeleton, `SKILL.md` stub, install path, VERSION, gitignore `out/`  
2. Normalize + digest + Spare + unit fixtures  
3. Kamea tables + path + unit fixtures  
4. Fuse layout + SVG export  
5. Stego SVG + PNG + verify round-trip  
6. Optional ciphertext payload  
7. Schemas + forge packet assembly  
8. Examples, smoke/`check`, privacy tests  
9. References + dual profiles + safety  
10. Optional AI polish procedure in `SKILL.md`  
11. QUICKSTART/README polish  

## 18. Open parameters (fixed defaults for v1)

These are explicit defaults so implementation is not blocked; they may be revisited without changing architecture:

| Parameter | v1 default |
|-----------|------------|
| Digest | SHA-256, hex lowercase |
| Symmetric crypto | AES-GCM with key from passphrase via PBKDF2-HMAC-SHA256 (stdlib-friendly); document upgrade path to Argon2id |
| Letter→number cipher for kamea | Documented standard Western occult digit mapping in `methods-kamea.md` (stable versioned table) |
| Default square if unspecified | Derived from digest mod available squares; operator override allowed |
| SVG canvas | Square viewBox, monochrome stroke, no readable residual Latin letters in silhouette by default |
| PNG | Optional; produced when a stdlib or declared dependency can rasterize, or via simple SVG→PNG tool if present; stego PNG skipped if no raster |
| AI provider | Host-default only; skill ships prompt text, does not hardcode one vendor |

---

## Approval record

Collaborative brainstorming (2026-08-07) locked:

- Approach 2 (engine + agent contract)  
- Hybrid packaging  
- Dual-mode framing  
- Standalone with future interop hooks  
- Multi-channel fusion + steganography as core (superseding single-method-only router)  

Next step after user review of this file: **writing-plans** for implementation—not ad-hoc coding.
