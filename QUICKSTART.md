# Sigil-Forge quickstart

Five commands from zero to a verified glyph (run from the skill root — clone or install dir).

```bash
# 1. Smoke-check the skill tree
python3 scripts/sigil_forge.py check

# 2. Construct a creative forge packet + master glyph
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --out out/sigil-forge

# 3. Verify SVG stego recovers the intent digest
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.svg

# 4. (Optional) Practice mode + local passphrase seal (prefer env over --passphrase)
export SIGIL_FORGE_PASSPHRASE='operator-secret'
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --mode practice \
  --seal-packet \
  --out out/sigil-forge

# 5. (Dev) Run the test suite
python3 -m pytest -v
```

**Install to Hermes** (optional):

```bash
bash install.sh --dry-run    # preview
bash install.sh              # → ~/.hermes/skills/sigil-forge
```

See [README.md](README.md) for overview and [SKILL.md](SKILL.md) for the Hermes agent contract.
