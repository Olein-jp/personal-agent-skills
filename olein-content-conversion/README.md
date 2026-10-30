# olein-content-conversion

オレインデザインの記事の有用性、検索意図、相談価値、実在サービス、導線を根拠付きで監査するCodexスキル。数値採点や成果保証は行わない。文体は既存の `olein-writing-style` に任せる。

## 導入

このリポジトリで開発し、完成したフォルダを `~/.agents/skills/olein-content-conversion` にリンクする。既存の同名フォルダを上書きしない。

```bash
ln -s /Users/olein/GitHub/personal-agent-skills/olein-content-conversion "$HOME/.agents/skills/olein-content-conversion"
```

公式の [Build skills](https://learn.chatgpt.com/docs/build-skills) に従う構造。新規スキルが一覧に出なければCodexを再起動する。同名スキルを複数の探索先に重複導入しない。利用環境のスキル一覧から名前・説明・パスを確認する。

## 呼び出し例

```text
$olein-content-conversion をPLANで使用してください。
テーマはWordPress更新前の確認、読者は企業のサイト担当者です。
自分で確認できることと相談を検討する条件を整理し、構成・調査不足・CTA方針を提案してください。
```

```text
$olein-content-conversion をAUDITで使用し、/absolute/path/article.mdを監査してください。
分析データはありません。本文は変更せず、根拠・判断不可事項・検証計画をMarkdownとJSONで別ファイルに保存してください。
```

```text
$olein-content-conversion のREVISEと $olein-writing-style を併用してください。
監査結果と同じ版の記事について優先改善だけを変更前後で提案してください。元原稿は上書きしないでください。
```

原稿、企画、公開URL、匿名化したGSC/GA4/問い合わせのCSVやJSONを必要な範囲で渡す。外部サービスの認証は不要。未取得情報は判断不可として残し、推測で数値やサービスを補わない。監査レポート以外の公開・送信・計測設定変更は含まない。

## 検証用の環境

JSON検証器にはPython 3.10以上と `scripts/requirements.txt` が必要。スキルを読むだけならライブラリは不要。

```bash
python3 -m venv /tmp/olein-content-conversion-venv
/tmp/olein-content-conversion-venv/bin/python -m pip install -r olein-content-conversion/scripts/requirements.txt
/tmp/olein-content-conversion-venv/bin/python olein-content-conversion/scripts/validate-audit.py <result.json>
/tmp/olein-content-conversion-venv/bin/python -m unittest discover -s olein-content-conversion/tests -v
```

新規出力はスキーマ・ルール1.1。既存1.0出力は旧形式のまま検証できる。版番号だけの自動移行はしない。

検証器はネットワークアクセスや記事の上書きを行わない。JSON Schema Draft 2020-12に加えてID、根拠取得状態、全18項目、3領域、モードと差分の整合を検査する。出典の実在・意味・CV因果関係の正しさは別途確認が必要。

## 機能と制限

- PLAN: 記事タイプ、意図、提供情報、判断材料、相談価値、構成、CTA方針、不足調査、仮説。
- AUDIT: 6領域18項目。各項目の根拠・条件・確信度・制限・検証方法を記録。
- REVISE: 監査IDと対応する変更前後の提案。原稿や既存スタイルを無断変更しない。
- 判断の種類はFACT / EVALUATION / HYPOTHESIS / UNVERIFIED。評価状態は適切 / 改善推奨 / 要確認 / 判定不可 / 評価対象外。
- SEO・コンテンツ、コンバージョン導線、読者体験・信頼性の3領域で、構造品質と実測・成果確認を別々に表示。A-01/E-03は部分確認を記録し、未確認動作も残す。点数や成果保証はない。
- 分析データなしでも構造監査は可能だが実際のSEO/CV成果は認定できない。
- 「WordPress健康診断」の独立サービスとしての提供条件は未確認。既存の基本チェックの範囲から商品名・料金・納品物を推測しない。
- CTAの最適位置・詳しさとCVの関係等にはサイト固有の実測が必要。一般公式資料では効果を確定できない。
- 初期版はモデルの意味判断を使うスキルであり、キーワード検出だけで記事を自動採点するプログラムではない。分析サービスへの自動接続・大規模バッチ処理・実験運用は未実装。

## 作成ファイルと役割

| パス | 役割 |
|---|---|
| `SKILL.md` | 起動条件・共通手順・3モード・責務分担 |
| `agents/openai.yaml` | UI名・説明・呼び出し例、自動選択は既定の有効 |
| `references/evidence-policy.md` | 根拠の順位・取得状態・判断分類・禁止事項 |
| `references/content-types.md` | 記事タイプと適用基準の調整 |
| `references/audit-rules.md` | 判定手順・ID安定性・重要度・領域集約 |
| `references/audit-rules.json` | 18項目の監査対象・根拠・合否・不明条件・確信度・改善確認の正本 |
| `references/service-mapping.md` | 開発時の公式サービス確認範囲と未確認事項 |
| `references/sources.md` | 確認した公式資料のURL・箇所・日時精度・限界、環境調査 |
| `references/measurement.md` | GSC/GA4/問い合わせの項目・取得条件・集計・検証計画 |
| `references/output-contract.md` | Markdown/JSONの対応・正式出力仕様 |
| `schemas/audit-result.schema.json` | 1.1版の出力スキーマ |
| `schemas/audit-result.v1.0.schema.json` | 過去の1.0出力を検証する凍結スキーマ |
| `assets/audit-report-template.md` | 人向けレポートの雛形 |
| `scripts/validate-audit.py` | 構造と参照整合の検査。終了コード0=合格、1=不整合、2=読込/依存エラー |
| `scripts/requirements.txt` | 検証器の依存関係 |
| `tests/test_validate_audit.py` | 構造回帰・破損入力の自動検査 |
| `tests/test_partial_results.py` | 1.1の部分確認・範囲別集約と1.0互換性の検査 |
| `tests/test-cases.md` | A〜Hの入力・期待結果・合格条件・禁止事項との対応 |
| `tests/results.md` | 実行結果、意味レビューと自動検査の区別 |
| `tests/fixtures/cases.json` | ケースの指定条件・合成事業資料・期待状態 |
| `tests/fixtures/analytics-f.json` | Fの期間・母数・イベント定義を含む合成データ |
| `tests/fixtures/official-updating-note.md` | Dで使う公式更新資料の開発時要約と適用限界 |
| `tests/fixtures/article-A.md`, `article-B.md`, `article-C.md`, `article-D.md`, `article-E.md`, `article-F.md`, `article-G.md`, `article-H.md` | ケースごとの合成記事・企画 |
| `tests/results/case-A.json`, `case-B.json`, `case-C.json`, `case-D.json`, `case-E.json`, `case-F.json`, `case-G.json`, `case-H.json` | 8件の正規化された限定レビュー参照出力 |
| `tests/results/case-A.md`, `case-B.md`, `case-C.md`, `case-D.md`, `case-E.md`, `case-F.md`, `case-G.md`, `case-H.md` | 同じ8件の人向けレポート |
| `README.md` | 導入・使用・ファイル構成・制約 |

## 今後の改善

匿名化した実記事と実測データでの運用評価、独立した新規依頼による意味評価、正式な健康診断仕様の確認、計測定義の標準化を優先する。実データで必要性が分かってからCSV正規化やレポート生成の自動化を追加する。

## 独立実行による評価

3つの新しい会話で4本の合成原稿を監査し、3記事タイプと機能組み合わせの境界を確認した。人による根拠・判定・重複指摘のレビューと集計は [Issue #1の評価記録](../evaluations/olein-content-conversion/issue-1-independent-2026-10-30/README.md) を参照。少数の固定ケースの結果であり、未知の記事の精度やSEO/CV効果を保証しない。
