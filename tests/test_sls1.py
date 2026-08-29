from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_sls1.py"
SPEC_PATH = ROOT / "standards" / "data" / "sls-1-v3.0-kiss.json"

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

    def test_rejects_extra_motion_class(self) -> None:
        self.assert_invalid(
            lambda data: data["allowed_motion"].update(double_flash={"kind": "flash", "cycle_ms": 1000, "on_ms": 100}),
            "allowed_motion must contain exactly",
        )

    def test_rejects_noncanonical_fast_timing(self) -> None:
        self.assert_invalid(
            lambda data: data["allowed_motion"]["fast_flash"].update(cycle_ms=250, on_ms=125),
            "motion timing must match canonical KISS timing",
        )

    def test_rejects_morse_like_pattern(self) -> None:
        self.assert_invalid(
            lambda data: data["patterns"]["K4"].update(name="DOUBLE_EQUAL"),
            "Morse-like/counting pattern names are forbidden",
        )

    def test_rejects_missing_secondary_carrier_for_error(self) -> None:
        self.assert_invalid(
            lambda data: data["secondary_carrier_required"].remove("ERROR"),
            "critical states missing secondary carrier requirement",
        )

    def test_rejects_overloaded_single_global_indicator(self) -> None:
        self.assert_invalid(
            lambda data: data["single_unlabelled_global_indicator_states"].append("ARMED"),
            "single unlabelled global indicator must be limited",
        )

    def test_rejects_expanded_human_gate(self) -> None:
        self.assert_invalid(
            lambda data: data["recognition_gate"].update(repetitions_per_state=10),
            "recognition gate repetitions_per_state must be 3",
        )

    def test_rejects_blind_single_light_gate(self) -> None:
        self.assert_invalid(
            lambda data: data["recognition_gate"].update(presentation="blind single light"),
            "recognition gate must use the complete labelled panel",
        )

    def test_rejects_missing_confirm_context(self) -> None:
        self.assert_invalid(
            lambda data: data["recognition_gate"]["slots"]["CONFIRM_REQUIRED"].update(label="STATUS"),
            "recognition gate slots must match the fixed KISS context map",
        )


if __name__ == "__main__":
    unittest.main()
