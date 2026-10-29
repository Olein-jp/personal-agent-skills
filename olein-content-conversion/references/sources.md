# 開発時に確認した一次資料

確認日: 2026-10-29 (JST、ページごとの秒単位の時刻は記録なし)。すべて本文を取得して確認。これは開発時の資料台帳であり、実行時のevidence台帳ではない。下記IDをそのまま「今回確認済み」と引用しない。取得状態と実際の確認日時を新しいレポートに記録する。

| ID | 発行元・タイトル / URL | 確認箇所・裏付け | 公開・更新日 | 限界 |
|---|---|---|---|---|
| CODEX-01 | OpenAI [Build skills](https://learn.chatgpt.com/docs/build-skills) | manifest、配置、呼び出し、段階的読込、シンボリックリンク、UIメタデータ | 表示確認できず | 元URL `https://developers.openai.com/codex/skills` から転送。実環境で再確認が必要 |
| CODEX-02 | OpenAI [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | 構造的検査と実際の依頼による評価を分ける | 表示確認できず | 本スキルの意味判断を保証するものではない |
| SEO-01 | Google [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | 自己評価、読者の目的、経験・信頼性、E-E-A-Tの説明 | 2026-10-05 | 一般指針。個別記事の順位・問い合わせ効果を証明しない |
| SEO-02 | Google [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) | 読者が使う言葉、構成、文字数・見出し数の迷信 | 2025-12-10 | 数量の一律基準や順位保証の根拠ではない |
| SEO-03 | Google [Influencing your title links](https://developers.google.com/search/docs/appearance/title-link?hl=en) | タイトルの内容一致、明瞭さ、検索結果での生成 | 2025-12-10 | 初回クエリなしURLはtimeout、hl=enで取得。表示タイトルを固定できない |
| SEO-04 | Google [Link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) | アンカーと文脈、クロール可能なHTML | 2025-12-10 | 内部リンク追加によるCV効果の証明ではない |
| GSC-01 | Google [Performance report: Overview and basic setup](https://support.google.com/webmasters/answer/7576553) | クリック、表示、CTR、平均掲載順位、期間とディメンション | 表示確認できず | hl=enで初回timeout、クエリなしで取得。実データは含まない |
| GSC-02 | Google [Dimensions and data groupings](https://support.google.com/webmasters/answer/17011259) | Queriesの匿名化・行の欠落、Pagesのcanonical集約 | 表示確認できず | 全クエリや個人の意図を把握できない |
| GA-01 | Google [About key events](https://support.google.com/analytics/answer/9267568?hl=en) | 事業上重要な行動とイベント、レポート | 表示確認できず | キーイベントが実際の問い合わせや受注を意味するかは設定次第 |
| GA-02 | Google [Select attribution settings](https://support.google.com/analytics/answer/10597962?hl=en) | レポートの帰属モデル、遡及期間 | 表示確認できず | 配分と因果効果は別。サイトの実際の設定は未確認 |
| GA-03 | Google [About data thresholds](https://support.google.com/analytics/answer/9383630?hl=en) | データ非表示の条件と品質表示 | 表示確認できず | 欠測を0件にできない。実データの状態は別途確認 |
| WP-01 | WordPress.org [Updating WordPress](https://wordpress.org/documentation/article/updating-wordpress/) | Back up WordPress、更新と復元 | 公開2018-10-30 / 更新2024-09-15 | 一般的な本体更新。個別プラグイン・PHP変更の安全性までは証明しない |

## 仕様とローカル環境の照合

公式CODEX-01で必須frontmatterはnameとdescription、任意リソースはscripts/references/assetsとagents/openai.yaml。リポジトリの `.agents/skills`、利用者の `~/.agents/skills` 等から探索し、リンク先も読む。明示指定とdescriptionによる自動選択があり、併用は対象スキルを依頼で指定して責務を分ける。専用の「継承」設定は追加しない。ローカルskill-creatorのinit_skill.py / quick_validate.pyとUI仕様も確認し、正式仕様にない独自frontmatterは使わない。

既存 `olein-writing-style` のSKILL.mdと5つのreferences (style-guide、wordpress-ja-notation、source-sample、visual-prompt-guidance、business-article-finalization) を確認済み。`~/.agents/skills/olein-writing-style` はこのリポジトリへのリンク。既存ファイルは変更しない。新スキルの同名ディレクトリ・導入先は開発前に存在しないことを確認した。

## 一次資料で一般的な効果を確認できない領域

CTAの最適数・最適位置、記事の詳しさと相談減少の関係、自社サービス案内の効果、相談境界の最適表現、自社読者の心理は、上記資料から効果を確定できない。C/D/Fの事業方針と編集評価はGoogleの公式要件ではない。Eの改善は当該サイトでの仮説として扱う。実測、顧客課題、著者経験、比較可能な変更前後データは初期開発では提供されていない。PHP等の記事固有の技術一次資料は監査時に調査する。
