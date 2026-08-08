"""Run receipts and proposal-only learning ledger.

Receipts: append-only JSONL of construct outcomes (integrity hash optional).
Learning ledger: operator-submitted observations with canon_status PROPOSED only —
never auto-promoted to skill corpus.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from paths import skill_root

RECEIPT_SCHEMA_VERSION = "1.0"
LEDGER_SCHEMA_VERSION = "1.0"
DEFAULT_LEDGER_NAME = "learning-ledger.jsonl"
DEFAULT_RECEIPTS_NAME = "run-receipts.jsonl"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def default_ledger_path() -> Path:
    env = os.environ.get("SIGIL_FORGE_LEDGER")
    if env:
        return Path(env).expanduser()
    return skill_root() / "out" / "sigil-forge" / DEFAULT_LEDGER_NAME


def default_receipts_path() -> Path:
    env = os.environ.get("SIGIL_FORGE_RECEIPTS")
    if env:
        return Path(env).expanduser()
    return skill_root() / "out" / "sigil-forge" / DEFAULT_RECEIPTS_NAME


def build_run_receipt(
    packet: dict[str, Any],
    *,
    skill_version: str,
    verify_ok: bool | None = None,
) -> dict[str, Any]:
    """Build a receipt dict from a forge packet (no plaintext intent required)."""
    channels = packet.get("channels") or []
    applied = [c.get("id") for c in channels if c.get("status") == "applied"]
    skipped = [
        {"id": c.get("id"), "detail": c.get("detail")}
        for c in channels
        if c.get("status") == "skipped"
    ]
    receipt = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "kind": "sigil_forge_run_receipt",
        "ts": _utc_now(),
        "skill_version": skill_version,
        "run_id": (packet.get("artifacts") or {}).get("run_id"),
        "mode": packet.get("mode"),
        "intent_digest": packet.get("intent_digest"),
        "channels_applied": applied,
        "channels_skipped": skipped,
        "methods": packet.get("methods") or {},
        "crypto_key_policy": (packet.get("crypto") or {}).get("key_policy"),
        "artifacts": {
            k: (packet.get("artifacts") or {}).get(k)
            for k in ("svg", "png", "packet_json", "polish_prompt_path")
        },
        "verify_ok": verify_ok,
        "canon_status": "OBSERVATION",
    }
    # Integrity over stable serialization without local path noise
    core = {
        "intent_digest": receipt["intent_digest"],
        "channels_applied": receipt["channels_applied"],
        "mode": receipt["mode"],
        "run_id": receipt["run_id"],
        "skill_version": skill_version,
    }
    blob = json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")
    receipt["receipt_hash"] = hashlib.sha256(blob).hexdigest()
    return receipt


def write_receipt_file(receipt: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def append_receipt_log(receipt: dict[str, Any], log_path: Path | None = None) -> Path:
    path = log_path or default_receipts_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(receipt, sort_keys=True) + "\n")
    return path


def build_ledger_entry(
    *,
    class_name: str,
    summary: str,
    run_id: str | None = None,
    intent_digest: str | None = None,
    channels: list[str] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entry = {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "kind": "sigil_forge_learning_entry",
        "ts": _utc_now(),
        "unix": int(time.time()),
        "class": class_name,
        "summary": summary,
        "run_id": run_id,
        "intent_digest": intent_digest,
        "channels": channels or [],
        "canon_status": "PROPOSED",  # never auto-canon
        "extra": extra or {},
    }
    return entry


def append_ledger(
    entry: dict[str, Any],
    ledger_path: Path | None = None,
) -> Path:
    if entry.get("canon_status") != "PROPOSED":
        raise ValueError("learning ledger entries must be canon_status=PROPOSED")
    path = ledger_path or default_ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
    return path


def read_ledger(ledger_path: Path | None = None, limit: int = 50) -> list[dict[str, Any]]:
    path = ledger_path or default_ledger_path()
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[dict[str, Any]] = []
    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
