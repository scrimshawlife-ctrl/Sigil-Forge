# Sigil Forge — Proof of Intent Implementation Plan

> **For agentic workers:** Use subagent-driven-development or executing-plans. Checkbox tasks for tracking.

**Goal:** Extend Sigil-Forge so a public artifact can bind to a privacy-preserving **intent commitment** and (optionally) a **ZK proof of knowledge**, without replacing the existing deterministic forge, digests, stego, or offline path.

**Architecture:** Layer new crypto surfaces onto construct→stego→packet→receipt→wallpaper→verify. Keep `intent_digest = SHA-256(normalized_intent)` as compatibility / forge-determinism identity. Add salted `intent_commitment` as privacy binding. Introduce domain-separated HKDF, intent capsules, Merkle `sigil_root`, versioned stego envelopes, pluggable `ProofProvider`, then Noir knowledge-of-intent MVP. Core Python never hard-depends on Node/Rust/Noir/zkVM.

**Tech Stack:** Python 3.10+ stdlib (`hashlib`, `hmac`, pure AES-GCM), optional `argon2-cffi`, optional external `nargo` for ZK only.

---

## Gate 0 — Architecture freeze (verified in live repo)

| Claim | Evidence |
|-------|----------|
| Current release | `VERSION` = **0.11.0** (policy track already shipped) |
| Digest | `crypto_payload.intent_digest` → SHA-256 hex of UTF-8 normalized intent |
| Seal | AES-256-GCM (`aes_gcm_pure`); default **PBKDF2-HMAC-SHA256** 200k; optional **Argon2id** via `prefer_argon2` |
| PNG stego | Magic `SF1\0` + 32-byte digest (+ optional sealed blob) |
| Wallpaper seed | Hash of `intent_digest|surface|mode|theme|schema` (not domain-separated) |
| Verify | Recovers digest from SVG/PNG; epsilon/metric cross-checks |
| Policy | Authority-seal exclusion + efficacy lint + human canon (do not regress) |

### Dataflow today

```text
intent → safety + authority gate → normalize → intent_digest
  → optional AES-GCM seal (packet only)
  → fuse layout (geometry from digest)
  → SVG stego + PNG LSB (SF1+digest)
  → forge-packet + run-receipt
  → optional wallpaper (seed from digest)
  → verify recovers digest
```

### Version numbering (critical)

**Do not label Proof-of-Intent as v0.11** — that tag is the policy track.

| Release | Scope |
|---------|--------|
| **v0.12.0** | Domains + salted commitment + capsule + Argon2 auto + artifact root + forge-manifest |
| **v0.12.1** | SF11 root embedding + wallpaper/receipt binding + `inspect` |
| **v0.12.2** | ProofProvider + Noir knowledge-of-intent MVP + `verify-proof` |
| **v0.12.x** | Hardening / dual ZK commitment |
| **v0.13.0-exp** | zkVM restricted forge-proof adapter (optional) |

---

## Global constraints

1. **Extend, do not replace** — old artifacts remain verifiable.
2. **Offline-first core** — no Node/Rust/Noir required for construct/verify/open.
3. **No plaintext intent** in public media by default.
4. **No homegrown crypto** — stdlib hash/HMAC/HKDF, existing AES-GCM, optional Argon2id, standard ZK black-boxes only.
5. **Retain `intent_digest`** for forge determinism and SF1 stego.
6. **Commitment nonce never public** — capsule or private state only.
7. **Merkle root must not include itself** (no circular packet hash).
8. **ZK optional** — missing Noir ⇒ skip, forge still succeeds.
9. **No efficacy claims** — proofs are provenance only.
10. **No authority seals** in default forge (policy track stands).

---

## Frozen design decisions

### D1 — Digest vs commitment

| ID | Formula | Role |
|----|---------|------|
| `intent_digest` | `SHA-256(UTF-8(normalized))` | Forge geometry, legacy stego, compat |
| `intent_commitment` | `SHA-256(domain ‖ nonce ‖ UTF-8(normalized))` | Privacy binding; public; per-run |

**Geometry keeps using `intent_digest`.** Using commitment for layout would make the same intent produce different monograms each run (random nonce) and break craft determinism.

### D2 — Merkle leaves (no self-reference)

Leaves (type-tagged, sorted lexicographically by type):

```text
intent_commitment
intent_digest
method_manifest_digest
canonical_glyph_digest
forge_manifest_digest      # public config+outputs WITHOUT root
ciphertext_digest          # if capsule
wallpaper_spec_digest      # if wallpaper in-run
proof_manifest_digest      # public fields only, if proof
```

**Not leaves:** `run-receipt.json`, packet fields that embed `sigil_root`, proof binary blobs.

### D3 — Artifact split

```text
forge-manifest.json   # hashed into root (no sigil_root field)
forge-packet.json     # may cite sigil_root + capsule paths
intent-capsule.json   # sealed witness (passphrase)
run-receipt.json      # records root; not a leaf
proofs/…              # optional
```

### D4 — Dual commitment (ZK only, v0.12.2+)

v0.12.0 ships SHA-256 salted commitment only. v0.12.2 may add optional `intent_commitment_zk` (Poseidon/Pedersen in Noir), bound to conventional commitment inside the capsule.

### D5 — Wallpaper seed

Keep digest-based seed for reproducible atmosphere (compat). Add `intent_commitment` + `sigil_root` to wallpaper receipts. Optional later: commitment-based seed behind a flag (unlinkable re-forges).

---

## File map

| Path | Role |
|------|------|
| `scripts/crypto_domains.py` | Domain constants + domain_join / domain_sha256 |
| `scripts/commitment.py` | Salted commitment generate/verify |
| `scripts/derivation.py` | HKDF-SHA256 (RFC 5869) |
| `scripts/intent_capsule.py` | Capsule build/open |
| `scripts/artifact_root.py` | Binary Merkle → sigil_root |
| `scripts/forge_manifest.py` | Deterministic public manifest |
| `scripts/forge_core.py` | Pure compute boundary (extract gradually) |
| `scripts/stego_envelope.py` | SF11 + dual verify with SF1 |
| `scripts/proofs/*` | ProofProvider abstraction + noir adapter |
| `zk/noir/intent_commitment/` | Circuit + test vectors |
| `schemas/intent-capsule.schema.json` | Capsule |
| `schemas/artifact-root.schema.json` | Root + leaves |
| `schemas/forge-manifest.schema.json` | Manifest |
| `schemas/proof-manifest.schema.json` | Proof metadata |
| Modify construct, crypto_payload, stego_*, verify, wallpaper, CLI, tests, docs |

---

## Phase 1 — Domain separation (v0.12.0)

**Domains (exact bytes):**

```python
INTENT_COMMITMENT_V1 = b"SIGIL-FORGE/INTENT-COMMITMENT/V1"
ARTIFACT_ROOT_V1     = b"SIGIL-FORGE/ARTIFACT-ROOT/V1"
MERKLE_LEAF_V1       = b"SIGIL-FORGE/MERKLE-LEAF/V1"
MERKLE_NODE_V1       = b"SIGIL-FORGE/MERKLE-NODE/V1"
WALLPAPER_SEED_V1    = b"SIGIL-FORGE/WALLPAPER-SEED/V1"
STEGO_PAYLOAD_V1     = b"SIGIL-FORGE/STEGO/V1"
FORGE_SEED_V1        = b"SIGIL-FORGE/FORGE-SEED/V1"
PROOF_BINDING_V1     = b"SIGIL-FORGE/ZK-PROOF/V1"
```

**API:** `encode_u32`, `domain_join(domain, *parts)`, `domain_sha256(domain, *parts)`.

**Tests:** Golden vectors; variable-length part ambiguity resistance.

---

## Phase 2 — Salted commitment (v0.12.0)

```text
C = SHA256(domain_join(INTENT_COMMITMENT_V1, nonce32, utf8(normalized)))
```

Public: `{scheme: sha256-salted-v1, commitment, domain}`.  
Private: `nonce` only in capsule or private witness.

**Construct wiring:** Always compute commitment; packet gains `intent_commitment` + `compatibility.intent_digest`.  
**PoI mode:** `--proof commitment` requires passphrase (seal capsule) or explicit risk-acknowledged private witness file.

**Tests:** Fixed nonce golden; different nonce → different C; public artifacts never contain nonce.

---

## Phase 3 — Intent capsule (v0.12.0)

Schema `intent-capsule.schema.json`. Sealed witness includes intent, normalized_intent, commitment_nonce, created_at.  
Reuse AES-GCM seal path; prefer Argon2id when available.  
Public shell includes commitment, intent_digest, public_bindings (forge_version, method_manifest_digest, artifact_root).

**Tests:** Round-trip; wrong passphrase fails; no plaintext in public shell.

---

## Phase 4 — Argon2id preferred (v0.12.0)

```text
--kdf auto|argon2id|pbkdf2-sha256
default auto → argon2id if importable else pbkdf2
crypto_version = 2 for new seals
```

Keep PBKDF2 open path for legacy. Do not remove PBKDF2.

---

## Phase 5 — HKDF derivation (v0.12.0)

Pure-Python HKDF-SHA256. Derive public channel seeds from commitment bytes + domain info.  
Do **not** re-seed Spare/kamea geometry from commitment.

**Tests:** RFC 5869 vectors; domain separation.

---

## Phase 6 — Artifact root (v0.12.0)

Binary Merkle with typed leaves; odd pad by duplicating last.  
`forge-manifest.json` hashed; **must not contain** `sigil_root`.  
Receipt/packet may record resulting root.

**Tests:** Stable root; leaf add changes root; circular inclusion unit-test fails closed.

---

## Phase 7 — SF11 root embedding (v0.12.1)

New payload envelope alongside SF1:

```text
if SF1 → intent_digest (legacy)
if SF11 → sigil_root (+ optional cross-check vs receipt)
```

SVG metadata + PNG LSB both support dual path.

---

## Phase 8 — Wallpaper binding (v0.12.1)

Wallpaper receipt gains `intent_commitment`, `sigil_root`, existing glyph/spec digests.  
Seed stays digest-based for compat unless opt-in commitment seed.

---

## Phase 9 — Proof abstraction (v0.12.2)

```python
class ProofProvider:
    def available(self) -> bool: ...
    def prove(self, witness, public_inputs) -> ProofResult: ...
    def verify(self, proof, public_inputs) -> bool: ...
```

Providers: `none`, later `noir`, later `risc0`.  
CLI: `--proof none|commitment|zk-knowledge`; `zk-forge` → explicit `NOT_IMPLEMENTED`.

---

## Phase 10–12 — Noir knowledge MVP (v0.12.2)

Circuit proves only knowledge of (intent, len, nonce) for ZK-friendly hash = public C_zk.  
`MAX_INTENT_BYTES = 256`, zero-padded, circuit checks padding.  
`zk/noir/intent_commitment/` + `noir_provider.py`; skip if nargo missing.

**Never claim functional ZK unless prove + independent verify-proof both pass.**

---

## Phase 13 — Verification UX

```bash
sigil_forge.py verify-proof <run-dir>
sigil_forge.py inspect <artifact>
```

JSON machine-readable; never print plaintext intent.

---

## Phase 14–15 — forge_manifest + forge_core

Extract pure `compute_forge(normalized, config) -> ForgeResult` with no FS/time/random/env/network. Construct becomes I/O shell. Prerequisite for future zkVM forge proof.

---

## CLI additions (summary)

```bash
construct --kdf auto|argon2id|pbkdf2-sha256
construct --proof none|commitment|zk-knowledge
open --capsule path
verify-proof <run>
inspect <glyph|wallpaper>
```

---

## Security assumptions (document)

1. Commitment hides intent only if nonce stays secret.  
2. `intent_digest` still allows dictionary attacks on low-entropy intents if leaked.  
3. ZK proves knowledge of preimage, not efficacy.  
4. Pure-Python AES is intentional offline tradeoff.  
5. Argon2 params are offline defaults, not HSM-grade.

---

## Explicit non-goals

No blockchain/NFT/cloud proof default; no replacing digest for geometry; no full forge in Noir in v0.12; no efficacy claims; no authority seals; no homegrown crypto.

---

## PR sequence

```text
PR A v0.12.0  domains + commitment + derivation + capsule + argon2 auto + merkle + manifest
PR B v0.12.1  SF11 stego + dual verify + wallpaper binding + inspect
PR C v0.12.2  ProofProvider + Noir circuit + verify-proof
PR D later    dual ZK commitment, zkVM adapter
```

---

## Test matrix (every claim executable)

Domain join goldens · commitment fixed-nonce · nonce absent from public media · SF1 regression · SF11 round-trip · Merkle non-circular · Argon2 auto / PBKDF2 fallback · capsule open/fail · wallpaper geometry_preserved · Noir missing skips · Noir present optional · policy_lint regression.

---

## Success criteria

- Legacy verify of v0.10/v0.11 artifacts still green.  
- New run can emit commitment + capsule + sigil_root offline without Noir.  
- Proof path reported functional only if generate + verify both pass.  
- Plaintext intent never in public carriers by default.
