# Publication QA Report Format

次の構造を使う。該当しない表を空行で埋めず、`該当なし: 外部Core Claimがないため`のように理由を短く示す。

```markdown
# Publication QA Report

## Overall Status
PASS / PASS WITH OPTIONALS / PENDING / FAIL

## Scope
- Article:
- Medium:
- Precision Mode:
- Files Checked:
- Additional Files Read:

## Blocking Issues
- None

## Pending Before Publish
- None

## Optional Improvements
- None

## Cross-Artifact Invariants

| Invariant | Required | Checked | Missing | Status |
| --- | ---: | ---: | --- | --- |
| Core Claim Traceability | | | | |
| Source Registry Exact URL | | | | |
| Verification State Evidence | | | | |
| Author Provenance | | | | |
| Required Coverage | | | | |
| Final Output Separation | | | | |

## Traceability Integrity

| Claim ID | Source ID | Registry Entry | Registry Exact URL | Ledger Exact URL | Checked Date | URL Match | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Required Coverage

| Requirement | Main Location | Result | Note |
| --- | --- | --- | --- |

## Author Provenance

| Expression / Claim | Type | Source | Result |
| --- | --- | --- | --- |

## Medium-specific Checks

## Final Decision Reason
```

## 記述規則

- 問題ごとに所在、確認事実、必要な対応を簡潔に書く。
- 同一問題をBlocking、Pending、Optionalへ重複掲載しない。
- `Additional Files Read`にはTask Packet外のファイルと読んだ理由を書く。なければ`None`とする。
- URL到達確認を行っていない場合は、形式確認と到達確認を区別して明記する。
- 本文の長い引用や入力成果物の再掲を避ける。
- `Final Decision Reason`では最も高い優先度の判定根拠を1〜3文でまとめる。
