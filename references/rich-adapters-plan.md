# Rich Orchestra/Kubrick/ComfyUI Adapters (Planned)

From expansion-spine: remaining optional later.

## Status
Not implemented in v0.13.0. Current has thin --interop fields only.

## Plan Outline
- Provide richer integration points for external tools (Orchestra, Kubrick, ComfyUI workflows).
- Expose more hooks: custom prompt packages, geometry export formats, receipt extensions.
- Keep core offline; adapters are opt-in thin layers or templates.
- Support for host AI backgrounds already partial; extend to full pipelines.
- No cloud image APIs in core.

## References
- references/wallpaper-prompt-contract.md
- references/wallpaper-framework.md
- scripts/wallpaper/
- --interop flag in construct/wizard

To implement: new references/adapters/ or scripts/adapters/ with example configs.
