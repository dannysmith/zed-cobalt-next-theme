# Port notes — Cobalt Next for Zed

Evergreen notes on why the port is shaped the way it is: how Zed's theme system works, how the Zed converter reads VS Code themes, specific decisions the port makes, and the things that were initially confusing enough to be worth writing down.

## Cobalt Next is Oceanic Next palette + Cobalt2 philosophy

The name "Cobalt Next" suggests a variant of Cobalt2, but its actual colour palette is Oceanic Next almost verbatim:

| Role         | Cobalt Next | Cobalt2     | Source       |
|--------------|-------------|-------------|--------------|
| Editor bg    | `#1b2b34`   | `#193549`   | Oceanic Next |
| Sidebar bg   | `#0f1c23`   | `#15232d`   | Oceanic Next |
| Surface      | `#343d46`   | `#234E6D`   | Oceanic Next |
| Foreground   | `#d8dee9`   | `#ffffff`   | Oceanic Next |
| Yellow       | `#fac863`   | `#ffc600`   | Oceanic Next |
| Teal / cyan  | `#5fb3b3`   | `#80fcff`   | Oceanic Next |
| Red          | `#ed6f7d`   | `#ff628c`   | Oceanic Next |
| Green        | `#99c794`   | `#3ad900`   | Oceanic Next |
| Purple       | `#c5a5c5`   | `#fb94ff`   | Oceanic Next |
| Orange       | `#eb9a6d`   | `#ff9d00`   | Oceanic Next |
| Blue         | `#5a9bcf`   | `#0088ff`   | Oceanic Next |

The "Cobalt" in the name refers to the *philosophy* — italic comments, italic language variables, angry-red tags, yellow classes, blue functions, the general colour choices for which concepts get which treatment. It's not a shared palette.

**Implication for the port:** the Zed port has to treat Cobalt Next as its own thing, not as a variant of anything else. In particular, the `wesbos/cobalt2-zed` extension is not a useful reference for syntax colours — see below.

## `wesbos/cobalt2-zed` is a Dracula reskin

Before writing this port from scratch we considered using `wesbos/cobalt2-zed` as a translation reference, on the theory that "if someone hand-ported Cobalt2 to Zed already, their translation choices are a good starting point for Cobalt Next". They aren't. That repo is:

- Authored by "MD. MOHIBUR RAHMAN", not Wes Bos
- LICENSE header says `Copyright (c) 2023 Dracula Theme`
- Contains the full Cobalt2 UI palette (`#193549` bg, `#ffc600` yellow, etc.) — so the `style` block is real Cobalt2
- …but the `syntax` block is literal Dracula colours: `#ff79c6` (Dracula pink) for booleans, `#bd93f9` (Dracula purple) for numbers, `#f8f8f2` (Dracula foreground) for embedded, `#ff5555` (Dracula red) for regex, `#8be9fd` (Dracula cyan) for URIs, etc.

Total git history of that repo: 5 commits, last one being "update syntax highlighting". It's "Cobalt2 UI chrome bolted onto a Dracula syntax theme", not a thoughtful hand-port. The only useful thing to take from it is the UI-block structure as a sanity check for Zed's key layout.

## How the Zed converter works

Zed ships a CLI at `crates/theme_importer` in the `zed-industries/zed` source tree. It's a VS Code → Zed theme converter. Understanding what it does and doesn't do is the single highest-leverage piece of context for understanding the hand-polish in `build-theme.py`.

### UI colour mapping

For each Zed UI key, the converter has a hard-coded lookup into VS Code's scheme — e.g. Zed's `editor.background` comes from VS Code's `editor.background`, Zed's `surface.background` comes from VS Code's `panel.background`, Zed's `border` comes from VS Code's `panel.border`, and so on. The mapping lives in `crates/theme_importer/src/vscode/converter.rs`.

This is mostly good, with two gotchas the port has to work around:

1. **`panel.background` vs `sideBar.background`.** The converter reads sidebar/surface backgrounds from VS Code's `panel.background`, which Cobalt Next sets to the editor background `#1b2b34`. But Cobalt Next's actual sidebar uses a separate `sideBar.background: #0f1c23` (darker). The port manually overrides `panel.background` and `surface.background` to `#0f1c23` to match. Terminal has its own `terminal.background` key and is unaffected.

2. **`border` vs `panel.border`.** The converter maps `border`, `border.variant`, `border.selected`, `border.transparent`, `border.disabled`, and `pane_group.border` all to VS Code's `panel.border`, which Cobalt Next sets to teal `#5fb3b3`. In VS Code this only shows up on a couple of narrow surfaces (panel separator, active tab underline). In Zed, `border` is the *ubiquitous* divider between every pane, sidebar, tab bar, and title bar. The result is a teal line around everything. The port overrides those keys to dark `#0b151b` (matching VS Code's `tab.border`) and reserves teal for `border.selected` only.

### Syntax token mapping

The converter uses a *reverse* weighted match. Zed's 40-token syntax set is fixed; for each Zed token, the converter has an ordered list of VS Code scopes that ought to correspond to it (e.g. `Function` → `["entity.function", "entity.name.function", "variable.function"]`). It scans the input theme's `tokenColors` for the rule that best matches the scope list, with earlier entries weighted higher, and takes that rule's colour.

Consequences:

- **One colour per Zed token.** Cobalt Next's per-language scope rules (`source.ts entity.name.type`, the JSON-key-by-depth rules, `[MARKDOWN] Heading Name Section`, etc.) don't survive. They're collapsed into whichever generic Zed token they resemble most.
- **Fallback chains.** If no scope matches directly, the converter has a fallback map: `Number → Constant`, `CommentDoc → Comment`, `Punctuation.* → Punctuation`, `String.* → String`. This is why setting one of `constant` / `comment` / `punctuation` / `string` tends to propagate automatically — but also why `string.escape` and `string.regex` silently inherit wrong colours when Cobalt Next uses unusual scope names (`constant.character.escape` and `string.regexp` respectively).
- **Warnings.** `--warn-on-missing` prints a line to stderr for every Zed token the converter couldn't fill. For Cobalt Next the list is `embedded`, `emphasis`, `emphasis.strong`, `enum`, `hint`, `label`, `predictive`, `preproc`, `primary`, `property`, `title`, `variant`. The port fills the ones that have a semantic match in Cobalt Next and leaves `hint` / `predictive` / `primary` intentionally empty.

## Zed's theme schema and syntax token set

The port targets schema `v0.2.0` (`https://zed.dev/schema/themes/v0.2.0.json`). There is no `v0.3.0` at time of writing; `v0.1.0` is the legacy schema used by e.g. `wesbos/cobalt2-zed` and has a slightly different key set (legacy status keys like `info`, `success`, `unreachable`, `predictive`, `renamed` are UI status colours in v0.1.0 but become syntax tokens or disappear in v0.2.0).

The 40-token syntax set Zed's converter recognises:

```
attribute, boolean, comment, comment.doc, constant, constructor,
embedded, emphasis, emphasis.strong, enum, function, hint, keyword,
label, link_text, link_uri, number, operator, predictive, preproc,
primary, property, punctuation, punctuation.bracket,
punctuation.delimiter, punctuation.list_marker, punctuation.special,
string, string.escape, string.regex, string.special,
string.special.symbol, tag, text.literal, title, type, variable,
variable.special, variant
```

A Zed theme's `syntax` object can also contain arbitrary dot-notation tokens beyond these 40 — Zed's resolver walks dot prefixes from most specific to least specific and picks the first match. See the next section.

## Dot-prefix resolution and tree-sitter scopes

Zed's `SyntaxTheme::highlight_id` (`crates/syntax_theme/src/syntax_theme.rs`) walks dot-separated prefixes of a tree-sitter capture name and picks the most specific matching theme entry. So if the theme has:

```json
"property": "#ed6f7d",
"property.json_key": "#fac863"
```

then a tree-sitter capture of `@property` matches `property` (red), and `@property.json_key` matches `property.json_key` (yellow, because it's more specific).

This matters for the one token the port fights with: `property`. Different languages' tree-sitter grammars tag conceptually different things as `@property`:

| Language | Tagged as | Example |
|---|---|---|
| JSON | `@property.json_key` | `"foo":` |
| YAML | `@property` (bare) | `foo:` |
| TS/JS plain field access | `@property` (bare) | `obj.foo` |
| TS/JS method call | `@function.method` | `obj.foo()` |
| TS/JS object literal key / labeled statement | `@property.name` | `{foo: 1}` |
| CSS property name | `@property` (bare) | `color:` |
| Rust / Go / Python / C / C++ struct or class field | `@property` (bare) | `obj.foo` |

In Cobalt Next's VS Code rules, these live at very different colours — YAML keys are red (matched by `entity.name.tag.yaml`), CSS property names are yellow (matched by `support.type.property-name`), TS plain field access is white (falls through to `variable`), JSON keys rotate by depth. In Zed, `@property` (bare) has to be *one* colour.

**The port picks red.** That matches YAML (the user's explicit priority) and CSS loses a small amount of fidelity (yellow → red). TS/Rust/Go/Python/C/C++ *bare* field access becomes red, but method calls (which are the overwhelming majority of dotted accesses in real code) are unaffected because they're tagged `@function.method`. The subscopes `property.name` and `property.json_key` override the bare `property` back to yellow for TS object literal keys and JSON keys respectively.

Full table of what each choice would cost:

| `property` colour | TS `foo.bar` | TS obj literal keys | YAML keys | CSS property names | JSON keys |
|---|---|---|---|---|---|
| white `#CDD3DE` | right | right | wrong (want red) | wrong (want yellow) | right via subscope |
| yellow `#fac863` | wrong | right | wrong (want red) | right | right via subscope |
| **red `#ed6f7d` (chosen)** | wrong | right (via `property.name`) | **right** | wrong (want yellow) | right via subscope |

## Port-specific decisions

### Markdown heading colour — magenta, not cyan, not purple

Cobalt Next's native rule for `entity.name.section.markdown` (heading) is purple `#c5a5c5` bold. The user maintains a VS Code `editor.tokenColorCustomizations` override that splits H1 cyan `#9cecfb` and H2 magenta `#e255a1`. Zed's `title` syntax token doesn't distinguish H1 from H2 — it's a single token. The port picks **H2 magenta `#e255a1` bold** per the user's preference. If the magenta is ever too disruptive, swap to cyan (H1) or revert to Cobalt Next's native purple.

### Constructor colour — yellow, not red

The converter incidentally routes `constructor` to the `[CSS] - Entity Tag Name` rule (red) because that rule's scope list contains `entity.name.tag`. The port overrides `constructor` to yellow `#FAC863` to match `type` — constructors in Rust/TS/Python are type-like things being invoked (`Some(x)`, `new ClassName()`), not function-like things.

### Three variants ship as one family

Cobalt Next offers three variants in VS Code: main, Dark (darker editor background with teal-tinted selections), and Minimal (as Dark with a lower-contrast tab bar). The Zed port ships all three as a single theme family with three entries. Switching is via Zed's theme selector — no cost to keeping them all.

The syntax block is identical across all three variants; they only differ in UI chrome. The build script applies the same `apply_fixes` pass to each variant independently.

### Player palette and accents

The Zed converter leaves `players` and `accents` empty by default. The port populates both from the syntax palette for visual consistency: player 0 is the local cursor (yellow `#fac863`, matching Cobalt Next's `editorCursor.foreground`) with a slate-grey selection; remaining players rotate through teal / green / purple / red / blue / orange for multi-cursor or collaborative editing.

### Intentionally empty syntax tokens

`hint`, `predictive`, and `primary` are left unset. The Zed converter source has no VS Code scope mapping for these, and no rule in Cobalt Next fits semantically. `hint` status colour (the UI-level one, for inlay hints) is set separately to `#65737e` (the palette's muted-foreground grey).

## Licence

- **Cobalt Next** — MIT, Copyright (c) 2017 David Leininger. The upstream licence lives at [`vscode/LICENSE`](vscode/LICENSE). MIT requires attribution preservation; the port credits David Leininger in `extension.toml`, the repo README, and the Zed theme family's `author` field.
- **Zed port** — MIT, Danny Smith. No constraints beyond standard MIT.
- **Zed `theme_importer`** — GPL (part of the Zed source tree). Used as a build-time CLI tool; its JSON output is data, not a derivative work, and nothing from the Zed tree ships in the final theme.
