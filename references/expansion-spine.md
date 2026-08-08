# Expansion spine

Version: **v1 documented targets** (not required for v1 completeness).

Sigil-Forge ships as a **lean Hermes skill** with schemas and a thin CLI so growth
does not require a rewrite. Implement these only after the v1 forge loop is solid.

## Packaging principle

| Now (v1) | Later |
|----------|--------|
| Lean skill tree under install dir | Same root; additive modules |
| `construct` / `verify` / `check` | `forge`, `doctor`, `eval`, `receipt` jobs |
| Fixed channel set | Additional craft channels with new IDs |
| Empty-ok `interop` | Richer handoff fields |

## Planned extension points

### CLI

- Full job surface: `do forge|doctor|eval|receipt` (names indicative).  
- `doctor`: environment, raster backends, schema presence.  
- `eval`: lightweight agent evals (refuse-harmful, mode tone, offline success).

### Receipts and learning

- Append-only **run receipts** beyond the forge packet.  
- Optional **learning ledger**: method preference observations, **proposal-only** —
  never auto-promote to canon without the human.

### Crypto upgrades

- Stronger KDF (e.g. **Argon2id**) for passphrase sealing.  
- Keep algorithm identifiers versioned in packet `crypto` fields.

### Craft channels

- **Shipped (v0.3):** `bind_runes`, `rose_cross_path` (see methods-*.md).  
- Later: multi-frame carriers, additional historical alphabets.  
- Each new channel: stable `id`, applied/skipped reporting, privacy review.
  Do **not** silently repurpose Enochian seal semantics.

### Receipts and learning (shipped v0.3)

- Run receipts: `run-receipt.json` + append-only `run-receipts.jsonl`.  
- Learning ledger: `learn` / `ledger` CLI — **PROPOSED only**, never auto-canon.

### Interop

- Optional Orchestra dual-naming export (`intent_token` / `sigil_glyph`) without
  collapsing Enochian authority seals into Spare intent glyphs.  
- Provider prompt adapters (Kubrick-style) and ComfyUI workflow export when present.  
- Fields remain optional and empty-ok for standalone use.

### AI polish

- Geometry-locked prompt builder (`prompt_polish` / Task 14 direction).  
- Seed from digest; negative prompts forbid readable text that breaks privacy.  
- Re-stego or presentation-only policy when raster verify would fail.

## Compatibility rules

1. **Do not break** forge-packet required keys without a `schema_version` bump.  
2. New channels append; old verifiers ignore unknown IDs gracefully or report unknown.  
3. Keep offline path working without new optional dependencies.  
4. Still never mutate `references/` at run time.

## Explicit non-goals (still)

- Required multi-provider adapter matrix on day one.  
- Full ritual liturgy or results-magic outcome engine.  
- Unlimited channel sprawl per single run.

## Related

- Runtime: `hermes-runtime-contract.md`  
- Design §14: `docs/superpowers/specs/2026-08-07-sigil-forge-design.md`
