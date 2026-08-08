"""Smoke: CLI `check` validates tree, schemas, modules, and dry construct."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "sigil_forge.py"


def test_check_exits_zero_and_reports_ok():
    r = subprocess.run(
        [sys.executable, str(CLI), "check"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert r.returncode == 0, f"stderr={r.stderr!r} stdout={r.stdout!r}"
    payload = json.loads(r.stdout)
    assert payload["ok"] is True
    assert payload.get("missing") == []
    assert "root" in payload
    assert payload["schemas_ok"] is True
    assert payload["modules_ok"] is True
    assert payload["construct_ok"] is True
    assert payload["verify_ok"] is True


def test_check_requires_schemas_and_modules():
    """Expanded check reports empty missing list and healthy sub-flags."""
    r = subprocess.run(
        [sys.executable, str(CLI), "check"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert r.returncode == 0
    payload = json.loads(r.stdout)
    assert payload["ok"] is True
    assert payload.get("missing") == []
    assert payload.get("schema_errors") == []
    assert payload.get("module_errors") == []
    assert payload.get("construct_error") in (None, "")
