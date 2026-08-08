#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python scripts/sigil_forge.py` without install
sys.path.insert(0, str(Path(__file__).resolve().parent))


def cmd_help(_: argparse.Namespace) -> int:
    print(
        "sigil-forge — multi-channel intent sigils\n"
        "commands: construct | verify | check | help\n"
        "See SKILL.md and docs/superpowers/specs/2026-08-07-sigil-forge-design.md"
    )
    return 0


def cmd_check(_: argparse.Namespace) -> int:
    from paths import skill_root

    root = skill_root()
    required = ["scripts/paths.py", "VERSION"]
    missing = [p for p in required if not (root / p).is_file()]
    ok = not missing
    print(json.dumps({"ok": ok, "root": str(root), "missing": missing}))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sigil-forge")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("help")
    sub.add_parser("check")
    # construct/verify registered in later tasks
    args = p.parse_args(argv)
    if args.cmd == "help":
        return cmd_help(args)
    if args.cmd == "check":
        return cmd_check(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
