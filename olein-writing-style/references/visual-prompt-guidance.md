# Visual Prompt Guidance

Use this guidance when an article would become meaningfully easier to understand with a visual. The goal is not to decorate the article or increase image count. A visual must carry explanatory work that prose alone handles less efficiently.

## When to Add a Visual Prompt

Add a prompt when at least one of these is true:

- A process has three or more stages whose order or branching matters.
- Several concepts, components, roles, or layers need to be understood in relation to one another.
- A before/after state or a comparison across multiple dimensions is central to the reader's decision.
- Spatial placement, hierarchy, information flow, or cause and effect would be clearer when seen.
- A concrete scene or annotated interface would help a beginner recognize what the prose describes.

Prefer prose, a short list, or a simple table when that communicates the point just as clearly. Do not add a generic eye-catch, decorative stock-photo prompt, mood image, or redundant illustration merely to break up text. Most articles need only zero to three explanatory visuals unless the user requests otherwise.

## Placement and Output Format

Place the block immediately after the paragraph that establishes the concept and before the detailed explanation that benefits from it. Keep it visibly separate from publishable prose so an editor can remove or act on it.

```markdown
<!-- 図版案
挿入位置: （直前の見出しや段落を具体的に示す）
目的: （この図で読者が理解できることを1文で示す）
形式: （フロー図／関係図／比較図／注釈付き画面／説明イラストなど）
生成プロンプト:
「（そのまま画像生成に使える具体的なプロンプト）」
代替テキスト: （画像を見られない読者にも要点が伝わる簡潔な説明）
-->
```

If the target publishing system removes HTML comments or the user requests visible production notes, use a clearly labeled bracketed block instead. Preserve the same fields.

## Prompt Requirements

Make each prompt self-contained. Describe the subject, layout, relationships, exact labels, visual hierarchy, color role, aspect ratio, and exclusions needed to produce the intended explanatory asset.

Apply these defaults unless the article or user specifies otherwise:

- Simple, restrained editorial design whose first purpose is comprehension.
- Flat two-dimensional layout, generous whitespace, clear grouping, and an obvious reading order.
- Minimal color palette: neutral background and text plus one or two muted accent colors used only to encode meaning.
- No ornamental gradients, shadows, glossy effects, 3D rendering, photorealistic decoration, mascots, or unrelated icons.
- Use `Noto Sans JP` for all Japanese text. Keep labels short and provide their exact spelling in the prompt.
- Use strong enough contrast and type sizes to remain readable when embedded in an article.
- Avoid dense text inside the image. Move explanations into the article or caption.
- Do not add facts, quantities, UI details, brand assets, or causal claims that the article and its sources do not support.
- State an appropriate aspect ratio. Prefer wide landscape formats such as 16:9 or 3:2 for article content, unless the subject requires another shape.

When Japanese typography must be pixel-perfect, keep generated in-image text to essential short labels and note in the prompt that labels may be typeset afterward using Noto Sans JP. For an interface explanation, prefer an annotated screenshot supplied by the user over an invented UI. If no source screenshot is available, describe the visual as a schematic rather than presenting it as an exact interface.

## Choosing the Visual Form

- Use a **flow diagram** for sequence, branching, or handoffs.
- Use a **relationship or layer diagram** for structure, dependency, ownership, or information flow.
- Use a **comparison diagram** only when the dimensions are stable and the contrast is easier to scan visually than in prose or a table.
- Use an **annotated screenshot** for exact controls, locations, or interface states when a reliable source image exists.
- Use an **explanatory illustration** for a physical or conceptual scene that genuinely supports recognition or recall; keep it diagrammatic rather than atmospheric.

Do not force a visual form before identifying the reader's confusion. Start with the concept the reader needs to grasp, then choose the smallest visual that resolves it.
