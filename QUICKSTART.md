# Sigil-Forge quickstart

Run from the skill root (clone or install dir). **Current version: 0.7.0.**

```bash
# 1. Smoke-check the skill tree
python3 scripts/sigil_forge.py check
# Optional: python3 scripts/sigil_forge.py doctor

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
  --out out/sigil-forge
python3 scripts/sigil_forge.py open out/sigil-forge/*/forge-packet.json

# 6. (Dev) Tests + Hermes frontmatter hygiene
python3 -m pytest -q
python3 scripts/validate_hermes_skill.py
```

**Install to Hermes** (optional):

```bash
bash install.sh --dry-run    # preview
bash install.sh              # → ~/.hermes/skills/sigil-forge
```

Wallpaper outputs live under `<run-id>/wallpaper/` and `<run-id>/receipts/`.
Canonical `glyph.svg` is never rewritten by wallpaper generation.

See [README.md](README.md), [SKILL.md](SKILL.md), and
[references/wallpaper-framework.md](references/wallpaper-framework.md).
