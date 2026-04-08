# Approach A — Phase 2 worklist

This is the concrete to-do list for Phase 2 hand-polish: every place
the converter (Approach C) and the Cobalt Next inventory (Approach A)
disagree, plus the unfilled tokens.

Source theme: `approach-c-output.json` (and the Dark/Minimal variants
have identical syntax blocks). Target: a final `cobalt-next.json` Zed
theme family.

## Wrong syntax token colours (must fix)

| Token              | Approach C value         | Should be              | Why |
|--------------------|--------------------------|------------------------|-----|
| `string.regex`     | `#99C794` (green)        | `#5FB3B3` (teal)       | Cobalt Next uses `string.regexp` (extra `p`); converter looks for `string.regex` and falls back to `string`. |
| `string.escape`    | `#eb9a6d` (orange)       | `#5FB3B3` (teal)       | Converter's StringEscape fallback hits `constant.character` first. |
| `link_text`        | `#ed6f7d` (red)          | `#99c794` (green)*     | Converter matched the niche `string.other.link` rule. Cobalt Next colors actual link text green via the markdown link-title rule. * For non-markdown link text, teal `#5FB3B3` (the URL glob rule) is also defensible. Pick green for consistency with markdown semantics. |
| `link_uri`         | `#ed6f7d` (red)          | `#5a9bcf` (blue)       | Markdown `markup.underline.link.markdown` rule. |
| `variable.special` | `#ed6f7d` (red)          | `#c5a5c5` italic (purple) | Cobalt Next has an explicit "D-Line Preference Edit" override on `variable.language` to purple italic; converter picked the JS-specific red rule instead. |

## Missing syntax tokens (must add)

| Token             | Add value                  | Source rule |
|-------------------|----------------------------|-------------|
| `emphasis`        | `#5a9bcf` italic           | `[MARKDOWN] Italic` |
| `emphasis.strong` | `#5FB3B3` bold             | `[MARKDOWN] Bold` |
| `title`           | `#9cecfb` bold *(or `#c5a5c5` bold for native)* | `[MARKDOWN] Heading Name Section`. Use `#9cecfb` to honour Danny's H1 override; H2 cannot be distinguished and will share the cyan. |
| `property`        | `#FAC863` (yellow)         | JSON key level-0 colour, also closest to "object property" in the source. |
| `variable.parameter` | `#eb9a6d` italic        | `Number, Constant, Function Argument, Tag Attribute, Embedded` rule (orange) — cf. Cobalt Next applies italic to `variable.parameter` via the Italicsify rule. |
| `embedded`        | `#d8dee9` (foreground)     | `[JAVASCRIPT] JSX Text` rule (`source.js meta.block`). |
| `enum`            | `#FAC863` (yellow)         | Falls under classes/types in Cobalt Next's mental model. |
| `label`           | `#5a9bcf` (blue)           | Closest analogue to function-like identifiers. |
| `preproc`         | `#c5a5c5` (purple)         | Treat as keyword-adjacent. |
| `variant`         | `#FAC863` (yellow)         | Treat as enum-adjacent. |

## Intentionally left empty

- `hint` — converter has no scope mapping for this; UI status colour
  `hint: #969696ff` already exists in `style`. Leaving syntax `hint`
  unset.
- `predictive` — same; not part of the source theme's vocabulary.
- `primary` — not part of the source theme's vocabulary.

## Missing UI keys to verify

The converter populated 64 of the ~150 possible Zed UI keys. Most
unfilled keys are because Cobalt Next doesn't define them, and that's
fine — they fall back to Zed defaults. Worth checking after install:

- `border.focused` got `#343d46` (a surface colour) — should perhaps be
  `#5fb3b3` (focus accent). Check whether focus rings look right.
- `accents` is empty `[]`. Cobalt Next doesn't define multi-cursor
  player palette. Suggest filling with the syntax palette
  (`[#5fb3b3, #fac863, #ed6f7d, #99c794, #c5a5c5, #5a9bcf, #eb9a6d]`)
  for visual consistency.
- `players` is empty `[]`. Suggest at least one entry with
  `cursor: #fac863, selection: #4f5b6680, background: #fac863`.
- Conflict status colour got `#c5a5c5` (purple) from
  `gitDecoration.conflictingResourceForeground`. Looks fine.
- `editor.indent_guide` and `editor.indent_guide_active` not set.
  Cobalt Next defines `editorIndentGuide.background: #343d46` and
  `editorIndentGuide.activeBackground: #65737e`. The converter ignored
  these — add them manually.

## Order of operations for Phase 2

1. Drop the converter family file (`approach-c-family.json`) into the
   Phase 2 working file `cobalt-next.json`.
2. Apply the 5 wrong-token fixes.
3. Apply the 10 missing-token additions.
4. Apply the UI tweaks (focused border, indent guides, accents,
   players).
5. Live-test in Zed; iterate.
