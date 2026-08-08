# Wallpaper framework

The wallpaper subsystem treats the **canonical glyph as immutable** and the
wallpaper as an **environmental carrier**.

```text
INTENT → CANONICAL SIGIL → PRESENTATION SPEC → BACKGROUND → COMPOSITE → VERIFY
```

## Contract (six properties)

1. Canonical geometry is immutable.  
2. Every wallpaper is reproducible (deterministic seed from digest + config).  
3. Phone/desktop layouts are composition-aware (safe zones), not naive crops.  
4. Plaintext intent stays out of public wallpapers by default.  
5. AI polish may change atmosphere only — never sigil topology.  
6. Every artifact records provenance back to the forge packet.

## Pipeline

```bash
# 1) forge master
python3 scripts/sigil_forge.py construct --intent "…" --out out/sf

# 2) wallpapers from run (procedural offline)
python3 scripts/sigil_forge.py wallpaper \
  --run out/sf/<run-id> \
  --surface phone_lock \
  --mode focus \
  --intensity balanced \
  --theme mercurial \
  --style "dark architectural minimalism"

# One-shot construct + wallpaper
python3 scripts/sigil_forge.py construct \
  --intent "…" --out out/sf --wallpaper --surface phone_lock --wp-mode focus

# Host AI background (pre-rendered file)
python3 scripts/sigil_forge.py wallpaper \
  --run out/sf/<run-id> --surface phone_lock \
  --background-method ai_generated \
  --background /path/to/ai-bg.png \
  --provider host_file --model "local-sd"

# Host AI background (shell provider; optional)
# export SIGIL_FORGE_BG_COMMAND='my-gen --prompt {prompt_path} --out {out_path} ...'
python3 scripts/sigil_forge.py wallpaper \
  --run out/sf/<run-id> --surface phone_lock \
  --background-method ai_generated --require-ai
```

Outputs under `run/wallpaper/` and `run/receipts/`.
See [wallpaper-prompt-contract.md](wallpaper-prompt-contract.md) for host wiring.

## Orthogonal dimensions

| Axis | Values |
|------|--------|
| surface | phone_lock, phone_home, tablet, desktop, desktop_ultrawide |
| mode | stealth, ambient, focus, ritual, immersive |
| placement | center, upper_third, lower_third, left_field, right_field, custom |
| intensity | subtle, balanced, strong |
| symbolic_theme | neutral, saturnine…lunar, custom |

## Geometry rules

**Allowed:** scale, translate, rotate, opacity, glow, colorization.  
**Forbidden:** add/remove strokes, move internal vertices, AI redraw of glyph.

Background generation uses prompts that **explicitly forbid inventing the sigil**.
Procedural backgrounds ship offline; operator PNG and host AI (file or shell
command) are optional. The skill does not call cloud image APIs itself.

## Schemas

- `schemas/wallpaper-spec.schema.json`
- `schemas/wallpaper-receipt.schema.json`
