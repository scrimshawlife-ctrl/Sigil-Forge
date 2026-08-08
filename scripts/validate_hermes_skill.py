#!/usr/bin/env python3
"""Validate Sigil-Forge SKILL.md against Hermes skill-authoring rules.

Rules derived from hermes-agent skill frontmatter validation + peer practice:
  - frontmatter at byte 0 with --- close
  - name + description required
  - description ≤ 1024 chars; first 57 chars should front-load triggers
  - description should start with "Use when"
  - name lowercase hyphens ≤ 64
  - body non-empty; total content ≤ 100_000 chars
  - recommend author/license/metadata.hermes.tags
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # stdlib-only fallback: minimal key parse
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
MAX_DESCRIPTION = 1024
MAX_NAME = 64
MAX_CONTENT = 100_000
INDEX_TRUNCATE = 57


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        raise ValueError("SKILL.md must start with --- (no leading whitespace/BOM)")
    m = re.search(r"\n---\s*\n", text[3:])
    if not m:
        raise ValueError("SKILL.md frontmatter not closed with \\n---\\n")
    fm_raw = text[3 : 3 + m.start()]
    body = text[3 + m.end() :]
    if yaml is not None:
        fm = yaml.safe_load(fm_raw)
    else:
        # Minimal fallback: only top-level scalars
        fm = {}
        for line in fm_raw.splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, _, v = line.partition(":")
                k, v = k.strip(), v.strip().strip("\"'")
                if k and not k.startswith(" "):
                    fm[k] = v
    if not isinstance(fm, dict):
        raise ValueError("frontmatter is not a YAML mapping")
    return fm, body


def validate(skill_path: Path = SKILL) -> dict:
    text = skill_path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    if len(text) > MAX_CONTENT:
        errors.append(f"SKILL.md length {len(text)} > {MAX_CONTENT}")
    if not text.startswith("---"):
        errors.append("must start with --- at byte 0")

    try:
        fm, body = _parse_frontmatter(text)
    except ValueError as exc:
        return {"ok": False, "errors": [str(exc)], "warnings": []}

    name = fm.get("name")
    desc = fm.get("description")
    if not name:
        errors.append("missing name")
    else:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(name)):
            errors.append(f"name must be lowercase-hyphen: {name!r}")
        if len(str(name)) > MAX_NAME:
            errors.append(f"name length {len(str(name))} > {MAX_NAME}")

    if not desc:
        errors.append("missing description")
    else:
        # folded YAML may be multi-line string
        d = " ".join(str(desc).split())
        if len(d) > MAX_DESCRIPTION:
            errors.append(f"description length {len(d)} > {MAX_DESCRIPTION}")
        if not d.lower().startswith("use when"):
            errors.append('description should start with "Use when"')
        head = d[:INDEX_TRUNCATE]
        if "sigil" not in head.lower() and "intent" not in head.lower():
            warnings.append(
                f"first {INDEX_TRUNCATE} chars of description should include "
                f"primary triggers (got {head!r})"
            )

    if not body.strip():
        errors.append("empty body after frontmatter")

    for key in ("version", "author", "license"):
        if key not in fm:
            warnings.append(f"missing peer field: {key}")

    hermes = (fm.get("metadata") or {}).get("hermes") if isinstance(fm.get("metadata"), dict) else None
    if not hermes:
        warnings.append("missing metadata.hermes")
    else:
        if "tags" not in hermes:
            warnings.append("missing metadata.hermes.tags")
        if "related_skills" not in hermes:
            warnings.append("missing metadata.hermes.related_skills (use [] if none)")

    # Section hygiene (Hermes peer structure)
    for section in ("# Sigil-Forge", "## Overview", "## When to Use", "## Common Pitfalls", "## Verification Checklist"):
        if section not in text and section.replace("Common ", "").replace(" Checklist", "") not in text:
            # allow aliases
            if section == "## Common Pitfalls" and "## Pitfalls" in text:
                warnings.append("prefer '## Common Pitfalls' over '## Pitfalls' (peer convention)")
            elif section == "## Verification Checklist" and "## Verification" in text:
                warnings.append(
                    "prefer '## Verification Checklist' over '## Verification' (peer convention)"
                )
            elif section.startswith("# "):
                pass
            else:
                warnings.append(f"missing section: {section}")

    ok = not errors
    return {
        "ok": ok,
        "errors": errors,
        "warnings": warnings,
        "name": name,
        "description_index_preview": " ".join(str(desc).split())[:INDEX_TRUNCATE] if desc else None,
        "content_chars": len(text),
    }


def main() -> int:
    report = validate()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
