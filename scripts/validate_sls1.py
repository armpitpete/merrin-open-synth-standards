#!/usr/bin/env python3
"""Validate the machine-readable SLS-1 v3 KISS contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "standards" / "data" / "sls-1-v3.0-kiss.json"

ALLOWED_COLOURS = {"white", "green", "blue", "amber", "red"}
ALLOWED_MOTION = {"steady", "slow_flash", "fast_flash"}
EXPECTED_MOTION = {
    "steady": {"kind": "steady"},
    "slow_flash": {"kind": "flash", "cycle_ms": 1000, "on_ms": 500},
    "fast_flash": {"kind": "flash", "cycle_ms": 500, "on_ms": 250},
}
EXPECTED_HUMAN_SEQUENCE = ["notice", "investigate", "lookup", "learned_recognition"]
REQUIRED_DOCUMENTATION = {
    "colour categories",
    "motion categories",
    "critical state meanings",
    "local labels or symbols",
}


def _events_in_rolling_second(motion: dict) -> int:
    if motion.get("kind") == "steady":
        return 0
    cycle = int(motion.get("cycle_ms", 0))
    if cycle <= 0:
        return 999
    return (1000 + cycle - 1) // cycle


def validate(spec: dict) -> list[str]:
    errors: list[str] = []

    if spec.get("standard_id") != "MERRIN-STD-SLS-1":
        errors.append("standard_id must be MERRIN-STD-SLS-1")
    if spec.get("version") != "v3.0-draft":
        errors.append("version must be v3.0-draft")

    if set(spec.get("allowed_colours", [])) != ALLOWED_COLOURS:
        errors.append("allowed_colours must be exactly white, green, blue, amber, red")

    motions = spec.get("allowed_motion", {})
    if set(motions) != ALLOWED_MOTION:
        errors.append("allowed_motion must contain exactly steady, slow_flash, fast_flash")
    for name, expected in EXPECTED_MOTION.items():
        if motions.get(name) != expected:
            errors.append(f"{name}: motion timing must match canonical KISS timing")

    ceiling = int(spec.get("max_visible_on_events_per_rolling_second", 0))
    if ceiling != 2:
        errors.append("max_visible_on_events_per_rolling_second must be 2")
    for name, motion in motions.items():
        if _events_in_rolling_second(motion) > ceiling:
            errors.append(f"{name}: exceeds {ceiling} visible on-events in a rolling second")

    patterns = spec.get("patterns", {})
    state_defaults = spec.get("state_defaults", {})
    for state in spec.get("mandatory_states", []):
        if state not in state_defaults:
            errors.append(f"mandatory state {state} has no default pattern")
    for state, pattern_id in state_defaults.items():
        pattern = patterns.get(pattern_id)
        if not pattern:
            errors.append(f"state {state} references unknown pattern {pattern_id}")
            continue
        if pattern.get("colour") not in ALLOWED_COLOURS:
            errors.append(f"{pattern_id}: unsupported colour {pattern.get('colour')!r}")
        if pattern.get("motion") not in ALLOWED_MOTION:
            errors.append(f"{pattern_id}: unsupported motion {pattern.get('motion')!r}")

    forbidden_tokens = ("double", "triple", "short_long", "long_short", "breathe")
    for pattern_id, pattern in patterns.items():
        normalized = str(pattern.get("name", "")).lower()
        if any(token in normalized for token in forbidden_tokens):
            errors.append(f"{pattern_id}: Morse-like/counting pattern names are forbidden in v3")

    critical = set(spec.get("critical_global_states", []))
    secondary = set(spec.get("secondary_carrier_required", []))
    missing_secondary = sorted(critical - secondary)
    if missing_secondary:
        errors.append(f"critical states missing secondary carrier requirement: {missing_secondary}")

    single_global = set(spec.get("single_unlabelled_global_indicator_states", []))
    if single_global != {"IDLE", "ACTIVE", "WARNING", "ERROR"}:
        errors.append("single unlabelled global indicator must be limited to IDLE, ACTIVE, WARNING, ERROR")

    fallbacks = spec.get("reduced_motion_fallbacks", {})
    for state in critical:
        fallback = fallbacks.get(state)
        if not fallback:
            errors.append(f"critical global state {state} lacks reduced-motion fallback")
            continue
        if fallback.get("animation") != "none":
            errors.append(f"{state}: reduced-motion fallback must set animation=none")
        if not fallback.get("text"):
            errors.append(f"{state}: reduced-motion fallback needs text")

    precedence = spec.get("precedence", [])
    if len(precedence) != len(set(precedence)):
        errors.append("precedence contains duplicate states")
    for state in critical:
        if state not in precedence:
            errors.append(f"critical global state {state} missing from precedence")

    human = spec.get("human_model", {})
    if human.get("sequence") != EXPECTED_HUMAN_SEQUENCE:
        errors.append("human_model sequence must be notice, investigate, lookup, learned_recognition")
    if human.get("first_sight_exact_state_required") is not False:
        errors.append("first-sight exact-state recognition must not be required")
    if human.get("abstract_browser_recognition_gate_required") is not False:
        errors.append("abstract browser recognition must not be a conformance gate")
    if not human.get("indicator_role"):
        errors.append("human_model must define the indicator role")
    if not human.get("documentation_role"):
        errors.append("human_model must define the documentation role")
    if not human.get("learning_goal"):
        errors.append("human_model must define the learning goal")

    if "recognition_gate" in spec:
        errors.append("recognition_gate is superseded; abstract quiz gates are not normative in v3")

    documentation = spec.get("documentation", {})
    if documentation.get("required") is not True:
        errors.append("product indicator documentation must be required")
    if set(documentation.get("must_define", [])) != REQUIRED_DOCUMENTATION:
        errors.append("documentation must define colour, motion, critical meanings, and local labels/symbols")
    if not documentation.get("lookup_target"):
        errors.append("documentation must define an unfamiliar-indicator lookup target")

    evidence = spec.get("implementation_evidence", {})
    if evidence.get("abstract_browser_quiz") != "not a conformance gate":
        errors.append("implementation evidence must mark abstract browser quizzes as non-conformance research")
    questions = evidence.get("real_use_questions", [])
    if len(questions) != 4 or not all(isinstance(question, str) and question.strip() for question in questions):
        errors.append("implementation evidence must define four real-use questions")

    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_SPEC
    spec = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(spec)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
