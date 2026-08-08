"""Agrippan planetary seals/characters — distinct from kamea name paths.

These are traditional planetary *characters* derived from the structure of the
magic squares (connectivity of successive numbers 1→n²), not intent letter paths.

See Agrippa Book II. Intelligence/spirit characters ship as provenance stubs
unless full corpus is expanded later.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from kamea import KAMEA_SQUARES, PLANET_ORDER, select_square


@dataclass
class PlanetarySealArtifact:
    planet: str
    artifact_class: str  # traditional_seal | intelligence_character | spirit_character
    path: list[list[float]]  # cell centers in unit coords
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


def traditional_seal_path(planet: str) -> PlanetarySealArtifact:
    """Draw the planetary seal by connecting 1 → 2 → … → n² on the kamea.

    This is a standard reconstruction of seals *from* the tables (distinct from
    mapping a personal name/intent onto the square).
    """
    key = planet.strip().lower()
    if key not in KAMEA_SQUARES:
        raise ValueError(f"unknown planet {planet!r}; allowed: {', '.join(PLANET_ORDER)}")
    square = KAMEA_SQUARES[key]
    n = len(square)
    n_max = n * n
    values = list(range(1, n_max + 1))
    path: list[list[float]] = []
    for v in values:
        cell = _find_cell(square, v)
        if cell is None:
            raise ValueError(f"kamea {key} missing value {v}")
        r, c = cell
        path.append([float(c + 0.5), float(r + 0.5)])
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
        },
    )


def intelligence_character_stub(planet: str) -> PlanetarySealArtifact:
    """Provenance stub for planetary intelligence character (corpus expansion)."""
    key = planet.strip().lower()
    if key not in KAMEA_SQUARES:
        raise ValueError(f"unknown planet {planet!r}")
    return PlanetarySealArtifact(
        planet=key,
        artifact_class="intelligence_character",
        path=[],
        successive_values=[],
        claimed_historical_status="corpus_stub",
        notes=["Intelligence character geometry not fully expanded in v0.3 corpus"],
        provenance={
            "method_id": f"planetary.intelligence_character.{key}",
            "status": "stub",
            "family": "planetary_character",
        },
    )


def spirit_character_stub(planet: str) -> PlanetarySealArtifact:
    """Provenance stub for planetary spirit character (corpus expansion)."""
    key = planet.strip().lower()
    if key not in KAMEA_SQUARES:
        raise ValueError(f"unknown planet {planet!r}")
    return PlanetarySealArtifact(
        planet=key,
        artifact_class="spirit_character",
        path=[],
        successive_values=[],
        claimed_historical_status="corpus_stub",
        notes=["Spirit character geometry not fully expanded in v0.3 corpus"],
        provenance={
            "method_id": f"planetary.spirit_character.{key}",
            "status": "stub",
            "family": "planetary_character",
        },
    )


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
        return intelligence_character_stub(planet)
    if kind == "spirit_character":
        return spirit_character_stub(planet)
    raise ValueError(f"unknown planetary seal kind {kind!r}")
