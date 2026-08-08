"""Hermes forge wizard: script, validate, apply."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from wizard import (
    answers_to_construct_kwargs,
    apply_answers,
    default_answers,
    validate_answers,
    wizard_script,
)

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "sigil_forge.py"


def test_wizard_script_has_steps():
    script = wizard_script()
    assert script["wizard_version"]
    ids = [s["id"] for s in script["steps"]]
    assert "intent" in ids
    assert "mode" in ids
    assert "planetary_seal" in ids
    assert "agent_rules" in script


def test_validate_requires_intent():
    r = validate_answers({})
    assert r["ok"] is False
    assert any("intent" in e for e in r["errors"])


def test_validate_safety_refusal():
    r = validate_answers({"intent": "I will murder my neighbor tomorrow"})
    assert r["ok"] is False
    assert any("safety" in e for e in r["errors"])


def test_validate_happy_path_defaults():
    r = validate_answers({"intent": "I maintain calm focus"})
    assert r["ok"] is True
    assert r["answers"]["mode"] == "creative"
    assert r["answers"]["kamea_encoding"] == "hebrew_gematria"


def test_answers_to_kwargs_planetary():
    mapped = answers_to_construct_kwargs(
        {
            "intent": "I maintain calm focus",
            "mode": "creative",
            "kamea_encoding": "latin_mod9_v1",
            "square": "jupiter",
            "planetary_seal": "intelligence_character",
            "spare_mode": "letter_monogram",
            "phonetic": False,
            "polish": False,
            "wallpaper": True,
            "wp_surface": "desktop",
            "wp_mode": "ambient",
            "wp_theme": "lunar",
            "seal_packet": False,
        }
    )
    assert mapped["construct"]["planetary_seal"] is True
    assert mapped["construct"]["planetary_seal_kind"] == "intelligence_character"
    assert mapped["construct"]["square"] == "jupiter"
    assert mapped["wallpaper"]["enabled"] is True
    assert mapped["wallpaper"]["surface"] == "desktop"


def test_apply_answers_constructs(tmp_path: Path):
    result = apply_answers(
        {
            "intent": "I maintain calm focus",
            "mode": "creative",
            "kamea_encoding": "latin_mod9_v1",
            "square": "auto",
            "planetary_seal": "none",
            "wallpaper": False,
        },
        out_root=tmp_path,
    )
    assert result["ok"] is True, result
    assert result["svg"]
    assert Path(result["svg"]).is_file()


def test_apply_with_wallpaper(tmp_path: Path):
    result = apply_answers(
        {
            "intent": "I maintain calm focus",
            "kamea_encoding": "latin_mod9_v1",
            "wallpaper": True,
            "wp_surface": "phone_lock",
            "wp_mode": "focus",
            "wp_theme": "mercurial",
        },
        out_root=tmp_path,
    )
    assert result["ok"] is True, result
    assert result.get("wallpaper", {}).get("ok") is True


def test_wizard_cli_script():
    r = subprocess.run(
        [sys.executable, str(CLI), "wizard", "--script"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["steps"]


def test_wizard_cli_apply(tmp_path: Path):
    ans = tmp_path / "answers.json"
    ans.write_text(
        json.dumps(
            {
                "intent": "I maintain calm focus",
                "kamea_encoding": "latin_mod9_v1",
                "planetary_seal": "intelligence_character",
                "square": "jupiter",
            }
        ),
        encoding="utf-8",
    )
    r = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "wizard",
            "--apply",
            str(ans),
            "--out",
            str(tmp_path / "out"),
        ],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    assert r.returncode == 0, r.stderr + r.stdout
    out = json.loads(r.stdout)
    assert out["ok"] is True
    assert Path(out["svg"]).is_file()


def test_default_answers_template():
    d = default_answers()
    assert d["mode"] == "creative"
    assert d["planetary_seal"] == "none"
