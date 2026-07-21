# personal-agent-skills

個人的に利用する Codex / AI エージェント向けスキルを管理・開発するためのリポジトリです。

このリポジトリでは、スキルそのものは小さく保ち、運用ルールや開発メモはこの README に集約します。各スキルの中には、原則として `SKILL.md` と必要最小限の `agents/`、`scripts/`、`references/`、`assets/` だけを置きます。

## 目的

- よく行う作業をスキルとして再利用できる形にする
- 過去のチャットで固まった作業手順や判断基準を、次回以降の Codex が使える形に整理する
- WordPress 開発、リリース、検証、ドキュメント整備など、自分の反復作業を安定化する
- ローカルの `~/.agents/skills` に導入しやすい形で、個人スキルを Git 管理する

## 管理中のスキル

- `codex-issue-writer`: Codex が実装しやすい GitHub Issue / PR 作業指示を作成する
- `olein-writing-style`: Olein らしい日本語文体で記事、告知、説明文を作成する
- `wp-plugin-review`: WordPress プラグインを WPCS とセキュリティ中心にレビューし、修正方針と PR 準備情報まで整理する

## 基本方針

### スキルは短く、実行可能にする

Codex はすでに一般的な知識を持っているため、`SKILL.md` には「この環境・この作業でないと分からないこと」を優先して書きます。

良いスキルに含めるもの:

- いつ使うべきかが分かる `description`
- 実行順序が重要なワークフロー
- リポジトリ固有の検証コマンド
- 失敗しやすい箇所と回避策
- 何度も書き直しているスクリプトやテンプレート

避けるもの:

- 一般論だけの長い説明
- 各スキル内の `README.md` や `CHANGELOG.md`
- チャットの経緯そのもの
- Codex が毎回読む必要のない大量の参考資料

### Progressive Disclosure を守る

スキルは、必要になった情報だけを段階的に読む前提で作ります。

標準構成:

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
├── references/
└── assets/
```

- `SKILL.md`: 必須。トリガー条件と中核手順を書く
- `agents/openai.yaml`: 推奨。Codex UI 向けの表示名、短い説明、初期プロンプトを書く
- `scripts/`: 何度も使う処理や、手順ミスを避けたい処理を置く
- `references/`: 必要な時だけ読む詳細情報を置く
- `assets/`: テンプレート、画像、雛形など、出力に使う素材を置く

## スキルの作成手順

### 1. 用途を具体化する

まず、次の点を短く整理します。

- どんな依頼でこのスキルを使うか
- どのリポジトリ、サービス、作業領域に関係するか
- 毎回迷いやすい判断は何か
- 成功判定は何か
- 検証に必要なコマンドや画面確認は何か

例:

```text
WordPress プラグインのリリース時に、バージョン同期、ビルド、ZIP 検証、タグ作成、GitHub Actions 確認までを漏れなく実施したい。
```

### 2. スキル名を決める

スキル名は小文字、数字、ハイフンのみを使います。

良い例:

- `wordpress-plugin-release-runbook`
- `wp-issue-verification`
- `github-pr-review-triage`

避ける例:

- `WordPressRelease`
- `release_skill`
- `my awesome skill`

### 3. スキルを初期化する

新規スキルは、Codex の `skill-creator` が提供する初期化スクリプトを使って作成します。このリポジトリ直下に `scripts/` がある前提ではなく、現在の環境では次の場所にあります。

```bash
python3 /Users/olein/.codex/skills/.system/skill-creator/scripts/init_skill.py <skill-name> --path .
```

必要に応じてリソース用ディレクトリも同時に作ります。

```bash
python3 /Users/olein/.codex/skills/.system/skill-creator/scripts/init_skill.py <skill-name> --path . --resources scripts,references,assets
```

このリポジトリ内で開発したあと、完成したスキルごとに `~/.agents/skills` へシンボリックリンクを作成します。

### 4. `SKILL.md` を編集する

`SKILL.md` の frontmatter は、原則として `name` と `description` だけにします。

```markdown
---
name: wordpress-plugin-release-runbook
description: WordPress プラグインのリリース作業を支援する。バージョン同期、ビルド、ZIP 検証、タグ作成、GitHub Actions 確認、デプロイ前後の安全確認が必要なときに使う。
---
```

`description` はスキルの起動条件になるため、特に丁寧に書きます。本文に「いつ使うか」を書いても、スキルが読み込まれる前には参照されないため、起動条件は `description` に入れます。

本文には、実際に次の Codex が作業できる粒度で書きます。

- 最初に確認するファイルや issue
- 安全上の注意
- 実行する順序
- 代表的な検証コマンド
- よくある失敗と切り分け
- 完了条件

### 5. リソースを追加する

繰り返し使うものは、本文に長く貼らずにリソース化します。

- コマンド列が壊れやすい: `scripts/`
- 長い仕様や参照資料が必要: `references/`
- 雛形や素材が必要: `assets/`

`references/` に分けた情報は、`SKILL.md` から「いつ読むべきか」が分かるようにリンクします。

### 6. 検証する

最低限、次を確認します。

```bash
python3 /Users/olein/.codex/skills/.system/skill-creator/scripts/quick_validate.py <path-to-skill-folder>
```

確認観点:

- `SKILL.md` の YAML frontmatter が壊れていない
- `name` とフォルダ名が一致している
- `description` が具体的で、起動条件を含んでいる
- 不要なファイルを増やしていない
- スクリプトを追加した場合、代表ケースで実行済みである

## ローカル Codex への導入

開発中はこのリポジトリで編集し、完成したスキルだけを `~/.agents/skills` に個別のシンボリックリンクとして配置します。

大まかな流れ:

1. このリポジトリでスキルを開発・作成する
2. `SKILL.md` と必要なリソースを整え、検証して完成させる
3. 完成したスキルごとに `~/.agents/skills` へシンボリックリンクを作成する

既存のスキルと共存させるため、`~/.agents/skills` フォルダ全体をこのリポジトリへのリンクに置き換えないでください。スキルごとのフォルダ単位でリンクします。

例:

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/wordpress-plugin-release-runbook" "$HOME/.agents/skills/wordpress-plugin-release-runbook"
```

同名のスキルがすでにある場合、`ln -s` は失敗します。作成前に確認します。

```bash
ls -ld "$HOME/.agents/skills/wordpress-plugin-release-runbook"
```

リンク済みかどうかは `ls -la` で確認できます。`->` が表示されていればシンボリックリンクです。

```bash
ls -la "$HOME/.agents/skills"
```

安全に作成する例:

```bash
SKILL_NAME="wordpress-plugin-release-runbook"
SOURCE="$PWD/$SKILL_NAME"
DEST="$HOME/.agents/skills/$SKILL_NAME"

mkdir -p "$HOME/.agents/skills"

if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  echo "すでに存在します: $DEST"
else
  ln -s "$SOURCE" "$DEST"
  echo "作成しました: $DEST -> $SOURCE"
fi
```

## 更新の流れ

1. 実際の作業で Codex が迷った点、失敗した点、毎回説明している点をメモする
2. 既存スキルに入れるか、新規スキルに分けるか判断する
3. `SKILL.md` は短く保ち、詳細は `references/` や `scripts/` に逃がす
4. 検証コマンドや完了条件を更新する
5. `quick_validate.py` と必要な実行確認を行う
6. 完成したスキルごとに `~/.agents/skills` へシンボリックリンクを作成する
7. 実際の依頼で使い、また改善する

## チャット由来の知見をスキル化する基準

過去のチャット内容は、そのまま貼るのではなく、次のように抽出して使います。

スキルに入れるべきもの:

- 何度も同じ確認をしている作業
- 特定リポジトリでの正しい検証順序
- 「これを見落とすと危ない」という注意点
- ユーザーの好みとして安定している運用
- 完了条件や報告の仕方

スキルに入れないもの:

- 一度だけの作業ログ
- 古くなりやすい一時的な状態
- 秘密情報、API キー、トークン、個人情報
- まだ検証されていない推測

## 個人スキルで特に大事にすること

### 実際の表面を確認する

ソースコードだけでなく、issue 本文、実行結果、ビルド成果物、画面、GitHub Actions、デプロイ結果など、ユーザーが実際に見る面を確認する手順を重視します。

### 完了条件を明確にする

「実装した」だけではなく、どこまでやれば完了かを書きます。

例:

- テストが通った
- ZIP の中身を確認した
- GitHub Actions が green になった
- バージョン表記が画面に出ている
- issue を close した

### 秘密情報を残さない

スキル、テスト出力、ログ、issue コメント、README には秘密情報を残しません。

特に扱いに注意するもの:

- API キー
- Webhook secret
- 認証 Cookie
- OAuth token
- 本番環境の接続情報

## 推奨レビュー観点

スキルを追加・更新したら、次の観点で見直します。

- そのスキルは本当に必要か
- `description` だけで起動条件が伝わるか
- 本文が長すぎないか
- 一般論ではなく、自分の作業に必要な知識になっているか
- 検証手順が実行可能か
- 古くなった情報を断定していないか
- 他のスキルと責務が重複していないか

## 今後追加したいスキル候補

- WordPress プラグインのリリース手順
- GitHub issue 起点の実装・検証・クローズ手順
- Playwright / screenshot ベースの表示確認
- ドキュメント、ヘルプ、利用規約、プライバシーポリシーの更新
- 依存関係アップデートの安全確認

## 運用メモ

- この README は、このリポジトリ全体の管理方針を書く場所
- 各スキル内には、Codex が作業時に読むための情報だけを置く
- チャットで得た知見は、ログではなく再利用可能な手順に変換してから入れる
- 迷ったら「次回の Codex がこの情報でより安全に、より短く作業できるか」で判断する
