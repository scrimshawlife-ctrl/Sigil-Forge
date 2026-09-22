# Deeper Geometric Multi-Channel Steganalysis (Planned)

From expansion-spine: remaining optional later.

## Status
Basic implementation completed (v0.14 prep). Channel analysis, geometric correlation, capacity estimation with light integration to stego modules.

Module: scripts/steganalysis.py (analyze_channels, geometric_correlation, estimate_capacity, generate_report)

## Plan Outline
- Add tools for deeper analysis of embedded channels.
- Support for multi-channel correlation, capacity estimation, attack simulation (offline).
- Integrate with inspect/verify commands.
- Output: steganalysis reports bound to runs.
- Maintain privacy: no plaintext leaks.
- Geometric analysis: path density, channel capacity, correlation between SVG/PNG/embedded.

## Skeleton Functions (in scripts/steganalysis.py)
- analyze_channels(artifact: dict) -> dict
- geometric_correlation(svg_data: str, png_data: bytes) -> dict
- estimate_capacity(channels: list) -> dict
- generate_report(analysis: dict, out_path: Path) -> Path

## References
- references/channels-and-steganography.md
- scripts/stego_*.py
- scripts/inspect_artifact.py
- scripts/verify.py
- scripts/stego_png.py

To implement: extend inspect/verify with --steganalysis flag; offline simulation only.

See also graphify/graft for channel usage stats.
