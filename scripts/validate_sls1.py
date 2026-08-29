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

EXPECTED_TOP_LEVEL_KEYS = {
    "standard_id",
    "version",
    "design_rule",
    "human_model",
    "max_visible_on_events_per_rolling_second",
    "allowed_colours",
    "allowed_motion",
    "mandatory_states",
    "critical_global_states",
    "precedence",
    "patterns",
    "state_defaults",
    "secondary_carrier_required",
    "single_unlabelled_global_indicator_states",
    "reduced_motion_fallbacks",
    "documentation",
    "implementation_evidence",
}
EXPECTED_HUMAN_MODEL_KEYS = {
    "sequence",
    "first_sight_exact_state_required",
    "indicator_role",
    "documentation_role",
    "learning_goal",
    "abstract_browser_recognition_gate_required",
}
EXPECTED_DOCUMENTATION_KEYS = {"required", "must_define", "lookup_target"}
EXPECTED_IMPLEMENTATION_EVIDENCE_KEYS = {"abstract_browser_quiz", "real_use_questions"}

EXPECTED_MANDATORY_STATES = [
    "IDLE",
    "ACTIVE",
    "ALT_SHIFTED",
    "MUTED_BYPASSED",
    "ARMED",
    "CONFIRM_REQUIRED",
    "RECORD_WRITE",
    "WARNING",
    "ERROR",
]
EXPECTED_CRITICAL_STATES = {
    "ERROR",
    "CONFIRM_REQUIRED",
    "ARMED",
    "RECORD_WRITE",
    "WARNING",
    "CLOCK_LOST",
}
EXPECTED_SECONDARY_CARRIER_REQUIRED = {
    "ARMED",
    "CONFIRM_REQUIRED",
    "RECORD_WRITE",
    "WARNING",
    "ERROR",
    "CLOCK_LOST",
}
EXPECTED_SINGLE_GLOBAL = {"IDLE", "ACTIVE", "WARNING", "ERROR"}
EXPECTED_PRECEDENCE = [
    "ERROR",
    "CONFIRM_REQUIRED",
    "ARMED",
    "RECORD_WRITE",
    "WARNING",
    "CLOCK_LOST",
    "MUTED_BYPASSED",
    "ALT_SHIFTED",
    "ACTIVE",
    "IDLE",
]
EXPECTED_PATTERNS = {
    "K0": {"name": "NEUTRAL_DIM", "colour": "white", "motion": "steady", "brightness": "dim"},
    "K1": {"name": "NORMAL_STEADY", "colour": "green", "motion": "steady", "brightness": "mid"},
    "K2": {"name": "MODE_STEADY", "colour": "blue", "motion": "steady", "brightness": "mid"},
    "K3": {"name": "NEUTRAL_SLOW_FLASH", "colour": "white", "motion": "slow_flash", "brightness": "mid"},
    "K4": {"name": "ATTENTION_STEADY", "colour": "amber", "motion": "steady", "brightness": "mid"},
    "K5": {"name": "ATTENTION_SLOW_FLASH", "colour": "amber", "motion": "slow_flash", "brightness": "mid"},
    "K6": {"name": "WRITE_STEADY", "colour": "red", "motion": "steady", "brightness": "mid"},
    "K7": {"name": "ATTENTION_FAST_FLASH", "colour": "amber", "motion": "fast_flash", "brightness": "bright"},
    "K8": {"name": "ERROR_FAST_FLASH", "colour": "red", "motion": "fast_flash", "brightness": "bright"},
    "K9": {"name": "CLOCK_SLOW_FLASH", "colour": "blue", "motion": "slow_flash", "brightness": "mid"},
}
EXPECTED_STATE_DEFAULTS = {
    "IDLE": "K0",
    "ACTIVE": "K1",
    "ALT_SHIFTED": "K2",
    "MUTED_BYPASSED": "K3",
    "ARMED": "K4",
    "CONFIRM_REQUIRED": "K5",
    "RECORD_WRITE": "K6",
    "WARNING": "K7",
    "ERROR": "K8",
    "CLOCK_PRESENT": "K2",
    "CLOCK_LOST": "K9",
    "TRANSPORT_RUN": "K1",
    "TRANSPORT_STOP": "K0",
    "SELECTED_FOCUSED": "K2",
    "LOCKED_HELD": "K4",
}
EXPECTED_FALLBACK_KEYS = {"text", "symbol", "animation"}


def _events_in_rolling_second(motion: dict) -> int:
    if motion.get("kind") == "steady":
        return 0
    cycle = int(motion.get("cycle_ms", 0))
    if cycle <= 0:
        return 999
    return (1000 + cycle - 1) // cycle


def _report_exact_set(errors: list[str], label: str, actual: object, expected: set[str]) -> None:
    try:
        actual_set = set(actual or [])
    except TypeError:
        errors.append(f"{label} must be a list containing exactly {sorted(expected)}")
        return
    if actual_set != expected:
        errors.append(f"{label} must contain exactly {sorted(expected)}")


def validate(spec: dict) -> list[str]:
    errors: list[str] = []

    if set(spec) != EXPECTED_TOP_LEVEL_KEYS:
        missing = sorted(EXPECTED_TOP_LEVEL_KEYS - set(spec))
        extra = sorted(set(spec) - EXPECTED_TOP_LEVEL_KEYS)
        errors.append(f"top-level contract keys must be exact; missing={missing}, extra={extra}")

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
        if isinstance(motion, dict) and _events_in_rolling_second(motion) > ceiling:
            errors.append(f"{name}: exceeds {ceiling} visible on-events in a rolling second")

    if spec.get("mandatory_states") != EXPECTED_MANDATORY_STATES:
        errors.append("mandatory_states must match the canonical SLS-1 v3 state list exactly")

    patterns = spec.get("patterns", {})
    if set(patterns) != set(EXPECTED_PATTERNS):
        missing = sorted(set(EXPECTED_PATTERNS) - set(patterns))
        extra = sorted(set(patterns) - set(EXPECTED_PATTERNS))
        errors.append(f"patterns must contain exactly canonical K0-K9; missing={missing}, extra={extra}")
    for pattern_id, expected in EXPECTED_PATTERNS.items():
        pattern = patterns.get(pattern_id)
        if pattern != expected:
            errors.append(f"{pattern_id}: pattern schema/value must match canonical KISS definition exactly")

    state_defaults = spec.get("state_defaults", {})
    if state_defaults != EXPECTED_STATE_DEFAULTS:
        errors.append("state_defaults must match the canonical state-to-pattern mapping exactly")

    forbidden_tokens = ("double", "triple", "short_long", "long_short", "breathe")
    for pattern_id, pattern in patterns.items():
        if not isinstance(pattern, dict):
            errors.append(f"{pattern_id}: pattern must be an object")
            continue
        normalized = str(pattern.get("name", "")).lower()
        if any(token in normalized for token in forbidden_tokens):
            errors.append(f"{pattern_id}: Morse-like/counting pattern names are forbidden in v3")

    _report_exact_set(errors, "critical_global_states", spec.get("critical_global_states"), EXPECTED_CRITICAL_STATES)
    _report_exact_set(
        errors,
        "secondary_carrier_required",
        spec.get("secondary_carrier_required"),
        EXPECTED_SECONDARY_CARRIER_REQUIRED,
    )

    single_global = set(spec.get("single_unlabelled_global_indicator_states", []))
    if single_global != EXPECTED_SINGLE_GLOBAL:
        errors.append("single unlabelled global indicator must be limited to IDLE, ACTIVE, WARNING, ERROR")

    fallbacks = spec.get("reduced_motion_fallbacks", {})
    if set(fallbacks) != EXPECTED_CRITICAL_STATES:
        errors.append("reduced_motion_fallbacks must cover exactly the canonical critical states")
    for state in EXPECTED_CRITICAL_STATES:
        fallback = fallbacks.get(state)
        if not isinstance(fallback, dict):
            errors.append(f"critical global state {state} lacks reduced-motion fallback")
            continue
        if set(fallback) != EXPECTED_FALLBACK_KEYS:
            errors.append(f"{state}: reduced-motion fallback keys must be exactly text, symbol, animation")
        if fallback.get("animation") != "none":
            errors.append(f"{state}: reduced-motion fallback must set animation=none")
        if not fallback.get("text"):
            errors.append(f"{state}: reduced-motion fallback needs text")
        if not fallback.get("symbol"):
            errors.append(f"{state}: reduced-motion fallback needs symbol")

    if spec.get("precedence") != EXPECTED_PRECEDENCE:
        errors.append("precedence must match the canonical SLS-1 v3 precedence exactly")

    human = spec.get("human_model", {})
    if set(human) != EXPECTED_HUMAN_MODEL_KEYS:
        errors.append("human_model keys must match the canonical v3 human-use contract exactly")
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
    if set(documentation) != EXPECTED_DOCUMENTATION_KEYS:
        errors.append("documentation keys must match the canonical v3 documentation contract exactly")
    if documentation.get("required") is not True:
        errors.append("product indicator documentation must be required")
    if set(documentation.get("must_define", [])) != REQUIRED_DOCUMENTATION:
        errors.append("documentation must define colour, motion, critical meanings, and local labels/symbols")
    if not documentation.get("lookup_target"):
        errors.append("documentation must define an unfamiliar-indicator lookup target")

    evidence = spec.get("implementation_evidence", {})
    if set(evidence) != EXPECTED_IMPLEMENTATION_EVIDENCE_KEYS:
        errors.append("implementation_evidence keys must match the canonical v3 evidence contract exactly")
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
