"""Intent digest and optional AES-GCM sealing (PBKDF2 key derivation)."""
from __future__ import annotations

import base64
import hashlib
import os
from typing import Any

from aes_gcm_pure import aes_gcm_decrypt, aes_gcm_encrypt

DEFAULT_PBKDF2_ITERATIONS = 200_000
MAX_PBKDF2_ITERATIONS = 1_000_000
_SALT_LEN = 16
_NONCE_LEN = 12  # standard 96-bit GCM IV
_TAG_LEN = 16
_REQUIRED_BLOB_KEYS = ("salt_b64", "nonce_b64", "ciphertext_b64")


def intent_digest(normalized: str) -> str:
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def derive_key(
    passphrase: str,
    salt: bytes,
    iterations: int = DEFAULT_PBKDF2_ITERATIONS,
) -> bytes:
    """PBKDF2-HMAC-SHA256 → 32-byte AES-256 key."""
    if not (1 <= iterations <= MAX_PBKDF2_ITERATIONS):
        raise ValueError(
            f"iterations must be in [1, {MAX_PBKDF2_ITERATIONS}], got {iterations}"
        )
    return hashlib.pbkdf2_hmac(
        "sha256",
        passphrase.encode("utf-8"),
        salt,
        iterations,
        dklen=32,
    )


def seal_intent(plaintext: str, passphrase: str) -> dict[str, Any]:
    """Encrypt intent with AES-256-GCM; key from PBKDF2-HMAC-SHA256.

    Returns a dict suitable for embedding as optional ciphertext channel:
    ciphertext_b64 includes ciphertext||tag (standard combined form).
    """
    salt = os.urandom(_SALT_LEN)
    nonce = os.urandom(_NONCE_LEN)
    key = derive_key(passphrase, salt)
    ct, tag = aes_gcm_encrypt(key, nonce, plaintext.encode("utf-8"))
    combined = ct + tag
    return {
        "ciphertext_b64": base64.b64encode(combined).decode("ascii"),
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "salt_b64": base64.b64encode(salt).decode("ascii"),
        "kdf": "pbkdf2-sha256",
        "alg": "aes-256-gcm",
        "iterations": DEFAULT_PBKDF2_ITERATIONS,
    }


def open_intent(blob: dict[str, Any], passphrase: str) -> str:
    """Decrypt a seal_intent blob; raises on auth failure / wrong passphrase."""
    if blob.get("alg") != "aes-256-gcm":
        raise ValueError(f"unsupported alg: {blob.get('alg')!r}")
    if blob.get("kdf") != "pbkdf2-sha256":
        raise ValueError(f"unsupported kdf: {blob.get('kdf')!r}")
    missing = [k for k in _REQUIRED_BLOB_KEYS if k not in blob]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")
    try:
        iterations = int(blob.get("iterations", DEFAULT_PBKDF2_ITERATIONS))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid iterations: {blob.get('iterations')!r}") from exc
    if not (1 <= iterations <= MAX_PBKDF2_ITERATIONS):
        raise ValueError(
            f"iterations must be in [1, {MAX_PBKDF2_ITERATIONS}], got {iterations}"
        )
    salt = base64.b64decode(blob["salt_b64"])
    nonce = base64.b64decode(blob["nonce_b64"])
    combined = base64.b64decode(blob["ciphertext_b64"])
    if len(salt) != _SALT_LEN:
        raise ValueError(f"salt must be {_SALT_LEN} bytes, got {len(salt)}")
    if len(nonce) != _NONCE_LEN:
        raise ValueError(f"nonce must be {_NONCE_LEN} bytes, got {len(nonce)}")
    if len(combined) < _TAG_LEN:
        raise ValueError("ciphertext too short")
    ct, tag = combined[:-_TAG_LEN], combined[-_TAG_LEN:]
    key = derive_key(passphrase, salt, iterations=iterations)
    pt = aes_gcm_decrypt(key, nonce, ct, tag)
    return pt.decode("utf-8")
