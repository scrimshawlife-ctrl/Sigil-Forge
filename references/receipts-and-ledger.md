# Receipts and learning ledger

## Run receipts

Every construct (unless `--no-receipt`) writes:

- `run-receipt.json` in the run directory
- Appends one line to `out/sigil-forge/run-receipts.jsonl` (override with
  `SIGIL_FORGE_RECEIPTS`)

Receipt fields include `intent_digest`, applied/skipped channels, methods,
skill version, and `receipt_hash`. **No plaintext intent** is required on the
receipt when the packet was sealed.

`canon_status` on receipts is `OBSERVATION`.

Schema: `schemas/run-receipt.schema.json`.

## Learning ledger

Operator-submitted observations only — **never auto-promoted to skill canon**.

```bash
python3 scripts/sigil_forge.py learn \
  --class channel_preference \
  --summary "bind_runes + rose_cross_path felt coherent for this intent" \
  --run-id 20260808T120000Z-abcdef01 \
  --channels bind_runes,rose_cross_path

python3 scripts/sigil_forge.py ledger --limit 20
```

Every entry has `canon_status: PROPOSED`. Default path:
`out/sigil-forge/learning-ledger.jsonl` (override `SIGIL_FORGE_LEDGER`).

Schema: `schemas/learning-ledger-entry.schema.json`.

The learning ledger is **append-only PROPOSED observations**. Promotion never
rewrites ledger lines to CANON in place and never edits `references/`.

## Human promotion (optional)

“Canon” here means **operator-local accepted proposals**, not silent skill
mutation. Optional later: a human PR that copies proposals into `references/`
offline.

1. Operator reviews `ledger --limit N` (or `ledger list` / `ledger export`).
2. `ledger promote --index K --i-confirm PROMOTE` appends to
   `out/sigil-forge/canon-proposals.jsonl` (override `SIGIL_FORGE_CANON_PROPOSALS`
   or `--out`).
3. Agent never runs promote without the explicit human confirm string `PROMOTE`.
4. Promoting does **not** edit `references/` or skill code, and does **not**
   change learning-ledger lines (they stay `PROPOSED`).
5. Optional offline: human opens a PR to absorb proposals into method docs.

Proposal records use `canon_status: HUMAN_PROMOTED` and embed the source entry
with `source_canon_status: PROPOSED`. Schema:
`schemas/canon-proposal.schema.json`.

```bash
python3 scripts/sigil_forge.py ledger --limit 20
python3 scripts/sigil_forge.py ledger promote --index 0 --i-confirm PROMOTE
```

## Hermes authority

- Agent may draft learn entries after operator confirmation.
- Agent may **not** rewrite references or treat PROPOSED ledger lines as truth.
- Promotion to canon proposals is human-only and requires `--i-confirm PROMOTE`.
