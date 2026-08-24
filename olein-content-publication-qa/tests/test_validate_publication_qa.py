from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SCRIPT = SKILL_ROOT / "scripts" / "validate_publication_qa.py"

spec = importlib.util.spec_from_file_location("validate_publication_qa", SCRIPT)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def merged(base: dict, override: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merged(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


class PublicationQARegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads((FIXTURES / "base.json").read_text(encoding="utf-8"))
        cls.cases = json.loads((FIXTURES / "cases.json").read_text(encoding="utf-8"))

    def test_acceptance_cases(self) -> None:
        self.assertEqual(12, len(self.cases))
        for case in self.cases:
            with self.subTest(case=case["id"], name=case["name"]):
                manifest = merged(self.base, case["override"])
                result = validator.validate(manifest)
                self.assertEqual(case["expected"], result["status"])

    def test_t12_scope_fixture_contains_only_allowed_files(self) -> None:
        case = next(item for item in self.cases if item["id"] == "T-12")
        manifest = merged(self.base, case["override"])
        self.assertEqual(manifest["allowed_files"], manifest["files_checked"])
        self.assertEqual([], manifest["additional_files_read"])

    def test_fail_takes_priority_over_pending(self) -> None:
        manifest = merged(
            self.base,
            {
                "required_coverage": [
                    {"requirement_id": "R-001", "covered": False, "critical": True}
                ],
                "pending_checks": [
                    {"code": "HUMAN_CONFIRMATION", "note": "本人確認待ち"}
                ],
            },
        )
        result = validator.validate(manifest)
        self.assertEqual("FAIL", result["status"])
        self.assertEqual(1, result["summary"]["blocking"])
        self.assertEqual(1, result["summary"]["pending"])


if __name__ == "__main__":
    unittest.main()
