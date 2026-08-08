"""Fuse Spare monogram + kamea path into a single layout."""

from __future__ import annotations

import math
from dataclasses import dataclass

from kamea import KAMEA_SQUARES, plot_path, select_square
from spare import letter_sequence, reduce_letters

# Canvas is always 0..100
CANVAS = 100.0
VIEW_BOX = (0.0, 0.0, CANVAS, CANVAS)

# Monogram sits on an outer circle around canvas center
_MONOGRAM_CX = CANVAS / 2.0
_MONOGRAM_CY = CANVAS / 2.0
_MONOGRAM_RADIUS = 40.0

# Kamea scaled into concentric inner region (0.35–0.65 of canvas)
_INNER_LO = 0.35 * CANVAS
_INNER_HI = 0.65 * CANVAS
_INNER_SPAN = _INNER_HI - _INNER_LO


@dataclass(frozen=True)
class Layout:
    monogram_points: list[tuple[float, float]]
    kamea_points: list[tuple[float, float]]
    view_box: tuple[float, float, float, float]
    spare_letters: str
    square_name: str


def _monogram_on_circle(letters: list[str]) -> list[tuple[float, float]]:
    """Place unique letters on a circle (equal angles) in sequence order."""
    n = len(letters)
    if n == 0:
        return []
    pts: list[tuple[float, float]] = []
    for i in range(n):
        # Start at top (-pi/2), equal steps; closed=False (polyline open)
        angle = -math.pi / 2.0 + (2.0 * math.pi * i) / n
        x = _MONOGRAM_CX + _MONOGRAM_RADIUS * math.cos(angle)
        y = _MONOGRAM_CY + _MONOGRAM_RADIUS * math.sin(angle)
        pts.append((x, y))
    return pts


def _scale_kamea(
    raw: list[tuple[float, float]], square_name: str
) -> list[tuple[float, float]]:
    """Scale plot_path unit-cell coords into the inner 0.35–0.65 region."""
    if not raw:
        return []
    order = len(KAMEA_SQUARES[square_name])
    if order <= 0:
        return []
    out: list[tuple[float, float]] = []
    for x, y in raw:
        sx = _INNER_LO + (x / order) * _INNER_SPAN
        sy = _INNER_LO + (y / order) * _INNER_SPAN
        out.append((sx, sy))
    return out


def build_layout(
    normalized: str,
    digest_hex: str,
    square_override: str | None = None,
) -> Layout:
    """Compose Spare monogram + kamea path into one layout (canvas 0..100)."""
    letters = letter_sequence(normalized)
    spare = reduce_letters(normalized)
    square_name = select_square(digest_hex, override=square_override)
    mono = _monogram_on_circle(letters)
    raw_kamea = plot_path(letters, square_name)
    kamea = _scale_kamea(raw_kamea, square_name)
    return Layout(
        monogram_points=mono,
        kamea_points=kamea,
        view_box=VIEW_BOX,
        spare_letters=spare,
        square_name=square_name,
    )
