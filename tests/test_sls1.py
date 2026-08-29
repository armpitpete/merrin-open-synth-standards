from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_sls1.py"
SPEC_PATH = ROOT / "standards" / "data" / "sls-1-v3.0-kiss.json"
MIGRATION_PATH = ROOT / "docs" / "SLS-1_V1_V2_TO_V3_MIGRATION.md"

module_spec = importlib.util.spec_from_file_location("validate_sls1", VALIDATOR_PATH)
validate_sls1 = importlib.util.module_from_spec(module_spec)
assert module_spec.loader is not None
module_spec.loader.exec_module(validate_sls1)


class SLS1ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw_spec = SPEC_PATH.read_text(encoding="utf-8")
        self.spec = validate_sls1.loads_contract(self.raw_spec)

    def assert_invalid(self, mutator, fragment: str) -> None:
        candidate = copy.deepcopy(self.spec)
        mutator(candidate)
        errors = validate_sls1.validate(candidate)
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected error containing {fragment!r}; got {errors!r}",
        )

    def assert_duplicate_member_rejected(self, raw: str, member: str) -> None:
        self.assertNotEqual(raw, self.raw_spec, "duplicate-member fixture injection did not alter the source")
        with self.assertRaises(validate_sls1.DuplicateJSONMemberError) as caught:
            validate_sls1.loads_contract(raw)
        self.assertIn(repr(member), str(caught.exception))

    def test_current_spec_passes(self) -> None:
        self.assertEqual(validate_sls1.validate(self.spec), [])

    def test_rejects_duplicate_top_level_allowed_motion_member(self) -> None:
        raw = self.raw_spec.replace(
            '  "allowed_motion": {\n',
            '  "allowed_motion": {"double_flash": {"kind": "flash", "cycle_ms": 1000, "on_ms": 100}},\n'
            '  "allowed_motion": {\n',
            1,
        )
        self.assert_duplicate_member_rejected(raw, "allowed_motion")

    def test_rejects_duplicate_event_ceiling_member(self) -> None:
        raw = self.raw_spec.replace(
            '  "max_visible_on_events_per_rolling_second": 2,\n',
            '  "max_visible_on_events_per_rolling_second": 99,\n'
            '  "max_visible_on_events_per_rolling_second": 2,\n',
            1,
        )
        self.assert_duplicate_member_rejected(raw, "max_visible_on_events_per_rolling_second")

    def test_rejects_duplicate_single_global_indicator_member(self) -> None:
        raw = self.raw_spec.replace(
            '  "single_unlabelled_global_indicator_states": ["IDLE", "ACTIVE", "WARNING", "ERROR"],\n',
            '  "single_unlabelled_global_indicator_states": ["IDLE", "ACTIVE", "ARMED", "WARNING", "ERROR"],\n'
            '  "single_unlabelled_global_indicator_states": ["IDLE", "ACTIVE", "WARNING", "ERROR"],\n',
            1,
        )
        self.assert_duplicate_member_rejected(raw, "single_unlabelled_global_indicator_states")

    def test_rejects_duplicate_nested_motion_kind(self) -> None:
        raw = self.raw_spec.replace(
            '    "steady": {"kind": "steady"},\n',
            '    "steady": {"kind": "flash", "kind": "steady"},\n',
            1,
        )
        self.assert_duplicate_member_rejected(raw, "kind")

    def test_rejects_duplicate_nested_documentation_required(self) -> None:
        raw = self.raw_spec.replace(
            '    "required": true,\n',
            '    "required": false, "required": true,\n',
            1,
        )
        self.assert_duplicate_member_rejected(raw, "required")

    def test_rejects_duplicate_nested_reduced_motion_text(self) -> None:
        raw = self.raw_spec.replace(
            '    "ERROR": {"text": "Error", "symbol": "×", "animation": "none"},\n',
            '    "ERROR": {"text": "All clear", "text": "Error", "symbol": "×", "animation": "none"},\n',
            1,
        )
        self.assert_duplicate_member_rejected(raw, "text")

    def test_rejects_unknown_top_level_field(self) -> None:
        self.assert_invalid(
            lambda data: data.update(pulse_sequences={"hidden": [1, 2, 3]}),
            "top-level contract keys must be exact",
        )

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

    def test_rejects_float_event_ceiling(self) -> None:
        self.assert_invalid(
            lambda data: data.update(max_visible_on_events_per_rolling_second=2.9),
            "must be the integer 2",
        )

    def test_rejects_string_event_ceiling(self) -> None:
        self.assert_invalid(
            lambda data: data.update(max_visible_on_events_per_rolling_second="2"),
            "must be the integer 2",
        )

    def test_rejects_duplicate_allowed_colour(self) -> None:
        self.assert_invalid(
            lambda data: data["allowed_colours"].append("red"),
            "allowed_colours must match the canonical ordered list exactly",
        )

    def test_rejects_morse_like_pattern(self) -> None:
        self.assert_invalid(
            lambda data: data["patterns"]["K4"].update(name="DOUBLE_EQUAL"),
            "pattern schema/value must match canonical KISS definition exactly",
        )

    def test_rejects_hidden_pattern_sequence_field(self) -> None:
        self.assert_invalid(
            lambda data: data["patterns"]["K4"].update(sequence=["short", "short"]),
            "pattern schema/value must match canonical KISS definition exactly",
        )

    def test_rejects_unreferenced_pattern_injection(self) -> None:
        self.assert_invalid(
            lambda data: data["patterns"].update(
                K10={"name": "HIDDEN", "colour": "amber", "motion": "steady", "brightness": "mid"}
            ),
            "patterns must contain exactly canonical K0-K9",
        )

    def test_rejects_semantic_state_remap(self) -> None:
        self.assert_invalid(
            lambda data: data["state_defaults"].update(ERROR="K1"),
            "state_defaults must match the canonical state-to-pattern mapping exactly",
        )

    def test_rejects_deleted_critical_contract_lists(self) -> None:
        def remove_contract(data: dict) -> None:
            data.pop("critical_global_states")
            data.pop("secondary_carrier_required")

        self.assert_invalid(remove_contract, "top-level contract keys must be exact")

    def test_rejects_modified_critical_state_set(self) -> None:
        self.assert_invalid(
            lambda data: data["critical_global_states"].remove("ERROR"),
            "critical_global_states must match the canonical ordered list exactly",
        )

    def test_rejects_duplicate_critical_state(self) -> None:
        self.assert_invalid(
            lambda data: data["critical_global_states"].append("ERROR"),
            "critical_global_states must match the canonical ordered list exactly",
        )

    def test_rejects_missing_secondary_carrier_for_error(self) -> None:
        self.assert_invalid(
            lambda data: data["secondary_carrier_required"].remove("ERROR"),
            "secondary_carrier_required must match the canonical ordered list exactly",
        )

    def test_rejects_duplicate_secondary_carrier(self) -> None:
        self.assert_invalid(
            lambda data: data["secondary_carrier_required"].append("ERROR"),
            "secondary_carrier_required must match the canonical ordered list exactly",
        )

    def test_rejects_overloaded_single_global_indicator(self) -> None:
        self.assert_invalid(
            lambda data: data["single_unlabelled_global_indicator_states"].append("ARMED"),
            "single_unlabelled_global_indicator_states must match the canonical ordered list exactly",
        )

    def test_rejects_duplicate_single_global_indicator_state(self) -> None:
        self.assert_invalid(
            lambda data: data["single_unlabelled_global_indicator_states"].append("ERROR"),
            "single_unlabelled_global_indicator_states must match the canonical ordered list exactly",
        )

    def test_rejects_precedence_remap(self) -> None:
        self.assert_invalid(
            lambda data: data["precedence"].reverse(),
            "precedence must match the canonical SLS-1 v3 precedence exactly",
        )

    def test_rejects_rewritten_design_rule(self) -> None:
        self.assert_invalid(
            lambda data: data.update(design_rule="Count three pulses to identify ERROR"),
            "design_rule must match the canonical SLS-1 v3 KISS rule exactly",
        )

    def test_rejects_rewritten_indicator_role(self) -> None:
        self.assert_invalid(
            lambda data: data["human_model"].update(indicator_role="encode the complete state in pulse counts"),
            "human_model indicator_role must match the canonical v3 role exactly",
        )

    def test_rejects_rewritten_documentation_role(self) -> None:
        self.assert_invalid(
            lambda data: data["human_model"].update(documentation_role="documentation is optional"),
            "human_model documentation_role must match the canonical v3 role exactly",
        )

    def test_rejects_rewritten_learning_goal(self) -> None:
        self.assert_invalid(
            lambda data: data["human_model"].update(learning_goal="memorise pulse counts before use"),
            "human_model learning_goal must match the canonical v3 goal exactly",
        )

    def test_rejects_rewritten_lookup_target(self) -> None:
        self.assert_invalid(
            lambda data: data["documentation"].update(lookup_target="no lookup is needed"),
            "documentation lookup_target must match the canonical v3 lookup requirement exactly",
        )

    def test_rejects_duplicate_documentation_definition(self) -> None:
        self.assert_invalid(
            lambda data: data["documentation"]["must_define"].append("critical state meanings"),
            "documentation.must_define must match the canonical ordered list exactly",
        )

    def test_rejects_rewritten_real_use_questions(self) -> None:
        self.assert_invalid(
            lambda data: data["implementation_evidence"]["real_use_questions"].__setitem__(
                0, "Can a stranger name the exact state after one second?"
            ),
            "implementation evidence real_use_questions must match the canonical v3 questions exactly",
        )

    def test_rejects_swapped_reduced_motion_symbols(self) -> None:
        def swap_symbols(data: dict) -> None:
            armed = data["reduced_motion_fallbacks"]["ARMED"]["symbol"]
            error = data["reduced_motion_fallbacks"]["ERROR"]["symbol"]
            data["reduced_motion_fallbacks"]["ARMED"]["symbol"] = error
            data["reduced_motion_fallbacks"]["ERROR"]["symbol"] = armed

        self.assert_invalid(
            swap_symbols,
            "reduced_motion_fallbacks must match the canonical state/text/symbol/animation mapping exactly",
        )

    def test_rejects_contradictory_reduced_motion_text(self) -> None:
        self.assert_invalid(
            lambda data: data["reduced_motion_fallbacks"]["ERROR"].update(text="All clear"),
            "reduced_motion_fallbacks must match the canonical state/text/symbol/animation mapping exactly",
        )

    def test_rejects_first_sight_exact_state_requirement(self) -> None:
        self.assert_invalid(
            lambda data: data["human_model"].update(first_sight_exact_state_required=True),
            "first-sight exact-state recognition must not be required",
        )

    def test_rejects_abstract_quiz_as_gate(self) -> None:
        self.assert_invalid(
            lambda data: data["human_model"].update(abstract_browser_recognition_gate_required=True),
            "abstract browser recognition must not be a conformance gate",
        )

    def test_rejects_reintroduced_recognition_gate(self) -> None:
        self.assert_invalid(
            lambda data: data.update(recognition_gate={"name": "blind quiz"}),
            "recognition_gate is superseded",
        )

    def test_rejects_missing_documentation_key(self) -> None:
        self.assert_invalid(
            lambda data: data["documentation"]["must_define"].remove("critical state meanings"),
            "documentation.must_define must match the canonical ordered list exactly",
        )

    def test_rejects_wrong_human_sequence(self) -> None:
        self.assert_invalid(
            lambda data: data["human_model"].update(sequence=["memorise", "decode"]),
            "human_model sequence must be notice, investigate, lookup, learned_recognition",
        )

    def test_migration_marks_abstract_quiz_as_retired_research(self) -> None:
        migration = MIGRATION_PATH.read_text(encoding="utf-8")
        self.assertNotIn("The v3 gate is a separate unfamiliar-person test", migration)
        self.assertIn("not a conformance gate", migration)


if __name__ == "__main__":
    unittest.main()