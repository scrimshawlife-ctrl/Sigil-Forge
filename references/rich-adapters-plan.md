# Rich Adapters Shipped (v0.14.0 + deeper)


From expansion-spine: completed in v0.14.0 + deeper wizard integration.

## Status
Shipped in v0.14.0 with wizard post-apply execution. Rich adapter data transformers for Orchestra/Kubrick/ComfyUI etc.

Module: scripts/adapters.py (list_adapters, load_adapter_config, export_geometry, render_prompt, bind_receipt)

## Plan Outline
- Provide richer integration points for external tools (Orchestra, Kubrick, ComfyUI workflows).
- Expose more hooks: custom prompt packages, geometry export formats, receipt extensions.
- Keep core offline; adapters are opt-in thin layers or templates.
- Support for host AI backgrounds already partial; extend to full pipelines.
- No cloud image APIs in core.
- Examples for prompt exchange, geometry export (SVG/JSON), receipt binding.
