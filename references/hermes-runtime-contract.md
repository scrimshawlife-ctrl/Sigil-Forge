# Hermes runtime contract

Version: **v2** (Sigil-Forge v0.10+)

Sigil-Forge is a **standalone Hermes skill**. Default install path:
`~/.hermes/skills/sigil-forge`. Skill name: `sigil-forge`.

## Two layers

| Layer | Owns | Does **not** own |
|-------|------|------------------|
| **Agent contract** (`SKILL.md`, `references/`) | Intake, wizard interview, mode, safety judgment, packet narrative, when to invoke scripts / host image tools | Inventing glyph geometry or fake stego success |
| **Construction engine** (`scripts/`) | Normalize, digest, optional encrypt, Spare, kamea, fusion, SVG/PNG, stego, wallpaper composite, verify | Mystical guarantees, external image APIs, mutating skill `references/` |

## Skill root resolution

1. `HERMES_SKILL_DIR` if set  
2. Else install/clone directory containing this skill  

Default out: `out/sigil-forge/<run-id>/` or `--out`.  
Wizard sessions: `out/wizard-sessions/<id>.json`.  
`run-id` = timestamp + short digest prefix.

## Artifact rule

- Write under user-chosen directory or skill `out/`.  
- **Never mutate `references/`** during ordinary runs.  
- Prefer hash-based run paths so listings do not leak full intent text.

## CLI surface

| Command | Role |
|---------|------|
| `wizard` | Guided interview: `--script`, `--next`, `--session-new`, `--apply` |
| `construct` | Full forge (expert / non-wizard) |
| `verify` | Recover digest / integrity from SVG or PNG |
| `wallpaper` | Device composites from a forge run |
| `open` | Decrypt sealed packet intent |
| `learn` / `ledger` | PROPOSED learning observations |
| `doctor` / `eval` / `check` | Health and offline evals |
| `help` | Command overview |

Entry: `python3 scripts/sigil_forge.py …`

## Wizard (Hermes default for new users)

1. Prefer `wizard --path quick` + **`--next` step runner** (one question per turn).  
2. Load `references/wizard.md` only when guiding (progressive disclosure).  
3. On `done`, `wizard --apply` then `verify`.  
4. Expert operators may skip to `construct`.

See `references/wizard.md`.

## Schemas

Under `schemas/` (validate when `jsonschema` available; structural checks always):

- `forge-packet.schema.json`  
- `channel-manifest.schema.json`  
- `construction-result.schema.json`  
- `wallpaper-spec.schema.json` / `wallpaper-receipt.schema.json`  

## Agent obligations

1. Safety before construct; refuse with no artifacts.  
2. Follow wizard step runner when guiding; one question per turn.  
3. Point to `references/` for method depth; do not invent cipher tables.  
4. Report channels honestly (`applied` / `skipped`).  
5. Never claim efficacy or stego success without verify.  
6. Standalone: no hard dependency on Kubrick, Orchestra, or ComfyUI.  
7. Wallpapers: atmosphere only — never AI-redraw canonical glyph.

## Host tools

- Image polish / wallpaper AI background is **optional** and post-master only.  
- Offline success is first-class: procedural glyph + packet without any image API.

## Progressive disclosure

Keep agent context lean:

1. Skill index (name/description) at session start  
2. `SKILL.md` when skill triggers  
3. `references/wizard.md` when guiding  
4. Method refs only when explaining that channel  

## Related

- Expansion: `expansion-spine.md`  
- Safety: `safety-and-framing.md`  
- Design: `docs/superpowers/specs/2026-08-07-sigil-forge-design.md`
