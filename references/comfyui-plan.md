# Optional Bundled ComfyUI Workflow Templates (Planned)

From expansion-spine: remaining optional later.

## Status
Basic implementation completed (v0.14 prep). Local-only template registry and renderer. Example workflow in docs/comfyui/.

Module: scripts/comfyui_templates.py (list_templates, load_template, render_template_for_wallpaper) + docs/comfyui/example_background.json

## Plan Outline
- Provide optional templates for ComfyUI (local) to generate backgrounds/atmospheres.
- Templates that respect immutable glyph, bind to receipts.
- Keep as docs/examples only; no execution in core.
- Compatible with --background-method ai_generated.
- Respect offline-first: user runs ComfyUI locally.

## Skeleton Functions (in scripts/comfyui_templates.py)
- list_templates() -> list[str]
- load_template(name: str) -> dict
- render_template_for_wallpaper(template: dict, glyph_hash: str) -> dict

## References
- references/wallpaper-prompt-contract.md
- references/wallpaper-framework.md
- scripts/wallpaper/providers.py
- --background-method

To implement: expand docs/comfyui/ with more JSON workflows; document local usage.

See also adapters plan for richer ComfyUI interop.
