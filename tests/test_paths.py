from pathlib import Path
import scripts.paths as paths


def test_default_state_is_native_without_hermes(monkeypatch, tmp_path):
    monkeypatch.delenv("HERMES_HOME", raising=False)
    monkeypatch.delenv("HERMES_SKILL_DIR", raising=False)
    monkeypatch.delenv("SIGIL_FORGE_STATE_DIR", raising=False)
    engine = tmp_path / "engine"
    engine.mkdir()
    monkeypatch.setenv("SIGIL_FORGE_HOME", str(engine))
    out = paths.default_out_dir()
    assert "hermes" not in str(out).lower()
    assert out == (engine / "state" / "products").resolve()


def test_configured_root_prefers_sigil_forge_home(monkeypatch, tmp_path):
    native = tmp_path / "sf"
    decoy = tmp_path / "hermes-skill"
    native.mkdir()
    decoy.mkdir()
    monkeypatch.setenv("SIGIL_FORGE_HOME", str(native))
    monkeypatch.setenv("HERMES_SKILL_DIR", str(decoy))
    assert paths.configured_root() == native.resolve()
    assert paths.skill_root() == native.resolve()


def test_skill_root_contains_scripts():
    assert (paths.skill_root() / "scripts" / "paths.py").is_file()


def test_make_run_id_uses_digest_prefix_not_full_intent():
    rid = paths.make_run_id("abcdef0123456789" * 4)
    assert "abcdef01" in rid
    assert " " not in rid
    assert len(rid) < 80


def test_run_dir_under_out():
    out = Path("/tmp/sf-out")
    d = paths.run_dir(out, "20260101T000000Z-abcdef01")
    assert d == out / "20260101T000000Z-abcdef01"
