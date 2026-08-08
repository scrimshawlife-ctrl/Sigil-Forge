# Noir circuit: intent_commitment (knowledge of intent)

## Statement

Private inputs: padded intent bytes + 32-byte nonce  
Public input: `SHA-256(nonce || intent_bytes[256])`

Matches `scripts/proofs/zk_commit.py` (`sha256-nonce-pad256-v1`).

## Requirements

- [nargo](https://noir-lang.org/) installed
- Core Sigil-Forge Python path works **without** nargo

## Build / prove / verify

```bash
cd zk/noir/intent_commitment
nargo compile
# Prover.toml is written by scripts/proofs/noir_provider.py
nargo prove
nargo verify
```

## Integration

```bash
python3 scripts/sigil_forge.py construct \
  --intent "…" --proof zk-knowledge --passphrase via env
python3 scripts/sigil_forge.py verify-proof out/sigil-forge/<run-id>
```

If nargo is missing, construct still succeeds and the proof-manifest records
`status: skipped` / `detail: noir_unavailable`. A local capsule knowledge
attestation may still be generated for offline operator verification (not ZK).
