"""Agrippan planetary seals/characters — distinct from kamea name paths.

Traditional seal: connect successive integers 1→n² on the planetary kamea.
Intelligence / spirit characters: prefer corpus **name_on_kamea** paths using
Agrippan intelligence/spirit names (see references/planetary-character-corpus.json).
Fallback: documented engine reconstructions (odds-then-evens / reverse successive).

These are separate artifact classes from kamea_path(intent). Not Goetic/Enochian.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from kamea import KAMEA_SQUARES, PLANET_ORDER, build_kamea_path, select_square
from planetary_corpus import entity_name_for_path, load_corpus, role_entry


@dataclass
class PlanetarySealArtifact:
    planet: str
    artifact_class: str  # traditional_seal | intelligence_character | spirit_character
    path: list[list[float]]
    successive_values: list[int]
    claimed_historical_status: str
    notes: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
    entity_name: str | None = None
    entity_number: int | None = None

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
            "construction": "successive_1_to_n2",
            "status": "shipped",
            "corpus_id": load_corpus().get("corpus_id"),
        },
    )


def _reconstruction_intelligence(planet: str) -> PlanetarySealArtifact:
    key = planet.strip().lower()
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
            "Fallback reconstruction: odd cells then even cells on the kamea",
            "Not a unique manuscript seal claim",
        ],
        provenance={
            "method_id": f"planetary.intelligence_character.{key}",
            "status": "fallback_reconstruction",
            "family": "planetary_character",
            "determinism": "deterministic",
            "not_kamea_name_path": True,
            "not_traditional_seal": True,
            "construction": "odds_then_evens",
        },
    )


def _reconstruction_spirit(planet: str) -> PlanetarySealArtifact:
    key = planet.strip().lower()
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
            "Fallback reconstruction: reverse successive path n²→1 on the kamea",
            "Not a unique manuscript seal claim",
        ],
        provenance={
            "method_id": f"planetary.spirit_character.{key}",
            "status": "fallback_reconstruction",
            "family": "planetary_character",
            "determinism": "deterministic",
            "not_kamea_name_path": True,
            "not_traditional_seal": True,
            "construction": "reverse_successive",
        },
    )


def _name_on_kamea_character(
    planet: str,
    *,
    kind: str,
) -> PlanetarySealArtifact | None:
    """Build intelligence/spirit path from corpus name on planetary kamea."""
    key = planet.strip().lower()
    try:
        role = role_entry(key, kind)
    except ValueError:
        return None
    construction = (role.get("construction") or "name_on_kamea").strip()
    if construction != "name_on_kamea":
        return None
    try:
        name, name_src = entity_name_for_path(role)
    except ValueError:
        return None

    try:
        # Hebrew names: pass as letters with hebrew_gematria (skips latin translit for pure Hebrew)
        # Latin names: encode via hebrew_gematria latin→hebrew pipeline
        prov = build_kamea_path(
            letters=name,
            square_name=key,
            encoding="hebrew_gematria",
        )
    except ValueError as exc:
        # NOT_COMPUTABLE etc.
        return None

    if not prov.path or not prov.reduced_numeric_sequence:
        return None

    corpus = load_corpus()
    entity_number = role.get("number")
    try:
        entity_number_i = int(entity_number) if entity_number is not None else None
    except (TypeError, ValueError):
        entity_number_i = None

    notes = [
        f"Corpus {kind} via name_on_kamea ({name_src}={name!r})",
        "Distinct from kamea_path(intent) and traditional planetary seal",
    ]
    for n in role.get("notes") or []:
        notes.append(str(n))
    if name_src == "name_hebrew":
        notes.append(f"latin label: {role.get('name_latin')}")

    return PlanetarySealArtifact(
        planet=key,
        artifact_class=kind,
        path=[[float(p[0]), float(p[1])] for p in prov.path],
        successive_values=list(prov.reduced_numeric_sequence),
        claimed_historical_status="corpus_name_path_agrippan",
        notes=notes,
        entity_name=str(role.get("name_latin") or name),
        entity_number=entity_number_i,
        provenance={
            "method_id": f"planetary.{kind}.{key}",
            "status": "corpus_name_on_kamea",
            "family": "planetary_character",
            "determinism": "deterministic",
            "not_kamea_name_path": True,  # not the *intent* kamea path
            "not_traditional_seal": True,
            "construction": "name_on_kamea",
            "corpus_id": corpus.get("corpus_id"),
            "entity_name_latin": role.get("name_latin"),
            "entity_name_hebrew": role.get("name_hebrew"),
            "entity_number": entity_number_i,
            "name_source": name_src,
            "encoding_system": prov.encoding_system,
            "original_numeric_sequence": list(prov.original_numeric_sequence),
            "reduced_numeric_sequence": list(prov.reduced_numeric_sequence),
            "source_tradition": corpus.get("source_tradition"),
        },
    )


def intelligence_character(planet: str) -> PlanetarySealArtifact:
    """Intelligence character: corpus name-on-kamea, else odds→evens reconstruction."""
    key = planet.strip().lower()
    if key not in KAMEA_SQUARES:
        raise ValueError(f"unknown planet {planet!r}")
    art = _name_on_kamea_character(key, kind="intelligence_character")
    if art is not None:
        return art
    fb = _reconstruction_intelligence(key)
    fb.notes.insert(0, "corpus name_on_kamea unavailable; using reconstruction fallback")
    fb.provenance["corpus_id"] = load_corpus().get("corpus_id")
    try:
        role = role_entry(key, "intelligence_character")
        fb.entity_name = role.get("name_latin")
        fb.entity_number = role.get("number")
        fb.provenance["entity_name_latin"] = role.get("name_latin")
        fb.provenance["entity_number"] = role.get("number")
    except ValueError:
        pass
    return fb


def spirit_character(planet: str) -> PlanetarySealArtifact:
    """Spirit character: corpus name-on-kamea, else reverse successive reconstruction."""
    key = planet.strip().lower()
    if key not in KAMEA_SQUARES:
        raise ValueError(f"unknown planet {planet!r}")
    art = _name_on_kamea_character(key, kind="spirit_character")
    if art is not None:
        return art
    fb = _reconstruction_spirit(key)
    fb.notes.insert(0, "corpus name_on_kamea unavailable; using reconstruction fallback")
    fb.provenance["corpus_id"] = load_corpus().get("corpus_id")
    try:
        role = role_entry(key, "spirit_character")
        fb.entity_name = role.get("name_latin")
        fb.entity_number = role.get("number")
        fb.provenance["entity_name_latin"] = role.get("name_latin")
        fb.provenance["entity_number"] = role.get("number")
    except ValueError:
        pass
    return fb


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
