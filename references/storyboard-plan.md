# Storyboard Shipped (v0.14.0 + deeper)


From expansion-spine: completed in v0.14.0 + deeper wizard integration.

## Status
Shipped in v0.14.0 with wizard post-apply execution. Multi-frame storyboard builder that produces indexed JSON carriers.

Module: scripts/storyboard.py (create_storyboard, add_frame)

## Plan
- Multi-frame carriers for sequential intent (storyboard as sequence of sigils/glyphs).
- Output: animated SVG/PNG or multi-page PDF-like in vault.
- Bind to sigil_root + frame index.
- Reuse core forge for each frame.
- Offline, no cloud.
