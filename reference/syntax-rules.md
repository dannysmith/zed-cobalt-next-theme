# Cobalt Next syntax rules — reference

An inventory of Cobalt Next's VS Code `tokenColors` rules, the distilled canonical palette, and the things Zed's theme model can't express. This is the reference the synthesis script (`build-theme.py`) is built against — when in doubt about why a Zed token got a particular colour, start here.

Source file: [`vscode/CobaltNext.json`](vscode/CobaltNext.json), the `tokenColors` array. The Dark variant has identical `tokenColors`; Minimal only adds one `[HTML] - Custom Tag` rule (yellow) and drops the `HTML Class Component` rule. This inventory covers the main variant.

## Canonical palette

Cobalt Next's 11-colour syntax palette, distilled from the rule inventory below:

| Role         | Hex       | Used for |
|--------------|-----------|----------|
| Slate grey   | `#65737e` | Comments |
| Off-white    | `#CDD3DE` | Plain variables |
| Muted fg     | `#d8dee9` | Paragraph text, heading punctuation |
| Purple       | `#c5a5c5` | Keywords, storage, markdown headings, `variable.language` (overridden to purple from red) |
| Dim purple   | `#BB80B3` | Attribute names |
| Teal         | `#5FB3B3` | Operators, punctuation, URLs, escapes, regex, markdown bold, quote punctuation, separators |
| Blue         | `#5a9bcf` | Functions, markdown italic, markdown quotes, link addresses, markdown code block |
| Red          | `#ed6f7d` | Tags, JSX entity references |
| Orange       | `#eb9a6d` | Numbers, constants, `variable.parameter`, markdown inline code |
| Yellow       | `#fac863` | Classes, types, support |
| Green        | `#99C794` | Strings, symbols, inherited class, markdown link text |

The UI chrome palette (backgrounds, borders, surfaces) is separate and lives in `build-theme.py`'s `PALETTE` dict.

## Rule inventory

The Zed converter operates by reverse-matching its own 40-token syntax set against VS Code scopes, so this inventory is mainly useful for understanding *why* a particular Zed token ends up with a particular colour, and which Cobalt Next rules are lost to the collapse from VS Code's per-language scopes into Zed's language-agnostic model.

"Proposed Zed token" is the closest match from Zed's 40-token set (`attribute`, `boolean`, `comment`, `comment.doc`, `constant`, `constructor`, `embedded`, `emphasis`, `emphasis.strong`, `enum`, `function`, `hint`, `keyword`, `label`, `link_text`, `link_uri`, `number`, `operator`, `predictive`, `preproc`, `primary`, `property`, `punctuation`, `punctuation.bracket`, `punctuation.delimiter`, `punctuation.list_marker`, `punctuation.special`, `string`, `string.escape`, `string.regex`, `string.special`, `string.special.symbol`, `tag`, `text.literal`, `title`, `type`, `variable`, `variable.special`, `variant`). `N/A` = no Zed token fits.

| # | Rule name | VS Code scopes (abbreviated) | Colour | Style | Zed token | Notes |
|---|---|---|---|---|---|---|
| 1 | Comment | `comment`, `punctuation.definition.comment` | `#65737e` | italic | `comment`, `comment.doc` | `comment.doc` resolves via Zed's fallback chain. |
| 2 | Variable | `variable` | `#CDD3DE` | — | `variable` | |
| 3 | Keyword, Storage | `keyword`, `storage.type`, `storage.modifier`, `storage.type.class.js` | `#c5a5c5` | — | `keyword` | |
| 4 | Operator, Misc | `keyword.operator`, `punctuation`, `punctuation.definition.tag`, `punctuation.definition.tag.html`, `keyword.other.template`, `keyword.other.substitution`, `punctuation.section.embedded` | `#5FB3B3` | — | `operator`, `punctuation`, `punctuation.*` | Propagates through Zed's `punctuation.*` subscopes via fallback. |
| 5 | Tag | `entity.name.tag`, `meta.tag.sgml`, `markup.deleted.git_gutter` | `#ed6f7d` | — | `tag` | |
| 6 | Function, Special Method | `entity.name.function`, `meta.function-call`, `variable.function`, `support.function`, `keyword.other.special-method` | `#5a9bcf` | — | `function` | |
| 7 | Other Variable, String Link | `support.other.variable`, `string.other.link` | `#ed6f7d` | — | *(niche)* | A TextMate-era scope. The converter mistakenly grafts this onto `link_text`/`link_uri`; hand-fixed in `build-theme.py`. |
| 8 | Number, Constant, Parameter, Embedded | `constant.numeric`, `constant.language`, `support.constant`, `constant.character`, `variable.parameter`, `keyword.other.unit` | `#eb9a6d` | — | `number`, `boolean`, `constant`, `variable.parameter` | `boolean` resolves via `constant.language`. `variable.parameter` is its own Zed token and needs manual fill. |
| 9 | String, Symbols, Inherited Class, Markup Heading | `string`, `constant.other.symbol`, `constant.other.key`, `entity.other.inherited-class`, `markup.heading` | `#99C794` | — | `string`, `string.special`, `string.special.symbol`, `text.literal` | String fallback cascades through all `string.*` subscopes. |
| 10 | Class, Support | `entity.name.class`, `entity.name.type.class`, `support.type`, `support.class`, `markup.changed.git_gutter` | `#FAC863` | — | `type` | |
| 11 | Sub-methods | `entity.name.module.js`, `variable.import.parameter.js`, `variable.other.class.js` | `#ed6f7d` | — | N/A | Language-specific, no direct Zed target. |
| 12 | Variable Language | `variable.language` | `#c5a5c5` | italic | `variable.special` | Cobalt Next's author explicitly overrides the default red with purple here ("D-Line Preference Edit" comment in the source). Rule 35 then re-assigns the same scope to red for JS; rule 12 is the intended winner. |
| 13 | `entity.name.method.js` | `entity.name.method.js` | `#D8DEE9` | — | N/A | Niche. |
| 14 | `meta.method.js` | `meta.class-method.js entity.name.function.js`, `variable.function.constructor` | `#D8DEE9` | — | N/A | Niche; `variable.function.constructor` would theoretically touch `constructor` but the converter doesn't look there. |
| 15 | Attributes | `entity.other.attribute-name` | `#BB80B3` | italic | `attribute` | |
| 16 | Regular Expressions | `string.regexp` | `#5FB3B3` | — | `string.regex` | Converter looks for `string.regex`, Cobalt Next uses `string.regexp` (extra `p`). Fallback to plain string gives wrong green. Hand-fixed in `build-theme.py`. |
| 17 | Escape Characters | `constant.character.escape` | `#5FB3B3` | — | `string.escape` | Converter's `StringEscape` fallback picks `constant.character` (orange) before finding the escape-specific rule. Hand-fixed. |
| 18 | URL | `*url*`, `*link*`, `*uri*` | `#5FB3B3` | underline | `link_text`, `link_uri` | Glob patterns — the converter's name-based matching can't see them. Links are hand-fixed to green/blue from the markdown-specific rules (47, 49) rather than teal. |
| 19 | Decorators | `tag.decorator.js entity.name.tag.js`, `tag.decorator.js punctuation.definition.tag.js` | `#5a9bcf` | italic | N/A | Niche JS. |
| 20 | ES7 Bind Operator | `source.js constant.other.object.key.js string.unquoted.label.js` | `#ed6f7d` | italic | N/A | Niche. |
| 21 | `[CSS] - Entity Tag Name` | `entity.name.tag`, `source.css entity.name.tag`, `source.scss entity.name.tag` | `#ed6f7d` | — | *(indirect)* | The converter incidentally routes this to `constructor`; hand-fixed to yellow to match `type` since constructors are type-like. |
| 22–28 | `[CSS]` per-type rules | `source.css entity`, `source.css support`, `source.css constant`, `source.css string`, `source.css variable` | various | — | N/A | Zed can't disambiguate by language. Generic scopes (rules 3/4/9/10 etc.) already cover these. |
| 29 | `[HTML] - *` | `text.html.basic entity.name`, `meta.tag.metadata.script.html entity.name.tag.html`, `text.html.basic entity.name.tag` | `#ed6f7d` | — | N/A | Redundant with rule 5 (`tag`). |
| 30 | `[JAVASCRIPT] Keyword` | `source.js keyword` | `#5fb3b3` | — | *(base `keyword` wins)* | Conflict: language-agnostic rule 3 says `keyword` is purple, this JS-specific rule says teal. Zed has no language scoping, so base rule wins. Purple is right. |
| 31 | `[JAVASCRIPT] Entity` | `source.js entity`, `source.js entity.name.tag` | `#ed6f7d` | — | N/A | |
| 32 | `[JAVASCRIPT] Punctuation` | `source.js punctuation` | `#5fb3b3` | — | *(part of `punctuation`)* | |
| 33 | `[JAVASCRIPT] JSX Text` | `source.js meta.block` | `#d8dee9` | — | N/A | Used as the colour hint for `embedded`. |
| 34 | `[JAVASCRIPT] Storage Type Function` | `source.js storage.type.function` | `#c5a5c5` | — | *(part of `keyword`)* | |
| 35 | `[JAVASCRIPT] Variable Language` | `variable.language`, `entity.name.type.class.js` | `#ed6f7d` | — | (superseded by rule 12) | See rule 12. The converter picks this over rule 12; the synthesis forces rule 12's purple italic. |
| 36 | HTML Class Component | `support.class.component.html` | `#ed6f7d` | — | N/A | Dropped in Minimal variant. |
| 37 | `[MARKDOWN] Changed` | `markup.changed` | `#c5a5c5` | — | N/A | |
| 38 | `[MARKDOWN] Heading Punctuation` | `punctuation.definition.heading.markdown` | `#d8dee9` | — | N/A | Only the `#` itself. |
| 39 | `[MARKDOWN] Heading Name Section` | `entity.name.section.markdown`, `markup.heading.setext.1.markdown`, `markup.heading.setext.2.markdown` | `#c5a5c5` | bold | `title` | Cobalt Next's native heading colour is purple bold; the Zed port overrides `title` to magenta `#e255a1` bold — see `notes.md`. |
| 40 | `[MARKDOWN] Paragraph` | `meta.paragraph.markdown` | `#d8dee9` | — | N/A | |
| 41 | `[MARKDOWN] Quote Punctuation` | `beginning.punctuation.definition.quote.markdown` | `#5FB3B3` | — | N/A | |
| 42 | `[MARKDOWN] Quote Paragraph` | `markup.quote.markdown meta.paragraph.markdown` | `#5a9bcf` | italic | N/A | Blue italic for blockquotes; no direct Zed token. |
| 43 | `[MARKDOWN] Separator` | `meta.separator.markdown` | `#5FB3B3` | — | N/A | |
| 44 | `[MARKDOWN] Bold` | `markup.bold.markdown` | `#5FB3B3` | bold | `emphasis.strong` | Hand-filled (converter leaves `emphasis.strong` empty). |
| 45 | `[MARKDOWN] Italic` | `markup.italic.markdown` | `#5a9bcf` | italic | `emphasis` | Hand-filled. |
| 46 | `[MARKDOWN] Lists` | `beginning.punctuation.definition.list.markdown` | `#5FB3B3` | — | `punctuation.list_marker` | Already teal via `punctuation` base. |
| 47 | `[MARKDOWN] Link Title` | `string.other.link.title.markdown` | `#99c794` | — | `link_text` | Hand-fixed — converter put `link_text` at red from rule 7. |
| 48 | `[MARKDOWN] Link/Image Title` | `string.other.link.title.markdown`, `string.other.link.description.markdown`, `string.other.link.description.title.markdown` | `#99c794` | — | `link_text` | Same as 47. |
| 49 | `[MARKDOWN] Link Address` | `markup.underline.link.markdown`, `markup.underline.link.image.markdown` | `#5a9bcf` | — | `link_uri` | Hand-fixed — converter had this as red. |
| 50 | `[MARKDOWN] Inline Code` | `fenced_code.block.language`, `markup.inline.raw.markdown` | `#eb9a6d` | — | `text.literal` | Orange is the intended colour but the port keeps the converter's green via the string fallback — both are defensible; green is cheaper. |
| 51 | `[MARKDOWN] Code Block` | (same scopes, duplicate rule) | `#5a9bcf` | — | N/A | Cobalt Next has two contradictory rules for the same scopes; the later one wins in VS Code. |
| 52 | `[TYPESCRIPT] Entity Name Type` | `source.ts entity.name.type` | `#fac863` | — | *(part of `type`)* | |
| 53 | `[TYPESCRIPT] Keyword` | `source.ts keyword` | `#c5a5c5` | — | *(part of `keyword`)* | |
| 54 | `[TYPESCRIPT] Punctuation Parameters` | `source.ts punctuation.definition.parameters` | `#5fb3b3` | — | *(part of `punctuation`)* | |
| 55 | `[TYPESCRIPT] Arrow Parameters` | `meta.arrow.ts punctuation.definition.parameters` | `#5fb3b3` | — | N/A | |
| 56–64 | JSON key by depth | 8 depth-conditional scopes | rotates | — | `property.json_key` | Zed can't rotate colours by nesting depth. The port pins `property.json_key` to yellow (the depth-0 colour) since Zed treats JSON keys uniformly. |
| 65 | Italicsify for Operator Mono | `modifier`, `this`, `comment`, `storage.modifier.js`, `entity.other.attribute-name.js` | — | italic | *(adds italic to existing rules)* | Sets only font style. Intent already captured by the italic on `keyword`, `attribute`, `comment`, `variable.special`. |

## Accepted losses

Things Zed's theme model can't replicate, and how the port settles them:

- **Per-language colour overrides.** Cobalt Next occasionally uses `source.ts keyword` or `source.js keyword` to vary a base colour per language. Zed has no language scoping in its theme model — one colour per token, full stop. Resolution: always take the language-agnostic rule's colour (the one without a `source.*` prefix).

- **JSON key depth rotation.** Cobalt Next rotates through 8 colours for JSON keys by nesting depth. Zed treats all JSON keys uniformly via `@property.json_key`. Resolution: pin `property.json_key` to the depth-0 colour (yellow).

- **Markdown H1 vs H2 distinction.** Zed's `title` syntax token covers both — it's a single token for "title-like things". Resolution: pick one colour for `title`; the port uses magenta `#e255a1` bold per user preference (see `notes.md`).

- **Italic-only rules.** Cobalt Next's `Italicsify for Operator Mono` rule sets italics without a colour. Zed applies font style per token and can't layer-italic a set of scopes atop their base colour. Resolution: the italics we set on `keyword`, `attribute`, `comment`, `variable.special` already cover the rule's intent.

- **Glob-pattern scopes** (`*url*`, `*link*`, `*uri*`). The converter's name-based matching can't see glob patterns. Resolution: the port explicitly sets `link_text` and `link_uri` from the markdown-specific rules (47, 49) instead.

- **`property` can't split YAML from TS field access from CSS property names.** All three tree-sitter grammars tag these as bare `@property`. The port optimises for YAML by setting `property` to red, which means TS/Rust/Go bare field access (non-call) also becomes red. Method calls (`@function.method`) are unaffected. See `notes.md` for the trade-off rationale.
