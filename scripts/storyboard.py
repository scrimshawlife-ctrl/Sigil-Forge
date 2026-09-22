#!/usr/bin/env python3
"""
Storyboard Carriers (Completed Basic Implementation)

Multi-frame sequential intent carriers.
Each frame carries a normalized intent + optional geometry.
Offline. Produces storyboard.json + per-frame artifacts.

From references/storyboard-plan.md
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def create_storyboard(frames: list[dict[str, Any]], out_dir: Path | None = None) -> Path:
    """Create a multi-frame storyboard directory + index."""
    out = out_dir or Path("storyboard")
    out.mkdir(parents=True, exist_ok=True)
    index: list[dict] = []
    for i, frame in enumerate(frames):
        frame_id = f"frame_{i:02d}"
        frame_path = out / f"{frame_id}.json"
        frame_data = {
            "frame_id": frame_id,
            "intent": frame.get("intent", ""),
            "geometry": frame.get("geometry", {}),
            "index": i,
        }
        frame_path.write_text(json.dumps(frame_data, indent=2), encoding="utf-8")
        index.append({"frame_id": frame_id, "path": str(frame_path), "intent": frame_data["intent"]})
    index_path = out / "storyboard.json"
    index_path.write_text(json.dumps({"frames": index, "count": len(index)}, indent=2), encoding="utf-8")
    return index_path


def add_frame(story: dict, intent: str, geometry: dict | None = None) -> dict:
    """Add a frame to an in-memory story dict."""
    if "frames" not in story:
        story["frames"] = []
    story["frames"].append({"intent": intent, "geometry": geometry or {}})
    return story


if __name__ == "__main__":
    print("storyboard — multi-frame carrier builder")
    frames = [
        {"intent": "I maintain calm focus", "geometry": {"mode": "creative"}},
        {"intent": "I build durable systems", "geometry": {"mode": "practice"}},
    ]
    idx = create_storyboard(frames, Path("/tmp/storyboard_demo"))
    print("created index:", idx)
    print("frames:", json.loads(idx.read_text())["count"])
