#!/usr/bin/env python3
"""
Optional Bundled ComfyUI Workflow Templates (Planned / Skeleton)

Local ComfyUI templates for backgrounds/atmospheres.
No execution, no cloud in core. User runs locally.

From references/comfyui-plan.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


TEMPLATES = {
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
}


def list_templates() -> list[str]:
    """List available optional templates."""
    return list(TEMPLATES.keys())


def load_template(name: str) -> dict[str, Any]:
    """Load a template (stub)."""
    if name not in TEMPLATES:
        raise ValueError(f"Unknown template: {name}")
    return {"template": name, **TEMPLATES[name]}


def render_template_for_wallpaper(template: dict[str, Any], glyph_hash: str) -> dict[str, Any]:
    """Render template bound to glyph (stub, no execution)."""
    return {
        "template": template["name"],
        "glyph_hash": glyph_hash[:16],
        "prompt_hint": "bind to immutable sigil",
        "workflow": template.get("workflow"),
        "note": "Run in local ComfyUI; output not embedded by core",
    }


if __name__ == "__main__":
    print("comfyui_templates skeleton — optional local workflows only")
    print("available:", list_templates())
    t = load_template("minimal_background")
    print("loaded:", t["name"])
