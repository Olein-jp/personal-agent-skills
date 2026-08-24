# QA Rules

## Core Claim Traceability

外部Core Claimごとに次のchainを実データで確認する。

```text
Claim ID → Source ID → Source Registry Entry → Exact URL → Checked Date
```

- `Exact URL`は`http://`または`https://`で始まる完全なURLとする。
- 資料名、`公式ドキュメント`、`Source Registry参照`、省略URL、空欄は無効とする。
- LedgerとRegistryの両方にURLがあれば完全一致を必須とする。
- URL形式の確認と到達確認を区別する。要求・実行していない到達確認を報告しない。
- Source ID不一致、Registry Entry欠落、Exact URL欠落・不正・不一致、Checked Date欠落はBlockingとする。

## Verification State

Claimを`Verified`へ強化した場合、次の3項目をすべて確認する。

- Verification Evidence ID
- Verification Reason
- Verification Date

1つでも欠ければBlockingとする。`Partially Confirmed`、`Supported`、`Unverified`を根拠なしに`Verified`へ昇格させない。

## Author Provenance

本人由来の表現をDirect Opinion、Verified Experience、Author-derived Inference、Editorial Judgmentに分類する。

- 一人称の判断、価値観、信念として扱えるのは、Direct Opinion、Verified Experience、Author-derived Inferenceだけである。
- Author-derived InferenceにはEX-IDまたは根拠Claimへの`Derived From`を必須とする。
- Verified Experienceには本人確認記録を必要とする。
- Editorial Judgmentを本人の意見として提示しない。
- 本人由来と確認できない一人称の経験・意見はBlockingとする。

## Required Coverage

- BriefのR-IDまたは同等の必須要件をすべて抽出する。
- 本文の主な説明箇所と対応させる。
- 読者が必要な判断を行える説明かを確認し、単語の出現だけでCoveredにしない。
- 重大な要件の欠落はBlockingとする。
- 軽微な補足候補はOptionalにできるが、必須要件をOptionalへ降格しない。

## Final Output Separation

公開候補本文にQAメモ、Calibration Notes、Unknown一覧、Pending作業、Must Not Change、内部向けStructural Decision、未解決タスクを混入させない。混入があればBlockingとし、QA ReportまたはFinal Handoffへの分離を求める。

## コンテンツ共通チェック

- 通常の記事本文で事業名が必要な場合は`オレインデザイン`とする。`Olein Design`はURL、コード、識別子、正確な引用など原文維持が必要な場合だけ許容する。
- WordPressを無条件に推奨していないか確認する。
- 不安を煽るだけで確認手順や相談すべき状態が示されない構成はBlocking候補とし、Briefと制作指針から重大性を判断する。
- 事業サイト記事では、自分で確認できる範囲、相談した方がよい状態、相談前に用意する情報、自然な相談導線をBriefと照合する。
- 入力された媒体固有の制作指針を優先し、対象外媒体の規則を適用しない。

## 入力不足

- 必須入力、媒体、精度モードを安全に特定できない場合は`PENDING`とする。
- 条件付き必須成果物が、本来作成済みであるべきなのに欠落して追跡不能な場合は`FAIL`とする。
- 外部状態や本人確認の完了待ちで、成果物の根本的な作り直しを必要としない場合は`PENDING`とする。
