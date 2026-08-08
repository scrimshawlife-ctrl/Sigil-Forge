# Policy Domains: Authority Seals · Efficacy · Canon Learning — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden Sigil-Forge’s three product policy domains so defaults stay safe (no Goetic/Enochian in the default forge, no efficacy claims, no auto-canon learning) while shipping explicit machinery for refusal, framing lint, and human-gated ledger review/promotion.

**Architecture:** Keep the default forge as an **intent-compression engine**. Treat Goetic/Enochian as **excluded families** with hard construct/wizard gates and a separate future interop *namespace* (not default channels). Treat efficacy as a **cross-artifact language policy** enforced by shared lint helpers on packets, polish prompts, and agent checklists. Treat learning as **PROPOSED-only append** plus an optional **human-confirmed** promotion path that writes operator-local canon proposals—never silent rewrite of `references/`.

**Tech Stack:** Python 3.10+ stdlib, existing `scripts/` CLI (`sigil_forge.py`), pytest, JSONL ledgers, existing schemas under `schemas/`.

## Global Constraints

- Default forge remains intent-only; **never** add Goetic/Enochian as default construct channels.
- **No** efficacy claims in creative or practice mode (`references/safety-and-framing.md`).
- Learning ledger entries stay `canon_status: PROPOSED` unless a **human-confirmed** promote path runs.
- Offline path: no required pip packages; optional `jsonschema` only.
- Never mutate `references/` at run time without an explicit human CLI + confirm flag.
- Proposal-only Hermes authority; agent may draft, not promote.

## Stance (read first)

| Domain | Product stance | This plan ships |
|--------|----------------|-----------------|
| Goetic / Enochian | **Excluded from default forge** | Harder gates + clearer refusal + optional *namespace stub* (not default channels) |
| Efficacy claims | **Forbidden** | Shared lint + packet/polish checks + tests + docs |
| Auto-canon learning | **Forbidden** | Keep PROPOSED-only; add human-gated review/promote tooling |

This is **not** a plan to enable efficacy claims or to dump Goetic seals into default construct. If product later wants a full authority-seal skill, that is a **separate skill or opt-in module**, planned as namespace-only here.

---

## File map

| Path | Responsibility |
|------|----------------|
| `scripts/policy_lint.py` | Shared efficacy phrase lint + authority-request classifiers |
| `scripts/ontology.py` | Already has `EXCLUDED_DEFAULT_FAMILIES` / `assert_not_entity_seal_request` — extend |
| `scripts/safety.py` | Harmful intent; may call policy classifiers or stay separate |
| `scripts/construct.py` | Call policy gates before encode |
| `scripts/wizard.py` | Refuse authority-seal requests in interview |
| `scripts/packet.py` | Lint `framing_notes` |
| `scripts/prompt_polish.py` | Lint polish prompt text |
| `scripts/receipt.py` | Ledger PROPOSED + promote helpers |
| `scripts/sigil_forge.py` | CLI: `ledger promote` / `policy check` |
| `schemas/learning-ledger-entry.schema.json` | Allow status enum only if promote path documented |
| `schemas/canon-proposal.schema.json` | New: human-gated promotion record |
| `references/distinction-enochian.md` | Expand goetic + default vs namespace |
| `references/safety-and-framing.md` | Efficacy lint list + agent duties |
| `references/receipts-and-ledger.md` | Human promote workflow |
| `references/authority-seal-namespace.md` | New: future interop boundaries |
| `tests/test_policy_*.py` | Gates, lint, promote |
| `SKILL.md` / `README.md` / `expansion-spine.md` | Align copy |

---

### Task 1: Policy lint module (efficacy + authority request detection)

**Files:**
- Create: `scripts/policy_lint.py`
- Create: `tests/test_policy_lint.py`
- Modify: none yet (consumed by later tasks)

**Interfaces:**
- Produces:
  - `EFFICACY_PATTERNS: list[re.Pattern]`
  - `AUTHORITY_SEAL_PATTERNS: list[re.Pattern]`
  - `lint_efficacy_text(text: str) -> list[str]`  # violation messages
  - `detect_authority_seal_request(text: str) -> tuple[bool, str | None]`  # (hit, family_hint)
  - `assert_no_efficacy(text: str, *, field: str = "text") -> None`  # raises ValueError

- [ ] **Step 1: Write failing tests**

```python
# tests/test_policy_lint.py
from policy_lint import (
    detect_authority_seal_request,
    lint_efficacy_text,
    assert_no_efficacy,
)

def test_efficacy_flags_works_and_manifests():
    hits = lint_efficacy_text("This sigil works and manifests wealth")
    assert hits
    assert any("efficacy" in h.lower() or "works" in h.lower() for h in hits)

def test_efficacy_allows_craft_language():
    hits = lint_efficacy_text(
        "Methods are craft history and symbolic compression; verify recovers digest."
    )
    assert hits == []

def test_authority_detects_enochian_and_goetic():
    ok, fam = detect_authority_seal_request("please forge an Enochian seal for the tablet")
    assert ok is True
    assert fam in ("enochian_seal", "authority_seal", "goetic_seal") or fam
    ok2, fam2 = detect_authority_seal_request("make a goetic seal of a spirit")
    assert ok2 is True

def test_authority_allows_intent_language():
    ok, _ = detect_authority_seal_request("I maintain calm focus while shipping")
    assert ok is False

def test_assert_no_efficacy_raises():
    try:
        assert_no_efficacy("guarantees results every time", field="framing_notes")
        assert False, "expected ValueError"
    except ValueError as e:
        assert "framing_notes" in str(e) or "efficacy" in str(e).lower()
```

- [ ] **Step 2: Run tests — expect FAIL**

```bash
cd /path/to/Sigil-Forge && .venv/bin/python -m pytest tests/test_policy_lint.py -q
```

Expected: import/collection errors or failures (module missing).

- [ ] **Step 3: Implement `scripts/policy_lint.py`**

```python
"""Cross-cutting product policy: efficacy language + authority-seal request detection.

Default forge stays intent-compression only. This module does not implement
Goetic/Enochian geometry — it refuses/classifies and lints language.
"""
from __future__ import annotations

import re
from typing import Iterable

# Phrase patterns (case-insensitive). Prefer multi-word to reduce false positives.
_EFFICACY = [
    r"\bthis sigil works\b",
    r"\bit will (manifest|work|cause)\b",
    r"\bguarantees? results?\b",
    r"\bproves? (that )?magic\b",
    r"\bcontacts? spirits?\b",
    r"\bmakes? (him|her|them) (love|obey)\b",
    r"\bsupernatural efficacy\b",
    r"\bwill (definitely|certainly) (manifest|come true)\b",
]

_AUTHORITY = [
    (r"\benochian\b", "enochian_seal"),
    (r"\bwatchtower\b", "enochian_seal"),
    (r"\bgoetic\b", "goetic_seal"),
    (r"\bgoetia\b", "goetic_seal"),
    (r"\bars\s+goetia\b", "goetic_seal"),
    (r"\bsolomonic (spirit )?seal\b", "goetic_seal"),
    (r"\bauthority seal\b", "authority_seal"),
    (r"\bspirit seal of binding\b", "authority_seal"),
]

EFFICACY_PATTERNS = [re.compile(p, re.I) for p in _EFFICACY]
AUTHORITY_SEAL_PATTERNS = [(re.compile(p, re.I), fam) for p, fam in _AUTHORITY]


def lint_efficacy_text(text: str) -> list[str]:
    if not text:
        return []
    hits: list[str] = []
    for pat in EFFICACY_PATTERNS:
        if pat.search(text):
            hits.append(f"efficacy_phrase:{pat.pattern}")
    return hits


def assert_no_efficacy(text: str, *, field: str = "text") -> None:
    hits = lint_efficacy_text(text)
    if hits:
        raise ValueError(f"efficacy_policy_violation field={field}: {hits}")


def detect_authority_seal_request(text: str) -> tuple[bool, str | None]:
    if not text:
        return False, None
    for pat, fam in AUTHORITY_SEAL_PATTERNS:
        if pat.search(text):
            return True, fam
    return False, None
```

Tune patterns if tests show false positives on “works” in programming sense — keep multi-word anchors.

- [ ] **Step 4: Run tests — expect PASS**

```bash
.venv/bin/python -m pytest tests/test_policy_lint.py -q
```

- [ ] **Step 5: Commit**

```bash
git add scripts/policy_lint.py tests/test_policy_lint.py
git commit -m "feat: policy lint for efficacy language and authority-seal requests"
```

---

### Task 2: Harden construct + ontology gates (no default authority seals)

**Files:**
- Modify: `scripts/ontology.py` (`assert_not_entity_seal_request`)
- Modify: `scripts/construct.py` (call extended gate)
- Modify: `scripts/wizard.py` (`next_step` early refuse)
- Create: `tests/test_authority_gate.py`

**Interfaces:**
- Consumes: `policy_lint.detect_authority_seal_request`
- Produces: construct/wizard raise or return `refused` with clear message pointing to `distinction-enochian.md`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_authority_gate.py
import pytest
from construct import run as construct_run
from wizard import next_step

def test_construct_refuses_enochian_request(tmp_path):
    with pytest.raises(ValueError) as ei:
        construct_run(
            "forge an Enochian seal for the air tablet",
            out_root=tmp_path,
        )
    assert "enochian" in str(ei.value).lower() or "authority" in str(ei.value).lower()

def test_construct_refuses_goetic_request(tmp_path):
    with pytest.raises(ValueError) as ei:
        construct_run("draw a goetic seal of binding", out_root=tmp_path)
    msg = str(ei.value).lower()
    assert "goetic" in msg or "authority" in msg or "excluded" in msg

def test_wizard_next_refuses_authority_intent():
    nxt = next_step({"intent": "I need an Enochian watchtower seal"}, path="quick")
    assert nxt.get("refused") is True
    assert nxt.get("done") is True
```

- [ ] **Step 2: Run — expect FAIL** (current gate may be weaker than these strings)

```bash
.venv/bin/python -m pytest tests/test_authority_gate.py -q
```

- [ ] **Step 3: Wire gate**

In `ontology.py`, implement/extend:

```python
from policy_lint import detect_authority_seal_request

def assert_not_entity_seal_request(intent: str) -> None:
    hit, fam = detect_authority_seal_request(intent)
    if hit:
        raise ValueError(
            "AUTHORITY_SEAL_EXCLUDED: "
            f"family={fam or 'authority_seal'} is not part of the default forge. "
            "Sigil-Forge builds intent-compression sigils only. "
            "See references/distinction-enochian.md and "
            "references/authority-seal-namespace.md. "
            "Do not silently substitute a Spare/kamea glyph."
        )
```

In `construct.py` (already calls `assert_not_entity_seal_request(intent)` near safety): ensure it runs **after** harm check and **before** normalize encode.

In `wizard.py` `next_step`, after intent safety check:

```python
from ontology import assert_not_entity_seal_request
# or detect_authority_seal_request and return refused payload
if intent:
    hit, fam = detect_authority_seal_request(intent)
    if hit:
        return {
            "ok": False,
            "done": True,
            "refused": True,
            "phase": "authority_policy",
            "error": f"AUTHORITY_SEAL_EXCLUDED family={fam}",
            "agent_instruction": (
                "Refuse. Do not construct. Explain intent-sigil vs authority-seal. "
                "Point to distinction-enochian.md. Offer a present-tense intent rewrite."
            ),
            ...
        }
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
.venv/bin/python -m pytest tests/test_authority_gate.py tests/test_policy_lint.py -q
```

- [ ] **Step 5: Commit**

```bash
git add scripts/ontology.py scripts/construct.py scripts/wizard.py tests/test_authority_gate.py
git commit -m "feat: hard-exclude Goetic/Enochian authority requests from default forge"
```

---

### Task 3: Efficacy lint on packets and polish prompts

**Files:**
- Modify: `scripts/packet.py` (`framing_notes`, `build_packet` or `write`)
- Modify: `scripts/prompt_polish.py`
- Create: `tests/test_efficacy_artifacts.py`

**Interfaces:**
- Consumes: `policy_lint.assert_no_efficacy` / `lint_efficacy_text`
- Produces: construct fails closed if framing/polish contains banned efficacy phrases; static framing_notes remain clean

- [ ] **Step 1: Write failing tests**

```python
# tests/test_efficacy_artifacts.py
from packet import framing_notes
from policy_lint import lint_efficacy_text

def test_builtin_framing_notes_clean():
    for mode in ("creative", "practice"):
        assert lint_efficacy_text(framing_notes(mode)) == []

def test_polish_prompt_rejects_efficacy():
    from prompt_polish import build_prompt
    # If build_prompt accepts free style text, inject bad style and expect raise
    # or post-lint the package strings:
    bad = "a sigil that guarantees results and contacts spirits"
    hits = lint_efficacy_text(bad)
    assert hits
```

Add one integration test that monkeypatches or calls a public lint on a fake polish package if style is concatenated into prompt text.

- [ ] **Step 2: Implement lint at write boundaries**

In `packet.py` when assembling packet:

```python
from policy_lint import assert_no_efficacy
notes = framing_notes(mode)
assert_no_efficacy(notes, field="framing_notes")
```

In `prompt_polish.build_prompt`, after building the package dict:

```python
for key in ("prompt", "negative", "geometry_lock", "style"):
    val = package.get(key)
    if isinstance(val, str):
        assert_no_efficacy(val, field=f"polish.{key}")
```

Do **not** ban the word “works” in isolation if it appears only in technical copy; patterns in Task 1 stay multi-word.

- [ ] **Step 3: Run tests + full suite subset**

```bash
.venv/bin/python -m pytest tests/test_efficacy_artifacts.py tests/test_construct_verify.py -q
```

- [ ] **Step 4: Commit**

```bash
git add scripts/packet.py scripts/prompt_polish.py tests/test_efficacy_artifacts.py
git commit -m "feat: fail-closed efficacy lint on framing notes and polish prompts"
```

---

### Task 4: CLI `policy check` for agents and CI

**Files:**
- Modify: `scripts/sigil_forge.py` (subcommand `policy`)
- Create: `tests/test_policy_cli.py`

**Interfaces:**
- CLI: `python3 scripts/sigil_forge.py policy check --text "..."`  
- CLI: `python3 scripts/sigil_forge.py policy check --file path`  
- Exit 0 if clean; 1 if efficacy and/or authority hits (JSON on stdout)

- [ ] **Step 1: Failing CLI test**

```python
import json, subprocess, sys
from pathlib import Path
CLI = Path(__file__).resolve().parents[1] / "scripts" / "sigil_forge.py"

def test_policy_check_cli_clean():
    r = subprocess.run(
        [sys.executable, str(CLI), "policy", "check", "--text", "I maintain calm focus"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0
    assert json.loads(r.stdout)["ok"] is True

def test_policy_check_cli_flags_efficacy():
    r = subprocess.run(
        [sys.executable, str(CLI), "policy", "check",
         "--text", "this sigil works and manifests gold"],
        capture_output=True, text=True,
    )
    assert r.returncode == 1
```

- [ ] **Step 2: Implement `cmd_policy`**

```python
def cmd_policy(args):
    from policy_lint import detect_authority_seal_request, lint_efficacy_text
    text = args.text or Path(args.file).read_text(encoding="utf-8")
    eff = lint_efficacy_text(text)
    auth, fam = detect_authority_seal_request(text)
    ok = not eff and not auth
    print(json.dumps({
        "ok": ok,
        "efficacy_hits": eff,
        "authority_seal_request": auth,
        "authority_family": fam,
    }, indent=2, sort_keys=True))
    return 0 if ok else 1
```

Register subparser `policy` → `check` with `--text` / `--file`.

- [ ] **Step 3: Tests pass + commit**

```bash
.venv/bin/python -m pytest tests/test_policy_cli.py -q
git add scripts/sigil_forge.py tests/test_policy_cli.py
git commit -m "feat: policy check CLI for efficacy and authority-seal requests"
```

---

### Task 5: Human-gated ledger review (still no auto-canon)

**Files:**
- Modify: `scripts/receipt.py` (or new `scripts/ledger_canon.py`)
- Modify: `scripts/sigil_forge.py` (`ledger list|promote|export`)
- Create: `schemas/canon-proposal.schema.json`
- Modify: `schemas/learning-ledger-entry.schema.json` (keep PROPOSED const for *ledger file*)
- Modify: `references/receipts-and-ledger.md`
- Create: `tests/test_ledger_promote.py`

**Interfaces:**
- Produces:
  - `export_proposed(limit) -> list[dict]`
  - `promote_entry(entry_id_or_index, *, confirm: str) -> dict`  
    writes `out/sigil-forge/canon-proposals.jsonl` with `canon_status: HUMAN_PROMOTED`  
    **does not** rewrite `references/` or change learning-ledger lines to CANON in-place
- Learning ledger file remains append-only PROPOSED observations
- Promotion requires `--i-confirm PROMOTE` (exact string)

**Design rule:** “Canon” for this skill means **operator-local accepted proposals**, not silent skill mutation. Optional later: human PR that copies proposals into `references/` offline.

- [ ] **Step 1: Write failing tests**

```python
# tests/test_ledger_promote.py
from pathlib import Path
from receipt import append_learning_entry, promote_to_canon_proposal, list_learning

def test_learning_entry_stays_proposed(tmp_path, monkeypatch):
    # point ledger path to tmp
    ...
    e = append_learning_entry(class_="channel_preference", summary="rose path coherent", ...)
    assert e["canon_status"] == "PROPOSED"

def test_promote_requires_confirm(tmp_path):
    try:
        promote_to_canon_proposal(entry, confirm="")
        assert False
    except ValueError:
        pass

def test_promote_writes_proposal_not_references(tmp_path):
    prop = promote_to_canon_proposal(entry, confirm="PROMOTE", out_dir=tmp_path)
    assert prop["canon_status"] == "HUMAN_PROMOTED"
    assert prop["source_canon_status"] == "PROPOSED"
    assert not (tmp_path / "references").exists()  # never touches skill references
```

- [ ] **Step 2: Implement promote path**

```python
# sketch in receipt.py or ledger_canon.py
def promote_to_canon_proposal(entry: dict, *, confirm: str, out_path: Path) -> dict:
    if confirm != "PROMOTE":
        raise ValueError("human confirm required: pass confirm='PROMOTE'")
    if entry.get("canon_status") != "PROPOSED":
        raise ValueError("only PROPOSED entries can be promoted")
    proposal = {
        "schema_version": "1.0.0",
        "kind": "sigil_forge_canon_proposal",
        "ts": ...,
        "canon_status": "HUMAN_PROMOTED",
        "source_canon_status": "PROPOSED",
        "entry": entry,
        "note": "Operator-local proposal only; does not mutate skill references/",
    }
    # append JSONL to out_path
    return proposal
```

CLI:

```bash
python3 scripts/sigil_forge.py ledger --limit 20
python3 scripts/sigil_forge.py ledger promote --index 0 --i-confirm PROMOTE
```

- [ ] **Step 3: Schema for canon proposal**

`schemas/canon-proposal.schema.json`: require `kind`, `canon_status` const `HUMAN_PROMOTED`, `entry`, `ts`.

Keep learning-ledger schema `canon_status` **const PROPOSED** so auto-canon cannot sneak into the observation log.

- [ ] **Step 4: Docs**

Update `references/receipts-and-ledger.md`:

```markdown
## Human promotion (optional)

1. Operator reviews `ledger --limit N`.
2. `ledger promote --index K --i-confirm PROMOTE` appends to `canon-proposals.jsonl`.
3. Agent never runs promote without explicit human confirm string.
4. Promoting does **not** edit `references/` or skill code.
5. Optional offline: human opens a PR to absorb proposals into method docs.
```

- [ ] **Step 5: Tests + commit**

```bash
.venv/bin/python -m pytest tests/test_ledger_promote.py -q
git add scripts/receipt.py scripts/sigil_forge.py schemas/canon-proposal.schema.json \
  references/receipts-and-ledger.md tests/test_ledger_promote.py
git commit -m "feat: human-gated canon proposals; learning ledger stays PROPOSED-only"
```

---

### Task 6: Documentation namespace for authority seals (no geometry)

**Files:**
- Create: `references/authority-seal-namespace.md`
- Modify: `references/distinction-enochian.md`
- Modify: `references/safety-and-framing.md`
- Modify: `references/expansion-spine.md`
- Modify: `SKILL.md` (When not to use + checklist)
- Modify: `README.md` (Safety section — already mentions exclusions; align with new CLI)

- [ ] **Step 1: Write `authority-seal-namespace.md`**

Content requirements (full prose in the file, not TBD):

1. Default forge = intent compression only.  
2. Goetic / Enochian / authority seals are **different artifact families**.  
3. This skill **refuses** to emit them via `construct` / wizard.  
4. Future option A: separate Hermes skill.  
5. Future option B: opt-in module behind `SIGIL_FORGE_ALLOW_AUTHORITY_NAMESPACE=1` **and** explicit CLI that still does not invent MS seals without a corpus — out of scope for geometry in this plan.  
6. Interop may carry `intent_token` only; no doctrine merge.  
7. Agent rule: never rename a Spare monogram as Enochian/Goetic.

- [ ] **Step 2: Expand distinction-enochian.md** with a Goetic subsection mirroring the table for intent vs goetic seals.

- [ ] **Step 3: Safety doc** — link efficacy lint list and `policy check` CLI.

- [ ] **Step 4: expansion-spine** — under Shipped (after implementation) or under Remaining:

```markdown
## Policy machinery (planned → shipped when Tasks 1–5 land)
- Efficacy lint + policy check CLI
- Authority-seal request exclusion (default forge)
- Human-gated canon proposals (no auto-canon, no references/ mutation)
```

- [ ] **Step 5: Commit docs**

```bash
git add references/ SKILL.md README.md
git commit -m "docs: authority-seal namespace, efficacy policy, human canon promotion"
```

---

### Task 7: Eval + doctor + release hygiene

**Files:**
- Modify: `scripts/sigil_forge.py` `cmd_eval` — add cases
- Modify: `scripts/sigil_forge.py` `cmd_check` — require `policy_lint.py` present
- Modify: `VERSION` → `0.11.0` when this track ships
- Modify: `references/expansion-spine.md` current release line

- [ ] **Step 1: Eval cases**

```python
# in cmd_eval
rec("refuse_enochian_request", raises_or_false_construct("Enochian seal ..."))
rec("refuse_efficacy_framing", lint_efficacy_text("this sigil works") != [])
rec("ledger_proposed_only", entry["canon_status"] == "PROPOSED")
```

- [ ] **Step 2: Full verification**

```bash
.venv/bin/python -m pytest -q
python3 scripts/sigil_forge.py check
python3 scripts/sigil_forge.py eval
python3 scripts/validate_hermes_skill.py
```

Expected: all ok / tests pass.

- [ ] **Step 3: Tag release notes in expansion-spine**

```markdown
| v0.11 | Policy track: authority-seal exclusion, efficacy lint, human-gated canon proposals |
```

- [ ] **Step 4: Commit + tag**

```bash
git add VERSION scripts/ references/ tests/
git commit -m "feat: v0.11 policy track — authority exclusion, efficacy lint, human canon"
git tag -a v0.11.0 -m "v0.11.0 product policy machinery"
```

---

## Explicit non-goals of *this* plan

| Non-goal | Why |
|----------|-----|
| Implementing Goetic/Enochian stroke corpora in default construct | Violates product boundary; needs separate skill/corpus program |
| Allowing efficacy claims in practice mode | Forbidden by safety contract |
| Auto-promoting PROPOSED → skill `references/` | Hermes authority is proposal-only |
| Soft-building a “safe” fake Enochian glyph when asked for one | Distinction rule: refuse or redirect, never rename |

---

## Dependency order

```text
Task 1 policy_lint
   ├── Task 2 construct/wizard gates
   ├── Task 3 packet/polish lint
   └── Task 4 policy CLI
Task 5 ledger promote (independent after 1 for shared JSON style)
Task 6 docs (after 2–5 APIs stable)
Task 7 eval/release
```

## Testing matrix

| Case | Expected |
|------|----------|
| Intent “I maintain calm focus” | construct + wizard ok |
| Intent with “Enochian seal” | refuse, no artifacts |
| Intent with “goetic seal” | refuse, no artifacts |
| Framing containing “this sigil works” | lint fail / no packet write |
| `learn` entry | always PROPOSED |
| `ledger promote` without confirm | error |
| `ledger promote --i-confirm PROMOTE` | proposal JSONL only |
| Agent tries to treat ledger as canon | docs + runtime contract forbid |

## Self-review

1. **Spec coverage:** All three domains (authority default exclusion, efficacy forbid, no auto-canon) have tasks; optional human promote does not equal auto-canon.  
2. **Placeholders:** None intentional — patterns and CLI sketches are concrete; implementers may extend pattern lists without changing architecture.  
3. **Types:** `detect_authority_seal_request -> tuple[bool, str | None]`; promote confirm is exact `"PROMOTE"`.

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-08-policy-authority-efficacy-canon.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — this session, task-by-task with checkpoints  

**Which approach?**
