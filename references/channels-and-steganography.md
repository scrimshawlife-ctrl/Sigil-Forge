# Channels and steganography (v1)

Version: **v1** channel set (fixed; unbounded research per run is a non-goal).

Every successful forge **attempts all channels** below. Each is recorded in the
forge packet as:

```json
{ "id": "<channel_id>", "status": "applied" | "skipped", "detail": "..." }
```

Order in `scripts/construct.py` (`_CHANNEL_ORDER`):

1. `spare_monogram`  
2. `kamea_path`  
3. `kamea_square_choice`  
4. `intent_digest`  
5. `optional_ciphertext`  
6. `svg_metadata`  
7. `path_epsilon`  
8. `path_order`  
9. `metric_quantize`  
10. `png_lsb`  
11. `gen_seed`  

## A. Ancient / classical craft (visible structure)

| ID | Description | Skip reasons (examples) |
|----|-------------|-------------------------|
| `spare_monogram` | Reduced unique consonants → circular monogram polyline | `no_letters_after_reduction` |
| `kamea_path` | Letter→number path on selected kamea | `no_path_points` |
| `kamea_square_choice` | Planet/size: operator `--square` or digest mod 7 | Always applied when construct runs |

## B. Modern cryptographic / digital craft

| ID | Description | Skip reasons |
|----|-------------|--------------|
| `intent_digest` | SHA-256 hex of **normalized** intent | Always applied on success |
| `optional_ciphertext` | AES-256-GCM of full intent under passphrase (PBKDF2-HMAC-SHA256); stored in **local packet** as `sealed_intent` | `no_passphrase` |

**Privacy:** ciphertext is for the local forge packet. v1 public PNG LSB embeds a
**digest-only** payload — never partial ciphertext in the public raster.

## C. Steganography

Public-facing media carry digest / channel bits **without plaintext intent** by
default. Stego exists for operator sovereignty and multi-encoding — not covert harm.

| ID | Medium | What embeds | Notes |
|----|--------|-------------|-------|
| `svg_metadata` | SVG | Namespaced private metadata: receipt/digest/method bitmap | Not plaintext intent |
| `path_epsilon` | SVG geometry | ±EPS coordinate LSB-analogue from digest bits | Sub-visual; may skip if no floats |
| `path_order` | SVG structure | Construction-order / manifest binding (monogram group before kamea); order_token derived from digest | Not residual stroke-order encoding of spare letters |
| `metric_quantize` | SVG attrs | `data-sf-metric` digest nibble attributes on path groups (first 8 / next 8 hex) | Not free-form angle/length encoding |
| `png_lsb` | PNG | Digest-only LSB payload when raster exists | Skipped: `no_raster_backend`, raster/embed errors |
| `gen_seed` | (AI polish) | Seed derived from digest | v1 construct: `skipped(no_ai_polish)` until polish used |

Implementation: `scripts/stego_svg.py`, `scripts/stego_png.py`.

## Capacity and failure modes

| Condition | Behavior |
|-----------|----------|
| Stego capacity exceeded | Apply max channels that fit; mark remainder `skipped(capacity)` — **never claim full embed** |
| No path floats | `path_epsilon` skipped |
| No raster backend | `png_lsb` skipped; forge still succeeds with SVG |
| PNG filter types unsupported | `png_lsb` skipped (`embed_failed:…`); no fake non-glyph PNG |
| Verify mismatch | Report failure; do not claim forged integrity |
| Harmful intent | Refuse **before** any embed |

## Privacy defaults

| Asset | Default content |
|-------|-----------------|
| Public SVG / PNG | Digest, stego payload, channel bitmap — **no plaintext intent** |
| Local forge packet | Plaintext `normalized_intent` unless `--seal-packet` + passphrase |
| Run directory name | Timestamp + short digest prefix (not full intent string) |

Construct runs a privacy assert on public SVG (phrase/spare-run leak checks with
length thresholds to avoid false positives on short intents).

## Verify

```bash
python3 scripts/sigil_forge.py verify path/to/glyph.svg
python3 scripts/sigil_forge.py verify path/to/glyph.png   # when png_lsb applied
```

Extract digest / channels; compare to packet. Never report stego success on an
artifact that fails verify.

## Related

- Method params: `methods-spare.md`, `methods-kamea.md`  
- Crypto defaults: AES-GCM + PBKDF2-HMAC-SHA256 (stdlib-friendly); Argon2id is expansion  
- Design §5: `docs/superpowers/specs/2026-08-07-sigil-forge-design.md`
