# Sigil-Forge

**Hermes skill** that turns a statement of intent into a **method-faithful, multi-channel sigil**: a procedural master glyph (SVG, optional PNG) fused from Spare-style letter reduction and classical kamea paths, plus a local forge packet with honest channel status and steganographic carriers.

Default framing is a **creative / focus tool** (clarify, compress, externalize). Optional **`practice`** mode uses practitioner-oriented language without efficacy claims. Construction is **offline-first** and **verifiable** — no image API required.

> Methods are craft history, symbolic compression, and data embedding — not proof of metaphysics. Never claims the sigil “works” or replaces professional help.

## Install

```bash
# Preview
bash install.sh --dry-run

# Default: ~/.hermes/skills/sigil-forge
bash install.sh

# Custom location
bash install.sh --target /path/to/skills/sigil-forge

# Version
bash install.sh --version
```

Requires **Python 3** (stdlib). Core path needs no pip packages. Optional: `jsonschema` for stricter packet validation.

From a clone without installing:

```bash
python3 scripts/sigil_forge.py check
```

## Construct (one example)

```bash
python3 scripts/sigil_forge.py construct \
  --intent "I maintain calm focus" \
  --mode creative \
  --out out/sigil-forge

# Verify public artifact recovers intent digest
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.svg
# Optional: python3 scripts/sigil_forge.py verify glyph.svg --expected-digest <64-hex>
```

**Warning:** `--passphrase` appears in the process list (`ps`/argv). Prefer:

```bash
export SIGIL_FORGE_PASSPHRASE='operator-secret'
python3 scripts/sigil_forge.py construct --intent "..." --seal-packet --out out/sigil-forge
```

Artifacts land under `out/sigil-forge/<run-id>/` (`glyph.svg`, `glyph.png`, `forge-packet.json`, `forge-packet.md`; optional `polish_prompt.json`). Run ids use timestamp + digest prefix so paths avoid full intent text.

```bash
# Geometry-locked polish package (no image API in this skill)
python3 scripts/sigil_forge.py construct --intent "..." --polish --out out/sigil-forge

# Open a sealed packet
export SIGIL_FORGE_PASSPHRASE='operator-secret'
python3 scripts/sigil_forge.py open out/sigil-forge/*/forge-packet.json
```

More detail: [QUICKSTART.md](QUICKSTART.md) · Hermes contract: [SKILL.md](SKILL.md)

## What you get

| Output | Role |
|--------|------|
| Master glyph (SVG/PNG) | Spare monogram + kamea + bind-runes + rose path; offline PNG |
| Forge packet | Channels, methods, digests, verify command |
| Run receipt | `run-receipt.json` + append-only receipt log (no plaintext required) |
| Stego carriers | SVG multi-channel + PNG LSB (digest-only on public PNG) |
| Optional polish_prompt.json | Geometry-locked host image prompt + `gen_seed` |
| Learning ledger | PROPOSED observations via `learn` / `ledger` (never auto-canon) |

Channel set and privacy rules: [references/channels-and-steganography.md](references/channels-and-steganography.md).

## Design

Full product design (goals, channels, packet shape, layout):

- [docs/superpowers/specs/2026-08-07-sigil-forge-design.md](docs/superpowers/specs/2026-08-07-sigil-forge-design.md)

Implementation plan: [docs/superpowers/plans/2026-08-07-sigil-forge.md](docs/superpowers/plans/2026-08-07-sigil-forge.md)

## License

MIT — see [LICENSE](LICENSE).
