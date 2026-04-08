# Approach A — Cobalt Next syntax-rule inventory

Source: `source/cobaltnext-vscode/themes/CobaltNext.json` lines 304–964
(the `tokenColors` array). Each row is one `tokenColors` entry.

Dark variant has identical `tokenColors` to main. Minimal adds one
"[HTML] - Custom Tag" rule (yellow) and drops the "HTML Class Component"
rule — otherwise identical. Inventory below uses the main variant.

## Legend

- **Proposed Zed token** — closest match from Zed's 40-token set
  (`attribute`, `boolean`, `comment`, `comment.doc`, `constant`,
  `constructor`, `embedded`, `emphasis`, `emphasis.strong`, `enum`,
  `function`, `hint`, `keyword`, `label`, `link_text`, `link_uri`,
  `number`, `operator`, `predictive`, `preproc`, `primary`, `property`,
  `punctuation`, `punctuation.bracket`, `punctuation.delimiter`,
  `punctuation.list_marker`, `punctuation.special`, `string`,
  `string.escape`, `string.regex`, `string.special`,
  `string.special.symbol`, `tag`, `text.literal`, `title`, `type`,
  `variable`, `variable.special`, `variant`). `N/A` = nothing fits.
- **Status** — ✓ matches Approach C; ✗ converter chose different color;
  ⊘ converter missed (no Zed token filled); ✗+⊘ both wrong and missed.

## Inventory

| # | Rule name                          | VS Code scopes (abbreviated)                      | Color     | Style    | Proposed Zed token    | Status | Notes |
|---|------------------------------------|----------------------------------------------------|-----------|----------|-----------------------|--------|-------|
| 1 | Comment                            | `comment`, `punctuation.definition.comment`       | `#65737e` | italic   | `comment`, `comment.doc` | ✓ | Converter propagates to comment.doc via fallback. |
| 2 | Variable                           | `variable`                                         | `#CDD3DE` | —        | `variable`            | ✓ |   |
| 3 | Keyword, Storage                   | `keyword`, `storage.type`, `storage.modifier`, `storage.type.class.js` | `#c5a5c5` | — | `keyword` | ✓ |   |
| 4 | Operator, Misc                     | `keyword.operator`, `punctuation`, `punctuation.definition.tag`, `punctuation.definition.tag.html`, `keyword.other.template`, `keyword.other.substitution`, `punctuation.section.embedded` | `#5FB3B3` | — | `operator`, `punctuation`, `punctuation.*` | ✓ | Teal. Converter picks this up cleanly via fallback chains. |
| 5 | Tag                                | `entity.name.tag`, `meta.tag.sgml`, `markup.deleted.git_gutter` | `#ed6f7d` | — | `tag` | ✓ |   |
| 6 | Function, Special Method           | `entity.name.function`, `meta.function-call`, `variable.function`, `support.function`, `keyword.other.special-method` | `#5a9bcf` | — | `function`, `constructor` (?) | ✓ | Blue. Constructor is a judgment call — see row 21. |
| 7 | Other Variable, String Link        | `support.other.variable`, `string.other.link`     | `#ed6f7d` | — | *(none; see note)*    | ✗ | Converter incorrectly assigned this to `link_text`/`link_uri`. These should be teal (see row 17). Real mapping: nothing — this is a niche TextMate scope. |
| 8 | Number, Constant, Parameter, Embedded | `constant.numeric`, `constant.language`, `support.constant`, `constant.character`, `variable.parameter`, `keyword.other.unit` | `#eb9a6d` | — | `number`, `boolean`, `constant`, `variable.parameter` | ✓ (mostly) | Orange. `boolean` resolves through `constant.language`. `variable.parameter` is its own Zed token but is absent from Approach C output. |
| 9 | String, Symbols, Inherited Class, Markup Heading | `string`, `constant.other.symbol`, `constant.other.key`, `entity.other.inherited-class`, `markup.heading` | `#99C794` | — | `string`, `string.special`, `string.special.symbol`, `text.literal`, `title` (weakly) | ✓ / ⊘ | Green. Converter propagates to all string.* via fallback. `title` would be close but converter doesn't match it. |
| 10 | Class, Support                    | `entity.name.class`, `entity.name.type.class`, `support.type`, `support.class`, `markup.changed.git_gutter` | `#FAC863` | — | `type` | ✓ | Yellow. |
| 11 | Sub-methods                       | `entity.name.module.js`, `variable.import.parameter.js`, `variable.other.class.js` | `#ed6f7d` | — | *(none; language-specific)* | — | Niche. |
| 12 | Variable Language                 | `variable.language`                                | `#c5a5c5` | italic   | `variable.special`    | ✗ | Cobalt Next OVERRIDES the default red with purple (explicit "D-Line Preference Edit" comment). Converter picked the LATER JS-specific rule (#31, red) instead. Should be **purple italic**. |
| 13 | entity.name.method.js             | `entity.name.method.js`                            | `#D8DEE9` | —        | *(none)*              | — | Niche. |
| 14 | meta.method.js                    | `meta.class-method.js entity.name.function.js`, `variable.function.constructor` | `#D8DEE9` | — | *(none)* | — | Niche, but `variable.function.constructor` could theoretically affect `constructor` — converter ignored. |
| 15 | Attributes                        | `entity.other.attribute-name`                      | `#BB80B3` | italic   | `attribute` | ✓ | Purple italic. |
| 16 | Regular Expressions               | `string.regexp`                                    | `#5FB3B3` | —        | `string.regex` | ✗ | **Converter looks for `string.regex`, Cobalt Next uses `string.regexp`. Fallback to plain string gives wrong green. Should be teal.** |
| 17 | Escape Characters                 | `constant.character.escape`                        | `#5FB3B3` | —        | `string.escape` | ✗ | **Converter's StringEscape fallback picks `constant.character` (orange) before finding the escape-specific rule. Should be teal.** |
| 18 | URL                               | `*url*`, `*link*`, `*uri*`                         | `#5FB3B3` | underline | `link_text`, `link_uri` | ✗ | **Glob patterns, converter can't see them. Should be teal underlined — currently red from rule #7.** |
| 19 | Decorators                        | `tag.decorator.js entity.name.tag.js`, `tag.decorator.js punctuation.definition.tag.js` | `#5a9bcf` | italic | *(none; niche JS)* | — | Could be aliased to `attribute` as a stretch, but Cobalt Next gives attributes purple. |
| 20 | ES7 Bind Operator                 | `source.js constant.other.object.key.js string.unquoted.label.js` | `#ed6f7d` | italic | *(none)* | — | Niche. |
| 21 | `[CSS] - Entity Tag Name`          | `entity.name.tag`, `source.css entity.name.tag`, `source.scss entity.name.tag` | `#ed6f7d` | — | (aliased to `tag` or `constructor`) | *(indirect)* | Converter assigned this to `constructor`. That's OK since red constructors don't clash. |
| 22–28 | `[CSS]` per-type rules          | `source.css entity`, `source.css support`, `source.css constant`, `source.css string`, `source.css variable` | various | — | *(none; language-specific)* | — | Zed can't disambiguate by language. Generic scopes already cover these via the base rules. |
| 29 | `[HTML] - *`                      | `text.html.basic entity.name`, `meta.tag.metadata.script.html entity.name.tag.html`, `text.html.basic entity.name.tag` | `#ed6f7d` | — | *(none; redundant with tag)* | — | Already covered by `tag`. |
| 30 | `[JAVASCRIPT] Keyword`            | `source.js keyword`                                | `#5fb3b3` | —        | *(would be `keyword`)* | — | **Conflict: language-agnostic rule says `keyword` is purple (#c5a5c5). This JS-specific rule says teal. Zed has no language scoping, so base rule wins. Purple is right.** |
| 31 | `[JAVASCRIPT] Entity`             | `source.js entity`, `source.js entity.name.tag`    | `#ed6f7d` | — | — | — | — |
| 32 | `[JAVASCRIPT] Punctuation`        | `source.js punctuation`                            | `#5fb3b3` | — | *(already handled by `punctuation`)* | — | — |
| 33 | `[JAVASCRIPT] JSX Text`           | `source.js meta.block`                             | `#d8dee9` | — | — | — | — |
| 34 | `[JAVASCRIPT] Storage Type Function` | `source.js storage.type.function`               | `#c5a5c5` | — | *(part of `keyword`)* | — | — |
| 35 | `[JAVASCRIPT] Variable Language`  | `variable.language`, `entity.name.type.class.js`   | `#ed6f7d` | — | `variable.special` (WRONG) | ✗ | See row 12. Converter picked this over row 12 which has the preference override. |
| 36 | HTML Class Component              | `support.class.component.html`                     | `#ed6f7d` | — | — | — | Dropped in Minimal variant. |
| 37 | `[MARKDOWN] Changed`              | `markup.changed`                                   | `#c5a5c5` | — | — | — | — |
| 38 | `[MARKDOWN] Heading Punctuation`  | `punctuation.definition.heading.markdown`          | `#d8dee9` | — | — | — | Only the `#` itself. |
| 39 | `[MARKDOWN] Heading Name Section` | `entity.name.section.markdown`, `markup.heading.setext.1.markdown`, `markup.heading.setext.2.markdown` | `#c5a5c5` | bold | `title` | ⊘ | **Converter never fills `title`.** Cobalt Next gives purple bold. Danny's override wants H1 cyan; H1/H2 cannot be distinguished in Zed. |
| 40 | `[MARKDOWN] Paragraph`            | `meta.paragraph.markdown`                          | `#d8dee9` | — | — | — | — |
| 41 | `[MARKDOWN] Quote Punctuation`    | `beginning.punctuation.definition.quote.markdown`  | `#5FB3B3` | — | — | — | — |
| 42 | `[MARKDOWN] Quote Paragraph`      | `markup.quote.markdown meta.paragraph.markdown`    | `#5a9bcf` | italic | — | — | Blue italic for blockquotes. No direct Zed token. |
| 43 | `[MARKDOWN] Separator`            | `meta.separator.markdown`                          | `#5FB3B3` | — | — | — | — |
| 44 | `[MARKDOWN] Bold`                 | `markup.bold.markdown`                             | `#5FB3B3` | bold | `emphasis.strong` | ⊘ | **Converter never fills `emphasis.strong`.** Should be teal bold. |
| 45 | `[MARKDOWN] Italic`               | `markup.italic.markdown`                           | `#5a9bcf` | italic | `emphasis` | ⊘ | **Converter never fills `emphasis`.** Should be blue italic. |
| 46 | `[MARKDOWN] Lists`                | `beginning.punctuation.definition.list.markdown`   | `#5FB3B3` | — | `punctuation.list_marker` | (indirect) | Already teal via `punctuation` base. |
| 47 | `[MARKDOWN] Link Title`           | `string.other.link.title.markdown`                 | `#99c794` | — | `link_text` | ⊘→✓ | Should be green (per Cobalt Next's markdown treatment). Converter has it as red from row 7. |
| 48 | `[MARKDOWN] Link/Image Title`     | `string.other.link.title.markdown`, `string.other.link.description.markdown`, `string.other.link.description.title.markdown` | `#99c794` | — | `link_text` | ⊘→✓ | Same as above. |
| 49 | `[MARKDOWN] Link Address`         | `markup.underline.link.markdown`, `markup.underline.link.image.markdown` | `#5a9bcf` | — | `link_uri` | ⊘→✗ | Should be blue. Converter has it as red. |
| 50 | `[MARKDOWN] Inline Code`          | `fenced_code.block.language`, `markup.inline.raw.markdown` | `#eb9a6d` | — | `text.literal` (?) | ⊘→✗ | Converter assigned `text.literal` = `#99C794` via string fallback, not orange. Orange is arguably correct but either works. |
| 51 | `[MARKDOWN] Code Block`           | (same scopes, duplicate rule)                      | `#5a9bcf` | — | — | — | Cobalt Next has two contradictory rules for the same scopes; later one wins in VS Code. |
| 52 | `[TYPESCRIPT] Entity Name Type`   | `source.ts entity.name.type`                       | `#fac863` | — | *(part of `type`)* | — | Already yellow via base rule. |
| 53 | `[TYPESCRIPT] Keyword`            | `source.ts keyword`                                | `#c5a5c5` | — | *(part of `keyword`)* | — | Agrees with base rule — purple. |
| 54 | `[TYPESCRIPT] Punctuation Parameters` | `source.ts punctuation.definition.parameters` | `#5fb3b3` | — | *(part of `punctuation`)* | — | — |
| 55 | `[TYPESCRIPT] Arrow Parameters`   | `meta.arrow.ts punctuation.definition.parameters`  | `#5fb3b3` | — | — | — | — |
| 56–64 | JSON key by depth              | 8 depth-conditional scopes                         | rotates | — | `property` / N/A | ⊘ | **Zed cannot rotate colors by nesting depth. Hard loss. Suggest `property` = `#FAC863` (the level-0 color) since Zed treats JSON keys uniformly.** |
| 65 | Italicsify for Operator Mono      | `modifier`, `this`, `comment`, `storage.modifier.js`, `entity.other.attribute-name.js` | — | italic | *(adds italic to existing rules)* | — | This rule sets no color, only font style. Confirms keyword+attribute italic across languages. |

## Canonical colour palette (distilled)

From the inventory, Cobalt Next's syntax palette:

| Colour       | Hex       | Used for                                                 |
|--------------|-----------|----------------------------------------------------------|
| Slate grey   | `#65737e` | Comments                                                 |
| Off-white    | `#CDD3DE` | Plain variables                                          |
| Purple       | `#c5a5c5` | Keywords, storage, markdown headings, `variable.language` (overridden) |
| Dim purple   | `#BB80B3` | Attribute names                                          |
| Teal         | `#5FB3B3` | Operators, punctuation, URLs, escapes, regex, markdown bold, quote punctuation, separators |
| Blue         | `#5a9bcf` | Functions, markdown italic, markdown quotes, link address, markdown code block |
| Red          | `#ed6f7d` | Tags, JSX entity references                              |
| Orange       | `#eb9a6d` | Numbers, constants, `variable.parameter`, markdown inline code |
| Yellow       | `#fac863` | Classes, types, support                                  |
| Green        | `#99C794` | Strings, symbols, inherited class, markdown link text    |
| Muted fg     | `#d8dee9` | Paragraph text, heading punctuation                      |

## Tokens Zed cannot express at all — accepted losses

- **Per-language colour overrides.** E.g. `source.ts keyword` = purple,
  `source.js keyword` = teal. Zed has no language scoping; one color wins.
  Resolution: take the language-agnostic rule's color (purple), since it
  appears first.
- **JSON key depth rotation.** Zed treats all property-name tokens
  uniformly. Pick one color (yellow — the depth-0 color) for
  `property`.
- **Markdown H1 vs H2 distinction.** Zed's `title` token covers both.
  Pick one color (Danny's H1 cyan `#9cecfb`, per his spec; or Cobalt
  Next's native purple `#c5a5c5` bold if the cyan is disruptive).
- **Italic-only rules** (`Italicsify for Operator Mono`, rule 65). Zed
  applies font style per syntax token, but only one style can be set
  per token, and it applies globally. The italics we set on `keyword`,
  `attribute`, `comment`, `variable.special` already cover the intent.
- **Glob-pattern scopes** (`*url*` `*link*` `*uri*`). The converter's
  name-based matching can't see these.
