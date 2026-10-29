# 初期版の検証記録

実施日: 2026-10-29 (JST)。最終の自動テストを15:33頃に実行。

## 実施結果

| 検査 | 結果 | 確認範囲 |
|---|---|---|
| skill-creator quick_validate.py | 合格 | frontmatter、名前、未完成雛形の検査 |
| Draft202012Validator.check_schema | 合格 | 正式JSON Schemaの定義 |
| unittest | 32件すべて合格 (最終実行1.047秒) | A〜Hの参照出力、ID、根拠参照、欠測、取得状態、日時・期間、領域集約、モード、差分、JSON読込み等 |
| A〜HのJSONレポート | 8件すべて合格 | 全18項目、必須データ取得状態、JSON Schemaと追加整合性検査 |
| A〜Hの限定意味レビュー | 下表の焦点について期待条件と整合 | 開発者であるCodexが合成入力を読んで判断し、Markdown/JSONを保存。独立した評価者ではない |
| 既存スタイルの変更確認 | 変更なし | git diffでolein-writing-styleに差分なし |
| 導入先 | 作成・参照確認済み | `~/.agents/skills/olein-content-conversion` → このリポジトリのスキル |

## A〜Hの観測

| ケース | 確認した結果 |
|---|---|
| A | 詳細な設計説明を尊重し、CTA追加を必須にしなかった |
| B | 自力確認と相談条件・合成提供範囲を分け、末尾の恐怖営業を改善推奨にした |
| C | 本文にCTAなしをFACTとして記録し、CV低下を認定せず、配置・問い合わせ経路は対象外にした |
| D | 保証・恐怖・出し惜しみ・危険手順の修正理由と前後比較を提示。未確認サービスと未記録実績の真偽は判断不可にした |
| E | 分析データなしの成果をUNVERIFIEDにし、0件や0点に変換しなかった |
| F | 4/100=4%、8/120=約6.67%、約2.67ポイント差と、送信完了1件の少数性を記録。因果効果と受注の認定を避け、検証の条件を示した |
| G | 循環した結論に限定して差分を提案し、筆者の判断を残し、架空経験・営業CTAを追加しなかった |
| H | 未執筆の企画を本文欠落と認定せず、PLANの8要素、取得不能と追加調査、仮説を提示した |

## 発見して修正した問題

初回の構造テストでは、jsonschema単体の環境で日時フォーマット検査が省略され、タイムゾーンなしの日時が通る問題を検出した (当時29件中1件失敗)。`rfc3339-validator`を依存に加え、未導入時は実行エラーにした。再検証後、日時を含めすべて合格。後から追加した破損入力の検査を含め、最終32件が合格した。

## 再現用コマンド

通常の導入・検証方法は [README](../README.md)。開発時はグローバル環境を変えず、依存を `/private/tmp/olein-conversion-validation-deps` に配置し、次を使用した。

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/olein-conversion-validation-deps python3 -m unittest discover -s olein-content-conversion/tests -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/olein-conversion-validation-deps python3 /Users/olein/.codex/skills/.system/skill-creator/scripts/quick_validate.py olein-content-conversion
```

## 検証の限界・残るレビュー

自動検査は正規化済み参照出力と不正入力の構造検証。本文から危険表現や因果誤認を自動抽出した結果ではない。A〜Hの参照出力を回帰検査できても、未知の記事で正しい評価を再生成できると証明したことにはならない。

今回の意味レビューは開発者による限定実施であり、人間による独立レビュー、新しいモデル実行での盲検評価、実記事による運用評価は未実施。将来の評価では [test-cases.md](test-cases.md) の入力だけを使い、期待結果・参照出力を先に渡さず実行する。原稿の意味・読者との適合・サービスの現行範囲・出典の真偽・修正文の声・因果解釈は人間が最終確認する。

実サイトでのGSC/GA4取得、CV改善実験、フォーム送信、外部公開は実施していない。独立サービスとしてのWordPress健康診断は未確認。公式資料とサービスの開発時確認範囲は [sources.md](../references/sources.md) と [service-mapping.md](../references/service-mapping.md) に記録した。
