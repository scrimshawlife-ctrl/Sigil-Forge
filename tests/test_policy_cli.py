import json
import subprocess
import sys
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "scripts" / "sigil_forge.py"


def test_policy_check_cli_clean():
    r = subprocess.run(
        [sys.executable, str(CLI), "policy", "check", "--text", "I maintain calm focus"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    assert json.loads(r.stdout)["ok"] is True


def test_policy_check_cli_flags_efficacy():
    r = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "policy",
            "check",
            "--text",
            "this sigil works and manifests gold",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1
