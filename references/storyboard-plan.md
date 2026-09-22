# Multi-frame Storyboard Carriers (Planned)

From expansion-spine: remaining optional later.

## Status
Basic implementation completed (v0.14 prep). Multi-frame storyboard builder that produces indexed JSON carriers.

Module: scripts/storyboard.py (create_storyboard, add_frame)

## Plan
- Multi-frame carriers for sequential intent (storyboard as sequence of sigils/glyphs).
- Output: animated SVG/PNG or multi-page PDF-like in vault.
- Bind to sigil_root + frame index.
- Reuse core forge for each frame.
- Offline, no cloud.

## Next
- Add scripts/storyboard.py skeleton.
- Integrate via --storyboard or wizard.
- See references/wallpaper-framework.md for carrier ideas.

