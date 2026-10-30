# REVISE 実記事評価

入力: https://olein-design.com/blog/wordpress-design-and-client-agreement
版: `html-sha256:28b82becaba5d3b9e11bd06ca1de93f4af7d372d33a0c2a8fb9c3d5c54183503`

inputs/article.html と同一版の inputs/audit-result-v1.1.json に対する差分提案。18項目は変更前原稿の監査判断を引き継ぎ、修正後の再監査合格を示さない。

## 領域別判定

- seo_content: 構造 要確認 / 実測 判定不可 / 未確認 A-01.observed_queries, B-01
- conversion: 構造 適切 / 実測 判定不可 / 未確認 E-03.submission, E-04
- reader_trust: 構造 適切 / 実測 評価対象外 / 未確認 なし

## 限定修正 B-01

構成を保ち、文章と画像を更新したい場合 / 第1段落の第2文

変更前:

> 新しいページには、決まったブロック構成を用意し、内容の編集に操作を絞る設定や、制限を解除できる人の設定を組み合わせます。

変更後:

> 新しいページには、決まったブロック構成を用意します。内容だけを編集する設定と、ブロックの移動・削除やロック解除の制限は分けて確認したいところです。対象の環境と担当者の権限で操作を試し、制作者へ依頼する範囲を決めます。

元AUDIT B-01の要確認に対応。内容のみの編集と通常ロックの操作制限を一括の設定として受け取られないよう、確認する操作を分ける。元文の誤りと断定せず、実装を保証しない。

## 優先改善・仮説

確定した修正必須問題はない。B-01 の確認条件を明示する提案1件のみ。技術的な解消や成果向上は未検証。

## 全18項目

### A-01 — 判定不可

UNVERIFIED / unknown / 重要性 info / 優先度 none

本文の読者・目的は確認できるが、実際の検索クエリとの一致は判定できない。

本文が想定するのは制作・進行担当者。これは観測された想定読者であり、実検索意図の証明ではない。 適用ルール: A-01

根拠: EV-ARTICLE「冒頭の読者指定」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-SEARCH-CONSOLE「データ未提供」: 今回の利用者入力に分析資料はない。

制限: 本文から想定する意図と実検索者の意図は別。クエリデータなし。

提案: 記事タイプや意図の仮説は、クエリ取得後に照合する。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "GSCの対象記事・期間・クエリごとの実測を確認し、想定した疑問との一致を検討する。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

- audience_goal: 適切 / EVALUATION / medium — 本文に想定読者と記事の目的が示され、説明範囲が対応する。 理由: 公開本文の構造評価に限定し、実検索意図の証明にしない。 制限: 実際の検索者の属性やクエリはこの観測から確定しない。
- observed_queries: 判定不可 / UNVERIFIED / unknown — 当該ページの実クエリが未提供で一致を検証できない。 理由: 想定する読者と検索で到達した読者の意図は別に確認する。 制限: 対象期間・検索タイプ・クエリ別集計が未取得。
### A-02 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

タイトルが問う設計理由に対し、本文が選択条件と説明方法を扱っている。

タイトルと回答範囲の対応を評価。検索結果の表示タイトル・CTRは未確認。 適用ルール: A-02

根拠: EV-ARTICLE「タイトルから結論まで」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 現状の問いと回答の関係を保つ。キーワードの機械的な追加は不要。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "タイトルの約束と対応節を照合。CTRを評価するなら同じクエリ構成・期間条件を使う。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### B-01 — 要確認

EVALUATION / medium / 重要性 info / 優先度 none

構成固定の仮例で、解除制限がどの機能を指すか確認が必要。

WP-LOCKはcontent-onlyのModify経路と通常ロックの権限を分けて説明する。canLockBlocksだけで両方を同じように制限できるとは確認できない。記事は具体設定を示していないので誤りと断定しない。 適用ルール: B-01

根拠: EV-ARTICLE「構成を保ち、文章と画像を更新したい場合」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-WP-LOCK「Apply content-only editing / Change permissions」: content-onlyのModify経路と、canLockBlocksによる通常ロック操作の権限を別々に説明。

制限: 対象版・テーマ・権限・具体設定が未提示。設定の誤りや実現不能を確定していない。

提案: 想定するWordPress版・テーマ・利用者権限で、構造変更へ進める経路を確認する。確認まで実現方法の保証は避ける。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "対象版・ロールで移動/削除/追加/Modify/解除を分けて試す。担当者が変更できる操作と記事の条件が一致したら確認完了。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### B-02 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

主要な技術説明の参照先が実在し、仮例と筆者の判断を区別している。

経験や効果の追加を要求せず、主要主張と公式資料の対応を評価した。 適用ルール: B-02

根拠: EV-ARTICLE「公式資料への参照と仮例の明示」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-WP-HIERARCHY「Single Page」: 固定ページではスラッグ等に基づくPHPテンプレートを選ぶ仕組みを説明。 / EV-WP-META「導入」: 検索条件として使うか、個別表示以外で使うかを判断材料として示す。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 仮例を実例や実績として書き換えない。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "技術主張と一次資料の位置を追跡できるかを確認する。今回の一部設定の懸念はB-01に記録。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### B-03 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

読者が設計を比較し、操作単位で役割を確認できる構成になっている。

設計判断の記事であり、実装チュートリアルの網羅性や文字数を合否基準にしない。 適用ルール: B-03

根拠: EV-ARTICLE「仮例、操作別表、結論」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 説明の詳しさを削る必要は見いだしていない。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "制作担当者が自案件の操作・担当・制約を整理できるかをレビューする。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### B-04 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

確認した主要機能の一般説明に、古さだけを理由とする問題は見いだしていない。

公開日の新旧ではなく現在の一次資料と照合。版や権限に依存する懸念はB-01へ限定して残す。 適用ルール: B-04

根拠: EV-ARTICLE「機能の役割」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-WP-HIERARCHY「Single Page」: 固定ページではスラッグ等に基づくPHPテンプレートを選ぶ仕組みを説明。 / EV-WP-PATTERN「Sync・編集」: パターンと同期の違い、挿入後の編集を説明。 / EV-WP-FIELDS「概要」: 投稿に付随するkey/valueのメタデータを説明。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 記事全体の最新化を要求しない。対象設定を再確認する場合だけ条件を添える。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "当該説明の根拠が更新されたとき、影響する箇所だけを再照合する。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### B-05 — 適切

EVALUATION / high / 重要性 none / 優先度 none

確認した本文の参照と問い合わせリンクは、説明と関連する先に到達する。

本文には公式参照と連絡先リンクがある。関連記事やサービス詳細リンクが少ないこと自体を欠陥にしない。 適用ルール: B-05

根拠: EV-ARTICLE「本文のa[href]」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-CONTACT「公開フォーム」: フォームと関連する問い合わせ種別を静的に確認。 / EV-GOOGLE-LINKS「リンク構造」: リンクのHTMLと文脈・アンカーの説明を推奨。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: リンク数の増加を目標にしない。任意の関連案内はD-02の仮説として扱う。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "アンカーとリンク先の内容・HTTP到達を確認。クリック効果は別途計測する。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### C-01 — 適切

EVALUATION / high / 重要性 none / 優先度 none

自己確認と影響する操作の境界が示されている。

自力で確認できることと公開環境に影響する変更を分けるという条件に適合。 適用ルール: C-01

根拠: EV-ARTICLE「次の案件では、予定している更新を1つ試してみる」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: この境界を維持する。不要な外注誘導は加えない。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "読者が資料と画面を確認でき、影響する試行には検証環境を選べるかをレビュー。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### C-02 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

現在の制作担当者への確認から外部相談へ進む条件が具体的。

相談を必須化せず、実装の調査が必要になる課題と相談前情報を示す。 適用ルール: C-02

根拠: EV-ARTICLE「結論の相談条件と準備情報」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-SERVICE-PARTNER「技術支援」: WordPress実装、改修、仕様整理を扱い、デザイン制作等は対象外。 / EV-SERVICE-MAINTENANCE「対応できること」: 改修、不具合調査、実装相談等を継続的に扱う。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 相談条件と準備情報を保つ。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "相談の対象・課題・提供範囲が一致するか再照合する。問い合わせの質は履歴がある場合のみ観測。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### C-03 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

相談獲得のために必要な判断材料を伏せる記述は確認していない。

記事の説明範囲と相談境界が対応する。コードの省略は設計判断の記事の目的から許容できる。 適用ルール: C-03

根拠: EV-ARTICLE「全体の説明範囲と結論」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 技術的に詳しいという理由だけで情報を削らない。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "中心疑問への回答と比較条件が提案後も残るかを確認する。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### D-01 — 適切

EVALUATION / high / 重要性 none / 優先度 none

記事の一般的な相談案内は、確認した実装・運用支援の範囲と矛盾しない。

未確認の商品名、料金、成果保証を補っていない。 適用ルール: D-01

根拠: EV-ARTICLE「結論の相談案内」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-SERVICE-PARTNER「対応範囲・除外」: WordPress実装、改修、仕様整理を扱い、デザイン制作等は対象外。 / EV-SERVICE-MAINTENANCE「対応できること」: 改修、不具合調査、実装相談等を継続的に扱う。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 現行で確認できた範囲に案内を限定する。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "相談内容と公式サービスの範囲を対応させる。個別受諾や成果を保証しない。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### D-02 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

設計や改修の判断という課題と、確認済みの技術支援との関連がある。

見た目のデザイン制作と、設計意図を踏まえた実装支援は混同しない。現状の連絡先案内にも関連性がある。 適用ルール: D-02

根拠: EV-ARTICLE「相談案内」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-SERVICE-PARTNER「技術支援・対象外業務」: WordPress実装、改修、仕様整理を扱い、デザイン制作等は対象外。 / EV-SERVICE-MAINTENANCE「実装相談」: 改修、不具合調査、実装相談等を継続的に扱う。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: HYPOTHESIS (任意): 主読者向けの技術支援ページを案内に添えると相談範囲を確認しやすくなる可能性。追加は必須としない。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: unverified — 関連サービス案内が範囲理解や適合した遷移を助けるという任意仮説。CV効果は未検証。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "現状と案内変更後で、記事閲覧セッションに対するサービス遷移セッション率と相談適合度を比較。イベント定義・必要母数・目標差・期間を事前設定し、未設定なら効果判断を保留する。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### E-01 — 適切

FACT / high / 重要性 none / 優先度 none

本文の末尾に問い合わせへの案内とリンクがある。

CTAの存在の観測に限定し、問い合わせ増加への効果を認定しない。 適用ルール: E-01

根拠: EV-ARTICLE「末尾のa[href="https://olein-design.com/contact"]」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: CTA不足という理由で増設を求めない。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "案内文とリンクの存在を確認する。実際のクリックや送信は別の測定対象。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### E-02 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

相談条件と準備情報を説明した文脈に案内が置かれている。

無条件な営業ではなく、困りごとの整理からつながる。主読者と運用中サイトの副読者が混在するが、それだけで不適切としない。 適用ルール: E-02

根拠: EV-ARTICLE「結論の前後文脈」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-SERVICE-PARTNER「技術支援」: WordPress実装、改修、仕様整理を扱い、デザイン制作等は対象外。 / EV-SERVICE-MAINTENANCE「実装相談」: 改修、不具合調査、実装相談等を継続的に扱う。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 現在の条件付き案内を維持する。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "相談対象者・課題・連絡先が結論と整合するかを確認。配置の最適性は実測なしに認定しない。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### E-03 — 判定不可

UNVERIFIED / unknown / 重要性 info / 優先度 none

静的な連絡先への到達は確認したが、送信成功までの経路は未検証。

現行ルールは送信未確認の範囲を判定不可とする。HTTP200と入力欄の確認を、送信や通知の成功に拡張しない。 適用ルール: E-03

根拠: EV-ARTICLE「問い合わせリンク」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。 / EV-CONTACT「公開フォーム」: フォームと関連する問い合わせ種別を静的に確認。

制限: 静的到達とフォーム要素のみ確認。入力操作・送信・通知未検証。

提案: フォーム不具合とは断定しない。送信検証が必要な場合は、対象と方法の許可を別途得る。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "許可を得たテスト送信で完了表示と受信を確認。静的表示・入力・送信・通知を別の確認結果として残す。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

- static_path: 適切 / FACT / high — 本文の連絡先リンクと、到達先ページの取得を確認している。 理由: 前回取得した公開HTMLとHTTP200に基づく静的到達の観測。 制限: ブラウザでの視覚的表示と入力・送信・通知は別の確認。
- submission: 判定不可 / UNVERIFIED / unknown — フォームの送信・完了・受信は確認していない。 理由: 静的取得を動作確認に拡張しない。送信テストは行っていない。 制限: 入力操作・送信・完了表示・受信は未検証。フォーム不具合とも成功とも断定しない。
### E-04 — 判定不可

UNVERIFIED / unknown / 重要性 info / 優先度 none

実際のSEO・遷移・問い合わせ成果と改善効果は評価できない。

GSC、GA4、問い合わせ履歴がすべて未提供。欠測を0件や失敗に換算しない。 適用ルール: E-04

根拠: EV-SEARCH-CONSOLE「未提供」: 今回の利用者入力に分析資料はない。 / EV-GA4「未提供」: 今回の利用者入力に分析資料はない。 / EV-INQUIRIES「未提供」: 今回の利用者入力に分析資料はない。

制限: 分析データ・対象期間・母数・計測定義・帰属はすべて未取得。

提案: 仮説の検証に必要な計測条件を整理する。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "GSCはページ別の期間・クエリ等、GA4は記事閲覧セッションと遷移/送信イベント、問い合わせは匿名の関連分類を取得。比較条件・必要母数・成功/反証条件を決めてから評価する。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### F-01 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

確認した本文には、恐怖や成果保証で相談を迫る表現を認めない。

表現と条件の書き方の評価であり、読者の心理的効果の測定ではない。 適用ルール: F-01

根拠: EV-ARTICLE「全体と相談案内」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 穏当な案内と筆者の判断の区別を保つ。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "条件のない不安喚起・保証が修正時に加わっていないかをレビュー。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}

### F-02 — 適切

EVALUATION / medium / 重要性 none / 優先度 none

公開中サイトへの影響に配慮した確認方法が示されている。

現場の安全な確認という範囲を評価。コード実行や個別サイトの安全性まで保証しない。 適用ルール: F-02

根拠: EV-ARTICLE「結論の検証環境と担当者確認」: 制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。

制限: 公開HTMLと本文の範囲の評価。視覚的な配置・個別実装・行動データの保証はしない。

提案: 本番での不用意な試行を求めない。

優先度理由: 確定した修正必須問題はない。要確認事項は調査順で扱い、成果推定で重要度を増やさない。

期待効果: not_applicable — 品質の評価または取得範囲の観測。成果への効果は認定しない。

検証: {"metric": "該当する記述と根拠・読者目的・適用条件の一致。行動指標を用いる場合は分母と定義を別途固定する。", "method": "影響する操作を検証環境で確認する境界を維持。B-01の解除設定の再現とは別に扱う。", "success_condition": "文書確認は条件と根拠が整合すること。未実測のSEO/CV改善は成功としない。", "confounders": ["対象版・ロール・テーマ差、流入/期間/端末差、同時変更、計測漏れや帰属の不明"]}


## 根拠台帳

- {"id": "EV-ARTICLE", "source_type": "article", "title": "その WordPress サイト、なぜその作り方を選びましたか ? | オレインデザイン", "publisher": "オレインデザイン", "source": "https://olein-design.com/blog/wordpress-design-and-client-agreement", "availability": "available", "checked_at": "2026-10-30T08:14:46+09:00", "published_date": "2026-10-29", "updated_date": "2026-10-29", "location": "冒頭、技術の役割、2つの仮例、操作別表、終盤", "observation": "制作者向けに設計と合意形成を整理し、仮例と判断を区別。自力確認・相談条件と問い合わせリンクを掲載。", "supports": ["想定読者、記事構成、CTA、表現の観測"], "limitations": ["公開本文とHTMLの確認。作者の実体験や成果の独立検証ではない。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-WP-HIERARCHY", "source_type": "official", "title": "Template Hierarchy – Theme Handbook | Developer.WordPress.org", "publisher": "WordPress.org", "source": "https://developer.wordpress.org/themes/classic-themes/basics/template-hierarchy/", "availability": "available", "checked_at": "2026-10-30T08:14:47+09:00", "published_date": "2014-10-22", "updated_date": "2024-07-24", "location": "Single Page", "observation": "固定ページではスラッグ等に基づくPHPテンプレートを選ぶ仕組みを説明。", "supports": ["page-service.phpという例の位置付け"], "limitations": ["クラシックテーマの説明。個別テーマの実装は未検証。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-WP-LOOP", "source_type": "official", "title": "The Loop – Theme Handbook | Developer.WordPress.org", "publisher": "WordPress.org", "source": "https://developer.wordpress.org/themes/classic-themes/basics/the-loop/", "availability": "available", "checked_at": "2026-10-30T08:14:47+09:00", "published_date": "2014-10-22", "updated_date": "2022-11-17", "location": "What the Loop Can Display / Basic Examples", "observation": "the_content()は投稿・固定ページの本文を表示する。", "supports": ["本文とテンプレートに直接書いた要素の区別"], "limitations": ["実際のテーマやフックを実行した検証ではない。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-WP-PATTERN", "source_type": "official", "title": "Block Patterns – Documentation – WordPress.org", "publisher": "WordPress.org", "source": "https://wordpress.org/documentation/article/block-pattern/", "availability": "available", "checked_at": "2026-10-30T08:14:47+09:00", "published_date": null, "updated_date": null, "location": "概要、Sync、How to customize a Block Pattern", "observation": "パターンと同期の違い、挿入後の編集を説明。", "supports": ["再利用するひな型と編集の説明"], "limitations": ["テーマ・権限・版ごとの動作は要確認。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-WP-LOCK", "source_type": "official", "title": "Block Locking API – Block Editor Handbook | Developer.WordPress.org", "publisher": "WordPress.org", "source": "https://developer.wordpress.org/block-editor/how-to-guides/curating-the-editor-experience/block-locking/", "availability": "available", "checked_at": "2026-10-30T08:14:47+09:00", "published_date": "2023-12-27", "updated_date": "2026-10-14", "location": "Apply content-only editing / Change permissions", "observation": "content-onlyのModify経路と、canLockBlocksによる通常ロック操作の権限を別々に説明。", "supports": ["解除できる人の設定という説明の適用条件"], "limitations": ["今回の資料だけで個別実装を再現していない。WordPressの対象版・テーマ・権限は未特定。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-WP-FIELDS", "source_type": "official", "title": "Assign custom fields – Documentation – WordPress.org", "publisher": "WordPress.org", "source": "https://wordpress.org/documentation/article/assign-custom-fields/", "availability": "available", "checked_at": "2026-10-30T08:14:47+09:00", "published_date": null, "updated_date": null, "location": "概要・Usage", "observation": "投稿に付随するkey/valueのメタデータを説明。", "supports": ["カスタムフィールドの役割"], "limitations": ["特定のプラグインの挙動を保証しない。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-WP-META", "source_type": "official", "title": "Creating a custom block that stores post meta – WordPress Developer Blog", "publisher": "WordPress.org", "source": "https://developer.wordpress.org/news/2023/03/creating-a-custom-block-that-stores-post-meta/", "availability": "available", "checked_at": "2026-10-30T08:14:48+09:00", "published_date": "2023-03-03", "updated_date": null, "location": "導入の保存先を判断する段落", "observation": "検索条件として使うか、個別表示以外で使うかを判断材料として示す。", "supports": ["記事が引用する保存先判断の根拠"], "limitations": ["2023年の実装チュートリアル。保存場所を一律に決める規則ではない。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-SERVICE-PARTNER", "source_type": "service", "title": "制作会社・デザイン会社向け技術支援 | オレインデザイン", "publisher": "オレインデザイン", "source": "https://olein-design.com/service/partnership", "availability": "available", "checked_at": "2026-10-30T08:14:47+09:00", "published_date": "2026-01-16", "updated_date": "2026-01-16", "location": "対応範囲 / 本サービスで対応しないこと", "observation": "WordPress実装、改修、仕様整理を扱い、デザイン制作等は対象外。", "supports": ["制作会社向け相談との関連"], "limitations": ["契約・納期・成果保証は確認していない。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-SERVICE-MAINTENANCE", "source_type": "service", "title": "WordPress運用・実装サポート | オレインデザイン", "publisher": "オレインデザイン", "source": "https://olein-design.com/service/maintenance", "availability": "available", "checked_at": "2026-10-30T08:14:47+09:00", "published_date": "2026-01-15", "updated_date": "2026-09-29", "location": "対応できること / 関わり方", "observation": "改修、不具合調査、実装相談等を継続的に扱う。", "supports": ["運用中の編集課題との関連"], "limitations": ["個別案件の受諾・単発対応や成果は保証しない。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-CONTACT", "source_type": "service", "title": "お問い合わせ | オレインデザイン", "publisher": "オレインデザイン", "source": "https://olein-design.com/contact", "availability": "available", "checked_at": "2026-10-30T08:14:47+09:00", "published_date": "2015-06-30", "updated_date": "2025-04-15", "location": "問い合わせ種別、公開フォーム", "observation": "フォームと関連する問い合わせ種別を静的に確認。", "supports": ["記事のリンクから連絡先への到達"], "limitations": ["HTTP取得のみ。ブラウザでの表示・入力・送信・到達通知は未検証。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-GOOGLE-CONTENT", "source_type": "official", "title": "Creating Helpful, Reliable, People-First Content | Google Search Central  |  Documentation  |  Google for Developers", "publisher": "Google Search Central", "source": "https://developers.google.com/search/docs/fundamentals/creating-helpful-content", "availability": "available", "checked_at": "2026-10-30T08:14:48+09:00", "published_date": null, "updated_date": null, "location": "Self-assess / People-first", "observation": "読者の目的、信頼できる説明、独自の価値を重視する一般指針。", "supports": ["内容品質の一般基準"], "limitations": ["個別の検索順位やCV効果を証明しない。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-GOOGLE-LINKS", "source_type": "official", "title": "SEO Link Best Practices for Google | Google Search Central  |  Documentation  |  Google for Developers", "publisher": "Google Search Central", "source": "https://developers.google.com/search/docs/crawling-indexing/links-crawlable", "availability": "available", "checked_at": "2026-10-30T08:14:48+09:00", "published_date": null, "updated_date": null, "location": "Make your links crawlable / Anchor text", "observation": "リンクのHTMLと文脈・アンカーの説明を推奨。", "supports": ["本文のリンク構造の確認基準"], "limitations": ["リンク数の基準やCV増加を証明しない。", "取得HTMLのSHA-256と一時保存先はretrieval.jsonを参照。"]}
- {"id": "EV-SEARCH-CONSOLE", "source_type": "analytics", "title": "Search Console (未提供)", "publisher": "未提供", "source": "未提供:search_console", "availability": "not_provided", "checked_at": null, "published_date": null, "updated_date": null, "location": "データ取得状態", "observation": "今回の利用者入力に分析資料はない。", "supports": ["実成果の評価範囲の制限"], "limitations": ["未取得は0件を意味しない。"]}
- {"id": "EV-GA4", "source_type": "analytics", "title": "GA4 (未提供)", "publisher": "未提供", "source": "未提供:ga4", "availability": "not_provided", "checked_at": null, "published_date": null, "updated_date": null, "location": "データ取得状態", "observation": "今回の利用者入力に分析資料はない。", "supports": ["実成果の評価範囲の制限"], "limitations": ["未取得は0件を意味しない。"]}
- {"id": "EV-INQUIRIES", "source_type": "analytics", "title": "問い合わせ履歴 (未提供)", "publisher": "未提供", "source": "未提供:inquiries", "availability": "not_provided", "checked_at": null, "published_date": null, "updated_date": null, "location": "データ取得状態", "observation": "今回の利用者入力に分析資料はない。", "supports": ["実成果の評価範囲の制限"], "limitations": ["未取得は0件を意味しない。"]}

## 全体制限・判定不可

- 根拠と監査は2026-10-30T08:14台に取得した同一版の固定資料を再利用。現行サービス・仕様の再確認ではない。
- B-01の環境動作は未検証のまま。修正文は確認条件の明示であり、疑義の解消・誤情報の修正完了とは扱わない。
- 元原稿と公開サイトは変更しない。別ファイルの修正文も公開候補の承認・公開QA合格ではない。
- 分析データと送信結果は未取得。改善によるSEO/CV効果を認定しない。
- 同じ評価担当が実行と意味照合を行う単一実記事テスト。汎用性能を証明しない。
