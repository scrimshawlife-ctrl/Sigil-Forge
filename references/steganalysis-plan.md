# Steganalysis Shipped (v0.14.0 + deeper)


From expansion-spine: completed in v0.14.0 + deeper wizard integration.

## Status
Shipped in v0.14.0 with wizard post-apply execution. Channel analysis, geometric correlation, capacity estimation with light integration to stego modules.

Module: scripts/steganalysis.py (analyze_channels, geometric_correlation, estimate_capacity, generate_report)

## Plan Outline
- Add tools for deeper analysis of embedded channels.
- Support for multi-channel correlation, capacity estimation, attack simulation (offline).
- Integrate with inspect/verify commands.
- Output: steganalysis reports bound to runs.
- Maintain privacy: no plaintext leaks.
- Geometric analysis: path density, channel capacity, correlation between SVG/PNG/embedded.
