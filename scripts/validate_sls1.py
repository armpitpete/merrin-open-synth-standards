#!/usr/bin/env python3
"""Validate the machine-readable SLS-1 v2 pattern contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "standards" / "data" / "sls-1-v2.0-patterns.json"


def _segments(pattern: dict) -> list[tuple[int, int]]:
    return [(int(item["level"]), int(item["duration_ms"])) for item in pattern.get("segments", [])]


def _canonical_cycle_signature(pattern: dict) -> tuple:
    if pattern.get("kind") != "pulse":
        return (pattern.get("kind"), pattern.get("brightness"), pattern.get("cycle_ms"))
    segments = _segments(pattern)
    rotations = []
    for i in range(len(segments)):
        rotated = tuple(segments[i:] + segments[:i])
        rotations.append(rotated)
    return ("pulse", min(rotations))


def _pulse_starts(pattern: dict) -> list[int]:
    if pattern.get("kind") != "pulse":
        return []
    starts = []
    elapsed = 0
    previous = 0
    for level, duration in _segments(pattern):
        if level == 1 and previous == 0:
            starts.append(elapsed)
        previous = level
        elapsed += duration
    return starts


def _max_pulses_in_rolling_window(pattern: dict, window_ms: int) -> int:
    if pattern.get("kind") != "pulse":
        return 0
    cycle = int(pattern["cycle_ms"])
    starts = _pulse_starts(pattern)
    if not starts:
        return 0
    repeated = []
    repeats = (window_ms // cycle) + 3
    for k in range(-1, repeats + 1):
        repeated.extend(start + k * cycle for start in starts)
    maximum = 0
    for phase in range(cycle):
        count = sum(phase <= t < phase + window_ms for t in repeated)
        maximum = max(maximum, count)
    return maximum


def validate(spec: dict) -> list[str]:
    errors: list[str] = []

    if spec.get("standard_id") != "MERRIN-STD-SLS-1":
        errors.append("standard_id must be MERRIN-STD-SLS-1")
    if spec.get("version") != "v2.0-draft":
        errors.append("version must be v2.0-draft")

    window = int(spec.get("signature_window_ms", 0))
    ceiling = int(spec.get("max_visible_pulses_per_rolling_second", 0))
    if window != 1000:
        errors.append("signature_window_ms must be 1000")
    if ceiling <= 0 or ceiling > 3:
        errors.append("pulse ceiling must be between 1 and 3 inclusive")

    patterns = spec.get("patterns", {})
    state_defaults = spec.get("state_defaults", {})

    for state in spec.get("mandatory_states", []):
        if state not in state_defaults:
            errors.append(f"mandatory state {state} has no default pattern")

    for state, pattern_id in state_defaults.items():
        if pattern_id not in patterns:
            errors.append(f"state {state} references unknown pattern {pattern_id}")

    for pattern_id, pattern in patterns.items():
        kind = pattern.get("kind")
        if kind not in {"steady", "breathe", "pulse"}:
            errors.append(f"{pattern_id}: unsupported kind {kind!r}")
            continue

        if kind == "pulse":
            segments = _segments(pattern)
            if not segments:
                errors.append(f"{pattern_id}: pulse pattern has no segments")
                continue
            if any(level not in {0, 1} for level, _ in segments):
                errors.append(f"{pattern_id}: segment levels must be 0 or 1")
            if any(duration <= 0 for _, duration in segments):
                errors.append(f"{pattern_id}: segment durations must be positive")
            total = sum(duration for _, duration in segments)
            cycle = int(pattern.get("cycle_ms", 0))
            if total != cycle:
                errors.append(f"{pattern_id}: segments total {total} ms but cycle is {cycle} ms")
            if _max_pulses_in_rolling_window(pattern, 1000) > ceiling:
                errors.append(f"{pattern_id}: exceeds {ceiling} visible pulses in a rolling second")
            if pattern.get("signature_required") and cycle > window:
                errors.append(f"{pattern_id}: critical signature cycle {cycle} ms exceeds {window} ms")

    critical_states = spec.get("critical_global_states", [])
    seen: dict[tuple, str] = {}
    for state in critical_states:
        pattern_id = state_defaults.get(state)
        if pattern_id is None:
            errors.append(f"critical global state {state} has no default pattern")
            continue
        pattern = patterns.get(pattern_id)
        if not pattern:
            continue
        if not pattern.get("signature_required"):
            errors.append(f"critical global state {state} uses non-signature pattern {pattern_id}")
        signature = _canonical_cycle_signature(pattern)
        if signature in seen:
            errors.append(f"critical global states {seen[signature]} and {state} have cyclically equivalent patterns")
        else:
            seen[signature] = state

    fallbacks = spec.get("reduced_motion_fallbacks", {})
    for state in critical_states:
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
    for state in critical_states:
        if state not in precedence:
            errors.append(f"critical global state {state} missing from precedence")

    required_names = {
        "WARNING": "WARNING_SHORT_LONG",
        "ERROR": "ERROR_LONG_SHORT",
        "ARMED": "DOUBLE_EQUAL_1HZ",
        "CONFIRM_REQUIRED": "TRIPLE_EQUAL_1HZ",
        "RECORD_WRITE": "PULSE_SHORT_1HZ",
        "CLOCK_LOST": "CLOCK_LOST_WIDE_DOUBLE",
    }
    for state, expected_name in required_names.items():
        pattern_id = state_defaults.get(state)
        actual_name = patterns.get(pattern_id, {}).get("name")
        if actual_name != expected_name:
            errors.append(f"{state}: expected canonical pattern {expected_name}, got {actual_name}")

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
