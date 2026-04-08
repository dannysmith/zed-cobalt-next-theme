# Approach C — Converter output notes

## What was run

```bash
./source/zed-theme-importer/target/debug/theme_importer \
  --warn-on-missing \
  -o approach-c-output.json \
  source/cobaltnext-vscode/themes/CobaltNext.json \
  2> approach-c-warnings.txt
```

Same for `CobaltNext-Dark.json` → `approach-c-output-dark.json` and
`CobaltNext-Minimal.json` → `approach-c-output-minimal.json`.

All three runs exited cleanly (exit 0). Output files are 4.5–4.6 KB
each. Warnings file is ~3 KB.

The three converter outputs were then wrapped into a single Zed
theme-family file `approach-c-family.json` (using `jq` to add
`$schema`, `author`, `name`, and the `themes` array), and copied to
`~/.config/zed/themes/cobalt-next.json` for live testing.

## What the converter got right

### UI chrome — basically perfect

The converter produces 75 populated UI keys. The key Cobalt Next
colors all land in the right slots:

- `background`, `editor.background`, `panel.background`, `terminal.background`,
  etc. all get `#1b2b34` (slate)
- `surface.background`, `tab.active_background`, `editor.active_line.background`
  all get `#343d46` (mid-slate surface)
- `editor.foreground` = `#fff`, `text` = `#d8dee9`
- All ANSI terminal colors map 1:1 from `terminal.ansi*` keys
- Scrollbar, gutter, tab bar, status bar, sidebar all populate from
  the right VS Code keys

The converter's UI mapping logic in
`zed-theme-importer/crates/theme_importer/src/vscode/converter.rs`
is well-tested for VS Code themes that follow the standard schema,
which Cobalt Next does.

### Syntax — most token mappings are right

Of the 27 syntax tokens the converter populated, 18 are correct:

| Token                  | Got       | Source rule |
|------------------------|-----------|-------------|
| `attribute`            | `#BB80B3` italic | "Attributes" |
| `comment`              | `#65737e` italic | "Comment" |
| `comment.doc`          | `#65737e` italic | (fallback to comment) |
| `keyword`              | `#c5a5c5` | "Keyword, Storage" |
| `function`             | `#5a9bcf` | "Function, Special Method" |
| `tag`                  | `#ed6f7d` | "Tag" |
| `type`                 | `#FAC863` | "Class, Support" |
| `variable`             | `#CDD3DE` | "Variable" |
| `string`, `string.special`, `string.special.symbol`, `text.literal` | `#99C794` | "String, Symbols, Inherited Class, Markup Heading" |
| `boolean`, `constant`, `number` | `#eb9a6d` | "Number, Constant, Function Argument..." |
| `operator`, `punctuation`, `punctuation.bracket`, `punctuation.delimiter`, `punctuation.list_marker`, `punctuation.special` | `#5FB3B3` | "Operator, Misc" |
| `constructor` | `#ed6f7d` | "[CSS] - Entity Tag Name" — coincidentally OK |

## What the converter got wrong

5 tokens have wrong colors. Full table in
`approach-a-phase2-worklist.md`. Summary:

| Token              | Got               | Should be             | Cause |
|--------------------|-------------------|------------------------|-------|
| `string.regex`     | green (string fallback) | teal `#5FB3B3`     | Cobalt Next uses `string.regexp`, converter looks for `string.regex` |
| `string.escape`    | orange `#eb9a6d`  | teal `#5FB3B3`        | Converter's StringEscape fallback hits `constant.character` first |
| `link_text`        | red `#ed6f7d`     | green `#99c794` (or teal) | Converter matched niche `string.other.link` instead of glob URL rule |
| `link_uri`         | red `#ed6f7d`     | blue `#5a9bcf`        | Same — Cobalt Next uses `markup.underline.link.markdown` |
| `variable.special` | red `#ed6f7d`     | purple `#c5a5c5` italic | Converter picked the JS-specific rule over the override |

## What the converter missed entirely (12 unfilled syntax tokens)

From `approach-c-warnings.txt`:

```
embedded, emphasis, emphasis.strong, enum, hint, label, predictive,
preproc, primary, property, title, variant
```

Of these, `hint`, `predictive`, and `primary` are intentionally empty
in the converter source (no scope mapping). The other 9 need manual
fills — see Phase 2 worklist for proposed values.

## Distance from the pass/fail bar

Holding the output up against the criteria from `plan.md`:

- ✓ Background, foreground, accent colours match (UI chrome perfect)
- ✗ Syntax highlighting in `.ts`/`.js` looks visually consistent —
  **needs the 5 wrong-token fixes**, especially `variable.special`
  (every `this`/`self`/etc. shows as red instead of italic purple) and
  the link/escape/regex teal-vs-other issues
- ✓ Cobalt Next palette family is recognisable (slate background,
  Oceanic accents)
- ✗ No glaring errors — the wrong `variable.special` is glaring in
  almost any JS/TS file. Also no markdown headings (`title` empty).

**Estimated visual fidelity** (without screenshots, will refine after
side-by-side test): **~75–80%**. The UI is at 95%+, the syntax is at
~65% (most colors right but the wrong ones are conspicuous).

A focused Phase 2 hand-polish — applying the 5 fixes + 9 fills + 4 UI
tweaks from the worklist — should get this to 90%+ in well under an
hour of editing.

## Files produced

| File                                 | Purpose |
|--------------------------------------|---------|
| `approach-c-output.json`             | Main variant, single theme |
| `approach-c-output-dark.json`        | Dark variant, single theme |
| `approach-c-output-minimal.json`     | Minimal variant, single theme |
| `approach-c-warnings.txt`            | Converter stderr (matches + warnings) |
| `approach-c-warnings-dark.txt`       | (same shape) |
| `approach-c-warnings-minimal.txt`    | (same shape) |
| `approach-c-family.json`             | All three wrapped as a Zed theme family — copied to `~/.config/zed/themes/cobalt-next.json` |
