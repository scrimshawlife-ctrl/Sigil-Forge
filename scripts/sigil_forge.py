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


def cmd_construct(args: argparse.Namespace) -> int:
    from construct import run as construct_run

    try:
        packet = construct_run(
            args.intent,
            mode=args.mode,
            out_root=Path(args.out) if args.out else None,
            passphrase=args.passphrase,
            square=args.square,
            seal_packet=bool(args.seal_packet),
        )
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1
    # Print compact summary to stdout (full packet on --json)
    if args.json:
        print(json.dumps(packet, indent=2, sort_keys=True))
    else:
        print(
            json.dumps(
                {
                    "ok": True,
                    "intent_digest": packet["intent_digest"],
                    "run_id": packet.get("artifacts", {}).get("run_id"),
                    "svg": packet.get("artifacts", {}).get("svg"),
                    "packet": packet.get("artifacts", {}).get("packet_json"),
                    "channels_applied": [
                        c["id"]
                        for c in packet.get("channels", [])
                        if c.get("status") == "applied"
                    ],
                },
                indent=2,
            )
        )
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    from verify import run as verify_run

    result = verify_run(Path(args.artifact))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sigil-forge")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("help", help="Show command overview")
    sub.add_parser("check", help="Smoke-check skill tree")

    pc = sub.add_parser("construct", help="Forge multi-channel sigil + packet")
    pc.add_argument("--intent", required=True, help="Statement of intent")
    pc.add_argument(
        "--mode",
        default="creative",
        choices=("creative", "practice"),
        help="Framing mode (default: creative)",
    )
    pc.add_argument(
        "--out",
        default=None,
        help="Output root (default: out/sigil-forge under skill root)",
    )
    pc.add_argument("--passphrase", default=None, help="Optional seal passphrase")
    pc.add_argument(
        "--square",
        default=None,
        help="Kamea square override (saturn..luna)",
    )
    pc.add_argument(
        "--seal-packet",
        action="store_true",
        help="Omit plaintext intent from packet (requires --passphrase)",
    )
    pc.add_argument(
        "--json",
        action="store_true",
        help="Print full forge-packet JSON",
    )

    pv = sub.add_parser("verify", help="Verify artifact recovers intent digest")
    pv.add_argument("artifact", help="Path to glyph.svg or glyph.png")

    args = p.parse_args(argv)
    if args.cmd == "help":
        return cmd_help(args)
    if args.cmd == "check":
        return cmd_check(args)
    if args.cmd == "construct":
        return cmd_construct(args)
    if args.cmd == "verify":
        return cmd_verify(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
