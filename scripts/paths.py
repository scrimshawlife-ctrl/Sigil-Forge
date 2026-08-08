from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import os


def skill_root() -> Path:
    env = os.environ.get("HERMES_SKILL_DIR")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent


def default_out_dir() -> Path:
    return skill_root() / "out" / "sigil-forge"


def make_run_id(digest_hex: str, when: datetime | None = None) -> str:
    ts = (when or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    prefix = (digest_hex or "0" * 8)[:8].lower()
    return f"{ts}-{prefix}"


def run_dir(out_root: Path, run_id: str) -> Path:
    return Path(out_root) / run_id
