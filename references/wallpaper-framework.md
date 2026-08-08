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

# 2) wallpapers from run
python3 scripts/sigil_forge.py wallpaper \
  --run out/sf/<run-id> \
  --surface phone_lock \
  --mode focus \
  --intensity balanced \
  --theme mercurial \
  --style "dark architectural minimalism"
```

Outputs under `run/wallpaper/` and `run/receipts/`.

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
Procedural backgrounds ship offline; AI/operator backgrounds are optional inputs.

## Schemas

- `schemas/wallpaper-spec.schema.json`
- `schemas/wallpaper-receipt.schema.json`
