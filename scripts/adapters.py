#!/usr/bin/env python3
"""
Rich Adapters (Completed Basic Implementation)

Opt-in adapters for external tools: Orchestra, Kubrick, ComfyUI, etc.
Exports geometry/prompts/receipts in compatible formats.
Core remains offline; adapters are thin data transformers.

From references/rich-adapters-plan.md
"""

from __future__ import annotations

from typing import Any

ADAPTERS: dict[str, dict[str, Any]] = {
    "orchestra": {"name": "Orchestra", "formats": ["prompt", "geometry"]},
    "kubrick": {"name": "Kubrick", "formats": ["receipt", "geometry"]},
    "comfyui": {"name": "ComfyUI", "formats": ["prompt", "template"]},
}


def list_adapters() -> list[str]:
    """List supported adapter names."""
    return list(ADAPTERS.keys())


def load_adapter_config(name: str) -> dict[str, Any]:
    """Load adapter configuration."""
    if name not in ADAPTERS:
        raise ValueError(f"Unknown adapter: {name}. Available: {list_adapters()}")
    return {"adapter": name, **ADAPTERS[name], "enabled": True}


def export_geometry_for_adapter(sigil: dict[str, Any], adapter: str = "comfyui") -> dict[str, Any]:
    """Export sigil geometry for the target adapter."""
    cfg = load_adapter_config(adapter)
    return {
        "adapter": adapter,
        "sigil_root": sigil.get("sigil_root"),
        "geometry": sigil.get("geometry", sigil.get("channels", {})),
        "supported_formats": cfg["formats"],
        "exported": True,
    }


def render_adapter_prompt(intent: str, adapter: str = "orchestra") -> str:
    """Render a prompt suitable for the external adapter."""
    cfg = load_adapter_config(adapter)
    return f"[{cfg['name']}] {intent}\n\n[geometry and channels ready for export]"


def bind_receipt_to_adapter(receipt: dict[str, Any], adapter_data: dict[str, Any]) -> dict[str, Any]:
    """Bind a forge receipt to adapter output data."""
    return {
        "receipt": receipt,
        "adapter": adapter_data.get("adapter"),
        "bound": True,
        "notes": "adapter binding (basic)",
    }


if __name__ == "__main__":
    print("adapters — rich interop for Orchestra/Kubrick/ComfyUI")
    print("available:", list_adapters())
    g = export_geometry_for_adapter({"sigil_root": "demo123"}, "comfyui")
    print("exported for", g["adapter"])
