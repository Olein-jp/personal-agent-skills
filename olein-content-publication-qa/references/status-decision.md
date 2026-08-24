# Status Decision

## 優先順位

次の順序でOverall Statusを決める。

1. Blocking問題が1件以上ある: `FAIL`
2. Blockingはないが、公開前に必要な外部確認・本人判断・成果物待ちがある: `PENDING`
3. BlockingもPendingもなく、任意改善だけがある: `PASS WITH OPTIONALS`
4. 必須要件をすべて満たし、残件がない: `PASS`

低い優先度の状態で高い優先度の問題を上書きしない。

## PASS

- 必須要件をすべて満たす。
- 必要なInvariantを実データで確認済みである。
- Blocking、Pending、Optionalが0件である。
- そのまま人間の公開判断へ進める。

## PASS WITH OPTIONALS

- BlockingとPendingが0件である。
- 任意の内部リンク、軽微な表現改善など、公開を止めない提案だけが残る。
- 任意改善だけを理由に`PENDING`へ落とさない。

## PENDING

- 成果物の根本的な再設計や前工程への差し戻しは不要である。
- 外部状態、人間の判断、予定された付属成果物の完成を待てば判定できる。
- 例: URL到達確認待ち、本人回答待ち、規格準拠カバー画像の作成待ち、媒体または精度モードが不明。

## FAIL

- 現在の成果物にBlocking問題がある。
- 調査、構成、執筆など前工程への差し戻し、または成果物自体の修正が必要である。
- 例: Traceability欠落、Verified不正昇格、Provenance欠落、重大なCoverage欠落、内部QA情報の混入、存在する画像の規格不適合。

## 境界事例

- Exact URLが記録されていない場合、単なる到達確認待ちではなくTraceability成果物の欠陥なので`FAIL`とする。
- カバー画像が未納だが作成工程が残っている場合は`PENDING`、納品済み画像が規格不適合なら`FAIL`とする。
- 問題の件数を合わせたり、根拠を推測したりしてStatusを引き上げない。
