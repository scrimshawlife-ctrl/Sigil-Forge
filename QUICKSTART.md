# Sigil-Forge quickstart

Five commands from zero to a verified glyph (run from the skill root — clone or install dir).

```bash
# 1. Smoke-check the skill tree
python3 scripts/sigil_forge.py check

# 2. Construct a creative forge packet + master glyph
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --out out/sigil-forge

# 3. Verify SVG + PNG stego recover the intent digest
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.svg
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.png

# 4. (Optional) Practice seal + open (prefer env over --passphrase)
export SIGIL_FORGE_PASSPHRASE='operator-secret'
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --mode practice \
  --seal-packet \
  --out out/sigil-forge
python3 scripts/sigil_forge.py open out/sigil-forge/*/forge-packet.json

# 5. (Dev) Tests + Hermes frontmatter hygiene
python3 -m pytest -v
python3 scripts/validate_hermes_skill.py
```

**Install to Hermes** (optional):

```bash
bash install.sh --dry-run    # preview
bash install.sh              # → ~/.hermes/skills/sigil-forge
```

See [README.md](README.md) for overview and [SKILL.md](SKILL.md) for the Hermes agent contract.
