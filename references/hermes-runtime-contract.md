# Hermes runtime contract

Version: **v1**

Sigil-Forge is a **standalone Hermes skill**. Default install path:
`~/.hermes/skills/sigil-forge`. Skill name: `sigil-forge`.

## Two layers

| Layer | Owns | Does **not** own |
|-------|------|------------------|
| **Agent contract** (`SKILL.md`, `references/`) | Intake, mode, safety judgment, packet narrative, when to invoke scripts / host image tools | Inventing glyph geometry or fake stego success |
| **Construction engine** (`scripts/`) | Normalize, digest, optional encrypt, Spare, kamea, fusion, SVG/PNG, stego embed/extract/verify | Mystical guarantees, external image APIs, mutating skill `references/` |

## Skill root resolution

1. `HERMES_SKILL_DIR` if set  
2. Else install/clone directory containing this skill  

Default out: `out/sigil-forge/<run-id>/` or `--out`.  
`run-id` = timestamp + short digest prefix.

## Artifact rule

- Write under user-chosen directory or skill `out/`.  
- **Never mutate `references/`** during ordinary runs.  
- Prefer hash-based run paths so listings do not leak full intent text.

## CLI surface (v1)

| Command | Role |
|---------|------|
| `construct` | Full forge: safety → … → packet |
| `verify` | Recover digest / integrity from SVG or PNG |
| `check` | Smoke-check skill tree and schemas |
| `help` | Command overview |

Entry: `python3 scripts/sigil_forge.py …`

## Schemas

Under `schemas/` (validate when `jsonschema` available; structural checks always):

- `forge-packet.schema.json`  
- `channel-manifest.schema.json`  
- `construction-result.schema.json`  

## Agent obligations

1. Follow `SKILL.md` procedure: safety → normalize/construct → dual-mode framing
   → optional geometry-locked polish → verify.  
2. Point to `references/` for method depth; do not invent cipher tables.  
3. Report channels honestly (`applied` / `skipped`).  
4. Never claim efficacy or stego success without verify.  
5. Standalone: no hard dependency on Kubrick, Orchestra, or ComfyUI. Optional
   `interop` fields on the packet remain empty-ok.

## Host tools

- Image polish (e.g. host Imagine tools) is **optional** and post-master only.  
- Skill ships procedure/prompt constraints; does not hardcode a single vendor API.  
- Offline success is first-class: procedural glyph + packet without any image API.

## Progressive disclosure

Keep agent context lean: load method references when constructing or explaining
that channel — not all docs on every turn.

## Related

- Expansion: `expansion-spine.md`  
- Safety: `safety-and-framing.md`  
- Design: `docs/superpowers/specs/2026-08-07-sigil-forge-design.md`
