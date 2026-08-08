"""Hermes-facing forge wizard — guided interview → construct kwargs.

Modes:
  - ``script``: emit full step list for the agent to walk conversationally
  - ``validate`` / ``apply``: check answers JSON and run construct (+ optional wallpaper)
  - ``interactive``: human TTY prompts (optional)

The skill stays offline-first; the wizard never invents geometry.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from safety import check_intent

WIZARD_VERSION = "1.0.0"

# Ordered interview steps for Hermes agents and interactive CLI.
STEPS: list[dict[str, Any]] = [
    {
        "id": "intent",
        "prompt": (
            "State your intent in present tense (e.g. \"I maintain calm focus\"). "
            "Avoid harm, coercion, or empty noise."
        ),
        "type": "text",
        "required": True,
        "example": "I maintain calm focus while shipping",
    },
    {
        "id": "mode",
        "prompt": "Framing mode: creative (default focus tool) or practice (practitioner tone, no efficacy claims).",
        "type": "choice",
        "choices": ["creative", "practice"],
        "default": "creative",
    },
    {
        "id": "kamea_encoding",
        "prompt": (
            "Kamea name-path encoding: hebrew_gematria (default, historically aligned), "
            "latin_extended, or latin_mod9_v1 (compatibility)."
        ),
        "type": "choice",
        "choices": ["hebrew_gematria", "latin_extended", "latin_mod9_v1"],
        "default": "hebrew_gematria",
    },
    {
        "id": "square",
        "prompt": "Planetary kamea square (auto = digest-derived), or saturn..luna.",
        "type": "choice",
        "choices": ["auto", "saturn", "jupiter", "mars", "sol", "venus", "mercury", "luna"],
        "default": "auto",
    },
    {
        "id": "planetary_seal",
        "prompt": (
            "Optional planetary character (distinct from intent kamea path): "
            "none, traditional_seal, intelligence_character (corpus name-on-kamea), "
            "or spirit_character."
        ),
        "type": "choice",
        "choices": [
            "none",
            "traditional_seal",
            "intelligence_character",
            "spirit_character",
        ],
        "default": "none",
    },
    {
        "id": "spare_mode",
        "prompt": "Spare family mode for intent compression.",
        "type": "choice",
        "choices": [
            "letter_monogram",
            "pictorial",
            "automatic_drawing",
            "mantric_alphabet",
            "phonetic_mantric",
        ],
        "default": "letter_monogram",
    },
    {
        "id": "phonetic",
        "prompt": "Also emit phoneme-sequence JSON carrier?",
        "type": "bool",
        "default": False,
    },
    {
        "id": "polish",
        "prompt": "Write geometry-locked polish_prompt.json for host image tools?",
        "type": "bool",
        "default": False,
    },
    {
        "id": "wallpaper",
        "prompt": "Compose a device wallpaper after forge (immutable glyph + atmosphere)?",
        "type": "bool",
        "default": False,
    },
    {
        "id": "wp_surface",
        "prompt": "Wallpaper surface (if wallpaper=yes).",
        "type": "choice",
        "choices": [
            "phone_lock",
            "phone_home",
            "tablet",
            "desktop",
            "desktop_ultrawide",
        ],
        "default": "phone_lock",
        "when": {"wallpaper": True},
    },
    {
        "id": "wp_mode",
        "prompt": "Wallpaper presentation mode.",
        "type": "choice",
        "choices": ["stealth", "ambient", "focus", "ritual", "immersive"],
        "default": "focus",
        "when": {"wallpaper": True},
    },
    {
        "id": "wp_theme",
        "prompt": "Wallpaper symbolic theme (e.g. mercurial, lunar, neutral).",
        "type": "text",
        "default": "neutral",
        "when": {"wallpaper": True},
    },
    {
        "id": "seal_packet",
        "prompt": "Seal plaintext intent out of the public packet? (requires passphrase env)",
        "type": "bool",
        "default": False,
    },
]


def wizard_script() -> dict[str, Any]:
    """Agent-facing interview script (Hermes reads this and asks the user)."""
    return {
        "wizard_version": WIZARD_VERSION,
        "skill": "sigil-forge",
        "purpose": (
            "Guide an operator from intent to a verified multi-channel sigil "
            "without inventing geometry or claiming efficacy."
        ),
        "agent_rules": [
            "Ask one step at a time unless the user already answered multiple fields.",
            "Run safety check before construct; refuse harmful intents with no artifacts.",
            "Never invent monogram/kamea paths — only call scripts via construct/wizard apply.",
            "Do not claim the sigil works or replaces professional help.",
            "After apply, offer verify on glyph.svg (and glyph.png when present).",
            "Wallpapers never AI-redraw the canonical glyph.",
        ],
        "steps": STEPS,
        "apply": {
            "cli": "python3 scripts/sigil_forge.py wizard --apply answers.json --out out/sigil-forge",
            "answers_schema": "flat object keyed by step id",
        },
        "defaults_template": default_answers(),
    }


def default_answers() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for step in STEPS:
        if "default" in step:
            out[step["id"]] = step["default"]
    return out


def _coerce_bool(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("1", "true", "yes", "y", "on")
    return bool(v)


def _step_active(step: dict[str, Any], answers: dict[str, Any]) -> bool:
    when = step.get("when")
    if not when:
        return True
    for k, need in when.items():
        got = answers.get(k)
        if isinstance(need, bool):
            if _coerce_bool(got) != need:
                return False
        elif got != need:
            return False
    return True


def validate_answers(raw: dict[str, Any] | None) -> dict[str, Any]:
    """Validate and normalize wizard answers. Returns {ok, answers, errors, warnings}."""
    raw = dict(raw or {})
    errors: list[str] = []
    warnings: list[str] = []
    answers: dict[str, Any] = {}

    for step in STEPS:
        sid = step["id"]
        active = _step_active(step, {**default_answers(), **raw, **answers})
        # Recompute active with progressive answers
        active = _step_active(step, {**default_answers(), **raw, **answers})
        if not active:
            continue
        if sid not in raw or raw[sid] in (None, ""):
            if step.get("required"):
                errors.append(f"missing required: {sid}")
                continue
            if "default" in step:
                answers[sid] = step["default"]
            continue
        val = raw[sid]
        if step["type"] == "bool":
            answers[sid] = _coerce_bool(val)
        elif step["type"] == "choice":
            s = str(val).strip()
            if s not in step["choices"]:
                errors.append(f"{sid}: {s!r} not in {step['choices']}")
            else:
                answers[sid] = s
        else:
            answers[sid] = str(val).strip()

    # Final when-filter defaults for inactive optional fields
    merged = {**default_answers(), **answers}
    for step in STEPS:
        if not _step_active(step, merged):
            answers.pop(step["id"], None)

    intent = (answers.get("intent") or "").strip()
    if intent:
        ok_s, reason = check_intent(intent)
        if not ok_s:
            errors.append(f"safety: {reason}")
        answers["intent"] = intent

    return {
        "ok": not errors,
        "answers": answers,
        "errors": errors,
        "warnings": warnings,
        "wizard_version": WIZARD_VERSION,
    }


def answers_to_construct_kwargs(answers: dict[str, Any]) -> dict[str, Any]:
    """Map wizard answers to construct.run kwargs (+ wallpaper flags)."""
    seal_kind = answers.get("planetary_seal") or "none"
    planetary = seal_kind != "none"
    square = answers.get("square") or "auto"
    kwargs: dict[str, Any] = {
        "mode": answers.get("mode") or "creative",
        "kamea_encoding": answers.get("kamea_encoding") or "hebrew_gematria",
        "spare_mode": answers.get("spare_mode") or "letter_monogram",
        "planetary_seal": planetary,
        "planetary_seal_kind": seal_kind if planetary else "traditional_seal",
        "phonetic": bool(answers.get("phonetic")),
        "write_polish": bool(answers.get("polish")),
        "seal_packet": bool(answers.get("seal_packet")),
        "square": None if square in (None, "", "auto") else square,
    }
    wallpaper = {
        "enabled": bool(answers.get("wallpaper")),
        "surface": answers.get("wp_surface") or "phone_lock",
        "mode": answers.get("wp_mode") or "focus",
        "theme": answers.get("wp_theme") or "neutral",
    }
    return {"intent": answers["intent"], "construct": kwargs, "wallpaper": wallpaper}


def apply_answers(
    answers: dict[str, Any],
    *,
    out_root: Path | str | None = None,
    passphrase: str | None = None,
) -> dict[str, Any]:
    """Validate answers, construct forge packet, optional wallpaper."""
    from construct import resolve_passphrase, run as construct_run

    report = validate_answers(answers)
    if not report["ok"]:
        return {"ok": False, "phase": "validate", **report}

    mapped = answers_to_construct_kwargs(report["answers"])
    intent = mapped["intent"]
    ck = mapped["construct"]
    if ck.get("seal_packet"):
        pp = resolve_passphrase(passphrase)
        if not pp:
            return {
                "ok": False,
                "phase": "validate",
                "errors": [
                    "seal_packet requires --passphrase or SIGIL_FORGE_PASSPHRASE"
                ],
                "answers": report["answers"],
            }
        ck = {**ck, "passphrase": pp}
    elif passphrase:
        ck = {**ck, "passphrase": resolve_passphrase(passphrase)}

    try:
        packet = construct_run(
            intent,
            out_root=Path(out_root) if out_root else None,
            **ck,
        )
    except (ValueError, RuntimeError) as exc:
        return {
            "ok": False,
            "phase": "construct",
            "error": str(exc),
            "answers": report["answers"],
        }

    result: dict[str, Any] = {
        "ok": True,
        "phase": "construct",
        "answers": report["answers"],
        "intent_digest": packet.get("intent_digest"),
        "run_id": (packet.get("artifacts") or {}).get("run_id"),
        "run_dir": (packet.get("artifacts") or {}).get("run_dir"),
        "svg": (packet.get("artifacts") or {}).get("svg"),
        "packet_path": (packet.get("artifacts") or {}).get("packet_json"),
        "channels_applied": [
            c["id"]
            for c in packet.get("channels", [])
            if c.get("status") == "applied"
        ],
    }

    wp = mapped["wallpaper"]
    if wp.get("enabled"):
        from wallpaper.pipeline import build_wallpaper

        run_dir = packet.get("artifacts", {}).get("run_dir")
        try:
            wr = build_wallpaper(
                Path(run_dir),
                surface=wp["surface"],
                mode=wp["mode"],
                symbolic_theme=wp["theme"],
                background_method="procedural",
            )
            result["wallpaper"] = wr
            if not wr.get("ok"):
                result["ok"] = False
                result["phase"] = "wallpaper"
                result["error"] = "wallpaper verification failed"
        except Exception as exc:  # noqa: BLE001
            result["ok"] = False
            result["phase"] = "wallpaper"
            result["error"] = str(exc)

    result["next"] = [
        f"python3 scripts/sigil_forge.py verify {result.get('svg')}",
        "Review forge-packet.json methods + ontology for provenance",
    ]
    return result


def interactive_answers(stdin=None, stdout=None) -> dict[str, Any]:
    """Prompt a human on TTY; returns raw answers dict."""
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    answers: dict[str, Any] = {}
    stdout.write("Sigil-Forge wizard (Ctrl+C to abort)\n")
    stdout.write("Methods are craft + encoding — no efficacy claims.\n\n")
    for step in STEPS:
        if not _step_active(step, {**default_answers(), **answers}):
            continue
        default = step.get("default", "")
        hint = ""
        if step["type"] == "choice":
            hint = f" [{'|'.join(step['choices'])}]"
        elif step["type"] == "bool":
            hint = " [y/N]" if not default else " [Y/n]"
        if default not in ("", None) and step["type"] != "bool":
            prompt = f"{step['prompt']}{hint} (default: {default}): "
        else:
            prompt = f"{step['prompt']}{hint}: "
        stdout.write(prompt)
        stdout.flush()
        line = stdin.readline()
        if line == "":
            break
        line = line.strip()
        if not line and "default" in step:
            answers[step["id"]] = step["default"]
            continue
        if step["type"] == "bool":
            if not line:
                answers[step["id"]] = bool(default)
            else:
                answers[step["id"]] = line.lower() in ("y", "yes", "1", "true")
        else:
            answers[step["id"]] = line
    return answers


def load_answers_file(path: Path | str) -> dict[str, Any]:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("answers file must be a JSON object")
    # Allow wrapping { "answers": {...} }
    if "answers" in data and isinstance(data["answers"], dict):
        return data["answers"]
    return data
