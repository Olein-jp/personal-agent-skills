# Issue #2: 実記事による PLAN / REVISE 評価

- 対象: https://olein-design.com/blog/wordpress-design-and-client-agreement
- 使用版: main `bc923efae4abb8fa161108884bb7c4e1e3168b30` のスキル1.1。詳細なファイルハッシュは manifest.json。
- 入力: inputs/article.html (元監査と同じHTML)、article.txt (本文抽出)、audit-result-v1.1.json (元監査の無変更コピー)、plan-brief.md (実テーマの再企画)。
- PLAN: [人用](plan-report.md) / [JSON正本](plan-result.json)。現在の記事の不足判定とは別の再企画。
- REVISE: [人用](revise-report.md) / [JSON正本](revise-result.json) / [別ファイルの本文案](revised-article.txt)。B-01に対応する1箇所だけ。18項目の判断は変更前原稿を対象とする。
- 意味・実用性・文体: [人レビュー表](human-review.md)。利用者レビュー待ち。
- 形式・改変範囲・入力保存: verification.json。verify.pyで再実行可能。

## 実行条件と限界

ユーザーが以前指定した実記事のテーマと既存監査を使い、同じ Codex が PLAN / REVISE と事後照合を実行。サブエージェントなし。独立・盲検評価ではなく、各1件の適用例。初回の両JSONは検証エラーなしで、形式上の修復は不要だった。意味の評価と形式の検証を別保存する。

元HTMLの取得日時は2026-10-30T08:14:46+09:00。元監査と固定資料の観測を再利用し、今回の現行仕様や現行サービスの再監査をしたとは扱わない。inputs/retrieval.jsonは過去の取得記録そのままで、当時の一時保存先・保存方針の記載を含む。今回の恒久保存ファイルとハッシュはmanifest.jsonを正本とする。公式資料全文は保存せずtechnical-evidence.mdに読んだ箇所と要約を残す。

元記事は所有者の依頼による評価入力としてこのフォルダへ保存。公開サイト・既存原稿・スキル・文体・分析設定は変更しない。フォーム送信なし。B-01は誤情報と確定せず、動作確認は保留。SEO/CV効果と公開前QAは対象外。

## 再検証

リポジトリルートで、スキルの scripts/requirements.txt を導入した Python 環境から次を実行する。共通処理は変更していないので全体テストの再実行は不要。

```sh
python3 evaluations/olein-content-conversion/issue-2-plan-revise-2026-10-30/verify.py
```

人レビューを承認前に自動で合格にしない。verify.pyは人による判断を生成しない。
