#!/usr/bin/env python3
"""
Storyboard Carriers (Planned / Skeleton)

Multi-frame sequential intent carriers.
No audio. Offline.

From references/storyboard-plan.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def create_storyboard(frames: list[dict[str, Any]], out_dir: Path | None = None) -> Path:
    """Stub: create multi-frame storyboard from frame intents."""
    out = out_dir or Path("storyboard")
    out.mkdir(exist_ok=True)
    for i, frame in enumerate(frames):
        (out / f"frame_{i:02d}.json").write_text(str(frame))
    return out / "storyboard.json"


def add_frame(story: dict, intent: str, geometry: dict | None = None) -> dict:
    """Stub for adding a frame."""
    story.setdefault("frames", []).append({"intent": intent, "geometry": geometry or {}})
    return story


if __name__ == "__main__":
    print("storyboard skeleton — planned for multi-frame carriers")
    s = create_storyboard([{"intent": "test frame"}])
    print("created", s)
