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
