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
BACKGROUND.METHOD
├── procedural          # offline default (pure Python atmosphere)
├── operator_supplied   # --background path
└── ai_generated        # host AI via file and/or shell command
    ├── host_file       # --background PATH (pre-rendered by any tool)
    ├── host_command    # --provider-command / SIGIL_FORGE_BG_COMMAND
    └── standin         # procedural fallback when host image missing
```

Prompts are always written to `wallpaper/background-prompt-<surface>.json`
for provenance (includes `prompt`, `negative`, `canvas`, `seed`, `output_hint`,
and `contract.forbid_glyph_invention`).

### Host command template

```bash
export SIGIL_FORGE_BG_COMMAND='my-gen --prompt {prompt_path} --out {out_path} --w {width} --h {height} --seed {seed}'
python3 scripts/sigil_forge.py wallpaper \
  --run out/sf/<run-id> \
  --surface phone_lock \
  --background-method ai_generated \
  --require-ai
```

Placeholders: `{prompt_path}`, `{out_path}`, `{width}`, `{height}`, `{seed}`, `{surface}`.

Two-phase (agent-friendly, no shell provider):

1. `wallpaper --background-method ai_generated` → prompt package + procedural stand-in  
2. Host generates PNG from the prompt package  
3. Re-run with `--background path/to/bg.png --background-method ai_generated`