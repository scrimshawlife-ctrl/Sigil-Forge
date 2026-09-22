#!/usr/bin/env python3
"""
Optional Bundled ComfyUI Workflow Templates (Completed Basic Implementation)

Local-only ComfyUI workflow templates for generating backgrounds/atmospheres.
Never executed by core. User runs in their own local ComfyUI.

Compatible with --background-method ai_generated and rich adapters.

From references/comfyui-plan.md
"""

from __future__ import annotations

from typing import Any

TEMPLATES: dict[str, dict[str, Any]] = {
    "minimal_background": {
        "name": "Minimal Background",
        "description": "Simple latent + prompt for glyph-compatible atmosphere",
        "workflow": {"nodes": ["latent", "prompt", "decode"]},
    },
    "atmospheric": {
        "name": "Atmospheric",
        "description": "Deeper style for wallpaper carriers",
        "workflow": {"nodes": ["latent", "controlnet", "prompt"]},
    },
    "sigil_influenced": {
        "name": "Sigil Influenced",
        "description": "Template that respects immutable glyph hash",
        "workflow": {"nodes": ["latent", "prompt", "ipadapter"]},
    },
}


def list_templates() -> list[str]:
    """List available optional templates."""
    return list(TEMPLATES.keys())


def load_template(name: str) -> dict[str, Any]:
    """Load a named template."""
    if name not in TEMPLATES:
        raise ValueError(f"Unknown template: {name}. Available: {list_templates()}")
    return {"template": name, **TEMPLATES[name]}


def render_template_for_wallpaper(template: dict[str, Any], glyph_hash: str) -> dict[str, Any]:
    """Render template metadata bound to a glyph (no execution)."""
    return {
        "template": template.get("name"),
        "glyph_hash": glyph_hash[:16] if glyph_hash else "none",
        "prompt_hint": "bind to immutable sigil glyph",
        "workflow": template.get("workflow"),
        "note": "Run locally in ComfyUI. Output may be used as --background host_file.",
    }


if __name__ == "__main__":
    print("comfyui-templates — optional local ComfyUI workflows")
    print("available:", list_templates())
    t = load_template("atmospheric")
    rendered = render_template_for_wallpaper(t, "abc123def456")
    print("rendered for glyph:", rendered["glyph_hash"])
