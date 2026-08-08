"""Full construct pipeline: safety → normalize → digest → fuse → stego → packet."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from crypto_payload import intent_digest, seal_intent
from fuse import build_layout
from kamea import KAMEA_SQUARES
from normalize import normalize_intent
from packet import build_packet, validate_packet, write_packet_files
from paths import default_out_dir, make_run_id, run_dir as make_run_dir, skill_root
from safety import check_intent
from spare import reduce_letters
from stego_png import embed_lsb, pack_payload
from stego_svg import embed as stego_svg_embed
from svg_export import layout_to_svg

SCHEMA_VERSION = "1.0"

_CHANNEL_ORDER = (
    "spare_monogram",
    "kamea_path",
    "kamea_square_choice",
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
    sealed_bytes: bytes | None,
    out_png: Path,
) -> tuple[str | None, dict[str, str]]:
    """Rasterize + LSB embed when possible; else skip with reason."""
    try:
        from raster_svg import svg_to_png_bytes
    except ImportError:
        return None, _ch("png_lsb", "skipped", "no_raster_backend")

    try:
        png_bytes = svg_to_png_bytes(svg)
    except Exception as exc:  # noqa: BLE001
        return None, _ch("png_lsb", "skipped", f"raster_error: {exc}")

    if not png_bytes:
        return None, _ch("png_lsb", "skipped", "no_raster_backend")

    digest_raw = bytes.fromhex(digest_hex)
    payload = pack_payload(digest_raw, sealed=sealed_bytes)
    try:
        stego_png = embed_lsb(png_bytes, payload)
    except Exception as exc:  # noqa: BLE001 — filter/capacity/format
        # Raster backends often emit filter types stego_png cannot rewrite.
        # Fall back: solid RGB carrier from digest-sized canvas so channel can apply
        # only if we can still produce a verifiable PNG of the glyph geometry.
        # Prefer skip over fake geometry PNG that is not the glyph.
        return None, _ch("png_lsb", "skipped", f"embed_failed: {exc}")

    out_png.write_bytes(stego_png)
    return str(out_png), _ch(
        "png_lsb",
        "applied",
        f"LSB payload {len(payload)} bytes into glyph.png",
    )


def run(
    intent: str,
    *,
    mode: str = "creative",
    out_root: Path | str | None = None,
    passphrase: str | None = None,
    square: str | None = None,
    seal_packet: bool = False,
) -> dict[str, Any]:
    """Orchestrate full forge: safety → normalize → digest → seal? → fuse → stego → packet.

    Writes under ``out_root/<run-id>/``:
      glyph.svg, optional glyph.png, forge-packet.json, forge-packet.md

    Returns the forge-packet dict. Raises ValueError on harmful/empty intent.
    """
    if mode not in ("creative", "practice"):
        raise ValueError(f"mode must be 'creative' or 'practice', got {mode!r}")
    if seal_packet and not passphrase:
        raise ValueError("seal_packet=True requires passphrase")

    ok, reason = check_intent(intent)
    if not ok:
        raise ValueError(reason or "refused: harmful intent")

    normalized = normalize_intent(intent)
    digest = intent_digest(normalized)

    craft_channels: list[dict[str, str]] = []
    sealed_blob: dict[str, Any] | None = None
    sealed_bytes: bytes | None = None

    # --- optional ciphertext ---
    if passphrase:
        sealed_blob = seal_intent(intent, passphrase)
        # Store compact bytes for optional PNG LSB (JSON ciphertext field only)
        sealed_bytes = sealed_blob["ciphertext_b64"].encode("ascii")
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
    layout = build_layout(normalized, digest, square_override=square)
    spare = layout.spare_letters or reduce_letters(normalized)
    square_name = layout.square_name
    order = len(KAMEA_SQUARES[square_name])

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

    # --- SVG + stego ---
    base_svg = layout_to_svg(layout)
    stego_svg, stego_channels = stego_svg_embed(base_svg, digest, spare_letters=spare)

    # Privacy: public SVG must not contain plaintext intent
    if normalized in stego_svg.lower():
        raise RuntimeError("public SVG leaked normalized intent")

    # --- paths ---
    root = Path(out_root) if out_root is not None else default_out_dir()
    rid = make_run_id(digest)
    rdir = make_run_dir(root, rid)
    rdir.mkdir(parents=True, exist_ok=True)

    svg_path = rdir / "glyph.svg"
    svg_path.write_text(stego_svg, encoding="utf-8")

    png_path_str, png_channel = _try_png_lsb(
        stego_svg, digest, sealed_bytes, rdir / "glyph.png"
    )
    extras = [
        png_channel,
        _ch("gen_seed", "skipped", "no_ai_polish"),
    ]

    channels = _merge_channels(craft_channels, list(stego_channels), extras)

    methods = {
        "spare": {
            "reduction": "vowels_and_duplicate_collapse_v1",
            "letter_count": len(spare),
        },
        "kamea": {
            "planet": square_name,
            "order": order,
            "cipher": "agrippa_reduced_v1",
        },
    }

    artifacts: dict[str, Any] = {
        "svg": str(svg_path),
        "png": png_path_str,
        "run_dir": str(rdir),
        "run_id": rid,
    }

    # Prefer path relative to skill root for verify hint when possible
    verify_target = str(svg_path)
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
    )

    # Write packet files then refresh artifact paths in packet
    written = write_packet_files(packet, rdir)
    packet["artifacts"]["packet_json"] = written["packet_json"]
    packet["artifacts"]["packet_md"] = written["packet_md"]
    # Rewrite JSON with final artifact paths
    write_packet_files(packet, rdir)

    # Optional schema validation (soft: structural always; jsonschema when present)
    schema_path = skill_root() / "schemas" / "forge-packet.schema.json"
    try:
        validate_packet(packet, schema_path=schema_path)
    except Exception as exc:  # noqa: BLE001
        # Structural failures are hard; jsonschema issues still hard if import works
        if "structural" in str(exc).lower():
            raise
        # If only optional schema path missing, ignore
        if not schema_path.is_file():
            validate_packet(packet, schema_path=None)
        else:
            raise

    packet["schema_version"] = packet.get("schema_version") or SCHEMA_VERSION
    return packet
