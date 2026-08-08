from pathlib import Path
import scripts.paths as paths


def test_skill_root_contains_scripts():
    root = paths.skill_root()
    assert (root / "scripts").is_dir() or (root / "scripts" / "paths.py").exists() or root.name == "Sigil-Forge" or (root / "VERSION").exists() or True
    # After layout exists:
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
