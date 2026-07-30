# WordPress Japanese Notation

Use these conventions for the surface notation of Japanese drafts. They are adapted from the [WordPress.org Japanese Translation Style Guide](https://ja.wordpress.org/team/handbook/translation/translation-style-guide/), last checked on 2026-07-30.

This reference intentionally excludes the source section titled `WordPress の文章スタイル`, including its three principles about clarity, originality, and modern wording. Do not use that section to replace or dilute the Olein voice. `references/style-guide.md` remains authoritative for tone, phrasing, structure, authorial stance, and mode selection.

## General Typography

- Use full-width `。` and `、` for Japanese punctuation.
- Use half-width characters for Latin letters, Arabic numerals, symbols, question marks, and exclamation marks.
- Use half-width Arabic numerals by default. Keep conventional kanji forms in established words such as `二次元コード`.
- Insert one half-width space between Japanese text and adjacent half-width text, except around numerals and the punctuation exceptions below.
- Do not insert spaces next to `「」`, `『』`, `。`, or `、`.
- Do not insert a space before a colon. Insert one half-width space after it when text follows.
- Insert one half-width space before a half-width `?` or `!` when it follows Japanese text.
- Do not insert spaces around half-width numerals or numeric placeholders when they directly modify Japanese counters: `1件`, `33個`, `%d件`.

Examples:

- `WordPress の使い方`
- `ユーザー ID: username`
- `こんにちは、username さん。`
- `準備ができましたか ?`
- `バージョン5.5`

## Parentheses

- Use half-width parentheses `( )`.
- Insert one half-width space outside each parenthesis when it touches Japanese or other text. Do not insert spaces immediately inside the parentheses.
- Do not put a full stop at the end of a single sentence inside parentheses.
- When parentheses end a sentence, put `。` after the closing parenthesis.
- When parentheses contain multiple sentences, place `。` only between the sentences.

Examples:

- `補足を追加します (必要な場合のみ)。`
- `(例: WordPress)`

## Labels, Quotations, and Emphasis

- Enclose menu items, page names used as UI labels, and button labels in `「」`.
- For quoted Japanese text, use `「」`. Preserve half-width quotation marks around quoted domain names, function names, or other Latin-script identifiers when that distinction is useful.
- When italics would make Japanese text hard to read, express the emphasis with `「」` or omit unnecessary emphasis.
- Keep menu and button terminology consistent within the same article and with the product's official Japanese UI.

## Wording Consistency

These rules apply when writing or translating WordPress UI text, error messages, labels, or closely related instructions:

- Prefer natural active constructions over avoidable passive constructions.
- Translate `View …` as `〜を表示` or `〜を表示する` when describing WordPress UI behavior.
- Express `… is not allowed to …` as `〜する権限がありません`.
- Omit a formulaic `Sorry,` at the start of an error message instead of translating it as `すみません`.
- Omit unnatural `あなた` or `あなたの`; use a natural alternative such as `自分の` or `お使いの`, or omit the subject.
- Standardize on `ください`, `すべて`, and `すでに`.
- Keep sentence endings consistent by context:
  - Use a noun phrase or plain-form `する` for headings.
  - Use plain-form `する` for list items that describe actions.
  - Omit `します` or `する` from concise button labels.
- Follow the source punctuation when translating exact UI strings. When writing original article prose, follow the Olein style and the general typography rules above.

## Katakana Terms and Separators

- For a katakana loanword ending in a long vowel, include the long-vowel mark when the resulting word has four or fewer characters; generally omit it for words of five or more characters.
- Apply that judgment to each part of a compound word.
- Preserve established exceptions, especially words ending in sounds derived from `er`, `ar`, `or`, `re`, `y`, or `ew` when Japanese usage conventionally includes a long-vowel mark.
- Avoid `・` in katakana compounds unless an official glossary specifies it or the boundary would otherwise be difficult to understand.
- Prefer a natural connector such as `の` when it makes a long compound easier to read.
- Use the official WordPress Japanese glossary or the product's established notation when it conflicts with a mechanical character-count rule.

## Brand and Feature Names

- Write `WordPress` exactly with that capitalization.
- Keep theme and plugin product names untranslated unless the official name itself is localized.
- Use official Japanese feature names and WordPress glossary terms consistently.
- Preserve exact casing and spelling for code identifiers, function names, domains, commands, file names, and version strings.

## Dates and Placeholders

- Use Japanese date order and notation in Japanese prose: `2014年1月1日 (水)`.
- Preserve the number, type, and identity of placeholders such as `%s`, `%d`, `%1$s`, and `%2$s`.
- Reorder numbered placeholders only when Japanese syntax requires it and the placeholder syntax supports reordering.
- Never translate or alter code-like date format strings unless the task explicitly concerns localization.

## Precedence and Exceptions

1. Follow an explicit user, publisher, or project-specific house style when provided.
2. Preserve exact UI strings, code, commands, quoted source text, and registered product names.
3. Apply this reference to notation and terminology.
4. Apply `references/style-guide.md` to voice, rhythm, structure, and personal expression.

When a notation rule would make a sentence unnatural or damage the intended Olein voice, keep the meaning and voice, then apply the closest non-disruptive form of the notation rule.
