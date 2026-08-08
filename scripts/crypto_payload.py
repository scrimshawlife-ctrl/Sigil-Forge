"""Intent digest and optional AES-GCM sealing (PBKDF2 default; Argon2id optional)."""
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
_ARGON2_TIME = 2
_ARGON2_MEMORY_KIB = 64 * 1024
_ARGON2_PARALLELISM = 2


def intent_digest(normalized: str) -> str:
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def argon2_available() -> bool:
    try:
        import argon2  # noqa: F401

        return True
    except ImportError:
        return False


def derive_key(
    passphrase: str,
    salt: bytes,
    iterations: int = DEFAULT_PBKDF2_ITERATIONS,
    *,
    kdf: str = "pbkdf2-sha256",
) -> bytes:
    """Derive 32-byte AES key. kdf: pbkdf2-sha256 (default) or argon2id if installed."""
    kdf = (kdf or "pbkdf2-sha256").lower()
    if kdf == "argon2id":
        try:
            from argon2.low_level import Type, hash_secret_raw
        except ImportError as exc:
            raise ValueError(
                "argon2id requested but argon2 package not installed; use pbkdf2-sha256"
            ) from exc
        return hash_secret_raw(
            secret=passphrase.encode("utf-8"),
            salt=salt,
            time_cost=_ARGON2_TIME,
            memory_cost=_ARGON2_MEMORY_KIB,
            parallelism=_ARGON2_PARALLELISM,
            hash_len=32,
            type=Type.ID,
        )
    if kdf != "pbkdf2-sha256":
        raise ValueError(f"unsupported kdf: {kdf!r}")
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


def seal_intent(
    plaintext: str,
    passphrase: str,
    *,
    prefer_argon2: bool = False,
) -> dict[str, Any]:
    """Encrypt intent with AES-256-GCM.

    Default KDF is PBKDF2-HMAC-SHA256 (offline stdlib). If prefer_argon2 and
    argon2 is importable, uses Argon2id instead.
    """
    salt = os.urandom(_SALT_LEN)
    nonce = os.urandom(_NONCE_LEN)
    kdf = "pbkdf2-sha256"
    iterations: int | None = DEFAULT_PBKDF2_ITERATIONS
    if prefer_argon2 and argon2_available():
        kdf = "argon2id"
        iterations = None
    key = derive_key(
        passphrase,
        salt,
        iterations if iterations is not None else DEFAULT_PBKDF2_ITERATIONS,
        kdf=kdf,
    )
    ct, tag = aes_gcm_encrypt(key, nonce, plaintext.encode("utf-8"))
    combined = ct + tag
    out: dict[str, Any] = {
        "ciphertext_b64": base64.b64encode(combined).decode("ascii"),
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "salt_b64": base64.b64encode(salt).decode("ascii"),
        "kdf": kdf,
        "alg": "aes-256-gcm",
    }
    if kdf == "pbkdf2-sha256":
        out["iterations"] = DEFAULT_PBKDF2_ITERATIONS
    else:
        out["argon2"] = {
            "time_cost": _ARGON2_TIME,
            "memory_kib": _ARGON2_MEMORY_KIB,
            "parallelism": _ARGON2_PARALLELISM,
        }
    return out


def open_intent(blob: dict[str, Any], passphrase: str) -> str:
    """Decrypt a seal_intent blob; raises on auth failure / wrong passphrase."""
    if blob.get("alg") != "aes-256-gcm":
        raise ValueError(f"unsupported alg: {blob.get('alg')!r}")
    kdf = (blob.get("kdf") or "pbkdf2-sha256").lower()
    if kdf not in ("pbkdf2-sha256", "argon2id"):
        raise ValueError(f"unsupported kdf: {blob.get('kdf')!r}")
    missing = [k for k in _REQUIRED_BLOB_KEYS if k not in blob]
    if missing:
        raise ValueError(f"missing required field(s): {', '.join(missing)}")
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
    if kdf == "pbkdf2-sha256":
        try:
            iterations = int(blob.get("iterations", DEFAULT_PBKDF2_ITERATIONS))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid iterations: {blob.get('iterations')!r}") from exc
        if not (1 <= iterations <= MAX_PBKDF2_ITERATIONS):
            raise ValueError(
                f"iterations must be in [1, {MAX_PBKDF2_ITERATIONS}], got {iterations}"
            )
        key = derive_key(passphrase, salt, iterations, kdf=kdf)
    else:
        key = derive_key(passphrase, salt, kdf=kdf)
    pt = aes_gcm_decrypt(key, nonce, ct, tag)
    return pt.decode("utf-8")
