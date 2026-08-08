import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_help_exits_zero():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sigil_forge.py"), "help"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0
    assert "construct" in r.stdout.lower() or "construct" in r.stderr.lower()
