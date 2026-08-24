#!/usr/bin/env python3
"""Validate a normalized publication-QA manifest without modifying source files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


VALID_PRECISION_MODES = {"Light", "Standard", "High Precision"}
AUTHOR_TYPES = {
    "Direct Opinion",
    "Verified Experience",
    "Author-derived Inference",
    "Editorial Judgment",
}


def is_exact_url(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def as_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key, [])
    return value if isinstance(value, list) else []


def finding(code: str, item: str, message: str) -> dict[str, str]:
    return {"code": code, "item": item, "message": message}


def item_label(value: Any, fallback: str) -> str:
    if isinstance(value, dict):
        return str(value.get("code") or value.get("id") or fallback)
    return str(value or fallback)


def validate(data: dict[str, Any]) -> dict[str, Any]:
    blocking: list[dict[str, str]] = []
    pending: list[dict[str, str]] = []
    optional: list[dict[str, str]] = []

    medium = data.get("medium")
    precision_mode = data.get("precision_mode")
    if not isinstance(medium, str) or not medium.strip():
        pending.append(finding("MISSING_MEDIUM", "Task Packet", "対象媒体を特定できません。"))
    if precision_mode not in VALID_PRECISION_MODES:
        pending.append(
            finding("MISSING_PRECISION_MODE", "Task Packet", "有効な精度モードを特定できません。")
        )

    for value in as_list(data, "required_inputs_missing"):
        pending.append(
            finding("MISSING_REQUIRED_INPUT", item_label(value, "input"), "必須入力が不足しています。")
        )

    sources: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(as_list(data, "sources"), start=1):
        if not isinstance(source, dict):
            blocking.append(finding("INVALID_SOURCE_ENTRY", f"source[{index}]", "Source Registry Entryがオブジェクトではありません。"))
            continue
        source_id = source.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            blocking.append(finding("MISSING_SOURCE_ID", f"source[{index}]", "Source IDがありません。"))
            continue
        if source_id in sources:
            blocking.append(finding("DUPLICATE_SOURCE_ID", source_id, "Source IDが重複しています。"))
        sources[source_id] = source

    external_core_claims = 0
    for index, claim in enumerate(as_list(data, "claims"), start=1):
        if not isinstance(claim, dict):
            blocking.append(finding("INVALID_CLAIM_ENTRY", f"claim[{index}]", "Claim Entryがオブジェクトではありません。"))
            continue
        claim_id = str(claim.get("claim_id") or f"claim[{index}]")
        is_external_core = bool(claim.get("external")) and bool(claim.get("core"))
        if is_external_core:
            external_core_claims += 1
            source_id = claim.get("source_id")
            source = sources.get(source_id) if isinstance(source_id, str) else None
            if not source_id or source is None:
                blocking.append(finding("SOURCE_ID_NOT_FOUND", claim_id, "参照先のSource IDがRegistryにありません。"))
            else:
                registry_url = source.get("exact_url")
                ledger_url = claim.get("ledger_exact_url")
                if not is_exact_url(registry_url):
                    blocking.append(finding("INVALID_EXACT_URL", claim_id, "RegistryのExact URLが欠落または不正です。"))
                if not source.get("checked_date"):
                    blocking.append(finding("MISSING_CHECKED_DATE", claim_id, "Source RegistryのChecked Dateがありません。"))
                if ledger_url not in (None, ""):
                    if not is_exact_url(ledger_url):
                        blocking.append(finding("INVALID_LEDGER_URL", claim_id, "LedgerのExact URLが不正です。"))
                    elif registry_url != ledger_url:
                        blocking.append(finding("URL_MISMATCH", claim_id, "RegistryとLedgerのExact URLが一致しません。"))
                elif precision_mode == "High Precision":
                    blocking.append(finding("MISSING_LEDGER_URL", claim_id, "High Precisionに必要なLedger Exact URLがありません。"))

        if claim.get("promoted_to_verified"):
            required = {
                "verification_evidence_id": "Evidence ID",
                "verification_reason": "Verification Reason",
                "verification_date": "Verification Date",
            }
            missing = [label for key, label in required.items() if not claim.get(key)]
            if missing:
                blocking.append(
                    finding("INVALID_VERIFIED_PROMOTION", claim_id, f"Verified昇格に必要な項目がありません: {', '.join(missing)}")
                )

    if precision_mode == "Light" and external_core_claims == 0:
        pass  # Lightでは存在しないSource Registryを要求しない。

    for index, requirement in enumerate(as_list(data, "required_coverage"), start=1):
        if not isinstance(requirement, dict):
            blocking.append(finding("INVALID_COVERAGE_ENTRY", f"coverage[{index}]", "Coverage Entryがオブジェクトではありません。"))
            continue
        requirement_id = str(requirement.get("requirement_id") or f"coverage[{index}]")
        if not requirement.get("covered"):
            if requirement.get("critical", True):
                blocking.append(finding("REQUIRED_COVERAGE_MISSING", requirement_id, "重大なRequired Coverageが本文で満たされていません。"))
            else:
                optional.append(finding("NONCRITICAL_COVERAGE_GAP", requirement_id, "必須判断を妨げない補足余地があります。"))

    for index, provenance in enumerate(as_list(data, "author_provenance"), start=1):
        if not isinstance(provenance, dict):
            blocking.append(finding("INVALID_PROVENANCE_ENTRY", f"provenance[{index}]", "Provenance Entryがオブジェクトではありません。"))
            continue
        expression_id = str(provenance.get("expression_id") or f"provenance[{index}]")
        provenance_type = provenance.get("type")
        if provenance_type not in AUTHOR_TYPES:
            blocking.append(finding("INVALID_PROVENANCE_TYPE", expression_id, "Author Provenanceの分類が不正です。"))
        if not provenance.get("confirmed", False):
            blocking.append(finding("UNCONFIRMED_AUTHOR_EXPRESSION", expression_id, "本人由来であることを確認できません。"))
        if provenance_type == "Author-derived Inference" and not provenance.get("derived_from"):
            blocking.append(finding("MISSING_DERIVED_FROM", expression_id, "Author-derived InferenceにDerived Fromがありません。"))
        if provenance_type == "Editorial Judgment" and provenance.get("presented_as_author_view"):
            blocking.append(finding("EDITORIAL_AS_AUTHOR_VIEW", expression_id, "Editorial Judgmentが本人の意見として提示されています。"))

    final_output = data.get("final_output", {})
    if isinstance(final_output, dict) and final_output.get("internal_qa_mixed"):
        blocking.append(finding("INTERNAL_QA_IN_FINAL", "Final Article", "公開候補本文に内部QA情報が混入しています。"))

    medium_text = medium.lower() if isinstance(medium, str) else ""
    if "ココナラ" in medium_text or "coconala" in medium_text:
        cover = data.get("coconala_cover")
        if not isinstance(cover, dict) or not cover.get("present"):
            pending.append(finding("COCONALA_COVER_PENDING", "Cover Image", "記事専用カバー画像が未納または未確認です。"))
        else:
            cover_format = str(cover.get("format") or "").lower()
            if cover.get("width") != 1280 or cover.get("height") != 720 or cover_format not in {"jpg", "jpeg", "image/jpeg"}:
                blocking.append(finding("INVALID_COCONALA_COVER", "Cover Image", "カバー画像が1280×720pxのJPEGではありません。"))

    for index, value in enumerate(as_list(data, "manual_blocking_issues"), start=1):
        label = item_label(value, f"manual-blocking[{index}]")
        message = value.get("note") if isinstance(value, dict) else str(value)
        blocking.append(finding("MANUAL_BLOCKING", label, str(message or "意味的なBlocking問題があります。")))

    for index, value in enumerate(as_list(data, "pending_checks"), start=1):
        label = item_label(value, f"pending[{index}]")
        message = value.get("note") if isinstance(value, dict) else str(value)
        pending.append(finding("PENDING_CHECK", label, str(message or "公開前の確認待ちがあります。")))

    for index, value in enumerate(as_list(data, "optional_improvements"), start=1):
        label = item_label(value, f"optional[{index}]")
        message = value.get("note") if isinstance(value, dict) else str(value)
        optional.append(finding("OPTIONAL_IMPROVEMENT", label, str(message or "任意改善があります。")))

    if blocking:
        status = "FAIL"
    elif pending:
        status = "PENDING"
    elif optional:
        status = "PASS WITH OPTIONALS"
    else:
        status = "PASS"

    return {
        "status": status,
        "summary": {
            "blocking": len(blocking),
            "pending": len(pending),
            "optional": len(optional),
            "external_core_claims": external_core_claims,
        },
        "blocking_issues": blocking,
        "pending_checks": pending,
        "optional_improvements": optional,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a normalized Olein publication-QA manifest.")
    parser.add_argument("manifest", help="Path to a UTF-8 JSON manifest.")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    args = parser.parse_args()

    path = Path(args.manifest).expanduser().resolve()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: could not read manifest: {error}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("error: manifest root must be a JSON object", file=sys.stderr)
        return 2

    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
