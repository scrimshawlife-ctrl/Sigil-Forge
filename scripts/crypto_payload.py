from __future__ import annotations
import hashlib


def intent_digest(normalized: str) -> str:
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
