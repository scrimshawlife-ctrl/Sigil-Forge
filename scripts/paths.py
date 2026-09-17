from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import os

# Canonical env (any agent / CLI). Hermes vars are last-compat only.
_ROOT_ENV = (
    "SIGIL_FORGE_HOME",
    "SIGIL_FORGE_ROOT",
    "SIGIL_FORGE_DIR",
    "SIGIL_FORGE_SKILL_DIR",
)
_HERMES_ROOT_ENV = "HERMES_SKILL_DIR"


def _expand(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def configured_root() -> Path | None:
    """Explicit install/clone root from env. Hermes is last-compat only."""
    for key in _ROOT_ENV:
        raw = os.environ.get(key)
        if raw:
            return _expand(raw)
    raw = os.environ.get(_HERMES_ROOT_ENV)
    if raw:
        return _expand(raw)
    return None


def skill_root() -> Path:
    env = configured_root()
    if env:
        return env
    return Path(__file__).resolve().parent.parent


def default_state_root() -> Path:
    """Product/session state. Not Hermes-specific.

    Order: SIGIL_FORGE_STATE_DIR → <configured root>/state → ~/.sigil-forge/state
    → legacy ~/.hermes/state/sigil-forge if that tree already exists.
    """
    state = os.environ.get("SIGIL_FORGE_STATE_DIR")
    if state:
        return _expand(state)
    env = None
    for key in _ROOT_ENV:
        raw = os.environ.get(key)
        if raw:
            env = _expand(raw)
            break
    if env is not None:
        return env / "state"
    native = Path.home() / ".sigil-forge" / "state"
    hermes_legacy = (
        Path(os.environ.get("HERMES_HOME") or str(Path.home() / ".hermes"))
        .expanduser()
        .resolve()
        / "state"
        / "sigil-forge"
    )
    if hermes_legacy.is_dir() and not native.exists():
        return hermes_legacy
    return native


def default_out_dir() -> Path:
    return default_state_root() / "products"


def default_session_dir() -> Path:
    return default_state_root() / "wizard-sessions"


def make_run_id(digest_hex: str, when: datetime | None = None) -> str:
    ts = (when or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    prefix = (digest_hex or "0" * 8)[:8].lower()
    return f"{ts}-{prefix}"


def run_dir(out_root: Path, run_id: str) -> Path:
    return Path(out_root) / run_id
