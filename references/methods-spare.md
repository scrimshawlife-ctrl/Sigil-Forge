# Methods: Spare-style monogram (v1)

Version: **v1** (locked for Sigil-Forge)

This document describes letter reduction and monogram geometry used by
`scripts/spare.py` and composed in `scripts/fuse.py`. Implementation is
deterministic; this file is doctrine and parameter reference.

## Tradition note

Austin Osman Spare’s chaos-magic lineage popularized collapsing a statement of
desire into a unique letter monogram so the conscious mind stops “reading” the
sentence. Sigil-Forge uses a **documented, code-defined reduction** inspired by
that craft for symbolic compression — **not** a claim of magical efficacy.

## Normalization prerequisite

Intent is first normalized (`scripts/normalize.py`):

1. Unicode NFKC  
2. Strip leading/trailing whitespace  
3. Lowercase  
4. Collapse internal whitespace to single spaces  

Empty after normalize → refuse (construction does not proceed).

## Reduction rule (v1)

From the normalized string:

1. Keep only Latin letters `a–z` (other characters ignored for Spare).  
2. **Strip vowels** including `y`: set `aeiouy`.  
3. **Collapse duplicates**: keep first occurrence only (order preserved).  

API:

- `letter_sequence(normalized) -> list[str]` — ordered unique consonants  
- `reduce_letters(normalized) -> str` — joined string of that sequence  

### Golden example

| Field | Value |
|-------|--------|
| Intent | `I maintain calm focus` |
| Normalized | `i maintain calm focus` |
| Spare letters | `mntclfs` |
| Sequence | `m n t c l f s` |

## Monogram geometry (fusion)

In `fuse.build_layout`:

- Unique letters are placed on a **circle** centered on the 100×100 canvas
  (`cx=50`, `cy=50`, radius `40`).
- Angles start at top (`-π/2`) and step equally around the circle.
- Points form an **open polyline** (not a closed ring) as the **primary
  silhouette**.
- Readable residual Latin letters are **not** drawn in the SVG body by default.

If reduction yields **no letters**, monogram points are empty and channel
`spare_monogram` is `skipped(no_letters_after_reduction)`. Construction may
still proceed via digest and kamea path.

## Channel reporting

| Channel ID | Applied when |
|------------|--------------|
| `spare_monogram` | At least one monogram point after reduction |

Packet `methods.spare`:

```json
{
  "reduction": "vowels_and_duplicate_collapse_v1",
  "letter_count": 7
}
```

## Fusion role

- Spare monogram = **outer / primary silhouette**.  
- Kamea path = **inner interwoven stroke** (see `methods-kamea.md`).  
- One master glyph; not disconnected doodles.

## Non-goals

- Freehand or LLM-invented monogram shapes  
- Binding runes or Rose Cross as Spare substitutes  
- Leaving plaintext intent or spare letter runs in public SVG  

## Related

- Engine: `scripts/spare.py`, `scripts/fuse.py`, `scripts/svg_export.py`  
- Example fixture: `examples/intents/calm_focus.json`  
- Safety / privacy: `safety-and-framing.md`, `channels-and-steganography.md`
