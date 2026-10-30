# 出力契約 v1.1

正式な機械形式は [audit-result.schema.json](../schemas/audit-result.schema.json) (JSON Schema Draft 2020-12)。jsonschemaのFormatCheckerも有効にする。`validate-audit.py` は追加でID参照、全項目の網羅、取得状態、3領域の集約、モード間の整合を検査する。未知の属性を禁止し、点数欄は設けない。原稿の自動監査器ではなく、Codexが作ったレポートの検証器である。

## 共通フィールド

- `schema_version` / `rules_version`: 新規出力はともに1.1。既存1.0出力も検証器で受け付け、凍結した`schemas/audit-result.v1.0.schema.json`を使う。版の混在は認めない。旧出力や評価履歴は書き換えない。
- `mode`, `created_at`: PLAN / AUDIT / REVISE、実際の作成日時 (タイムゾーン必須)。
- `subject`: 原稿/企画の場所、version (推奨SHA-256)、対象読者、目的、主タイプ、explicit/inferred/unknown、推定理由、取得範囲。記事URLと提供原稿の版が違えば明記する。
- `evidence`: 台帳。source_typeはarticle / plan / official / service / analytics / business / supplementary。取得可否と内容の真偽を分ける。欠測資料も台帳に入れられる。
- `datasets`: search_console / ga4 / inquiriesの3種を必ず列挙。missingなら期間と取得日時はnull、partialなら不明な条件を明記。状態availableはデータ取得済みであり成果保証ではない。
- `findings`: 18固定IDを順番通りに1件ずつ出す。categoryはルール定義と一致。問題がない項目も理由を記録する。証拠はevidence_idと具体的な位置・観測を付ける。
- `summaries`: seo_content / conversion / reader_trustの3領域を順に出す。それぞれstructure (構造品質)、outcomes (実測・成果確認)、unverified_checks、limitationsを必須とする。structure/outcomesはstatus、check_ids、reason、limitationsを持つ。単一の領域statusは廃止する。集約規則はaudit-rules.md。
- `plan`: PLANだけオブジェクト。search_intent、required_information、decision_information、consultation_value、outline、cta_policy、missing_research、hypothesesを配列で埋める。その他はnull。
- `revisions`: REVISEでは少なくとも1つの変更前後ペア。追加はbeforeが空文字、削除はafterが空文字。元位置、監査ID、理由を必須とする。その他は空配列。
- `limitations`: 全体の未確認範囲。制限が見つからなければ「確認範囲外の保証なし」と明示し、空にしない。

## 部分確認 (checks)

A-01とE-03には、ルールで定義された部分キーを定義順に1回ずつ含める。各部分はkey、classification、status、confidence、finding、rationale、evidence、limitationsを持つ。証拠の構造と分類の要件は親項目と同じ。親の修正案・検証計画は維持し、部分ごとに同じ提案を重複させない。

- A-01.audience_goalとA-01.observed_queriesを区別する。読者指定の観測ができても、実クエリ未取得なら後者はUNVERIFIED。
- E-03.static_pathとE-03.submissionを区別する。送信未確認で静的到達まで判定不可にしない。
- checksのkeyはルールと一致させる。範囲はルール側が定義するため、出力側で都合よくoutcomeに変更して問題を構造集約から外せない。
- 領域のunverified_checksには動作未確認も含める。構造表示で適切になっても未確認を隠さない。

旧形式の互換性は読込みの互換性であり、旧出力へ部分判断を自動推測して補うものではない。新旧比較は同じ入力版・根拠の範囲で行う。

## 指摘の読み方

`classification`は判断の種類、`status`は評価状態、`severity`は問題の重要性、`confidence`は主張の確信度。`rationale`にどのルール条件に該当したか記述する。`limitations`には証拠不足、範囲、推定を残す。`priority_reason`は効果予測ではなく読者への影響と記事目的から説明する。

`expected_effect.status`はunverified / observed / not_applicable。observedは取得済み実測のevidence_idsが必須で、観測された変化だけをdescriptionに記す。因果が証明されたという意味ではない。HYPOTHESISはunverified。未取得データから「効果あり」にしない。

`validation`はmetric、method、success_condition、confoundersを必須とする。修正文の正確性確認とCV検証を分ける。該当なしの場合も理由を書く。実数・母数・期間・条件はevidenceの観測またはvalidationに明記する。丸めや率の算出条件も残す。

Markdownは同じJSONを正本として、概要、領域別状態、全18項目、優先改善、仮説、判断不可、検証計画、台帳を人が読める形にする。情報量が多ければ長文を別表にしても、IDと根拠・理由を省略しない。JSONだけにある重大な制限をMarkdownから隠さない。テンプレートの括弧を埋めたまま成果物として出さない。
