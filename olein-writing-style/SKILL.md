---
name: olein-writing-style
description: Write Japanese blog posts, articles, drafts, outlines, announcements, and explanatory copy in the user's Olein-style voice. Use when the user asks Codex to draft, rewrite, polish, structure, or ideate Japanese writing that should sound like the user's past posts on olein-design.com/blog or note.com/olein_jp, especially WordPress/web production articles, personal essays, learning reflections, family notes, service announcements, and practical how-to content.
---

# Olein Writing Style

## Core Workflow

1. Clarify the target medium, topic, audience, and intended action when they are not obvious from the request.
2. Read `references/style-guide.md` before drafting or rewriting.
3. Read and apply `references/wordpress-ja-notation.md` before drafting or rewriting. Treat it as the default for Japanese typography, spacing, punctuation, labels, names, and terminology. Preserve the Olein voice for tone, phrasing, structure, and authorial stance.
4. Read `references/source-sample.md` when you need evidence of the sampled article set, title patterns, or platform differences.
5. Assume the article must stand on its own for an interested beginner unless the user explicitly defines a more knowledgeable audience. Do not assume that the reader has read an earlier article or knows terminology explained elsewhere.
6. Build a brief experience inventory from facts the user has provided in the request, conversation, project notes, or source material. Capture the situation, what the author did or observed, any friction or surprise, the result, and the author's current interpretation. Never invent an experience or convert a general assumption into a first-person claim.
7. When experience is important but the available facts are insufficient, ask one to three focused questions before a final draft. If the user wants a draft without answering, use explicit placeholders such as `[実体験を追記: 更新作業で困った場面と、そのとき確認したこと]` or keep the passage experience-neutral. Do not hide missing facts behind plausible prose.
8. When the writing requires external facts, current information, product details, technical specifications, laws, prices, events, statistics, or third-party claims, research primary or official sources first and base the draft on the highest-confidence information available.
9. Choose one mode before writing:
   - **Technical article**: practical WordPress/web explanation.
   - **Practical opinion**: professional judgment from experience.
   - **Personal essay**: reflective note from daily life, learning, family, or work.
   - **Announcement**: warm, concise notice for books, courses, events, or services.
10. Weave at least one concrete, relevant experience into an article when the format and available evidence support it. Use the experience to explain a decision, caution, change of view, or practical recommendation; do not add an anecdote only as decoration. Short notices, reference-only copy, and other formats where an anecdote would feel forced are exempt.
11. When using reference links, place each link where it helps the reader: either on the relevant word/phrase itself or at the end of the section that discusses that source.
12. Continue to include a consolidated reference-link list at the bottom when external sources are used.
13. Draft in Japanese unless the user explicitly requests another language.
14. After drafting, scan for technical terms, abbreviations, industry jargon, and unfamiliar concepts. At the first occurrence in that article, add a short plain-language explanation when an interested beginner may not understand the term or why it matters. Explain the name, mechanism, or consequence when that is what makes the concept understandable. Keep established terms when accuracy or discoverability benefits from them; explain rather than merely replace them. Follow the detailed guidance in `references/style-guide.md`.
15. When the target is an Olein Design business-site blog article, or the supplied publisher requirements explicitly call for self-service boundaries, consultation guidance, internal-link routing, and a service CTA, read and apply `references/business-article-finalization.md` after drafting and before the final self-check. Do not apply it automatically to personal essays, note articles, short announcements, X posts, Coconala blog posts, or general explanatory copy without a consultation path unless the user or medium-specific instructions explicitly require the same checks.
16. Review the text first for clarity and coherence as Japanese prose, then for conformity with the Olein writing style and the Japanese notation rules. Perform the self-check in this file and revise once before answering.

## Writing Priorities

- Write from a first-person, experience-based standpoint. Prefer `僕` for personal pieces and softer professional articles; use `当方` or service-centered phrasing only when the context is business-like.
- Distinguish the author's direct experience, observed patterns from client work, professional judgment, and externally verified facts. Anonymize client details and omit identifying information unless the user explicitly authorizes its use.
- Prefer small, concrete details that affect the author's judgment over broad claims such as `多くの現場で感じています`. A useful experience shows what happened, what was difficult, and what the author now does differently.
- Make the reader feel guided, not lectured. Explain the premise, show why it matters, then offer a practical way forward.
- Make each article understandable on its own. A link to an earlier explanation may supplement the current article, but must not replace the brief explanation needed in the current article.
- Preserve useful technical vocabulary while pairing difficult terms with concise, concrete explanations. Do not make the reader leave the article merely to understand the sentence in front of them.
- Keep the tone calm, sincere, and slightly conversational. Light self-correction, parenthetical nuance, and "個人的には" style hedging are part of the voice.
- Use the WordPress Japanese notation conventions as surface-level writing rules, not as a replacement voice. Do not flatten Olein's experience-led phrasing into generic UI copy or translation prose.
- Preserve technical accuracy. When writing about WordPress or web production, separate facts, current constraints, and personal judgment.
- Prefer verified facts over fluent prose. If reliable primary or official information cannot be found, say so and either narrow the claim or mark it as uncertain.
- Prioritize clear meaning over surface-level imitation. Do not reproduce wording or sentence patterns from the samples when doing so makes the text ambiguous or difficult to follow.
- Avoid over-polished marketing copy. The voice should feel like a practitioner writing honestly from real experience.

## Structural Defaults

For technical articles:

1. Short context about why the topic matters.
2. Definition or current situation, including plain-language explanations of unfamiliar terms at first occurrence.
3. Practical steps, examples, or decision points.
4. Notes and caveats from implementation or operation.
5. A modest conclusion such as "参考になれば嬉しいです" or "ぜひ活用してみてください".

For personal essays:

1. Start from a recent event or a simple observation.
2. Explain the situation with concrete details.
3. Reflect on what changed, what was learned, or what remains unclear.
4. End gently, without forcing a grand lesson.

For announcements:

1. State what happened.
2. Add why it matters or who it is for.
3. Share background or intent.
4. End with a simple invitation.

## Self-Check

Before returning the draft, verify the quality of the Japanese prose first, then verify the Olein writing style.

### Japanese Clarity

- Each sentence communicates one understandable point, with a clear relationship between its subject and predicate.
- Sentences and paragraphs follow a logical sequence without missing connections or abrupt changes in topic.
- Omitted subjects, pronouns, and demonstratives such as `これ`, `それ`, and `この` have clear referents.
- The wording does not create unintended ambiguity, unnecessary repetition, or sentences that require rereading.
- Every technical term, abbreviation, industry expression, or unfamiliar concept that an interested beginner may not understand is explained at its first occurrence in this article.
- Each necessary explanation makes the relevant point clear: what the term means, why it has that name, how it works, or what effect it has. A circular definition or a parenthetical synonym that is equally difficult does not count.
- The draft does not omit a necessary explanation merely because another article or linked source explains the term.
- Familiar words are not over-explained, and explanations do not interrupt the article more than necessary.
- Each section has a clear purpose, and the conclusion follows naturally from the preceding explanation.
- Stylistic revisions preserve the intended meaning and technical accuracy.

### Olein Style

- The piece does not sound like generic corporate copy.
- The authorial stance is humble but not evasive.
- At least one concrete experience supports the article's reasoning when the format and supplied facts make that appropriate.
- Every first-person experience is grounded in information actually supplied or verified; no event, result, client reaction, family detail, or emotion has been invented.
- The draft clearly distinguishes direct experience, anonymized observation, professional judgment, and external fact.
- Important claims include context, conditions, or caveats.
- External factual claims are grounded in primary or official sources whenever possible.
- Reference links appear near the relevant section or phrase, and a consolidated reference list remains at the bottom when sources are used.
- Unverified, secondary, or inferred information is not presented as confirmed fact.
- Headings are plain and useful.
- Parentheses, examples, and small asides are used naturally, not excessively.
- The ending is warm and practical rather than dramatic.

### Japanese Notation

- The draft follows `references/wordpress-ja-notation.md` for character width, spacing, punctuation, parentheses, numerals, UI labels, names, and terminology.
- The notation pass does not remove Olein-specific voice, personal judgment, conversational rhythm, or mode-specific structure.
- Translation-only rules are applied only when the draft actually contains translated UI text, labels, messages, or placeholders.
