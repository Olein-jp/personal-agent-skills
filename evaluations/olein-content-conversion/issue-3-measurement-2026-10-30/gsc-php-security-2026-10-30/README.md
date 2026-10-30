# GSC実データによるIssue #3の評価

利用者指定のPHPセキュリティ記事と未加工のSearch Console ZIPで実施した。元ZIPはDownloadsに保持し、Gitに追加していない。全クエリも外部に送信せず、一般的な検索語の限定例と集計・ハッシュだけを記録した。

- provenance.json: 原本・取得範囲・来歴・不明条件・スキル版。
- calculation.json: 表別の件数・率・空欄・丸め・差分。
- audit-result.json / audit-report.md: 1.1形式の全18項目、検証仮説と未確認事項。
- human-review.md / human-review-record.json: 元データと解釈について利用者がM1〜M5を承認。
- verification.json: 原本・CSVハッシュ、別計算の照合、スキル不変、監査JSON形式検証。
- retrieval.json: 公開資料の取得日時・ハッシュ・一時保存先。記事本文のHTMLもGit外の一時キャッシュに保持。長期再現には利用者側の原ZIPとキャッシュの保持が必要。

## 再計算

リポジトリルートから、提供ZIPの現存するパスを指定する。ZIPを変更しない。

```sh
python3 evaluations/olein-content-conversion/issue-3-measurement-2026-10-30/recalculate.py /path/to/original.zip /tmp/recalculated.json
```

JSON形式の検証にはスキルの scripts/requirements.txt の依存を使う。verify.py は provenance.json の元ZIP保存先と retrieval.json のローカル記事キャッシュを読み取り、元データとの独立した再計算照合と正式validatorを実行する。ファイルが移動・削除された場合は元パスへ用意するか明示的に参照パスを更新し、元のハッシュと一致するか確認する。

```sh
python3 evaluations/olein-content-conversion/issue-3-measurement-2026-10-30/gsc-php-security-2026-10-30/verify.py
```

今回の環境での実行結果はverification.jsonに保存。共通処理の欠陥は再現しておらず、スキル本体・共通テストは変更していない。

## 結論と限界

GSCはpartial。期間は日付表の2026-07-28〜2026-10-27、出力日時・タイムゾーン不明。日別・ページ別と国・デバイス別の差は未解消。各表を別々に扱い、空欄・空表・未提供を0件に置換していない。10月21日の流入集中、現在原稿と期間中の改稿版の違いがあるため改稿の効果は認定しない。GA4・問い合わせはmissing。フォーム送信は未検証。

利用者が元ZIPと照合してM1〜M5を承認。形式検証とは分けて保存した。実データの限界を含めた評価としてIssue #3の受入条件を満たすが、SEO/CV効果・個別環境の安全性・汎用性能の保証ではない。公開サイト・原データは変更していない。
