# Agent runtime contract

Version: **v4** (Sigil-Forge v0.13+ agent-agnostic)

Sigil-Forge is a **standalone construction engine** (CLI + `forge_core`), not a plugin.  
`SKILL.md` is an optional agent contract. Hermes may install a copy under
`~/.hermes/skills/sigil-forge`; that is **not** the product identity.

**Skill vs plugin vs engine:** The engine is `python3 scripts/sigil_forge.py`.
An agent contract teaches when/how to call it. A plugin would inject always-on
tools/hooks — not the product shape here.

## Two layers

| Layer | Owns | Does **not** own |
|-------|------|------------------|
| **Agent contract** (`SKILL.md`, `references/`) | Intake, wizard interview, mode, safety judgment, packet narrative, when to invoke scripts / host image tools | Inventing glyph geometry or fake stego success |
| **Construction engine** (`scripts/`) | Normalize, digest, optional encrypt, Spare, kamea, fusion, SVG/PNG, stego, wallpaper composite, verify, PoI surfaces | Mystical guarantees, external image APIs, mutating skill `references/` |

## Root resolution

1. `SIGIL_FORGE_HOME` / `SIGIL_FORGE_ROOT` / `SIGIL_FORGE_DIR` / `SIGIL_FORGE_SKILL_DIR`  
2. Else install/clone directory containing this tree  
3. `HERMES_SKILL_DIR` — last-compat only  

Default state: `$SIGIL_FORGE_STATE_DIR` or `~/.sigil-forge/state`.  
Products: `<state>/products/<run-id>/`.  
Wizard sessions: `<state>/wizard-sessions/<id>.json`.  
Legacy `~/.hermes/state/sigil-forge` is used only if that tree already exists
and the native state dir does not. Explicit `--out` always wins.

`run-id` = timestamp + short digest prefix.

## Artifact rule

- Write under the user-chosen directory or default state products directory.
- **Never mutate `references/`** during ordinary runs.  
- Prefer hash-based run paths so listings do not leak full intent text.

## CLI surface

| Command | Role |
|---------|------|
| `wizard` | Guided interview: `--script`, `--next`, `--session-new`, `--apply`; full path includes `proof`/`kdf` |
| `construct` | Full forge (expert / non-wizard); optional `--proof` / `--kdf` / `--seal-packet` |
| `verify` | Recover digest / integrity from SVG or PNG |
| `verify-proof` | Check local/Noir/risc0 proof manifests for a run |
| `inspect` | Public PoI/SF11 surfaces without disclosing intent |
| `wallpaper` | Device composites from a forge run |
| `open` | Decrypt sealed packet; `--capsule` for intent-capsule.json |
| `learn` / `ledger` | PROPOSED learning observations; human `ledger promote` only |
| `policy check` | Efficacy + authority-seal request lint (preflight) |
| `doctor` / `eval` / `check` | Health, packaging gates, offline evals |
| `help` | Command overview |

Entry: `python3 scripts/sigil_forge.py …`

## Install / packaging gates

```bash
bash install.sh --dry-run
bash install.sh                 # → ~/.sigil-forge
bash install.sh --hermes        # optional: ~/.hermes/skills/sigil-forge
export SIGIL_FORGE_HOME="$HOME/.sigil-forge"
python3 scripts/validate_hermes_skill.py   # optional agent-contract hygiene
python3 scripts/sigil_forge.py check       # files + modules + contract + dry construct/PoI
python3 scripts/sigil_forge.py doctor      # packaging: standalone-engine
```

Install excludes: `.git`, `out/`, `.venv`, caches, `.worktrees`, `docs/superpowers`.

## Wizard (default for new users / headless agents)

1. Prefer `wizard --path quick` + **`--next` step runner** (one question per turn).  
2. Load `references/wizard.md` only when guiding (progressive disclosure).  
3. On `done`, `wizard --apply` then `verify`.  
4. Expert operators may skip to `construct`.  
5. PoI depth: load `references/proof-of-intent.md` only when commitments/proofs are in play.  
6. Full-path wizard may set `proof` / `kdf`; apply returns capsule paths + next-hints when sealed.

See `references/wizard.md` · `references/proof-of-intent.md`.

## Schemas

Under `schemas/` (validate when `jsonschema` available; structural checks always):

- `forge-packet.schema.json`  
- `channel-manifest.schema.json`  
- `construction-result.schema.json`  
- `wallpaper-spec.schema.json` / `wallpaper-receipt.schema.json`  
- `intent-capsule.schema.json` / `artifact-root.schema.json` / `forge-manifest.schema.json`  
- `proof-manifest.schema.json`  

## Agent obligations

1. Safety before construct; refuse with no artifacts.  
2. Follow wizard step runner when guiding; one question per turn.  
3. Point to `references/` for method depth; do not invent cipher tables.  
4. Report channels honestly (`applied` / `skipped`).  
5. Never claim efficacy or stego success without verify.  
6. Standalone: no hard dependency on Hermes, Kubrick, Orchestra, ComfyUI, or Abraxas core.  
7. Wallpapers: atmosphere only — never AI-redraw canonical glyph.  
8. PoI: never put commitment nonce in public media; never claim ZK without dual pass.

Thin `--interop` may name Abraxas skills (`abx-esoteric-intelligence`, `abraxas-ingest`)
and `specialist_id=sigil-forge`; it does not import Abraxas or grant forecast/canon.

## Host tools

- Image polish / wallpaper AI background is **optional** and post-master only.  
- Offline success is first-class: procedural glyph + packet without any image API.  
- Optional Noir/risc0 tooling never required for construct/verify/open.

## Progressive disclosure

Keep agent context lean:

1. Skill index (name/description) at session start  
2. `SKILL.md` when the contract triggers  
3. `references/wizard.md` when guiding  
4. `references/proof-of-intent.md` when commitments / capsules / proofs arise  
5. Method refs only when explaining that channel  

## Related

- Expansion: `expansion-spine.md`  
- PoI: `proof-of-intent.md`  
- Safety: `safety-and-framing.md`  
- Design: `docs/superpowers/specs/2026-08-07-sigil-forge-design.md` (clone only; not installed)
