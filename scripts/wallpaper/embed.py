"""Optional wallpaper digest binding (never plaintext intent)."""

from __future__ import annotations

from pathlib import Path

from stego_png import DIGEST_LEN, embed_lsb, pack_payload, write_rgb_png
from stego_png import read_rgb_png
from wallpaper.seed import wallpaper_payload


def embed_binding(
    png_path: Path,
    *,
    intent_digest: str,
    wallpaper_spec_digest: str,
    source_glyph_digest: str,
    mode: str = "intent_digest",
) -> str | None:
    """LSB-embed a binding digest into wallpaper PNG when possible.

    mode:
      - none: no-op
      - intent_digest: embed SHA256(intent) raw
      - channel_digest: embed wallpaper_payload(...) raw
    Returns new sha256 of file or None if skipped.
    """
    if mode == "none":
        return None
    try:
        data = png_path.read_bytes()
        w, h, rgb = read_rgb_png(data)
    except Exception:
        return None

    if mode == "channel_digest":
        digest_hex = wallpaper_payload(
            intent_digest=intent_digest,
            wallpaper_spec_digest=wallpaper_spec_digest,
            source_glyph_digest=source_glyph_digest,
        )
    else:
        digest_hex = intent_digest

    raw = bytes.fromhex(digest_hex)
    if len(raw) != DIGEST_LEN:
        return None
    payload = pack_payload(raw)
    try:
        # re-encode filter-0 then LSB
        clean = write_rgb_png(w, h, rgb)
        out = embed_lsb(clean, payload)
        png_path.write_bytes(out)
        from wallpaper.seed import file_sha256

        return file_sha256(str(png_path))
    except Exception:
        return None
