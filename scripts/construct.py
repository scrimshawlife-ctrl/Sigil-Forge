"""Full construct pipeline: safety → normalize → digest → fuse → stego → packet."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

from crypto_payload import intent_digest, seal_intent
from fuse import build_layout
from kamea import DEFAULT_KAMEA_ENCODING, KAMEA_SQUARES
from normalize import normalize_intent
from ontology import assert_not_entity_seal_request, default_packet_ontology
from packet import build_packet, validate_packet, write_packet_files
from paths import default_out_dir, make_run_id, run_dir as make_run_dir, skill_root
from safety import check_intent
from spare import reduce_letters
from stego_png import embed_lsb, pack_payload
from stego_svg import embed as stego_svg_embed
from svg_export import layout_to_svg

# Env passphrase avoids argv exposure (process list / shell history).
PASSPHRASE_ENV = "SIGIL_FORGE_PASSPHRASE"


def resolve_passphrase(explicit: str | None = None) -> str | None:
    """CLI/explicit passphrase wins; else ``SIGIL_FORGE_PASSPHRASE`` env."""
    if explicit is not None and str(explicit) != "":
        return str(explicit)
    env = os.environ.get(PASSPHRASE_ENV)
    if env is not None and env != "":
        return env
    return None

SCHEMA_VERSION = "1.2"

_CHANNEL_ORDER = (
    "spare_monogram",
    "kamea_path",
    "kamea_square_choice",
    "bind_runes",
    "rose_cross_path",
    "planetary_seal",
    "intent_digest",
    "optional_ciphertext",
    "svg_metadata",
    "path_epsilon",
    "path_order",
    "metric_quantize",
    "png_lsb",
    "gen_seed",
)


def _ch(cid: str, status: str, detail: str) -> dict[str, str]:
    return {"id": cid, "status": status, "detail": detail}


# Phrase-scan threshold: short normalized intents skip substring scan (stego
# never embeds them; short strings false-positive against hex/coords/metadata).
_PRIVACY_PHRASE_MIN_LEN = 12
_PRIVACY_SPARE_MIN_LEN = 4


def _assert_svg_privacy(svg: str, *, normalized: str, spare: str) -> None:
    """Raise RuntimeError if public SVG appears to leak intent or spare letters.

    Short intents (len < 12) skip the phrase scan — stego path never embeds
    plaintext intent. Spare letter runs are checked when len >= 4.
    """
    svg_low = svg.lower()
    if len(normalized) >= _PRIVACY_PHRASE_MIN_LEN and normalized in svg_low:
        raise RuntimeError("public SVG leaked normalized intent")
    spare_low = (spare or "").lower()
    if len(spare_low) >= _PRIVACY_SPARE_MIN_LEN and spare_low in svg_low:
        raise RuntimeError("public SVG leaked spare letters")


def _merge_channels(
    craft: list[dict[str, str]],
    stego: list[dict[str, str]],
    extras: list[dict[str, str]],
) -> list[dict[str, str]]:
    by_id: dict[str, dict[str, str]] = {}
    for c in craft + stego + extras:
        by_id[c["id"]] = c
    ordered = [by_id[i] for i in _CHANNEL_ORDER if i in by_id]
    # Any unexpected ids after known order
    for cid, c in by_id.items():
        if cid not in _CHANNEL_ORDER:
            ordered.append(c)
    return ordered


def _try_png_lsb(
    svg: str,
    digest_hex: str,
    out_png: Path,
    *,
    monogram_points: list[tuple[float, float]] | None = None,
    kamea_points: list[tuple[float, float]] | None = None,
) -> tuple[str | None, dict[str, str]]:
    """Rasterize + LSB embed when possible; else skip with reason.

    Prefer stdlib layout raster (filter-0 RGB, always LSB-compatible). Fall
    back to optional SVG backends, re-encoding when needed.

    Public PNG payload is digest-only (``pack_payload(digest)``). Full seal
    blob stays in the local forge packet.
    """
    png_bytes: bytes | None = None
    source = "none"

    # 1. Stdlib layout geometry → filter-0 RGB PNG (Hermes offline default)
    if monogram_points is not None or kamea_points is not None:
        try:
            from layout_raster import layout_to_png_bytes

            png_bytes = layout_to_png_bytes(
                monogram_points or [],
                kamea_points or [],
            )
            source = "layout_raster"
        except Exception:  # noqa: BLE001
            png_bytes = None

    # 2. Optional SVG raster backends
    if not png_bytes:
        try:
            from raster_svg import svg_to_png_bytes

            png_bytes = svg_to_png_bytes(svg)
            source = "svg_backend" if png_bytes else "none"
        except Exception as exc:  # noqa: BLE001
            return None, _ch("png_lsb", "skipped", f"raster_error: {exc}")

    if not png_bytes:
        return None, _ch("png_lsb", "skipped", "no_raster_backend")

    # If backend PNG is not filter-0 RGB, re-encode via layout when available
    digest_raw = bytes.fromhex(digest_hex)
    payload = pack_payload(digest_raw)
    try:
        stego_png = embed_lsb(png_bytes, payload)
    except Exception:
        # Retry with pure layout raster if external PNG was incompatible
        if source != "layout_raster" and (
            monogram_points is not None or kamea_points is not None
        ):
            try:
                from layout_raster import layout_to_png_bytes

                png_bytes = layout_to_png_bytes(
                    monogram_points or [],
                    kamea_points or [],
                )
                stego_png = embed_lsb(png_bytes, payload)
                source = "layout_raster_retry"
            except Exception as exc:  # noqa: BLE001
                return None, _ch("png_lsb", "skipped", f"embed_failed: {exc}")
        else:
            return None, _ch("png_lsb", "skipped", "embed_failed: incompatible_png")

    out_png.write_bytes(stego_png)
    return str(out_png), _ch(
        "png_lsb",
        "applied",
        f"LSB digest-only {len(payload)} bytes via {source}",
    )


def run(
    intent: str,
    *,
    mode: str = "creative",
    out_root: Path | str | None = None,
    passphrase: str | None = None,
    square: str | None = None,
    seal_packet: bool = False,
    write_polish: bool = False,
    polish_style: str | None = None,
    write_receipt: bool = True,
    kamea_encoding: str | None = None,
    spare_mode: str = "letter_monogram",
    planetary_seal: bool = False,
    planetary_seal_kind: str = "traditional_seal",
) -> dict[str, Any]:
    """Orchestrate full forge: safety → normalize → digest → seal? → fuse → stego → packet.

    Writes under ``out_root/<run-id>/``:
      glyph.svg, glyph.png (when raster ok), forge-packet.json/md,
      run-receipt.json (default), optional polish_prompt.json when ``write_polish``.

    Returns the forge-packet dict. Raises ValueError on harmful/empty intent.
    """
    if mode not in ("creative", "practice"):
        raise ValueError(f"mode must be 'creative' or 'practice', got {mode!r}")

    passphrase = resolve_passphrase(passphrase)
    if seal_packet and not passphrase:
        raise ValueError(
            "seal_packet=True requires passphrase "
            f"(--passphrase or ${PASSPHRASE_ENV})"
        )

    ok, reason = check_intent(intent)
    if not ok:
        raise ValueError(reason or "refused: harmful intent")
    assert_not_entity_seal_request(intent)

    normalized = normalize_intent(intent)
    digest = intent_digest(normalized)
    enc = (kamea_encoding or DEFAULT_KAMEA_ENCODING).strip().lower()

    craft_channels: list[dict[str, str]] = []
    sealed_blob: dict[str, Any] | None = None

    # --- optional ciphertext (local packet only; not embedded in public PNG) ---
    if passphrase:
        sealed_blob = seal_intent(intent, passphrase)
        craft_channels.append(
            _ch(
                "optional_ciphertext",
                "applied",
                f"aes-256-gcm pbkdf2-sha256 iter={sealed_blob.get('iterations')}",
            )
        )
        key_policy = "passphrase"
        crypto = {
            "algorithm": "aes-256-gcm",
            "kdf": "pbkdf2-sha256",
            "key_policy": key_policy,
            "ciphertext_present": True,
        }
    else:
        craft_channels.append(
            _ch("optional_ciphertext", "skipped", "no_passphrase")
        )
        crypto = {
            "algorithm": "none",
            "key_policy": "none",
            "ciphertext_present": False,
        }

    craft_channels.append(
        _ch("intent_digest", "applied", f"sha256 hex len={len(digest)}")
    )

    # --- fuse layout ---
    layout = build_layout(
        normalized,
        digest,
        square_override=square,
        kamea_encoding=enc,
        spare_mode=spare_mode,
        include_planetary_seal=planetary_seal,
        planetary_seal_kind=planetary_seal_kind,
    )
    spare = layout.spare_letters or reduce_letters(normalized)
    square_name = layout.square_name
    order = len(KAMEA_SQUARES[square_name])

    # Dual craft empty → fail closed (no fake empty glyph)
    if (not layout.monogram_points and not layout.kamea_points) or (
        not spare and not layout.kamea_points
    ):
        raise ValueError(
            "NOT_COMPUTABLE: no monogram or kamea craft geometry after letter "
            "reduction (e.g. all-vowel / no surviving consonants). Rewrite the "
            "intent in present tense with consonants that survive Spare "
            "reduction (drop vowels/y and duplicate letters), then re-run construct."
        )

    if layout.monogram_points:
        craft_channels.append(
            _ch(
                "spare_monogram",
                "applied",
                f"letters={len(spare)} points={len(layout.monogram_points)}",
            )
        )
    else:
        craft_channels.append(
            _ch("spare_monogram", "skipped", "no_letters_after_reduction")
        )

    if layout.kamea_points:
        craft_channels.append(
            _ch(
                "kamea_path",
                "applied",
                f"planet={square_name} points={len(layout.kamea_points)}",
            )
        )
    else:
        craft_channels.append(
            _ch("kamea_path", "skipped", "no_path_points")
        )

    choice_src = "operator_override" if square else "digest_mod"
    craft_channels.append(
        _ch(
            "kamea_square_choice",
            "applied",
            f"planet={square_name} order={order} via={choice_src}",
        )
    )

    # Bind-runes + Rose Cross expansion craft channels
    if layout.bind_polylines and layout.bind_runes:
        craft_channels.append(
            _ch(
                "bind_runes",
                "applied",
                f"runes={len(layout.bind_runes)} strokes={len(layout.bind_polylines)}",
            )
        )
    else:
        craft_channels.append(
            _ch("bind_runes", "skipped", "no_runes_after_mapping")
        )

    if layout.rose_points and len(layout.rose_points) >= 1:
        craft_channels.append(
            _ch(
                "rose_cross_path",
                "applied",
                f"hebrew_petals={len(layout.rose_slots)} points={len(layout.rose_points)}",
            )
        )
    else:
        craft_channels.append(
            _ch("rose_cross_path", "skipped", "no_rose_path_points")
        )

    if planetary_seal and layout.planetary_seal_path:
        craft_channels.append(
            _ch(
                "planetary_seal",
                "applied",
                f"kind={planetary_seal_kind} planet={square_name} "
                f"points={len(layout.planetary_seal_path)}",
            )
        )
    else:
        craft_channels.append(
            _ch(
                "planetary_seal",
                "skipped",
                "not_requested" if not planetary_seal else "empty_seal",
            )
        )

    # --- SVG + stego ---
    base_svg = layout_to_svg(layout)
    stego_svg, stego_channels = stego_svg_embed(base_svg, digest, spare_letters=spare)

    # Privacy guard: public SVG must not leak plaintext intent or spare runs.
    # Short normalized intents (len < 12) skip the phrase scan — stego never
    # embeds them, and short substrings false-positive against hex/metadata.
    _assert_svg_privacy(stego_svg, normalized=normalized, spare=spare)

    # --- atomic run dir: stage under out_root, promote only after full success ---
    root = Path(out_root) if out_root is not None else default_out_dir()
    root.mkdir(parents=True, exist_ok=True)
    rid = make_run_id(digest)
    final_dir = make_run_dir(root, rid)
    staging = Path(
        tempfile.mkdtemp(prefix=f".sf-staging-{rid}-", dir=str(root))
    )

    try:
        svg_path = staging / "glyph.svg"
        svg_path.write_text(stego_svg, encoding="utf-8")

        # Prefer layout raster including bind/rose geometry
        png_path_str, png_channel = _try_png_lsb(
            stego_svg,
            digest,
            staging / "glyph.png",
            monogram_points=list(layout.monogram_points),
            kamea_points=list(layout.kamea_points),
        )
        # Re-apply with full layout if simple mono/kamea path was used
        if png_path_str and (layout.bind_polylines or layout.rose_points):
            try:
                from layout_raster import layout_to_png_bytes
                from stego_png import embed_lsb, pack_payload as _pack

                full_png = layout_to_png_bytes(
                    layout.monogram_points,
                    layout.kamea_points,
                    bind_polylines=layout.bind_polylines,
                    rose_points=layout.rose_points,
                )
                stego_full = embed_lsb(full_png, _pack(bytes.fromhex(digest)))
                (staging / "glyph.png").write_bytes(stego_full)
                png_channel = _ch(
                    "png_lsb",
                    "applied",
                    "LSB digest-only via layout_raster+bind+rose",
                )
            except Exception:  # noqa: BLE001
                pass

        # Optional geometry-locked AI polish prompt (no image API)
        gen_seed_channel = _ch("gen_seed", "skipped", "no_ai_polish")
        polish_path_final: str | None = None
        if write_polish:
            import json as _json

            from prompt_polish import build_prompt

            stroke_count = (1 if layout.monogram_points else 0) + (
                1 if layout.kamea_points else 0
            )
            summary = {
                "intent_digest": digest,
                "stroke_count": stroke_count,
                "path_count": stroke_count,
                "view_box": list(layout.view_box),
                "bbox": [0.0, 0.0, 100.0, 100.0],
                "square_name": square_name,
            }
            polish_pkg = build_prompt(summary, polish_style)
            polish_file = staging / "polish_prompt.json"
            polish_file.write_text(
                _json.dumps(polish_pkg, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            gen_seed_channel = _ch(
                "gen_seed",
                "applied",
                f"seed={polish_pkg['seed']} polish_prompt.json",
            )
            polish_path_final = str(final_dir / "polish_prompt.json")

        extras = [png_channel, gen_seed_channel]

        channels = _merge_channels(craft_channels, list(stego_channels), extras)

        kprov = layout.kamea_provenance or {}
        methods = {
            "spare": {
                "family": "intent_compression",
                "mode": (layout.spare_result or {}).get("mode", spare_mode),
                "reduction": "vowels_and_duplicate_collapse_v1",
                "letter_count": len(spare),
                "determinism": (layout.spare_result or {}).get("determinism"),
                "semantic_verification": (layout.spare_result or {}).get(
                    "semantic_verification"
                ),
                "spare_result": layout.spare_result,
            },
            "kamea": {
                "family": "name_path",
                "planet": square_name,
                "order": order,
                "encoding_system": kprov.get("encoding_system", enc),
                "transliteration_system": kprov.get("transliteration_system"),
                "original_numeric_sequence": kprov.get("original_numeric_sequence"),
                "reduced_numeric_sequence": kprov.get("reduced_numeric_sequence"),
                "reduction_operations": kprov.get("reduction_operations"),
                "path": kprov.get("path"),
                "claimed_historical_status": kprov.get("claimed_historical_status"),
                # legacy key kept for readers:
                "cipher": kprov.get("encoding_system", enc),
            },
            "bind_runes": {
                "family": "alphabetic_ligature",
                "system": "elder_futhark_stick_v1",
                "historical_basis": "runic_ligature",
                "intent_sigil_system": {"status": "modern_derivation"},
                "claimed_historical_status": "modern_derivation",
                "runes": list(layout.bind_runes or []),
            },
            "rose_cross": layout.rose_provenance
            or {
                "method_id": "rose_cross.hebrew_petal_path",
                "family": "name_path",
            },
            "planetary_seal": layout.planetary_seal
            or {"status": "not_requested"},
        }
        ontology = default_packet_ontology(
            spare_mode=spare_mode,
            kamea_encoding=enc,
            include_bind=True,
            include_rose=True,
            include_planetary_seal=bool(planetary_seal),
            planet=square_name if planetary_seal else None,
        )
        provenance = {
            "kamea": kprov,
            "rose_cross": layout.rose_provenance,
            "spare": layout.spare_result,
            "planetary_seal": layout.planetary_seal,
            "bind_runes": {
                "claimed_historical_status": "modern_derivation",
                "historical_basis": "runic_ligature",
            },
        }

        # Artifact paths point at the final location (post-promote).
        final_svg = final_dir / "glyph.svg"
        final_png = final_dir / "glyph.png" if png_path_str else None
        packet_json_path = final_dir / "forge-packet.json"
        packet_md_path = final_dir / "forge-packet.md"
        receipt_path_final = final_dir / "run-receipt.json"
        artifacts: dict[str, Any] = {
            "svg": str(final_svg),
            "png": str(final_png) if final_png else None,
            "run_dir": str(final_dir),
            "run_id": rid,
            "packet_json": str(packet_json_path),
            "packet_md": str(packet_md_path),
        }
        if polish_path_final:
            artifacts["polish_prompt_path"] = polish_path_final
        if write_receipt:
            artifacts["receipt_json"] = str(receipt_path_final)

        verify_target = str(final_svg)
        verify_cmd = f"python3 scripts/sigil_forge.py verify {verify_target}"

        include_normalized = not seal_packet
        packet = build_packet(
            mode=mode,
            intent_digest=digest,
            channels=channels,
            methods=methods,
            artifacts=artifacts,
            crypto=crypto,
            verify_cmd=verify_cmd,
            normalized_intent=normalized if include_normalized else None,
            sealed_blob=sealed_blob if passphrase else None,
            include_normalized=include_normalized,
            ontology=ontology,
            provenance=provenance,
        )
        packet["schema_version"] = packet.get("schema_version") or SCHEMA_VERSION

        # Validate before promote — incomplete runs never leave a public run dir.
        schema_path = skill_root() / "schemas" / "forge-packet.schema.json"
        try:
            validate_packet(packet, schema_path=schema_path)
        except Exception as exc:  # noqa: BLE001
            if "structural" in str(exc).lower():
                raise
            if not schema_path.is_file():
                validate_packet(packet, schema_path=None)
            else:
                raise

        write_packet_files(packet, staging)

        if write_receipt:
            from receipt import (
                append_receipt_log,
                build_run_receipt,
                write_receipt_file,
            )

            version = "0.0.0"
            vpath = skill_root() / "VERSION"
            if vpath.is_file():
                version = vpath.read_text(encoding="utf-8").strip() or version
            # verify_ok filled after promote when caller re-verifies; leave None
            receipt = build_run_receipt(packet, skill_version=version, verify_ok=None)
            write_receipt_file(receipt, staging / "run-receipt.json")
            try:
                append_receipt_log(receipt)
            except OSError:
                pass

        # Promote staging → final (replace any prior run with same id).
        if final_dir.exists():
            shutil.rmtree(final_dir)
        staging.rename(final_dir)
        staging = None  # ownership transferred
        return packet
    finally:
        if staging is not None and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
