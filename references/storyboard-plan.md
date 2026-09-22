# Multi-frame Storyboard Carriers (Planned)

From expansion-spine: remaining optional later.

## Status
Not implemented in v0.13.0. Current is single image (glyph + wallpaper).

## Plan Outline
- Support multi-frame sequences for storyboards or animations.
- Extend channels to include frame sequences or time-based.
- Output formats: animated SVG, GIF, or multi-PNG with manifest.
- Bind to sigil_root and intent.
- Optional with --multi-frame or in wizard.
- Keep offline, no cloud.

## References
- references/wallpaper-framework.md
- references/channels-and-steganography.md
- scripts/wallpaper/

To implement: new scripts/storyboard.py or extend wallpaper/pipeline.py.
