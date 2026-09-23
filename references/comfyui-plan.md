# Comfyui Shipped (v0.14.0 + deeper)


From expansion-spine: completed in v0.14.0 + deeper wizard integration.

## Status
Shipped in v0.14.0 with wizard post-apply execution. Local-only template registry and renderer. Example workflow in docs/comfyui/.

Module: scripts/comfyui_templates.py (list_templates, load_template, render_template_for_wallpaper) + docs/comfyui/example_background.json

## Plan Outline
- Provide optional templates for ComfyUI (local) to generate backgrounds/atmospheres.
- Templates that respect immutable glyph, bind to receipts.
- Keep as docs/examples only; no execution in core.
- Compatible with --background-method ai_generated.
- Respect offline-first: user runs ComfyUI locally.
