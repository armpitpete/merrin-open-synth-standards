#!/usr/bin/env python3
"""Validate the machine-readable SLS-1 v3 KISS contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "standards" / "data" / "sls-1-v3.0-kiss.json"

EXPECTED_ALLOWED_COLOURS = ["white", "green", "blue", "amber", "red"]
ALLOWED_MOTION = {"steady", "slow_flash", "fast_flash"}
EXPECTED_MOTION = {
    "steady": {"kind": "steady"},
    "slow_flash": {"kind": "flash", "cycle_ms": 1000, "on_ms": 500},
    "fast_flash": {"kind": "flash", "cycle_ms": 500, "on_ms": 250},
}
EXPECTED_DESIGN_RULE = "KISS: colour carries category, motion carries urgency, context carries exact local meaning"
EXPECTED_HUMAN_SEQUENCE = ["notice", "investigate", "lookup", "learned_recognition"]
EXPECTED_INDICATOR_ROLE = (
    "make a labelled or contextual condition visibly active; do not encode the whole state name in a blink alphabet"
)
EXPECTED_DOCUMENTATION_ROLE = "provide the exact meaning on first encounter"
EXPECTED_LEARNING_GOAL = "after lookup, the same convention should be easier to recognise on later encounters"
EXPECTED_LOOKUP_TARGET = (
    "a user encountering an unfamiliar indicator can determine its exact meaning from the product documentation "
    "without decoding a pulse sequence"
)
EXPECTED_REAL_USE_QUESTIONS = [
    "Is an important state noticeable during realistic use?",
    "Can the user find the explanation when the indicator is unfamiliar?",
    "Does the documentation resolve the exact meaning correctly?",
    "Does repeated use make the convention easier to recognise without adding a more complex code?",
]
EXPECTED_DOCUMENTATION_DEFINITIONS = [
    "colour categories",
    "motion categories",
    "critical state meanings",
    "local labels or symbols",
]

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
EXPECTED_CRITICAL_STATES = [
    "ERROR",
    "CONFIRM_REQUIRED",
    "ARMED",
    "RECORD_WRITE",
    "WARNING",
    "CLOCK_LOST",
]
EXPECTED_SECONDARY_CARRIER_REQUIRED = [
    "ARMED",
    "CONFIRM_REQUIRED",
    "RECORD_WRITE",
    "WARNING",
    "ERROR",
    "CLOCK_LOST",
]
EXPECTED_SINGLE_GLOBAL = ["IDLE", "ACTIVE", "WARNING", "ERROR"]
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
EXPECTED_REDUCED_MOTION_FALLBACKS = {
    "ARMED": {"text": "Armed", "symbol": "A", "animation": "none"},
    "CONFIRM_REQUIRED": {"text": "Confirm", "symbol": "!", "animation": "none"},
    "RECORD_WRITE": {"text": "Writing", "symbol": "W", "animation": "none"},
    "WARNING": {"text": "Warning", "symbol": "△", "animation": "none"},
    "ERROR": {"text": "Error", "symbol": "×", "animation": "none"},
    "CLOCK_LOST": {"text": "Clock lost", "symbol": "C", "animation": "none"},
}


def _events_in_rolling_second(motion: dict) -> int:
    if motion.get("kind") == "steady":
        return 0
    cycle = motion.get("cycle_ms")
    if type(cycle) is not int or cycle <= 0:
        return 999
    return (1000 + cycle - 1) // cycle


def _require_exact_list(errors: list[str], label: str, actual: object, expected: list[str]) -> None:
    if actual != expected:
        errors.append(f"{label} must match the canonical ordered list exactly")


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
    if spec.get("design_rule") != EXPECTED_DESIGN_RULE:
        errors.append("design_rule must match the canonical SLS-1 v3 KISS rule exactly")

    _require_exact_list(errors, "allowed_colours", spec.get("allowed_colours"), EXPECTED_ALLOWED_COLOURS)

    motions = spec.get("allowed_motion", {})
    if set(motions) != ALLOWED_MOTION:
        errors.append("allowed_motion must contain exactly steady, slow_flash, fast_flash")
    for name, expected in EXPECTED_MOTION.items():
        if motions.get(name) != expected:
            errors.append(f"{name}: motion timing must match canonical KISS timing")

    ceiling = spec.get("max_visible_on_events_per_rolling_second")
    if type(ceiling) is not int or ceiling != 2:
        errors.append("max_visible_on_events_per_rolling_second must be the integer 2")
    for name, motion in motions.items():
        if isinstance(motion, dict) and _events_in_rolling_second(motion) > 2:
            errors.append(f"{name}: exceeds 2 visible on-events in a rolling second")

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

    _require_exact_list(
        errors,
        "critical_global_states",
        spec.get("critical_global_states"),
        EXPECTED_CRITICAL_STATES,
    )
    _require_exact_list(
        errors,
        "secondary_carrier_required",
        spec.get("secondary_carrier_required"),
        EXPECTED_SECONDARY_CARRIER_REQUIRED,
    )
    _require_exact_list(
        errors,
        "single_unlabelled_global_indicator_states",
        spec.get("single_unlabelled_global_indicator_states"),
        EXPECTED_SINGLE_GLOBAL,
    )

    fallbacks = spec.get("reduced_motion_fallbacks", {})
    if fallbacks != EXPECTED_REDUCED_MOTION_FALLBACKS:
        errors.append("reduced_motion_fallbacks must match the canonical state/text/symbol/animation mapping exactly")

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
    if human.get("indicator_role") != EXPECTED_INDICATOR_ROLE:
        errors.append("human_model indicator_role must match the canonical v3 role exactly")
    if human.get("documentation_role") != EXPECTED_DOCUMENTATION_ROLE:
        errors.append("human_model documentation_role must match the canonical v3 role exactly")
    if human.get("learning_goal") != EXPECTED_LEARNING_GOAL:
        errors.append("human_model learning_goal must match the canonical v3 goal exactly")

    if "recognition_gate" in spec:
        errors.append("recognition_gate is superseded; abstract quiz gates are not normative in v3")

    documentation = spec.get("documentation", {})
    if set(documentation) != EXPECTED_DOCUMENTATION_KEYS:
        errors.append("documentation keys must match the canonical v3 documentation contract exactly")
    if documentation.get("required") is not True:
        errors.append("product indicator documentation must be required")
    _require_exact_list(
        errors,
        "documentation.must_define",
        documentation.get("must_define"),
        EXPECTED_DOCUMENTATION_DEFINITIONS,
    )
    if documentation.get("lookup_target") != EXPECTED_LOOKUP_TARGET:
        errors.append("documentation lookup_target must match the canonical v3 lookup requirement exactly")

    evidence = spec.get("implementation_evidence", {})
    if set(evidence) != EXPECTED_IMPLEMENTATION_EVIDENCE_KEYS:
        errors.append("implementation_evidence keys must match the canonical v3 evidence contract exactly")
    if evidence.get("abstract_browser_quiz") != "not a conformance gate":
        errors.append("implementation evidence must mark abstract browser quizzes as non-conformance research")
    if evidence.get("real_use_questions") != EXPECTED_REAL_USE_QUESTIONS:
        errors.append("implementation evidence real_use_questions must match the canonical v3 questions exactly")

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
