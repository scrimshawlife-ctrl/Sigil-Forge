#!/usr/bin/env python3
"""
Rich Adapters (Planned / Skeleton)

Hooks for Orchestra, Kubrick, ComfyUI and similar external tools.
Opt-in, offline-first, no cloud execution in core.

From references/rich-adapters-plan.md
Current thin interop only via --interop.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


ADAPTERS = {
    "orchestra": {"name": "Orchestra", "formats": ["prompt", "geometry"]},
    "kubrick": {"name": "Kubrick", "formats": ["receipt", "geometry"]},
    "comfyui": {"name": "ComfyUI", "formats": ["prompt", "template"]},
}


def load_adapter_config(name: str) -> dict[str, Any]:
    """Load adapter config (stub)."""
    if name not in ADAPTERS:
        raise ValueError(f"Unknown adapter: {name}")
    return {"adapter": name, **ADAPTERS[name], "enabled": True}


def export_geometry_for_adapter(sigil: dict[str, Any], adapter: str = "comfyui") -> dict[str, Any]:
    """Export sigil geometry in adapter-friendly format (stub)."""
    cfg = load_adapter_config(adapter)
    return {
        "adapter": adapter,
        "sigil_root": sigil.get("sigil_root"),
        "geometry": sigil.get("geometry", {}),
        "supported_formats": cfg["formats"],
    }


def render_adapter_prompt(intent: str, adapter: str = "orchestra") -> str:
    """Render prompt for external adapter (stub)."""
    cfg = load_adapter_config(adapter)
    return f"[{cfg['name']}] Intent: {intent}\n\n[geometry export ready]"


def bind_receipt_to_adapter(receipt: dict[str, Any], adapter_data: dict[str, Any]) -> dict[str, Any]:
    """Bind forge receipt to adapter output (stub)."""
    return {
        "receipt": receipt,
        "adapter": adapter_data.get("adapter"),
        "bound": True,
        "notes": "planned extension",
    }


if __name__ == "__main__":
    print("adapters skeleton — rich interop for Orchestra/Kubrick/ComfyUI")
    cfg = load_adapter_config("comfyui")
    print("loaded:", cfg["name"])
