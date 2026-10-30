# B-01 の固定資料との照合

- 出典: https://developer.wordpress.org/block-editor/how-to-guides/curating-the-editor-experience/block-locking/
- 取得日時: 2026-10-30T08:14:47+09:00 (以前の監査時の観測。今回の現行仕様確認ではない)
- 保存キャッシュの SHA-256: `8403e6e5a7a97e8f0842c0119c276ffeedf16baf9155f534aed0c2b1294d40ff`
- 参照箇所: Apply content-only editing in patterns or templates / Change permissions to control locking ability

読めた資料は、内容のみの編集で使える構造変更への経路と、通常のブロックロックを操作できる権限を別に説明している。元記事は具体設定を特定していないため、設定の誤りとは断定できない。修正案では制限の種類を分け、対象環境・担当者権限で試すことを示す。個別実装の再現、改稿による理解・成果の向上は未検証。

元 HTML 全体は複製せず、今回読んだ範囲の要約と元キャッシュのハッシュを残す。原監査の根拠日時・状態は書き換えない。その他の原監査の判定は原稿版への評価として引き継ぐだけで、現行サービスの提供や送信成功を再認定しない。
