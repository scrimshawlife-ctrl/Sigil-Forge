# Sigil-Forge Release Notes & Upgrades

**Current: v0.13.0** (standalone engine, offline-first wallpaper product)

Analysis performed via clone, graft, graphify, full test runs, E2E verification, code reads, and gh.

## v0.13.0 Completion Status (Shipped)
- All features from README table and expansion-spine.md delivered and verified:
  - Wizard step runner (quick/full paths, --next, sessions, PoI proof/kdf)
  - Craft methods: Spare, kamea (encodings), Rose Cross, bind-runes, planetary (plate corpus)
  - Stego: SVG + PNG LSB (SF11 dual verify, SF12 vault)
  - Wallpaper product: immutable glyph composite + sealed vault (intent+methods in PNG)
  - PoI: commitment, sigil_root, capsule, local_capsule verify-proof (zk optional graceful)
  - Ops, policy/safety (hard refusals), ledger (PROPOSED only), schemas, hermes SKILL.md contract
- Verification:
  - 234/234 tests passed
  - `check` + `doctor` + `validate_hermes_skill.py` → all green
  - E2E: construct (with --proof commitment --wallpaper) + verify + open --wallpaper + verify-proof → all ok, geometry_preserved, vault embedded, verified
- Architecture (graphify + graft):
  - 131 code files, ~1912 nodes / 3090 edges (graphify)
  - 104 files / 739 nodes / 2035 edges (graft)
  - God nodes: run(), build_wallpaper(), normalize_intent(), next_step(), build_layout(), embed(), check_intent(), cmd_wizard()
  - Clean boundaries: forge_core.py (pure deterministic), wallpaper/pipeline.py orchestrator, stego_png.py (pure LSB), safety.py (heuristic gates)
- Packaging: agent-agnostic (recent), lean install, standalone + Hermes opt-in

No critical bugs found. Minor hygiene only (intentional path bootstrap in sigil_forge.py for bare imports).

## v0.14 Planned / Upgrades (from expansion-spine + analysis)
**From expansion-spine "Remaining":**
- Scanned unique MS plate import pipeline (current: scholarly vectorization)
- Multi-frame storyboard carriers
- Richer adapters (Orchestra / Kubrick / ComfyUI beyond thin --interop fields)
- Deeper geometric multi-channel steganalysis
- Optional bundled ComfyUI workflow templates (keep no cloud APIs)

**Explicit non-goals (preserve):**
- Goetic/Enochian/authority seals in default forge
- Efficacy claims
- Auto-canon promotion
- Cloud image APIs

**From this analysis (high priority):**
- CI/CD: `.github/workflows/ci.yml` added (pytest matrix, check/doctor/validate, E2E smoke, policy). PR opened.
- GitHub Releases automation on tags
- Import robustness polish (optional)
- More test coverage for host-AI wallpaper, full PoI flows
- Periodic graft build + graphify --code-only in dev
- Update source-manifest.yaml and references/ on new methods

## Recent Changes (post v0.13)
- PRs: #25 agent-agnostic standalone, #24 install safety, #23 wallpaper product
- Graph + graft artifacts generated during analysis (local, git-ignored where appropriate)

## Verification Checklist (from SKILL.md)
All items from the contract's Verification Checklist passed in analysis runs.

## How to Verify This Release
```bash
python3 scripts/sigil_forge.py check
python3 scripts/sigil_forge.py doctor
python3 -m pytest tests/ -q
# E2E example (see full analysis)
export SIGIL_FORGE_PASSPHRASE=...
python3 scripts/sigil_forge.py construct --intent "..." --proof commitment --wallpaper ...
```

**Full analysis artifacts:** graft/, graphify-out/ (regenerable), local clone reports.

See:
- references/expansion-spine.md
- SKILL.md
- references/source-and-upgrades.md
- docs/ (GitHub Pages landing)

MIT. Offline-first. Proposal-only.

---
*Draft generated during autonomous continuation of analysis on 2026-09-22. Update on next release.*

## Post-PR Verification (autonomous continuation)
- Full test suite: 234/234 passed (after unsetting SIGIL_FORGE_PASSPHRASE; prior flakes were env-only).
- PR #26 force-updated to clean diff (only 138 additions: CI, RELEASE_NOTES, .gitignore).
- Comment posted on PR with status.
- Local graft/graphify artifacts cleaned (regenerable via `graft build` / `graphify . --code-only`).

**PR**: https://github.com/scrimshawlife-ctrl/Sigil-Forge/pull/26


## Release
- GitHub release created for v0.13.0: https://github.com/scrimshawlife-ctrl/Sigil-Forge/releases/tag/v0.13.0
- Tag v0.13.0 points to wallpaper merge; CI/docs added on top.
