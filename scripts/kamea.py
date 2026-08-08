"""Planetary kamea (magic squares), Agrippa letter cipher, and path plotting.

Squares are the classic Agrippa / Western occult planetary tables (orders 3–9).
See references/methods-kamea.md for tables and sources.
"""

from __future__ import annotations

# Stable Chaldean order: Saturn 3 … Luna 9
PLANET_ORDER: tuple[str, ...] = (
    "saturn",
    "jupiter",
    "mars",
    "sol",
    "venus",
    "mercury",
    "luna",
)

# Hardcoded Agrippa planetary kamea placements (row-major, top → bottom).
KAMEA_SQUARES: dict[str, list[list[int]]] = {
    # Saturn 3×3 — Lo Shu orientation (magic constant 15)
    "saturn": [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6],
    ],
    # Jupiter 4×4 (magic constant 34)
    "jupiter": [
        [4, 14, 15, 1],
        [9, 7, 6, 12],
        [5, 11, 10, 8],
        [16, 2, 3, 13],
    ],
    # Mars 5×5 (magic constant 65)
    "mars": [
        [11, 24, 7, 20, 3],
        [4, 12, 25, 8, 16],
        [17, 5, 13, 21, 9],
        [10, 18, 1, 14, 22],
        [23, 6, 19, 2, 15],
    ],
    # Sol (Sun) 6×6 (magic constant 111)
    "sol": [
        [6, 32, 3, 34, 35, 1],
        [7, 11, 27, 28, 8, 30],
        [19, 14, 16, 15, 23, 24],
        [18, 20, 22, 21, 17, 13],
        [25, 29, 10, 9, 26, 12],
        [36, 5, 33, 4, 2, 31],
    ],
    # Venus 7×7 (magic constant 175)
    "venus": [
        [22, 47, 16, 41, 10, 35, 4],
        [5, 23, 48, 17, 42, 11, 29],
        [30, 6, 24, 49, 18, 36, 12],
        [13, 31, 7, 25, 43, 19, 37],
        [38, 14, 32, 1, 26, 44, 20],
        [21, 39, 8, 33, 2, 27, 45],
        [46, 15, 40, 9, 34, 3, 28],
    ],
    # Mercury 8×8 (magic constant 260)
    "mercury": [
        [8, 58, 59, 5, 4, 62, 63, 1],
        [49, 15, 14, 52, 53, 11, 10, 56],
        [41, 23, 22, 44, 45, 19, 18, 48],
        [32, 34, 35, 29, 28, 38, 39, 25],
        [40, 26, 27, 37, 36, 30, 31, 33],
        [17, 47, 46, 20, 21, 43, 42, 24],
        [9, 55, 54, 12, 13, 51, 50, 16],
        [64, 2, 3, 61, 60, 6, 7, 57],
    ],
    # Luna (Moon) 9×9 (magic constant 369)
    "luna": [
        [37, 78, 29, 70, 21, 62, 13, 54, 5],
        [6, 38, 79, 30, 71, 22, 63, 14, 46],
        [47, 7, 39, 80, 31, 72, 23, 55, 15],
        [16, 48, 8, 40, 81, 32, 64, 24, 56],
        [57, 17, 49, 9, 41, 73, 33, 65, 25],
        [26, 58, 18, 50, 1, 42, 74, 34, 66],
        [67, 27, 59, 10, 51, 2, 43, 75, 35],
        [36, 68, 19, 60, 11, 52, 3, 44, 76],
        [77, 28, 69, 20, 61, 12, 53, 4, 45],
    ],
}


def letter_to_number(ch: str) -> int:
    """Agrippa-style reduced digital mapping v1: A/J/S=1 … I/R=9, Z=8.

    Only the first character of ``ch`` is used (case-insensitive). Non a–z
    letters raise ValueError.
    """
    if not ch:
        raise ValueError("empty character")
    c = ch[0].lower()
    if c < "a" or c > "z":
        raise ValueError(f"not a letter: {ch!r}")
    # A=1 … I=9, J=1 … R=9, S=1 … Z=8
    return (ord(c) - ord("a")) % 9 + 1


def select_square(digest_hex: str, override: str | None = None) -> str:
    """Choose a planetary square: operator override, else digest mod 7.

    ``digest_hex`` is interpreted as an unsigned hex integer. Index into
    ``PLANET_ORDER`` (Chaldean order). Invalid overrides raise ValueError.
    """
    if override is not None:
        key = override.strip().lower()
        if key not in KAMEA_SQUARES:
            allowed = ", ".join(PLANET_ORDER)
            raise ValueError(f"unknown square {override!r}; allowed: {allowed}")
        return key
    raw = (digest_hex or "").strip().lower()
    if not raw:
        raw = "0"
    try:
        n = int(raw, 16)
    except ValueError as e:
        raise ValueError(f"invalid digest_hex: {digest_hex!r}") from e
    return PLANET_ORDER[n % len(PLANET_ORDER)]


def _find_cell(square: list[list[int]], number: int) -> tuple[int, int] | None:
    """Return (row, col) of ``number`` in square, or None if missing."""
    for r, row in enumerate(square):
        for c, val in enumerate(row):
            if val == number:
                return r, c
    return None


def plot_path(letters: list[str], square_name: str) -> list[tuple[float, float]]:
    """Map letters → Agrippa numbers → cell centers on the named kamea.

    Cell centers use unit cell size: ``(col + 0.5, row + 0.5)`` with
    origin at the top-left cell. Missing numbers are skipped.
    """
    key = square_name.strip().lower()
    if key not in KAMEA_SQUARES:
        allowed = ", ".join(PLANET_ORDER)
        raise ValueError(f"unknown square {square_name!r}; allowed: {allowed}")
    square = KAMEA_SQUARES[key]
    pts: list[tuple[float, float]] = []
    for ch in letters:
        if not ch or not ch[0].isalpha():
            continue
        try:
            num = letter_to_number(ch)
        except ValueError:
            continue
        cell = _find_cell(square, num)
        if cell is None:
            continue
        r, c = cell
        pts.append((c + 0.5, r + 0.5))
    return pts
