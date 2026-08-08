# Wallpaper framework

**Product thesis (v0.13+):** the **wallpaper PNG is the end deliverable**.  
Corpus methods (Spare, kamea, Rose Cross, bind-runes, planetary plates) still
build the **immutable glyph**. Intent, method provenance, digests, and related
forge surfaces are **layered and encrypted into the image** (SF12 LSB vault).

Sidecar files under a forge run (`forge-packet.json`, capsule, manifests) remain
useful for operators and agents — they are **workspace**, not the handoff object.

```text
INTENT
  → corpus methods → CANONICAL GLYPH (immutable geometry)
  → presentation (surface / atmosphere)
  → COMPOSITE WALLPAPER
  → SF12 stego vault (encrypted intent + methods + digests)
  → DELIVERABLE
```

## Contract

1. Canonical glyph geometry is immutable (scale/place/opacity only on composite).  
2. Methods respect method corpus / ontology — no invented stroke tables.  
3. **Public** wallpaper may carry digests/`sigil_root` only.  
4. **Private** payload (intent, methods, channels, commitments) lives in the
   sealed vault — requires passphrase.  
5. Plaintext intent must not appear in visible pixels or public JSON by default.  
6. AI atmosphere may change background only — never redraw glyph topology.  
7. Every wallpaper records provenance (receipt + optional public digests).

## SF12 product envelope

| Layer | Content |
|-------|---------|
| Visible | Glyph composite on atmosphere (phone/desktop) |
| Public stego | `intent_digest` + `sigil_root` (verify without passphrase) |
| Private vault | AES-GCM sealed JSON: intent, normalized intent, methods, channels, ontology, commitment surfaces, wallpaper presentation summary |

```bash
export SIGIL_FORGE_PASSPHRASE='…'

# One-shot product path
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --wallpaper --surface phone_lock \
  --embed vault \
  --out out/sigil-forge

# Open the deliverable (not the packet)
python3 scripts/sigil_forge.py open --wallpaper \
  out/sigil-forge/*/wallpaper/phone-lock.png --json
```

`--embed auto` (default): **vault** when passphrase present, else public **sf11**.

## Pipeline

```bash
# 1) forge master (geometry + packet workspace)
python3 scripts/sigil_forge.py construct --intent "…" --out out/sf

# 2) product wallpapers from run
python3 scripts/sigil_forge.py wallpaper \
  --run out/sf/<run-id> \
  --surface phone_lock \
  --mode focus \
  --theme mercurial \
  --embed vault

# Host AI atmosphere (optional)
python3 scripts/sigil_forge.py wallpaper \
  --run out/sf/<run-id> --surface phone_lock \
  --background-method ai_generated \
  --background /path/to/ai-bg.png \
  --provider host_file --embed vault
```

Outputs under `run/wallpaper/` and `run/receipts/`.  
See [wallpaper-prompt-contract.md](wallpaper-prompt-contract.md) for host AI.

## Orthogonal dimensions

| Axis | Values |
|------|--------|
| surface | phone_lock, phone_home, tablet, desktop, desktop_ultrawide |
| mode | stealth, ambient, focus, ritual, immersive |
| placement | center, upper_third, lower_third, left_field, right_field, custom |
| intensity | subtle, balanced, strong |
| symbolic_theme | neutral, saturnine…lunar, custom |
| embed | auto, vault, sf11, intent_digest, channel_digest, none |

## Geometry rules

**Allowed:** scale, translate, rotate, opacity, glow, colorization.  
**Forbidden:** add/remove strokes, move internal vertices, AI redraw of glyph.

Background generation uses prompts that **explicitly forbid inventing the sigil**.
Procedural backgrounds ship offline; operator PNG and host AI are optional.

## Schemas

- `schemas/wallpaper-spec.schema.json`
- `schemas/wallpaper-receipt.schema.json`

## Related

- PoI: `proof-of-intent.md`  
- Channels: `channels-and-steganography.md`  
- Methods: `methods-spare.md`, `methods-kamea.md`, …
