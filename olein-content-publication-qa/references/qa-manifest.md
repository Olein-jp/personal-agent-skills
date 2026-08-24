# QA Manifest

`scripts/validate_publication_qa.py`は、記事成果物を直接意味解析するのではなく、Codexが成果物を読んで正規化したJSONを検査する。manifestは一時ファイルとして作成できる。Task Packetが保存を許可していない場合、記事Workspaceへ保存しない。

## 最小例

```json
{
  "article": "記事タイトル",
  "medium": "オレインデザイン事業サイト",
  "precision_mode": "Standard",
  "required_inputs_missing": [],
  "claims": [],
  "sources": [],
  "required_coverage": [
    {"requirement_id": "R-001", "covered": true, "critical": true}
  ],
  "author_provenance": [],
  "final_output": {"internal_qa_mixed": false},
  "pending_checks": [],
  "optional_improvements": [],
  "manual_blocking_issues": []
}
```

## 主なフィールド

- `claims`: `claim_id`、`external`、`core`、`source_id`、任意の`ledger_exact_url`、`promoted_to_verified`、昇格時の`verification_evidence_id`、`verification_reason`、`verification_date`
- `sources`: `source_id`、`exact_url`、`checked_date`
- `required_coverage`: `requirement_id`、意味的確認後の`covered`、`critical`
- `author_provenance`: `expression_id`、`type`、`confirmed`、必要な`derived_from`
- `final_output.internal_qa_mixed`: 内部QA情報が本文に混入しているか
- `coconala_cover`: 対象時に`present`、`width`、`height`、`format`
- `pending_checks`: 外部状態や人間判断待ちの項目。各要素に`code`と`note`を持たせる。
- `optional_improvements`: 公開を止めない改善項目。
- `manual_blocking_issues`: 意味的検査で発見したBlocking項目。

## scriptの責務

scriptはSource ID参照、URL形式と一致、Checked Date、Verified昇格、正規化済みCoverageとAuthor Provenance、Final Output混入、ココナラ画像、Status優先順位を決定的に検査する。

scriptは本文からCoverageやAuthor Provenanceを自動判定しない。正規化値の正しさは、Codexが原成果物を読んで確認する。
