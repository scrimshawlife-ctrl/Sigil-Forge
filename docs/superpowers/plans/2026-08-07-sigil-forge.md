# Sigil-Forge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a standalone Hermes skill that forges multi-channel sigils (Spare + kamea fusion, steganography, forge packet, verify) offline-first with optional AI polish.

**Architecture:** Deterministic Python construction engine under `scripts/` plus Hermes agent contract in `SKILL.md` and `references/`. Agent handles intake, dual-mode framing, and safety; scripts own normalize → digest → fuse → stego → packet → verify. Hybrid packaging: lean install now, schemas/CLI spine ready to expand.

**Tech Stack:** Python 3.10+ stdlib only for core (hashlib, hmac, secrets, json, struct, xml.etree, unittest). Optional: `jsonschema` for full schema validation. No required image APIs. PNG stego uses pure-Python minimal PNG writer/reader or skip channel if raster unavailable.

**Spec:** `docs/superpowers/specs/2026-08-07-sigil-forge-design.md`

## Global Constraints

- Python 3.10+; core path must run with stdlib only
- Never write plaintext intent into public SVG/PNG by default
- Never mutate `references/` during ordinary runs; artifacts go to `out/` or `--out`
- Outputs are proposal-only; no efficacy claims
- Refuse harmful intents before any encode
- Channel set is the fixed v1 list; each channel is `applied` or `skipped(reason)`
- AI polish is optional and must not replace the procedural master as verify source of truth
- Skill name: `sigil-forge`; install default: `~/.hermes/skills/sigil-forge`
- Digest: SHA-256 hex lowercase; crypto: AES-GCM + PBKDF2-HMAC-SHA256 (stdlib)
- Distinguish Spare/kamea intent sigils from Enochian seals (do not implement Enochian)

---

## File Map

| Path | Responsibility |
|------|----------------|
| `scripts/paths.py` | Resolve skill root, out dirs, run ids |
| `scripts/normalize.py` | Intent normalization |
| `scripts/crypto_payload.py` | Digest + optional AES-GCM seal/open |
| `scripts/spare.py` | Letter reduction + monogram letter sequence |
| `scripts/kamea.py` | Squares, cipher, path points |
| `scripts/fuse.py` | Compose monogram + kamea into layout primitives |
| `scripts/svg_export.py` | Layout → SVG string/file |
| `scripts/stego_svg.py` | Metadata + path epsilon + order/metric embed/extract |
| `scripts/stego_png.py` | Optional PNG LSB embed/extract |
| `scripts/safety.py` | Harmful-intent heuristics (CLI + agent mirror) |
| `scripts/packet.py` | Build forge-packet JSON (+ optional MD summary) |
| `scripts/construct.py` | Full pipeline orchestration |
| `scripts/sigil_forge.py` | CLI: `construct`, `verify`, `check`, `help` |
| `schemas/*.json` | construction-result, forge-packet, channel-manifest |
| `tests/*.py` | Unit + integration + privacy |
| `examples/intents/*.json` | Golden fixtures |
| `references/*.md` | Method doctrine, profiles, safety, expansion |
| `SKILL.md` | Hermes contract |
| `install.sh`, `VERSION`, `README.md`, `QUICKSTART.md`, `.gitignore` | Packaging |

---

### Task 1: Scaffold + paths + CLI shell

**Files:**
- Create: `.gitignore`, `VERSION`, `scripts/paths.py`, `scripts/sigil_forge.py`, `tests/test_paths.py`, `tests/test_cli_help.py`
- Modify: (none required beyond new files)

**Interfaces:**
- Produces:
  - `paths.skill_root() -> Path`
  - `paths.default_out_dir() -> Path`
  - `paths.make_run_id(digest_hex: str, when: datetime | None = None) -> str`
  - `paths.run_dir(out_root: Path, run_id: str) -> Path`
  - CLI exits 0 on `help` and `check` (check may be partial until later tasks)

- [ ] **Step 1: Write failing tests for paths and CLI help**

```python
# tests/test_paths.py
from pathlib import Path
import scripts.paths as paths

def test_skill_root_contains_scripts():
    root = paths.skill_root()
    assert (root / "scripts").is_dir() or (root / "scripts" / "paths.py").exists() or root.name == "Sigil-Forge" or (root / "VERSION").exists() or True
    # After layout exists:
    assert (paths.skill_root() / "scripts" / "paths.py").is_file()

def test_make_run_id_uses_digest_prefix_not_full_intent():
    rid = paths.make_run_id("abcdef0123456789" * 4)
    assert "abcdef01" in rid
    assert " " not in rid
    assert len(rid) < 80

def test_run_dir_under_out():
    out = Path("/tmp/sf-out")
    d = paths.run_dir(out, "20260101T000000Z-abcdef01")
    assert d == out / "20260101T000000Z-abcdef01"
```

```python
# tests/test_cli_help.py
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_help_exits_zero():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sigil_forge.py"), "help"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0
    assert "construct" in r.stdout.lower() or "construct" in r.stderr.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /home/scrimshawlife/Sigil-Forge && python3 -m pytest tests/test_paths.py tests/test_cli_help.py -v`  
Expected: FAIL (module/file missing) or collection error

- [ ] **Step 3: Implement scaffold**

`.gitignore`:
```
out/
__pycache__/
*.pyc
.pytest_cache/
.venv/
*.egg-info/
```

`VERSION`:
```
0.1.0
```

`scripts/paths.py`:
```python
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import os


def skill_root() -> Path:
    env = os.environ.get("HERMES_SKILL_DIR")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent


def default_out_dir() -> Path:
    return skill_root() / "out" / "sigil-forge"


def make_run_id(digest_hex: str, when: datetime | None = None) -> str:
    ts = (when or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    prefix = (digest_hex or "0" * 8)[:8].lower()
    return f"{ts}-{prefix}"


def run_dir(out_root: Path, run_id: str) -> Path:
    return Path(out_root) / run_id
```

`scripts/sigil_forge.py`:
```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python scripts/sigil_forge.py` without install
sys.path.insert(0, str(Path(__file__).resolve().parent))


def cmd_help(_: argparse.Namespace) -> int:
    print(
        "sigil-forge — multi-channel intent sigils\n"
        "commands: construct | verify | check | help\n"
        "See SKILL.md and docs/superpowers/specs/2026-08-07-sigil-forge-design.md"
    )
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    from paths import skill_root

    root = skill_root()
    required = ["scripts/paths.py", "VERSION"]
    missing = [p for p in required if not (root / p).is_file()]
    ok = not missing
    print(json.dumps({"ok": ok, "root": str(root), "missing": missing}))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sigil-forge")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("help")
    sub.add_parser("check")
    # construct/verify registered in later tasks
    args = p.parse_args(argv)
    if args.cmd == "help":
        return cmd_help(args)
    if args.cmd == "check":
        return cmd_check(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

Ensure `tests/` can import: add empty `scripts/__init__.py` only if needed; prefer inserting `scripts/` on path in tests:

```python
# tests/conftest.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_paths.py tests/test_cli_help.py -v`  
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .gitignore VERSION scripts/paths.py scripts/sigil_forge.py tests/
git commit -m "chore: scaffold sigil-forge paths and CLI shell"
```

---

### Task 2: Normalize + digest

**Files:**
- Create: `scripts/normalize.py`, `scripts/crypto_payload.py`, `tests/test_normalize.py`, `tests/test_crypto_digest.py`
- Modify: none

**Interfaces:**
- Produces:
  - `normalize.normalize_intent(text: str) -> str`
  - `crypto_payload.intent_digest(normalized: str) -> str`  # 64 hex chars
  - Raises `ValueError` on empty after normalize

- [ ] **Step 1: Write failing tests**

```python
# tests/test_normalize.py
from normalize import normalize_intent
import pytest

def test_normalize_lower_strip_collapse_space():
    assert normalize_intent("  I Maintain Calm  Focus  ") == "i maintain calm focus"

def test_normalize_empty_raises():
    with pytest.raises(ValueError):
        normalize_intent("   ")

def test_normalize_keeps_letters_for_reduction():
    assert "sigil" in normalize_intent("Sigil-Forge ships.")
```

```python
# tests/test_crypto_digest.py
from crypto_payload import intent_digest
from normalize import normalize_intent

def test_digest_stable():
    n = normalize_intent("I maintain calm focus")
    d1 = intent_digest(n)
    d2 = intent_digest(n)
    assert d1 == d2
    assert len(d1) == 64
    assert d1 == d1.lower()

def test_digest_changes_with_intent():
    a = intent_digest(normalize_intent("alpha intent here"))
    b = intent_digest(normalize_intent("beta intent here"))
    assert a != b
```

- [ ] **Step 2: Run tests — expect FAIL**

Run: `python3 -m pytest tests/test_normalize.py tests/test_crypto_digest.py -v`

- [ ] **Step 3: Implement**

```python
# scripts/normalize.py
from __future__ import annotations
import re
import unicodedata


def normalize_intent(text: str) -> str:
    if text is None:
        raise ValueError("intent is required")
    s = unicodedata.normalize("NFKC", str(text))
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    if not s:
        raise ValueError("intent is empty after normalization")
    return s
```

```python
# scripts/crypto_payload.py  (Task 2: digest only; Task 6 adds seal/open)
from __future__ import annotations
import hashlib


def intent_digest(normalized: str) -> str:
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
```

Task 6 adds AES-256-GCM seal/open via vendored pure-Python AES-GCM (`scripts/aes_gcm_pure.py`) plus `hashlib.pbkdf2_hmac` so core stays free of hard pip deps.

- [ ] **Step 4: Run tests — expect PASS**

Run: `python3 -m pytest tests/test_normalize.py tests/test_crypto_digest.py -v`

- [ ] **Step 5: Commit**

```bash
git add scripts/normalize.py scripts/crypto_payload.py tests/test_normalize.py tests/test_crypto_digest.py
git commit -m "feat: normalize intent and SHA-256 digest"
```

---

### Task 3: Spare letter reduction

**Files:**
- Create: `scripts/spare.py`, `tests/test_spare.py`, `examples/intents/calm_focus.json`

**Interfaces:**
- Produces:
  - `spare.reduce_letters(normalized: str) -> str`  # consonants/remaining glyphs only, no vowels, unique order preserved
  - `spare.letter_sequence(normalized: str) -> list[str]`  # list of single chars A-Z
  - Vowels for English reduction: `aeiou` (and `y` treated as vowel when not sole remaining letter — document: **y is always stripped as vowel in v1**)

- [ ] **Step 1: Write failing tests**

```python
# tests/test_spare.py
from spare import reduce_letters, letter_sequence
from normalize import normalize_intent

def test_classic_reduction_drops_vowels_and_dupes():
    n = normalize_intent("I maintain calm focus")
    # i m a i n t a i n c a l m f o c u s
    # letters only, no vowels, first occurrence: m n t c l f s
    assert reduce_letters(n) == "mntclfs"

def test_letter_sequence_matches_reduce():
    n = normalize_intent("It is my will to remain calm")
    assert "".join(letter_sequence(n)) == reduce_letters(n)

def test_all_vowels_yields_empty():
    assert reduce_letters(normalize_intent("aeiou you")) == ""
```

`examples/intents/calm_focus.json`:
```json
{
  "intent": "I maintain calm focus while shipping Sigil-Forge",
  "normalized": "i maintain calm focus while shipping sigil-forge",
  "spare_reduced": "mntnclmfcswhlshppngsglfrg"
}
```

Wait — reduction must drop **duplicate letters** globally (first occurrence only) and vowels. Recompute carefully for tests and fix golden file in implementation:

Rule (locked v1):
1. Keep only `a-z`
2. Remove vowels `a e i o u y`
3. Collapse to unique letters preserving first-seen order

For `"i maintain calm focus"`:
letters: i,m,a,i,n,t,a,i,n,c,a,l,m,f,o,c,u,s  
no vowels: m,n,t,n,c,l,m,f,c,s  
unique first-seen: m,n,t,c,l,f,s → `mntclfs`

Update golden accordingly after computing full intent string in Task 3 implementation; test above is source of truth for short phrase.

- [ ] **Step 2: Run — expect FAIL**

- [ ] **Step 3: Implement**

```python
# scripts/spare.py
from __future__ import annotations
import re

_VOWELS = set("aeiouy")


def letter_sequence(normalized: str) -> list[str]:
    chars = re.findall(r"[a-z]", normalized.lower())
    out: list[str] = []
    seen: set[str] = set()
    for ch in chars:
        if ch in _VOWELS:
            continue
        if ch in seen:
            continue
        seen.add(ch)
        out.append(ch)
    return out


def reduce_letters(normalized: str) -> str:
    return "".join(letter_sequence(normalized))
```

- [ ] **Step 4: Run — expect PASS**

- [ ] **Step 5: Commit**

```bash
git add scripts/spare.py tests/test_spare.py examples/intents/
git commit -m "feat: Spare-style letter reduction"
```

---

### Task 4: Kamea squares + path

**Files:**
- Create: `scripts/kamea.py`, `tests/test_kamea.py`, `references/methods-kamea.md` (tables can live in code; doc explains)

**Interfaces:**
- Produces:
  - `KAMEA_SQUARES: dict[str, list[list[int]]]` keys: `saturn|jupiter|mars|sol|venus|mercury|luna` sizes 3..9
  - `letter_to_number(ch: str) -> int`  # A=1..I=9, J=1..R=9, S=1..Z=8 (Agrippa-style digital mapping v1)
  - `select_square(digest_hex: str, override: str | None = None) -> str`
  - `plot_path(letters: list[str], square_name: str) -> list[tuple[float,float]]`  # cell centers in unit square grid

**Cipher (locked v1 Agrippa reduced):**

```
1: A J S
2: B K T
3: C L U
4: D M V
5: E N W
6: F O X
7: G P Y
8: H Q Z
9: I R
```

Magic squares: use standard planetary kamea number placements (hardcode full 3×3 Saturn through 9×9 Luna in `kamea.py` as nested lists). Path: for each letter number, find cell containing that number; append center `(c+0.5, r+0.5)`; if number missing (should not), skip.

- [ ] **Step 1: Write failing tests**

```python
# tests/test_kamea.py
from kamea import letter_to_number, select_square, plot_path, KAMEA_SQUARES

def test_saturn_square_is_3x3_magic():
    s = KAMEA_SQUARES["saturn"]
    assert len(s) == 3 and all(len(r) == 3 for r in s)
    assert sorted(x for row in s for x in row) == list(range(1, 10))

def test_letter_to_number_agrippa():
    assert letter_to_number("a") == 1
    assert letter_to_number("j") == 1
    assert letter_to_number("t") == 2

def test_select_square_override():
    assert select_square("abc", override="mars") == "mars"

def test_select_square_from_digest():
    name = select_square("00" * 32)
    assert name in KAMEA_SQUARES

def test_plot_path_nonempty():
    pts = plot_path(list("mntclfs"), "saturn")
    assert len(pts) >= 1
    assert all(len(p) == 2 for p in pts)
```

- [ ] **Step 2: Run — expect FAIL**

- [ ] **Step 3: Implement `scripts/kamea.py`** with full hardcoded squares (Saturn 3×3 classic Lo Shu orientation as commonly published for planetary kamea; document source in `references/methods-kamea.md`). Include all seven squares.

- [ ] **Step 4: Run — expect PASS**

- [ ] **Step 5: Commit**

```bash
git add scripts/kamea.py tests/test_kamea.py references/methods-kamea.md
git commit -m "feat: kamea squares, Agrippa cipher, and path plot"
```

---

### Task 5: Fuse layout + SVG export

**Files:**
- Create: `scripts/fuse.py`, `scripts/svg_export.py`, `tests/test_fuse_svg.py`

**Interfaces:**
- Produces:
  - `@dataclass Layout`: `monogram_points: list[tuple[float,float]]`, `kamea_points: list[tuple[float,float]]`, `view_box: tuple[float,float,float,float]`, `spare_letters: str`, `square_name: str`
  - `fuse.build_layout(normalized: str, digest_hex: str, square_override: str | None = None) -> Layout`
  - `svg_export.layout_to_svg(layout: Layout, stroke: str = "#0a0a0a", bg: str = "#f7f4ef") -> str`
  - Monogram points: place unique letters on a circle (equal angles) in sequence order, then polyline closed=False
  - Kamea points: scale `plot_path` into concentric inner region (0.35–0.65 of canvas)

- [ ] **Step 1: Write failing tests**

```python
# tests/test_fuse_svg.py
from normalize import normalize_intent
from crypto_payload import intent_digest
from fuse import build_layout
from svg_export import layout_to_svg

def test_layout_has_both_channels_when_letters_exist():
    n = normalize_intent("I maintain calm focus")
    d = intent_digest(n)
    lay = build_layout(n, d, square_override="saturn")
    assert lay.spare_letters == "mntclfs"
    assert len(lay.monogram_points) >= 2
    assert len(lay.kamea_points) >= 1

def test_svg_contains_paths_not_plaintext_intent():
    n = normalize_intent("I maintain calm focus")
    d = intent_digest(n)
    svg = layout_to_svg(build_layout(n, d, square_override="saturn"))
    assert "<svg" in svg
    assert "path" in svg.lower() or "polyline" in svg.lower()
    assert "i maintain calm focus" not in svg.lower()
```

- [ ] **Step 2: Run — expect FAIL**

- [ ] **Step 3: Implement fuse + svg_export** (canvas 0..100 viewBox; monochrome strokes; two path groups with ids `spare-monogram` and `kamea-path`)

- [ ] **Step 4: Run — expect PASS**

- [ ] **Step 5: Commit**

```bash
git add scripts/fuse.py scripts/svg_export.py tests/test_fuse_svg.py
git commit -m "feat: fuse monogram+kamea layout into SVG"
```

---

### Task 6: Optional ciphertext (AES-GCM + PBKDF2)

**Files:**
- Create: `scripts/aes_gcm_pure.py` (minimal pure AES-GCM or use only digest if AES too large — **locked: use `cryptography` as optional; if absent, provide Fernet-like seal via pure implementation**)

**Pragmatic lock for implementers:** Implement seal/open with:

```python
# scripts/crypto_payload.py expanded
import os, hashlib, hmac, secrets
from dataclasses import dataclass

# Use Python 3's available APIs:
# PBKDF2: hashlib.pbkdf2_hmac
# AES-GCM: implement via optional dependency cryptography;
# FALLBACK: ChaCha-like is not in stdlib either.
# REQUIRED for v1 tests: vendor a minimal aes_gcm (~single file) from a known test vector set.
```

**Interfaces:**
- `derive_key(passphrase: str, salt: bytes, iterations: int = 200_000) -> bytes`  # 32 bytes
- `seal_intent(plaintext: str, passphrase: str) -> dict` → `{ciphertext_b64, nonce_b64, salt_b64, kdf: "pbkdf2-sha256", alg: "aes-256-gcm"}`
- `open_intent(blob: dict, passphrase: str) -> str`
- Without passphrase: construct still works; `crypto.key_policy = "none"` and no ciphertext channel

- [ ] **Step 1: Tests round-trip seal/open + wrong passphrase fails**

```python
# tests/test_crypto_seal.py
from crypto_payload import seal_intent, open_intent
import pytest

def test_seal_roundtrip():
    blob = seal_intent("secret intent", "correct horse")
    assert "ciphertext_b64" in blob
    assert open_intent(blob, "correct horse") == "secret intent"

def test_wrong_passphrase_fails():
    blob = seal_intent("secret intent", "correct horse")
    with pytest.raises(Exception):
        open_intent(blob, "wrong")
```

- [ ] **Step 2–4: Implement pure AES-GCM file + wire into crypto_payload; pass tests**

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: optional AES-GCM intent sealing with PBKDF2"
```

---

### Task 7: SVG steganography + structural channels

**Files:**
- Create: `scripts/stego_svg.py`, `tests/test_stego_svg.py`

**Interfaces:**
- `ChannelStatus = TypedDict` with `id`, `status` (`applied`|`skipped`), `detail`
- `embed(svg: str, digest_hex: str, spare_letters: str, extras: dict | None = None) -> tuple[str, list[ChannelStatus]]`
- `extract(svg: str) -> dict` → must include `intent_digest`
- Channels implemented here: `svg_metadata`, `path_epsilon`, `path_order`, `metric_quantize` (metric: encode first N nibbles of digest into quantized stroke-width or data attributes on path groups — v1 uses `data-sf-metric` attribute list to avoid geometry breakage, AND path_epsilon for true geometric stego)

**v1 geometric stego (locked minimal viable):**
1. `svg_metadata`: XML element `metadata/sf:payload` with base64 JSON `{v:1, d:<digest>, m:<method_bitmap>}` — **not** plaintext
2. `path_epsilon`: for each float in path `d` or polyline points, add `±(bit*eps)` with `eps=0.001`, bits from digest
3. `path_order`: if multiple subpaths, order already fixed by construction; encode by storing permutation id in metadata (if only 2 paths, swap allowed only when digest bit0=1 — document carefully). Simpler v1: store `order_token` derived from digest in metadata and mark `path_order` applied as **manifest binding** when monogram path is emitted before kamea path always, and residual letters packed into metadata field `r` as the reduced spare string is **NOT** full intent — spare reduced letters only is OK in public? Spec says no plaintext **intent**. Reduced letters leak partial intent. **Lock:** do not put spare reduced string in public SVG; only digest + channel bitmap.

- [ ] **Step 1: Tests**

```python
# tests/test_stego_svg.py
from normalize import normalize_intent
from crypto_payload import intent_digest
from fuse import build_layout
from svg_export import layout_to_svg
from stego_svg import embed, extract

def test_embed_extract_digest():
    n = normalize_intent("I maintain calm focus")
    d = intent_digest(n)
    svg = layout_to_svg(build_layout(n, d, square_override="saturn"))
    out, channels = embed(svg, d, spare_letters="mntclfs")
    got = extract(out)
    assert got["intent_digest"] == d
    assert any(c["id"] == "svg_metadata" and c["status"] == "applied" for c in channels)
    assert n not in out.lower()
```

- [ ] **Step 2–4: Implement + pass**

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: SVG metadata and geometric steganography"
```

---

### Task 8: PNG LSB stego (optional channel)

**Files:**
- Create: `scripts/stego_png.py`, `scripts/raster_svg.py`, `tests/test_stego_png.py`

**Interfaces:**
- `raster_svg.svg_to_png_bytes(svg: str) -> bytes | None` — try `cairosvg` or `resvg` or PIL+svglib; if none available return None
- `stego_png.embed_lsb(png_bytes: bytes, payload: bytes) -> bytes`
- `stego_png.extract_lsb(png_bytes: bytes, n: int) -> bytes`
- Payload format: magic `SF1\0` + digest raw 32 bytes + optional sealed blob length-prefixed

If raster unavailable: channel `png_lsb` → `skipped("no_raster_backend")` without failing construct.

- [ ] **Step 1: Unit test LSB on a synthetic solid PNG created without SVG** (generate minimal 64×64 RGB PNG with pure Python writer in test helper)

```python
# tests/test_stego_png.py
from stego_png import embed_lsb, extract_lsb, write_rgb_png, read_rgb_png

def test_lsb_roundtrip_synthetic():
    raw = bytes([0, 0, 0] * (32 * 32))
    png = write_rgb_png(32, 32, raw)
    payload = b"SF1\x00" + b"\x11" * 32
    out = embed_lsb(png, payload)
    got = extract_lsb(out, len(payload))
    assert got == payload
```

- [ ] **Step 2–4: Implement pure PNG RGB read/write + LSB; pass tests**

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: PNG LSB steganography channel"
```

---

### Task 9: Safety gate

**Files:**
- Create: `scripts/safety.py`, `tests/test_safety.py`

**Interfaces:**
- `safety.check_intent(text: str) -> tuple[bool, str]` — `(ok, reason)`  
- Refuse categories (keyword/heuristic v1, case-insensitive): explicit violence against others, self-harm instructions, non-consensual control/"force X to love me", child exploitation. Prefer false negatives over blocking mundane "kill process" engineering language — require multi-word harmful patterns.

```python
# tests/test_safety.py
from safety import check_intent

def test_allows_calm_focus():
    ok, _ = check_intent("I maintain calm focus while shipping")
    assert ok

def test_blocks_harm_others():
    ok, reason = check_intent("I will murder my neighbor tomorrow")
    assert not ok
    assert reason
```

- [ ] Implement keyword lists carefully; commit `feat: intent safety gate`

---

### Task 10: Construct pipeline + packet + verify CLI

**Files:**
- Create: `scripts/construct.py`, `scripts/packet.py`, `schemas/forge-packet.schema.json`, `schemas/construction-result.schema.json`, `schemas/channel-manifest.schema.json`, `tests/test_construct_verify.py`
- Modify: `scripts/sigil_forge.py` — add `construct` and `verify` subcommands

**Interfaces:**
- `construct.run(intent: str, *, mode: str = "creative", out_root: Path | None = None, passphrase: str | None = None, square: str | None = None, seal_packet: bool = False) -> dict`
  Returns packet dict and writes files under run dir:
  - `glyph.svg` (stego'd)
  - `glyph.png` (if raster ok)
  - `forge-packet.json`
  - `forge-packet.md` (human summary)
- `verify.run(artifact_path: Path) -> dict` with `ok: bool`, `intent_digest`, `channels_checked`

CLI:
```bash
python3 scripts/sigil_forge.py construct --intent "..." --mode creative --out out/sigil-forge
python3 scripts/sigil_forge.py verify out/sigil-forge/<run-id>/glyph.svg
```

Packet must include fields from spec §9.

- [ ] **Step 1: Integration test**

```python
# tests/test_construct_verify.py
from pathlib import Path
from construct import run as construct_run
from verify_mod import run as verify_run  # or construct.verify

def test_construct_and_verify(tmp_path: Path):
    packet = construct_run(
        "I maintain calm focus while shipping Sigil-Forge",
        mode="creative",
        out_root=tmp_path,
        square="saturn",
    )
    svg = Path(packet["artifacts"]["svg"])
    assert svg.is_file()
    assert packet["intent_digest"]
    text = svg.read_text(encoding="utf-8")
    assert "i maintain calm" not in text.lower()
    v = verify_run(svg)
    assert v["ok"] is True
    assert v["intent_digest"] == packet["intent_digest"]

def test_construct_refuses_harm(tmp_path: Path):
    import pytest
    with pytest.raises(ValueError):
        construct_run("I will murder my neighbor tomorrow", out_root=tmp_path)
```

Put `verify` in `scripts/verify_mod.py` named `verify.py` — careful: `verify.py` is fine as `import verify`.

- [ ] **Step 2–4: Implement pipeline, schemas (JSON Schema draft-07), CLI wiring, pass tests**

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: construct pipeline, forge packet, and verify CLI"
```

---

### Task 11: Check/smoke expansion + privacy tests

**Files:**
- Create: `tests/test_privacy.py`, `tests/test_check.py`
- Modify: `scripts/sigil_forge.py` `cmd_check` to require schemas + scripts modules + one dry construct to temp

```python
# tests/test_privacy.py
from pathlib import Path
from construct import run

def test_public_svg_has_no_plaintext(tmp_path: Path):
    intent = "I maintain calm focus while shipping Sigil-Forge"
    packet = run(intent, out_root=tmp_path, square="saturn")
    svg = Path(packet["artifacts"]["svg"]).read_text(encoding="utf-8")
    assert intent.lower() not in svg.lower()
    # packet local may contain intent
    assert packet.get("normalized_intent") or packet.get("crypto", {}).get("ciphertext_present")
```

- [ ] Implement; commit `test: privacy and expanded check smoke`

---

### Task 12: Hermes SKILL.md + references + profiles

**Files:**
- Create:
  - `SKILL.md`
  - `references/methods-spare.md`
  - `references/channels-and-steganography.md`
  - `references/profiles-creative.md`
  - `references/profiles-practice.md`
  - `references/safety-and-framing.md`
  - `references/hermes-runtime-contract.md`
  - `references/expansion-spine.md`
  - `references/distinction-enochian.md`
  - (methods-kamea.md may already exist from Task 4)

**SKILL.md requirements:**
- YAML frontmatter: `name: sigil-forge`, description starting with `Use when` (triggers in first 57 chars), version from VERSION, license MIT, metadata.hermes tags Creative/Sigil/Intent/Steganography
- Sections: Overview, When to Use / Not, Prerequisites, Procedure (mirror construct flow), Modes, Channels table, CLI, Pitfalls, Verification
- Procedure must: safety → normalize → construct scripts → dual-mode notes → optional AI polish geometry-locked → never claim efficacy
- Point to references for method detail

- [ ] Write files; commit `docs: Hermes SKILL contract and method references`

---

### Task 13: install.sh + README + QUICKSTART + golden examples

**Files:**
- Create: `install.sh`, `README.md`, `QUICKSTART.md`
- Modify: `examples/intents/*.json` with verified golden reductions from actual engine

`install.sh` (minimal, peer-shaped):
- Default target `$HOME/.hermes/skills/sigil-forge`
- Copy skill tree (exclude `.git`, `out/`)
- `--dry-run`, `--target`, `--version`
- Post-install: `python3 "$TARGET/scripts/sigil_forge.py" check`

`README.md`: what it is, install, one construct example, link to design spec  
`QUICKSTART.md`: 5 commands from zero to verify

- [ ] Manually run:

```bash
bash install.sh --dry-run
python3 scripts/sigil_forge.py check
python3 scripts/sigil_forge.py construct --intent "I maintain calm focus" --out out/sigil-forge
python3 scripts/sigil_forge.py verify out/sigil-forge/*/glyph.svg
python3 -m pytest -v
```

Expected: all green

- [ ] Commit `chore: install script, docs, and golden examples`

---

### Task 14: AI polish procedure (agent-only, no API client)

**Files:**
- Modify: `SKILL.md` section "Optional AI polish"
- Create: `scripts/prompt_polish.py`, `tests/test_prompt_polish.py`

**Interfaces:**
- `prompt_polish.build_prompt(layout_summary: dict, style: str | None) -> dict` with keys `prompt`, `negative`, `seed` (int from first 8 hex of digest), `geometry_lock` (short text constraints from path bbox / stroke count)
- Does **not** call any API
- Packet may store `artifacts.polish_prompt_path`

```python
def test_seed_from_digest():
    from prompt_polish import build_prompt
    p = build_prompt({"intent_digest": "abcd" * 16, "stroke_count": 2}, style="ink on parchment")
    assert p["seed"] == int("abcdabcd", 16)  # or first 8 hex
    assert "geometry" in p["prompt"].lower() or "sigil" in p["prompt"].lower()
    assert "do not add text" in p["negative"].lower() or "text" in p["negative"].lower()
```

- [ ] Commit `feat: geometry-locked AI polish prompt builder`

---

### Task 15: Final verification gate

- [ ] Run full suite: `python3 -m pytest -v`
- [ ] Run: `python3 scripts/sigil_forge.py check` → `ok: true`
- [ ] Construct + verify round-trip on sample intent
- [ ] Confirm design checklist:

| Spec requirement | Task |
|------------------|------|
| Spare + kamea fusion | 3,4,5 |
| Multi-channel stego | 7,8 |
| Digest + optional seal | 2,6 |
| Forge packet + schemas | 10 |
| Verify | 10 |
| Privacy default | 11 |
| Safety refuse | 9 |
| Dual mode framing | 10,12 |
| Hermes SKILL | 12 |
| Install hybrid spine | 1,13 |
| AI polish optional | 14 |
| Expansion spine docs | 12 |

- [ ] Commit any fixes: `chore: v0.1.0 verification polish`
- [ ] Tag optional: `git tag v0.1.0`

---

## Self-Review (plan vs spec)

**Coverage:** All major design sections map to tasks 1–15. Expansion spine is documentation-only in Task 12 (`expansion-spine.md`), not full CLI `doctor|eval|receipt` (correct YAGNI).

**Placeholders:** None intentional; AES implementation is constrained to pure/vendored AES-GCM in Task 6.

**Type consistency:**
- `intent_digest` → 64-char hex throughout
- `construct.run` → packet dict with `artifacts.svg`, `intent_digest`, `channels`
- `verify.run` → `{ok, intent_digest}`
- Channel ids match design: `spare_monogram`, `kamea_path`, `kamea_square_choice`, `intent_digest`, `optional_ciphertext`, `svg_metadata`, `path_epsilon`, `path_order`, `metric_quantize`, `png_lsb`, `gen_seed`

**Note for implementers:** Register channel status for craft channels in `construct.py` even though geometry is produced by fuse (e.g. `spare_monogram: applied` when monogram_points non-empty).

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-07-sigil-forge.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks, fast iteration  
2. **Inline Execution** — execute tasks in this session with checkpoints  

Which approach?
