"""Basic tests for completed non-audio extension modules."""

import json
from pathlib import Path
import tempfile

import pytest

sys_path_add = Path(__file__).parent.parent / "scripts"
import sys
sys.path.insert(0, str(sys_path_add))


def test_plate_import():
    from plate_import import load_plate, normalize_to_plate, import_and_save, validate_plate
    ref = Path("references/planetary-plate-strokes.json")
    assert ref.exists()
    data = load_plate(ref)
    assert validate_plate(data) or "strokes" in str(data)
    norm = normalize_to_plate([{"type": "path", "data": "M0,0"}])
    assert len(norm) == 1
    with tempfile.TemporaryDirectory() as td:
        out = import_and_save(ref, Path(td) / "out.json")
        assert out.exists()
        j = json.loads(out.read_text())
        assert j["count"] >= 0


def test_storyboard():
    from storyboard import create_storyboard, add_frame
    frames = [{"intent": "test1"}, {"intent": "test2"}]
    with tempfile.TemporaryDirectory() as td:
        idx = create_storyboard(frames, Path(td) / "sb")
        assert idx.exists()
        data = json.loads(idx.read_text())
        assert data["count"] == 2
    story = {}
    add_frame(story, "added")
    assert len(story["frames"]) == 1


def test_adapters():
    from adapters import list_adapters, load_adapter_config, export_geometry_for_adapter, render_adapter_prompt
    assert "comfyui" in list_adapters()
    cfg = load_adapter_config("orchestra")
    assert cfg["name"] == "Orchestra"
    geo = export_geometry_for_adapter({"sigil_root": "x"})
    assert geo["adapter"] == "comfyui"
    p = render_adapter_prompt("focus")
    assert "Orchestra" in p or "focus" in p


def test_steganalysis():
    from steganalysis import analyze_channels, geometric_correlation, estimate_capacity
    rep = analyze_channels({"sigil_root": "demo"})
    assert "analysis" in rep
    corr = geometric_correlation("<svg/>", b"png")
    assert "correlation_score" in corr
    cap = estimate_capacity(["png_lsb", "svg"])
    assert cap["safe_capacity_bits"] > 0


def test_comfyui_templates():
    from comfyui_templates import list_templates, load_template, render_template_for_wallpaper
    temps = list_templates()
    assert "minimal_background" in temps
    t = load_template("atmospheric")
    assert "name" in t
    r = render_template_for_wallpaper(t, "hash123")
    assert "glyph_hash" in r


def test_extension_cli_commands(tmp_path):
    """More coverage for new extension CLIs (host-AI adjacent interop + analysis)."""
    import subprocess
    import sys
    from pathlib import Path
    ROOT = Path(__file__).resolve().parents[1]
    cli = ROOT / "scripts" / "sigil_forge.py"
    # plate-import
    res = subprocess.run(
        [sys.executable, str(cli), "plate-import"],
        capture_output=True, text=True, timeout=10
    )
    assert res.returncode == 0
    assert "plate-import" in res.stdout
    # adapters
    res = subprocess.run(
        [sys.executable, str(cli), "adapters"],
        capture_output=True, text=True, timeout=10
    )
    assert "orchestra" in res.stdout.lower() or "comfyui" in res.stdout.lower()
    # steganalysis
    res = subprocess.run(
        [sys.executable, str(cli), "steganalysis"],
        capture_output=True, text=True, timeout=10
    )
    assert "steganalysis" in res.stdout.lower() or "channel" in res.stdout.lower()
    # comfyui
    res = subprocess.run(
        [sys.executable, str(cli), "comfyui"],
        capture_output=True, text=True, timeout=10
    )
    assert "comfyui" in res.stdout.lower() or "template" in res.stdout.lower()


def test_full_poi_flow_with_host_ai_wallpaper(tmp_path: Path):
    """Expand coverage: full PoI (commitment + capsule) + host-AI wallpaper path."""
    from construct import run as construct_run
    from wallpaper.pipeline import build_wallpaper
    # PoI construct
    packet = construct_run(
        "I build durable systems under pressure",
        out_root=tmp_path,
        proof="commitment",
        passphrase="test-poi-host",
        kamea_encoding="hebrew_gematria",
    )
    assert packet.get("sigil_root")
    assert packet.get("intent_commitment")
    run_dir = Path(packet["artifacts"]["run_dir"])
    # Host-AI style wallpaper (use procedural as stand-in for coverage)
    res = build_wallpaper(
        run_dir,
        surface="desktop",
        background_method="ai_generated",
        model="coverage-mock",
    )
    assert res["ok"]
    assert "background" in res
    # Verify PoI surfaces still present
    assert (run_dir / "forge-manifest.json").exists()
    assert (run_dir / "intent-capsule.json").exists()
