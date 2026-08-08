# Sigil-Forge quickstart

Run from the skill root (clone or install dir). **Current version: 0.12.5.**

Hermes packaging: this is a **skill** (`SKILL.md` + offline CLI), not a plugin.

```bash
# 1. Smoke-check the skill tree (files, modules, Hermes frontmatter, dry PoI construct)
python3 scripts/sigil_forge.py check
# Optional: python3 scripts/sigil_forge.py doctor

# 1b. Hermes wizard (step-by-step — preferred for new users)
# python3 scripts/sigil_forge.py wizard --session-new --path quick
# python3 scripts/sigil_forge.py wizard --next --session <id> --answers-json '{"intent":"…"}'
# python3 scripts/sigil_forge.py wizard --apply answers.json --path quick --out out/sigil-forge

# 2. Construct a creative forge packet + master glyph
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --out out/sigil-forge

# 3. Verify SVG + PNG stego recover the intent digest
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.svg
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.png

# 4. Compose device wallpapers (immutable glyph + atmosphere)
#    Replace <run-id> with the directory name under out/sigil-forge/
python3 scripts/sigil_forge.py wallpaper \
  --run out/sigil-forge/<run-id> \
  --surface phone_lock \
  --mode focus \
  --theme mercurial \
  --style "dark architectural minimalism"

# One-shot construct + wallpaper:
# python3 scripts/sigil_forge.py construct --intent "…" --out out/sigil-forge \
#   --wallpaper --surface phone_lock --wp-mode focus --theme mercurial

# Host AI background (after generating from wallpaper/background-prompt-*.json):
# python3 scripts/sigil_forge.py wallpaper --run out/sigil-forge/<run-id> \
#   --surface phone_lock --background-method ai_generated \
#   --background /path/to/ai-bg.png --provider host_file

# Or multi-surface defaults:
# python3 scripts/sigil_forge.py wallpaper --run out/sigil-forge/<run-id>

# 5. (Optional) Practice seal + open (prefer env over --passphrase)
export SIGIL_FORGE_PASSPHRASE='operator-secret'
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --mode practice \
  --seal-packet \
  --proof commitment \
  --out out/sigil-forge
python3 scripts/sigil_forge.py open out/sigil-forge/*/forge-packet.json
python3 scripts/sigil_forge.py open --capsule out/sigil-forge/*/intent-capsule.json --json
python3 scripts/sigil_forge.py inspect out/sigil-forge/*/glyph.svg
python3 scripts/sigil_forge.py verify-proof out/sigil-forge/*/ --passphrase "$SIGIL_FORGE_PASSPHRASE"

# 6. (Dev) Tests + Hermes frontmatter hygiene
python3 -m pytest -q
python3 scripts/validate_hermes_skill.py
```

**Install to Hermes** (skill tree under `~/.hermes/skills/sigil-forge`):

```bash
bash install.sh --dry-run    # preview
bash install.sh              # install + post-check (validate_hermes + check)
export HERMES_SKILL_DIR="$HOME/.hermes/skills/sigil-forge"
python3 "$HERMES_SKILL_DIR/scripts/sigil_forge.py" doctor
# Reload Hermes skills if the agent is already running
```

Wallpaper outputs live under `<run-id>/wallpaper/` and `<run-id>/receipts/`.
Canonical `glyph.svg` is never rewritten by wallpaper generation.

See [README.md](README.md), [SKILL.md](SKILL.md),
[references/hermes-runtime-contract.md](references/hermes-runtime-contract.md),
[references/proof-of-intent.md](references/proof-of-intent.md), and
[references/wallpaper-framework.md](references/wallpaper-framework.md).
