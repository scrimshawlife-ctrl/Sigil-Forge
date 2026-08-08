"""Rose-path craft channel (method-inspired letter rose).

Draws a path across a 22-slot rose (matching the traditional Hebrew-letter
rose petal count used in published Rose Cross talisman work). Latin letters
map into the 22 slots via a stable reduction — a structural craft proxy, not
a claim of closed-order initiation or Enochian authority seals.
"""

from __future__ import annotations

import math
import re
from typing import Sequence

# 22 rose slots (0..21). Latin a-z map via (ord-a) % 22 after consonant filter.
ROSE_SLOTS = 22


def letters_for_rose(text: str) -> list[str]:
    """a-z only, vowels stripped (same spirit as Spare), unique first-seen."""
    chars = re.findall(r"[a-z]", text.lower())
    vowels = set("aeiouy")
    out: list[str] = []
    seen: set[str] = set()
    for ch in chars:
        if ch in vowels:
            continue
        if ch in seen:
            continue
        seen.add(ch)
        out.append(ch)
    return out


def letter_to_slot(ch: str) -> int:
    c = ch.lower()
    if not c or not ("a" <= c <= "z"):
        return 0
    return (ord(c) - ord("a")) % ROSE_SLOTS


def slot_point(
    slot: int,
    *,
    cx: float = 50.0,
    cy: float = 50.0,
    radius: float = 28.0,
) -> tuple[float, float]:
    """Place slot on a circle; slot 0 at top (-pi/2)."""
    s = int(slot) % ROSE_SLOTS
    angle = -math.pi / 2.0 + (2.0 * math.pi * s) / ROSE_SLOTS
    return (cx + radius * math.cos(angle), cy + radius * math.sin(angle))


def build_rose_path(
    spare_or_normalized: str,
    *,
    cx: float = 50.0,
    cy: float = 50.0,
    radius: float = 28.0,
    max_points: int = 12,
) -> tuple[list[tuple[float, float]], list[int]]:
    """Return polyline points + slot indices for the rose path.

    Empty letter set → empty path (channel skipped).
    """
    letters = letters_for_rose(spare_or_normalized)[:max_points]
    if not letters:
        # Fall back: use full a-z extract without vowel strip if all vowels
        letters = []
        seen: set[str] = set()
        for ch in re.findall(r"[a-z]", spare_or_normalized.lower()):
            if ch not in seen:
                seen.add(ch)
                letters.append(ch)
            if len(letters) >= max_points:
                break
    if not letters:
        return [], []
    slots = [letter_to_slot(ch) for ch in letters]
    pts = [slot_point(s, cx=cx, cy=cy, radius=radius) for s in slots]
    # Close path softly toward first point for rose cohesion when ≥3
    if len(pts) >= 3:
        pts = pts + [pts[0]]
    return pts, slots


def rose_ring(
    *,
    cx: float = 50.0,
    cy: float = 50.0,
    radius: float = 28.0,
    n: int = ROSE_SLOTS,
) -> list[tuple[float, float]]:
    """Optional decorative ring (not required for channel success)."""
    return [
        slot_point(i, cx=cx, cy=cy, radius=radius)
        for i in range(n)
    ] + [slot_point(0, cx=cx, cy=cy, radius=radius)]
