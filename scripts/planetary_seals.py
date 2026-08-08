"""Agrippan planetary seals/characters — distinct from kamea name paths.

Traditional seal: connect successive integers 1→n² on the planetary kamea.
Intelligence character: deterministic geometric reconstruction — path through
odd cells then even cells (documented engine reconstruction, not a claim of
a unique manuscript seal).
Spirit character: reverse successive path  n²→1 (documented reconstruction).

See Agrippa Book II. These are separate artifact classes from kamea_path(intent).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from kamea import KAMEA_SQUARES, PLANET_ORDER, select_square


@dataclass
class PlanetarySealArtifact:
    planet: str
    artifact_class: str  # traditional_seal | intelligence_character | spirit_character
    path: list[list[float]]
    successive_values: list[int]
    claimed_historical_status: str
    notes: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _find_cell(square: list[list[int]], number: int) -> tuple[int, int] | None:
    for r, row in enumerate(square):
        for c, val in enumerate(row):
            if val == number:
                return r, c
    return None


def _path_for_values(square: list[list[int]], values: list[int]) -> list[list[float]]:
    path: list[list[float]] = []
    for v in values:
        cell = _find_cell(square, v)
        if cell is None:
            raise ValueError(f"kamea missing value {v}")
        r, c = cell
        path.append([float(c + 0.5), float(r + 0.5)])
    return path


def traditional_seal_path(planet: str) -> PlanetarySealArtifact:
    """Connect 1 → 2 → … → n² on the kamea (seal-from-table reconstruction)."""
    key = planet.strip().lower()
    if key not in KAMEA_SQUARES:
        raise ValueError(f"unknown planet {planet!r}; allowed: {', '.join(PLANET_ORDER)}")
    square = KAMEA_SQUARES[key]
    n = len(square)
    n_max = n * n
    values = list(range(1, n_max + 1))
    path = _path_for_values(square, values)
    return PlanetarySealArtifact(
        planet=key,
        artifact_class="traditional_seal",
        path=path,
        successive_values=values,
        claimed_historical_status="historically_aligned_agrippan_character",
        notes=[
            "Path follows successive integers 1..n² on the planetary kamea",
            "Distinct artifact class from kamea_path(intent/name)",
        ],
        provenance={
            "source": "Agrippa Book II planetary tables → seal reconstruction",
            "method_id": f"planetary.traditional_seal.{key}",
            "family": "planetary_character",
            "determinism": "deterministic",
            "not_kamea_name_path": True,
            "status": "shipped",
        },
    )


def intelligence_character(planet: str) -> PlanetarySealArtifact:
    """Deterministic reconstruction: odds ascending then evens ascending.

    Documented engine geometry for a distinct intelligence character path —
    not claimed as the unique historical manuscript glyph.
    """
    key = planet.strip().lower()
    if key not in KAMEA_SQUARES:
        raise ValueError(f"unknown planet {planet!r}")
    square = KAMEA_SQUARES[key]
    n_max = len(square) ** 2
    odds = [v for v in range(1, n_max + 1) if v % 2 == 1]
    evens = [v for v in range(1, n_max + 1) if v % 2 == 0]
    values = odds + evens
    path = _path_for_values(square, values)
    return PlanetarySealArtifact(
        planet=key,
        artifact_class="intelligence_character",
        path=path,
        successive_values=values,
        claimed_historical_status="engine_reconstruction_documented",
        notes=[
            "Intelligence character: odd cells then even cells on the kamea",
            "Engine reconstruction with provenance — not a unique MS seal claim",
        ],
        provenance={
            "method_id": f"planetary.intelligence_character.{key}",
            "status": "shipped_reconstruction",
            "family": "planetary_character",
            "determinism": "deterministic",
            "not_kamea_name_path": True,
            "not_traditional_seal": True,
        },
    )


def spirit_character(planet: str) -> PlanetarySealArtifact:
    """Deterministic reconstruction: reverse successive path n² → 1."""
    key = planet.strip().lower()
    if key not in KAMEA_SQUARES:
        raise ValueError(f"unknown planet {planet!r}")
    square = KAMEA_SQUARES[key]
    n_max = len(square) ** 2
    values = list(range(n_max, 0, -1))
    path = _path_for_values(square, values)
    return PlanetarySealArtifact(
        planet=key,
        artifact_class="spirit_character",
        path=path,
        successive_values=values,
        claimed_historical_status="engine_reconstruction_documented",
        notes=[
            "Spirit character: reverse successive path n²→1 on the kamea",
            "Engine reconstruction with provenance — not a unique MS seal claim",
        ],
        provenance={
            "method_id": f"planetary.spirit_character.{key}",
            "status": "shipped_reconstruction",
            "family": "planetary_character",
            "determinism": "deterministic",
            "not_kamea_name_path": True,
            "not_traditional_seal": True,
        },
    )


# Back-compat aliases
def intelligence_character_stub(planet: str) -> PlanetarySealArtifact:
    return intelligence_character(planet)


def spirit_character_stub(planet: str) -> PlanetarySealArtifact:
    return spirit_character(planet)


def seal_for(
    planet: str,
    *,
    kind: str = "traditional_seal",
    digest_hex: str | None = None,
) -> PlanetarySealArtifact:
    """Factory: traditional_seal | intelligence_character | spirit_character."""
    if planet in (None, "", "auto") and digest_hex:
        planet = select_square(digest_hex)
    kind = (kind or "traditional_seal").strip().lower()
    if kind == "traditional_seal":
        return traditional_seal_path(planet)
    if kind == "intelligence_character":
        return intelligence_character(planet)
    if kind == "spirit_character":
        return spirit_character(planet)
    raise ValueError(f"unknown planetary seal kind {kind!r}")
