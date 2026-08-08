"""Verify a forged artifact recovers the embedded intent digest."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from stego_png import DIGEST_LEN, MAGIC, extract_lsb, unpack_payload
from stego_svg import extract as extract_svg


def _verify_svg(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    got = extract_svg(text)
    digest = got.get("intent_digest")
    channels = list(got.get("channels_detected") or [])
    ok = bool(digest) and isinstance(digest, str) and len(digest) == 64
    return {
        "ok": ok,
        "intent_digest": digest.lower() if isinstance(digest, str) and digest else None,
        "channels_checked": channels,
        "artifact": str(path),
        "kind": "svg",
    }


def _verify_png(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    channels: list[str] = []
    digest_hex: str | None = None
    try:
        # SF1 magic + 32-byte digest = 36 bytes minimum
        raw = extract_lsb(data, 4 + DIGEST_LEN)
        if raw[:4] != MAGIC:
            return {
                "ok": False,
                "intent_digest": None,
                "channels_checked": channels,
                "artifact": str(path),
                "kind": "png",
                "detail": "bad PNG LSB magic",
            }
        # Try full payload with optional sealed (probe remaining capacity later)
        # Re-extract full fixed header first; sealed optional.
        digest, _sealed = unpack_payload(raw)
        digest_hex = digest.hex()
        channels.append("png_lsb")
        return {
            "ok": True,
            "intent_digest": digest_hex,
            "channels_checked": channels,
            "artifact": str(path),
            "kind": "png",
        }
    except Exception as exc:  # noqa: BLE001 — verify reports failure
        return {
            "ok": False,
            "intent_digest": None,
            "channels_checked": channels,
            "artifact": str(path),
            "kind": "png",
            "detail": f"png extract failed: {exc}",
        }


def run(artifact_path: Path | str) -> dict[str, Any]:
    """Verify artifact recovers digest.

    Returns ``{ok, intent_digest, channels_checked, ...}``.
    """
    path = Path(artifact_path)
    if not path.is_file():
        return {
            "ok": False,
            "intent_digest": None,
            "channels_checked": [],
            "artifact": str(path),
            "detail": "file not found",
        }
    suffix = path.suffix.lower()
    if suffix == ".svg":
        return _verify_svg(path)
    if suffix == ".png":
        return _verify_png(path)
    # Try SVG text first (some paths lack extension)
    try:
        head = path.read_bytes()[:256]
        if b"<svg" in head.lower() or b"<?xml" in head:
            return _verify_svg(path)
        if head.startswith(b"\x89PNG"):
            return _verify_png(path)
    except OSError:
        pass
    return {
        "ok": False,
        "intent_digest": None,
        "channels_checked": [],
        "artifact": str(path),
        "detail": f"unsupported artifact type: {suffix or 'unknown'}",
    }
