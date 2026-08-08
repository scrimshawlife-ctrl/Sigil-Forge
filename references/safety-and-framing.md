# Safety and framing

Version: **v1**

## Core rules

1. **No supernatural efficacy claims** in creative or practice mode.  
2. Methods are craft history, symbolic compression, and data embedding — not
   proof of metaphysics.  
3. **Safety refusal runs before** normalize encode, stego, or packet write.  
4. Intent text is **sensitive**: hash in run paths; no telemetry; no default
   plaintext in public SVG/PNG.  
5. Steganography is for **operator sovereignty and multi-encoding**, not assisting
   covert harm.  
6. Distinguish **Chaos/Spare intent sigils** from **Enochian seals** (authority /
   placement). See `distinction-enochian.md`.

## Authority (Hermes)

- All creative outputs are **proposal-only**.  
- The skill may craft symbols, embed data, and write **local** artifacts.  
- The skill may **not** claim efficacy, contact third parties, spend money, or
  promote artifacts to “canon” without the human operator.

## Refusal categories (engine + agent)

`scripts/safety.py` uses multi-word heuristics (prefer false negatives over
blocking mundane phrases like “kill process”). The **agent** still applies
judgment for edge cases the keyword gate misses.

Refuse (do not soft-build a “safe” version of the harmful form):

| Category | Examples of spirit (not exhaustive) |
|----------|-------------------------------------|
| Violence against others | Murder, kill person, shoot/stab person, poison person |
| Self-harm | Kill myself, suicide plans, self-harm |
| Non-consensual control | Force/make someone love/obey; control mind/will |
| Child exploitation | Any sexual or abusive intent involving minors |

Also refuse or rewrite:

- Empty / pure-noise intent after normalize  
- Cultural or closed-practice material the operator forbids  

On refusal: explain briefly, invite a constructive rewrite, **write no forge
artifacts**.

## Framing language

| Allowed | Forbidden |
|---------|-----------|
| Compress, encode, externalize, craft, verify | Works, manifests, guarantees results |
| Historical method, symbolic carrier | Proves magic, contacts spirits |
| Optional personal practice notes | Obligatory ritual that causes outcomes |
| Multi-channel stego for integrity/privacy | Covert harm, surveillance abuse |

Packet always includes mode-appropriate `framing_notes` without efficacy claims
(`scripts/packet.py`).

## Privacy

| Asset | Default |
|-------|---------|
| Public SVG/PNG | Digest + stego bits; **no** plaintext intent |
| Forge packet | May include `normalized_intent` unless `--seal-packet` + passphrase |
| Run id | Timestamp + digest prefix |
| `references/` | Read-only during ordinary runs |

Debug modes that weaken privacy must be **explicit and labeled** (not default).

## Fail-closed construct errors

| Condition | Behavior |
|-----------|----------|
| Harmful intent | `ValueError` / refuse — no encode |
| Empty intent | Refuse; ask for clear present-tense statement |
| Invalid square | Error with allowed set; do not invent squares |
| Verify mismatch | Report failure; no integrity claim |
| Stego capacity | Skip remainder with reason; never claim full embed |

## Related

- Profiles: `profiles-creative.md`, `profiles-practice.md`  
- Channels: `channels-and-steganography.md`  
- Runtime: `hermes-runtime-contract.md`
