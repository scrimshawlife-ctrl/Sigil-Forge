# Wallpaper background prompt contract

## Principle

> Generate the environment, not the canonical glyph.

The model (or procedural engine) creates atmosphere. Sigil Forge places the
vector sigil deterministically.

## Universal negative fragment

```text
text, typography, letters, writing, numbers, watermark, logo, rune, runes,
sigil, occult symbol, magic circle, pentagram, glyph, pseudo-text,
calligraphy, diagram, UI, app icons
```

## Provider abstraction

```text
BACKGROUND.PROVIDER
├── procedural          # offline default
├── ai_generated        # host supplies image from prompt package
├── operator_supplied   # --background path
└── comfyui / local_diffusion  # future
```

Prompts are always written to `wallpaper/background-prompt-<surface>.json`
for provenance even when using procedural stand-ins.
