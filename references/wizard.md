# Forge wizard (Hermes)

Guided interview so operators never have to memorize CLI flags. The engine still
owns geometry; the agent/host owns conversation and safety judgment.

## Hermes agent flow

1. User asks to forge a sigil, is new, or says “wizard” / “guide me”.
2. Load steps:

   ```bash
   python3 scripts/sigil_forge.py wizard --script
   ```

3. Ask **one step at a time** (or batch if the user already answered).
4. When complete, write `answers.json` and apply:

   ```bash
   python3 scripts/sigil_forge.py wizard --apply answers.json --out out/sigil-forge
   ```

5. Verify:

   ```bash
   python3 scripts/sigil_forge.py verify <run>/glyph.svg
   ```

## Agent rules (also in script JSON)

- Safety before construct; refuse with no artifacts.
- Never invent monogram/kamea paths.
- No efficacy claims.
- Wallpapers do not AI-redraw the canonical glyph.

## Answers shape

Flat object keyed by step id. Defaults fill gaps.

```json
{
  "intent": "I maintain calm focus",
  "mode": "creative",
  "kamea_encoding": "hebrew_gematria",
  "square": "auto",
  "planetary_seal": "none",
  "spare_mode": "letter_monogram",
  "phonetic": false,
  "polish": false,
  "wallpaper": false,
  "seal_packet": false
}
```

`planetary_seal`: `none` | `traditional_seal` | `intelligence_character` | `spirit_character`

## Human TTY (optional)

```bash
python3 scripts/sigil_forge.py wizard --interactive --out out/sigil-forge
```

Prefer Hermes conversational flow for skill runs; interactive is for local CLI users.
