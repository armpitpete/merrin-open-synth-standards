from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_standard_maturity.py"
SPEC = importlib.util.spec_from_file_location("validate_standard_maturity", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
MaturityError = MODULE.MaturityError
validate_repository = MODULE.validate_repository
VERSION = "v1.0-test"


def standard_text(standard_id: str, status: str) -> str:
    return f"""---
standard_id: {standard_id}
title: Fixture
version: {VERSION}
status: {status}
scope: Test fixture.
license: CC-BY-4.0
---

# Fixture
"""


def write_readme(root: Path, standard_id: str, status: str) -> None:
    (root / "README.md").write_text(
        "| Standard | Title | What it answers | Status |\n"
        "|---|---|---|---|\n"
        f"| [{standard_id}](standards/fixture.md) | Fixture | Test | {status} |\n",
        encoding="utf-8",
    )


def accepted_review() -> dict[str, str]:
    return {
        "decision": "ACCEPT FOR CURRENT STATUS",
        "evidence": "https://example.invalid/review",
    }


class StandardMaturityTests(unittest.TestCase):
    def test_current_repository_standards_remain_draft(self):
        found = dict(validate_repository(ROOT))
        self.assertEqual(
            found,
            {
                "MERRIN-STD-HIL-1": "Draft",
                "MERRIN-STD-SLS-1": "Draft",
            },
        )

    def test_publication_alone_cannot_create_stable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "standards").mkdir()
            (root / "standards" / "fixture.md").write_text(
                standard_text("TEST-1", "Stable"), encoding="utf-8"
            )
            with self.assertRaisesRegex(MaturityError, "Stable requires evidence/maturity/TEST-1.json"):
                validate_repository(root)

    def test_maturity_evidence_must_match_exact_standard_version(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "standards").mkdir()
            evidence_dir = root / "evidence" / "maturity"
            evidence_dir.mkdir(parents=True)
            (root / "standards" / "fixture.md").write_text(
                standard_text("TEST-1", "Freeze Candidate"), encoding="utf-8"
            )
            payload = {
                "standard_id": "TEST-1",
                "version": "v0.9-old",
                "status": "Freeze Candidate",
                "implementation_or_use": [
                    {
                        "context": "bounded implementation",
                        "evidence": "https://example.invalid/use",
                    }
                ],
                "review": accepted_review(),
            }
            (evidence_dir / "TEST-1.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(MaturityError, "version mismatch"):
                validate_repository(root)

    def test_stable_requires_multiple_independent_contexts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "standards").mkdir()
            evidence_dir = root / "evidence" / "maturity"
            evidence_dir.mkdir(parents=True)
            (root / "standards" / "fixture.md").write_text(
                standard_text("TEST-1", "Stable"), encoding="utf-8"
            )
            payload = {
                "standard_id": "TEST-1",
                "version": VERSION,
                "status": "Stable",
                "implementations": [
                    {
                        "implementation_id": "instrument-a",
                        "independent_context": True,
                        "successful_use": True,
                        "evidence": "https://example.invalid/a",
                    }
                ],
                "review": accepted_review(),
            }
            (evidence_dir / "TEST-1.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(MaturityError, "at least two implementation contexts"):
                validate_repository(root)

    def test_stable_requires_explicit_successful_use(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "standards").mkdir()
            evidence_dir = root / "evidence" / "maturity"
            evidence_dir.mkdir(parents=True)
            (root / "standards" / "fixture.md").write_text(
                standard_text("TEST-1", "Stable"), encoding="utf-8"
            )
            payload = {
                "standard_id": "TEST-1",
                "version": VERSION,
                "status": "Stable",
                "implementations": [
                    {
                        "implementation_id": "instrument-a",
                        "independent_context": True,
                        "successful_use": True,
                        "evidence": "https://example.invalid/a",
                    },
                    {
                        "implementation_id": "instrument-b",
                        "independent_context": True,
                        "successful_use": False,
                        "evidence": "https://example.invalid/b",
                    },
                ],
                "review": accepted_review(),
            }
            (evidence_dir / "TEST-1.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(MaturityError, "must declare successful use"):
                validate_repository(root)

    def test_duplicate_implementation_context_cannot_fake_stable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "standards").mkdir()
            evidence_dir = root / "evidence" / "maturity"
            evidence_dir.mkdir(parents=True)
            (root / "standards" / "fixture.md").write_text(
                standard_text("TEST-1", "Stable"), encoding="utf-8"
            )
            payload = {
                "standard_id": "TEST-1",
                "version": VERSION,
                "status": "Stable",
                "implementations": [
                    {
                        "implementation_id": "same-instrument",
                        "independent_context": True,
                        "successful_use": True,
                        "evidence": "https://example.invalid/a",
                    },
                    {
                        "implementation_id": "same-instrument",
                        "independent_context": True,
                        "successful_use": True,
                        "evidence": "https://example.invalid/b",
                    },
                ],
                "review": accepted_review(),
            }
            (evidence_dir / "TEST-1.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(MaturityError, "identifiers must be distinct"):
                validate_repository(root)

    def test_freeze_candidate_requires_bounded_implementation_or_use_and_review(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "standards").mkdir()
            evidence_dir = root / "evidence" / "maturity"
            evidence_dir.mkdir(parents=True)
            (root / "standards" / "fixture.md").write_text(
                standard_text("TEST-1", "Freeze Candidate"), encoding="utf-8"
            )
            payload = {
                "standard_id": "TEST-1",
                "version": VERSION,
                "status": "Freeze Candidate",
                "implementation_or_use": [],
                "review": accepted_review(),
            }
            (evidence_dir / "TEST-1.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(MaturityError, "requires bounded implementation or use evidence"):
                validate_repository(root)

    def test_readme_cannot_claim_a_different_maturity_status(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "standards").mkdir()
            (root / "standards" / "fixture.md").write_text(
                standard_text("TEST-1", "Draft"), encoding="utf-8"
            )
            write_readme(root, "TEST-1", "Stable")
            with self.assertRaisesRegex(MaturityError, "README maturity status must match"):
                validate_repository(root)

    def test_stable_structure_can_pass_but_does_not_prove_evidence_truth_by_itself(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "standards").mkdir()
            evidence_dir = root / "evidence" / "maturity"
            evidence_dir.mkdir(parents=True)
            (root / "standards" / "fixture.md").write_text(
                standard_text("TEST-1", "Stable"), encoding="utf-8"
            )
            write_readme(root, "TEST-1", "Stable")
            payload = {
                "standard_id": "TEST-1",
                "version": VERSION,
                "status": "Stable",
                "implementations": [
                    {
                        "implementation_id": "instrument-a",
                        "independent_context": True,
                        "successful_use": True,
                        "evidence": "https://example.invalid/a",
                    },
                    {
                        "implementation_id": "instrument-b",
                        "independent_context": True,
                        "successful_use": True,
                        "evidence": "https://example.invalid/b",
                    },
                ],
                "review": accepted_review(),
            }
            (evidence_dir / "TEST-1.json").write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(validate_repository(root), [("TEST-1", "Stable")])


if __name__ == "__main__":
    unittest.main()
