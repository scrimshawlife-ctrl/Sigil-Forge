# Rich Orchestra/Kubrick/ComfyUI Adapters (Planned)

From expansion-spine: remaining optional later.

## Status
Not implemented in v0.13.0. Current has thin --interop fields only.

Basic skeleton added: scripts/adapters.py (rich adapter hooks + template loaders).

## Plan Outline
- Provide richer integration points for external tools (Orchestra, Kubrick, ComfyUI workflows).
- Expose more hooks: custom prompt packages, geometry export formats, receipt extensions.
- Keep core offline; adapters are opt-in thin layers or templates.
- Support for host AI backgrounds already partial; extend to full pipelines.
- No cloud image APIs in core.
- Examples for prompt exchange, geometry export (SVG/JSON), receipt binding.

## Skeleton Functions (in scripts/adapters.py)
- load_adapter_config(name: str) -> dict
- export_geometry_for_adapter(sigil: dict, adapter: str) -> dict
- render_adapter_prompt(intent: str, adapter: str) -> str
- bind_receipt_to_adapter(receipt: dict, adapter_data: dict) -> dict

## References
- references/wallpaper-prompt-contract.md
- references/wallpaper-framework.md
- scripts/wallpaper/
- --interop flag in construct/wizard
- references/hermes-runtime-contract.md

To implement: new references/adapters/ or extend scripts/adapters.py with example configs. Wire via wizard interop.

See also graphify/graft for integration points.
