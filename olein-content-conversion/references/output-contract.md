# 出力契約 v1.0

正式な機械形式は [audit-result.schema.json](../schemas/audit-result.schema.json) (JSON Schema Draft 2020-12)。jsonschemaのFormatCheckerも有効にする。`validate-audit.py` は追加でID参照、全項目の網羅、取得状態、3領域の集約、モード間の整合を検査する。未知の属性を禁止し、点数欄は設けない。原稿の自動監査器ではなく、Codexが作ったレポートの検証器である。

## 共通フィールド

- `schema_version` / `rules_version`: ともに1.0。ルール変更時は版とテストを併せて更新する。
- `mode`, `created_at`: PLAN / AUDIT / REVISE、実際の作成日時 (タイムゾーン必須)。
- `subject`: 原稿/企画の場所、version (推奨SHA-256)、対象読者、目的、主タイプ、explicit/inferred/unknown、推定理由、取得範囲。記事URLと提供原稿の版が違えば明記する。
- `evidence`: 台帳。source_typeはarticle / plan / official / service / analytics / business / supplementary。取得可否と内容の真偽を分ける。欠測資料も台帳に入れられる。
- `datasets`: search_console / ga4 / inquiriesの3種を必ず列挙。missingなら期間と取得日時はnull、partialなら不明な条件を明記。状態availableはデータ取得済みであり成果保証ではない。
- `findings`: 18固定IDを順番通りに1件ずつ出す。categoryはルール定義と一致。問題がない項目も理由を記録する。証拠はevidence_idと具体的な位置・観測を付ける。
- `summaries`: seo_content / conversion / reader_trustの3領域を順に出す。状態の集約規則はaudit-rules.md。reasonとlimitationsに未調査範囲を含める。
- `plan`: PLANだけオブジェクト。search_intent、required_information、decision_information、consultation_value、outline、cta_policy、missing_research、hypothesesを配列で埋める。その他はnull。
- `revisions`: REVISEでは少なくとも1つの変更前後ペア。追加はbeforeが空文字、削除はafterが空文字。元位置、監査ID、理由を必須とする。その他は空配列。
- `limitations`: 全体の未確認範囲。制限が見つからなければ「確認範囲外の保証なし」と明示し、空にしない。

## 指摘の読み方

`classification`は判断の種類、`status`は評価状態、`severity`は問題の重要性、`confidence`は主張の確信度。`rationale`にどのルール条件に該当したか記述する。`limitations`には証拠不足、範囲、推定を残す。`priority_reason`は効果予測ではなく読者への影響と記事目的から説明する。

`expected_effect.status`はunverified / observed / not_applicable。observedは取得済み実測のevidence_idsが必須で、観測された変化だけをdescriptionに記す。因果が証明されたという意味ではない。HYPOTHESISはunverified。未取得データから「効果あり」にしない。

`validation`はmetric、method、success_condition、confoundersを必須とする。修正文の正確性確認とCV検証を分ける。該当なしの場合も理由を書く。実数・母数・期間・条件はevidenceの観測またはvalidationに明記する。丸めや率の算出条件も残す。

Markdownは同じJSONを正本として、概要、領域別状態、全18項目、優先改善、仮説、判断不可、検証計画、台帳を人が読める形にする。情報量が多ければ長文を別表にしても、IDと根拠・理由を省略しない。JSONだけにある重大な制限をMarkdownから隠さない。テンプレートの括弧を埋めたまま成果物として出さない。
