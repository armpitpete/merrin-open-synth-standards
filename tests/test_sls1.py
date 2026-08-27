from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_sls1.py"
SPEC_PATH = ROOT / "standards" / "data" / "sls-1-v2.0-patterns.json"

module_spec = importlib.util.spec_from_file_location("validate_sls1", VALIDATOR_PATH)
validate_sls1 = importlib.util.module_from_spec(module_spec)
assert module_spec.loader is not None
module_spec.loader.exec_module(validate_sls1)


class SLS1ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))

    def assert_invalid(self, mutator, fragment: str) -> None:
        candidate = copy.deepcopy(self.spec)
        mutator(candidate)
        errors = validate_sls1.validate(candidate)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_current_spec_passes(self) -> None:
        self.assertEqual(validate_sls1.validate(self.spec), [])

    def test_rejects_two_second_critical_signature(self) -> None:
        def mutate(data):
            data["patterns"]["P5"]["segments"][-1]["duration_ms"] += 1000
            data["patterns"]["P5"]["cycle_ms"] = 2000
        self.assert_invalid(mutate, "critical signature cycle 2000 ms exceeds 1000 ms")

    def test_rejects_four_pulses_per_second(self) -> None:
        def mutate(data):
            data["patterns"]["P5"]["segments"] = [
                {"level": 1, "duration_ms": 100},
                {"level": 0, "duration_ms": 150},
            ] * 4
            data["patterns"]["P5"]["cycle_ms"] = 1000
        self.assert_invalid(mutate, "exceeds 3 visible pulses")

    def test_rejects_duplicate_critical_pattern(self) -> None:
        def mutate(data):
            source_id = data["state_defaults"]["ARMED"]
            target_id = data["state_defaults"]["WARNING"]
            data["patterns"][target_id] = copy.deepcopy(data["patterns"][source_id])
            data["patterns"][target_id]["name"] = "WARNING_SHORT_LONG"
        self.assert_invalid(mutate, "cyclically equivalent")

    def test_rejects_missing_warning_pattern(self) -> None:
        self.assert_invalid(
            lambda data: data["state_defaults"].pop("WARNING"),
            "mandatory state WARNING has no default pattern",
        )

    def test_rejects_motion_only_critical_fallback(self) -> None:
        self.assert_invalid(
            lambda data: data["reduced_motion_fallbacks"]["ERROR"].update(animation="pulse"),
            "reduced-motion fallback must set animation=none",
        )


if __name__ == "__main__":
    unittest.main()
