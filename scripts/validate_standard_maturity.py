#!/usr/bin/env python3
"""Validate Merrin Open Synth Standards maturity claims without inflating publication into proof."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = {"Draft", "Freeze Candidate", "Stable", "Deprecated"}
ACCEPT_DECISION = "ACCEPT FOR CURRENT STATUS"


class MaturityError(ValueError):
    pass


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise MaturityError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs_no_duplicates)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MaturityError(f"invalid maturity evidence JSON: {path}") from exc


def _frontmatter(path: Path) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise MaturityError(f"cannot read standard: {path}") from exc
    if not lines or lines[0].strip() != "---":
        raise MaturityError(f"standard is missing frontmatter: {path}")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise MaturityError(f"standard frontmatter is not closed: {path}") from exc
    values: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise MaturityError(f"unsupported frontmatter line in {path}: {raw}")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key in values:
            raise MaturityError(f"duplicate frontmatter field {key} in {path}")
        values[key] = value
    return values


def _require_review(payload: dict[str, Any], standard_id: str) -> None:
    review = payload.get("review")
    if not isinstance(review, dict):
        raise MaturityError(f"{standard_id}: maturity promotion requires a review record")
    if review.get("decision") != ACCEPT_DECISION:
        raise MaturityError(f"{standard_id}: maturity review must accept the current status")
    evidence = review.get("evidence")
    if not isinstance(evidence, str) or not evidence.strip():
        raise MaturityError(f"{standard_id}: maturity review requires an evidence pointer")


def _validate_sidecar(root: Path, standard_id: str, status: str) -> None:
    path = root / "evidence" / "maturity" / f"{standard_id}.json"
    if not path.is_file():
        raise MaturityError(f"{standard_id}: {status} requires {path.relative_to(root)}")
    payload = _load_json(path)
    if not isinstance(payload, dict):
        raise MaturityError(f"{standard_id}: maturity evidence must be an object")
    if payload.get("standard_id") != standard_id:
        raise MaturityError(f"{standard_id}: maturity evidence standard_id mismatch")
    if payload.get("status") != status:
        raise MaturityError(f"{standard_id}: maturity evidence status mismatch")
    _require_review(payload, standard_id)

    if status == "Freeze Candidate":
        real_use = payload.get("real_use")
        if not isinstance(real_use, list) or not real_use:
            raise MaturityError(f"{standard_id}: Freeze Candidate requires real-use evidence")
        for item in real_use:
            if not isinstance(item, dict):
                raise MaturityError(f"{standard_id}: real-use evidence entries must be objects")
            if not isinstance(item.get("context"), str) or not item["context"].strip():
                raise MaturityError(f"{standard_id}: real-use evidence requires a context")
            if not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
                raise MaturityError(f"{standard_id}: real-use evidence requires an evidence pointer")

    elif status == "Stable":
        implementations = payload.get("implementations")
        if not isinstance(implementations, list) or len(implementations) < 2:
            raise MaturityError(f"{standard_id}: Stable requires at least two implementation contexts")
        ids: list[str] = []
        for item in implementations:
            if not isinstance(item, dict):
                raise MaturityError(f"{standard_id}: implementation evidence entries must be objects")
            implementation_id = item.get("implementation_id")
            if not isinstance(implementation_id, str) or not implementation_id.strip():
                raise MaturityError(f"{standard_id}: Stable implementation requires implementation_id")
            if item.get("independent_context") is not True:
                raise MaturityError(f"{standard_id}: Stable implementation must declare an independent context")
            if not isinstance(item.get("evidence"), str) or not item["evidence"].strip():
                raise MaturityError(f"{standard_id}: Stable implementation requires an evidence pointer")
            ids.append(implementation_id)
        if len(set(ids)) != len(ids):
            raise MaturityError(f"{standard_id}: Stable implementation identifiers must be distinct")

    elif status == "Deprecated":
        reason = payload.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise MaturityError(f"{standard_id}: Deprecated requires a reason")


def validate_repository(root: Path) -> list[tuple[str, str]]:
    standards_dir = root / "standards"
    if not standards_dir.is_dir():
        raise MaturityError("standards directory is missing")

    found: list[tuple[str, str]] = []
    ids: set[str] = set()
    for path in sorted(standards_dir.glob("*.md")):
        meta = _frontmatter(path)
        standard_id = meta.get("standard_id", "").strip()
        status = meta.get("status", "").strip()
        if not standard_id:
            raise MaturityError(f"standard_id is missing: {path}")
        if standard_id in ids:
            raise MaturityError(f"duplicate standard_id: {standard_id}")
        ids.add(standard_id)
        if status not in ALLOWED_STATUSES:
            raise MaturityError(f"{standard_id}: unsupported maturity status {status!r}")
        if status != "Draft":
            _validate_sidecar(root, standard_id, status)
        found.append((standard_id, status))

    if not found:
        raise MaturityError("no standards found")
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    try:
        found = validate_repository(Path(args.root).resolve())
    except MaturityError as exc:
        print(exc)
        return 1
    for standard_id, status in found:
        print(f"valid maturity: {standard_id} = {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
