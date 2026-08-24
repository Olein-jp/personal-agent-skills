---
name: olein-content-publication-qa
description: オレインデザインの記事について、Task Packet、制作指針、Article Brief、公開候補本文、調査記録を照合し、Core Claimの追跡可能性、Required Coverage、Author Provenance、媒体固有要件を確認して公開前QA判定を行う。記事成果物間の整合性確認、Source RegistryとExact URLの確認、ChatGPTで作成した記事の機械的な公開判定を求められたときに使う。通常の文章校正、新規執筆、企画、全面リライト、WordPressコードレビュー、一般的な事実調査だけの依頼には使わない。
---

# Olein Content Publication QA

## 目的

指定された記事成果物だけを照合し、公開を止める問題、公開前の確認待ち、任意改善を分離する。本文の書き直しや不足根拠の推測は行わず、Publication QA Reportを返す。

## 最初に確認すること

1. Task Packetから対象記事、媒体、精度モード、必読ファイル、必須確認項目、出力先、更新可否、終了条件を取得する。
2. Task Packet、コンテンツ制作指針、Article Briefまたは同等の要件定義、公開候補本文が揃っているか確認する。
3. 次の条件付き成果物を確認する。
   - 外部Core Claimがある: Research + Fact Sheet、Source Registry、または同等成果物
   - Author-derived Inferenceまたは本人Experienceがある: Experience Registryまたは本人確認記録
   - ココナラブログ: 媒体固有の制作指針とカバー画像情報
   - High Precision: Verification State TransitionsとTraceability Ledger
4. 精度モードまたは媒体を安全に特定できない場合は、推測せず`PENDING`にする。

## スコープと権限

- 初期動作はread-onlyとし、公開候補本文を変更しない。
- Task PacketでQA Reportの保存先と更新許可が明示された場合だけ、Reportを保存する。
- Issue、管理表、公開状態を変更しない。記事を公開しない。
- 調査、本文修正、Issue同期、公開操作をこのQA工程へ取り込まない。
- 新しい調査が必要なら、理由と戻すべき工程を示して`PENDING`または`FAIL`にする。
- Task Packetにないファイルを読む必要がある場合は最小限にし、ファイル名と理由をReportへ記録する。

## ワークフロー

1. `references/qa-rules.md`を読み、対象の精度モードに必要なInvariantとBlocking条件を選ぶ。
2. BriefからR-IDまたは同等のRequired Coverageを抽出し、本文の主な説明箇所と対応させる。単語の存在だけでCoveredにしない。
3. 外部Core Claimごとに、Claim IDからChecked Dateまでを実データでたどる。件数の自己申告だけで確認済みにしない。
4. 本人由来の表現を分類し、Author ProvenanceとDerived Fromを確認する。
5. 公開候補本文に内部QA情報や未解決タスクが混入していないか確認する。
6. 対象媒体の制作指針を優先して媒体固有要件を確認する。ココナラブログの場合だけ`references/coconala-blog.md`も読む。
7. 機械検査が有効な場合、確認結果を`references/qa-manifest.md`の形式に正規化し、`python3 <skill-dir>/scripts/validate_publication_qa.py <manifest.json>`を実行する。scriptの結果は補助証拠であり、意味的なCoverageやProvenanceをscriptだけでPASSにしない。
8. `references/status-decision.md`に従ってOverall Statusを1つ決める。`FAIL`が1件でもあれば`FAIL`、それ以外で`PENDING`があれば`PENDING`とする。
9. `references/output-format.md`に従ってReportを返す。Blocking、Pending、Optionalで同じ問題を重複報告しない。

## 精度モード

- **Light**: 外部Core Claimがなければ存在しないSource Registryを要求しない。外部Core Claimがあれば最小でも`Claim → Source ID → Registry → Exact URL → Checked Date`を確認する。
- **Standard**: Core Claimを完全に確認する。Supporting ClaimとContextは結論や安全性に影響しない範囲で簡略化できる。ExperienceにはEX-IDとDerived Fromを確認する。
- **High Precision**: Core Claim、Registry、Ledgerを行単位で照合し、Verifiedへの昇格にEvidence ID、理由、確認日があるか確認する。

## Context Budget

- Task Packetに指定された必読ファイルから開始する。
- 他の記事Workspace、過去記事、過去の回帰テスト、PERSONALIZED一式、無関係なサービス資料を無条件に読まない。
- Reportで入力内容を長く再掲しない。
- 該当しない検査に空の表を出さず、`該当なし`の理由を短く書く。

## 完了条件

- 必要なInvariantを実データで照合した。
- Blocking、Pending、Optionalを分離した。
- Overall Statusと根拠が一致している。
- 本文や外部状態を無断で変更していない。
- 読んだファイルと、追加で読んだファイルの理由をReportに記録した。

## リソース

- `references/qa-rules.md`: Invariant、Provenance、Coverage、媒体共通の検査規則。
- `references/status-decision.md`: `PASS`、`PASS WITH OPTIONALS`、`PENDING`、`FAIL`の決定規則。
- `references/output-format.md`: Publication QA Reportの出力形式。
- `references/qa-manifest.md`: 機械検査用JSONの形式とscriptの限界。
- `references/coconala-blog.md`: ココナラブログの場合だけ読む媒体固有要件。
- `scripts/validate_publication_qa.py`: 正規化済みmanifestの決定的な整合性検査。
