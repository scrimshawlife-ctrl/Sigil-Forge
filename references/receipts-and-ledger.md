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

## Hermes authority

- Agent may draft learn entries after operator confirmation.
- Agent may **not** rewrite references or treat PROPOSED ledger lines as truth.
- Promotion to canon is human-only, out of band.
