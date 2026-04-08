# Phase 0 — Pre-flight findings

**Decision: GO** — with two important model corrections that change the
shape of Phase 1.

---

## 0.1 Cobalt Next source availability — ✅

Three independent sources, all containing the same JSON:

1. **Upstream repo:** `https://github.com/davidleininger/cobaltnext-vscode`
   (linked from the marketplace `package.json`). Cloned to
   `source/cobaltnext-vscode/`.
2. **Local extension install:** `~/.vscode/extensions/dline.cobaltnext-0.4.5/themes/`
   (already on disk).
3. **Marketplace:** publicly downloadable as `.vsix`.

The extension ships **three variants** (all `vs-dark`):
- `CobaltNext.json` — main, 965 lines
- `CobaltNext-Dark.json` — 969 lines, differs slightly
- `CobaltNext-Minimal.json` — 974 lines, differs slightly

For the port we use `CobaltNext.json` as canonical (matches Danny's active
selection in VS Code per his spec doc). The other variants can be
revisited if Danny wants to ship multiple flavours.

## 0.2 Cobalt Next licence — ✅ MIT

`LICENSE.txt`: **MIT, Copyright (c) 2017 David Leininger**.

Free to derive and republish with attribution. Phase 4 (publish as
extension) is unblocked from a licensing standpoint. A courtesy heads-up
to David Leininger before submitting upstream is still polite, not
required.

## 0.3 Cobalt2 access — ✅ both repos cloned, both MIT

- `source/cobalt2-vscode/` — `wesbos/cobalt2-vscode`, MIT (Wes Bos & Roberto Achar, 2018).
  Theme JSON is at `theme/cobalt2.json` (note: `theme`, singular).
- `source/cobalt2-zed/` — `wesbos/cobalt2-zed`, full history kept (5 commits).
  LICENSE header oddly says "Copyright (c) 2023 Dracula Theme" but is MIT.

## 0.4 Zed `theme_importer` builds — ✅

- Cloned `zed-industries/zed` (`--depth 1 --filter=blob:none --sparse`,
  but had to disable sparse mode because workspace `Cargo.toml`
  references `tooling/perf` and other crates outside `crates/`).
- Working tree is ~106 MB after disabling sparse.
- `cargo build -p theme_importer` — clean build, **5m30s**, no errors.
- `target/debug/theme_importer --help` works as expected.
- CLI: `theme_importer [--warn-on-missing] [-o output] <input>`.
- Note: `theme_importer` itself is GPL'd (the rest of the Zed source
  tree). Using it as a CLI tool is fine; the JSON it outputs is data,
  not a derivative work in any meaningful sense.

---

## Two model corrections that matter for Phase 1

### Correction 1: Cobalt Next is Oceanic Next + Cobalt2 *philosophy*, not Cobalt2 + tweaks

The plan's mental model was "Cobalt Next is mostly Cobalt2 with some
Oceanic Next influences". After reading `CobaltNext.json`, this is
backwards. Cobalt Next's actual palette:

| Role            | Cobalt Next      | Cobalt2          | Source       |
|-----------------|------------------|------------------|--------------|
| Editor bg       | `#1b2b34`        | `#193549`        | Oceanic Next |
| Sidebar bg      | `#0f1c23`        | `#15232d`        | Oceanic Next |
| Surface         | `#343d46`        | `#234E6D`        | Oceanic Next |
| Foreground      | `#d8dee9`        | `#ffffff`        | Oceanic Next |
| Cursor / yellow | `#fac863`        | `#ffc600`        | Oceanic Next |
| Cyan / teal     | `#5fb3b3`        | `#80fcff`        | Oceanic Next |
| Red             | `#ed6f7d`        | `#ff628c`        | Oceanic Next |
| Green           | `#99c794`        | `#3ad900`        | Oceanic Next |
| Purple          | `#c5a5c5`        | `#fb94ff`        | Oceanic Next |
| Orange          | `#eb9a6d`        | `#ff9d00`        | Oceanic Next |
| Blue            | `#5a9bcf`        | `#0088ff`        | Oceanic Next |

These are not "tweaks of Cobalt2", they're a different palette entirely.
Visually, side-by-side, Cobalt Next looks like Oceanic Next with the
Cobalt2 *spirit* in token *choices* (e.g. tags get the angry red
treatment, italics on comments and language variables, attributes get a
distinct purple). The "deep blue background with yellow / orange / pink
accents" line in the original plan's pass/fail criteria needs adjusting:
the background is a desaturated **slate**, not a deep blue, and the
yellow is `#fac863` (warm/dim) not `#ffc600` (electric).

**Implication for Phase 1:** Approach A's diff against Cobalt2 will show
massive structural color differences, not "mostly pure colour swaps".
The patch-onto-Zed-Cobalt2 strategy is almost certainly **not viable**
— it would mean re-coloring nearly every UI element. Approach A still
has value as a *categorisation exercise* (which families of scopes does
Cobalt Next add that Cobalt2 doesn't define) but its original framing
as a viability test for the patch strategy is dead on arrival.

### Correction 2: Cobalt2 Zed is not a Cobalt2 hand-port — it's a Dracula reskin

The plan treated `wesbos/cobalt2-zed` as a "gold-standard reference for
what a successful VS Code → Zed conversion of a Cobalt-family theme
looks like". Reading the JSON, this is wrong:

- **Author** field: `"MD. MOHIBUR RAHMAN"` (not Wes Bos)
- **LICENSE header**: `Copyright (c) 2023 Dracula Theme`
- **Most syntax colors are literal Dracula colors**:
  - `#ff79c6` (Dracula pink) — boolean, constructor, operator, tag, punctuation.delimiter, string.escape, etc.
  - `#bd93f9` (Dracula purple) — enum, hint, number, string.special.symbol
  - `#f8f8f2` (Dracula foreground) — embedded, link_text, preproc, punctuation.bracket
  - `#ff5555` (Dracula red) — string.regex
  - `#8be9fd` (Dracula cyan) — link_uri, type.super
  - `#f1fa8c` (Dracula yellow) — text.literal
  - `#ffb86c` (Dracula orange) — property, variable.parameter

The **UI chrome** (background `#193549`, yellow `#ffc600`, red `#ff628c`,
etc.) is real Cobalt2. So it's "Cobalt2 UI chrome bolted onto a Dracula
syntax theme". That's a hack, not a reference.

Additional smells:
- Schema URL is `v0.1.0` (the plan and current Zed use `v0.2.0`).
- Uses non-standard syntax tokens that the modern Zed schema doesn't
  recognise: `interface`, `entity`, `meta`, `parameters`, `preproc`,
  `primary`, `text.literal`, `variant`, `punctuation.list_marker`,
  `punctuation.special`, `type.super`, `string.special.symbol`, `hint`.
  These are likely silently dropped on load.
- Total of **5 git commits** ever, including "Initial commit" and a
  "hotfix: add themes array". Definitely not iteratively refined.

**Implication for Phase 1:** Approach B's premise — "extract the
translation rules a careful hand-port used" — is broken because there
*are no thoughtful translation rules to extract*. Approach B still has
narrow value:
- The `style` (UI) block IS real Cobalt2 and demonstrates how to
  populate Zed UI keys for a Cobalt-family theme. We can use its UI
  block structure as a layout reference.
- The git history confirms there's no automated baseline+iterate
  pattern to copy.
- It tells us the converter (Approach C) is *probably* the strongest
  starting point because nobody in the Cobalt-family ecosystem has
  done a proper hand-port yet.

This **elevates Approach C and Phase 2 hand-polish**, and **demotes
Approach B from "highest-value learning" to "ten-minute UI structure
sanity check"**.

---

## Bonus context gathered while exploring

### How the Zed converter actually works (relevant to Phase 1 planning)

`crates/theme_importer/src/vscode/converter.rs` and `syntax.rs`:

- **UI colors** are mapped 1:1 from a fixed list of VS Code keys
  (`editor.background` → `editor.background`, `panel.background` →
  `panel.background`, `tab.activeBackground` → `tab.active_background`,
  etc.). Cobalt Next defines all these keys, so UI conversion should be
  high-quality.
- **Syntax tokens** use a *reverse* weighted-match: for each of 40 Zed
  tokens, the converter has an ordered list of VS Code scopes it cares
  about (e.g. `Function` → `["entity.function", "entity.name.function",
  "variable.function"]`). It scans the input theme's `tokenColors` for
  the rule that best matches, with earlier scopes weighted higher,
  and picks that rule's color. **One color per Zed token, no fan-out.**
- This means none of Cobalt Next's per-language rules
  (`source.ts entity.name.type`, the JSON-key-by-depth rules,
  `[MARKDOWN] - Heading Name Section`, etc.) survive automated
  conversion. They get collapsed into the generic Zed token they
  resemble.
- The converter has fallback chains: `Number → Constant`, `CommentDoc →
  Comment`, `Punctuation* → Punctuation`, `String* → String`. Useful
  to know when reasoning about why a color "appeared" in the wrong slot.
- `--warn-on-missing` logs `"No matching token color found for '<token>'"`
  to stderr for any Zed token that found no source. This is the list
  Phase 2 starts from.

### Cobalt Next's notable syntax structure

(Read from `themes/CobaltNext.json` lines 304–964.)

| Concept                | Color      | Style     |
|------------------------|------------|-----------|
| Comment                | `#65737e`  | italic    |
| Variable               | `#CDD3DE`  | —         |
| Keyword / storage      | `#c5a5c5`  | —         |
| Operator / punctuation | `#5FB3B3`  | —         |
| Tag                    | `#ed6f7d`  | —         |
| Function               | `#5a9bcf`  | —         |
| Number / parameter / constant | `#eb9a6d` | — |
| String / heading       | `#99C794`  | —         |
| Class / type / support | `#FAC863`  | —         |
| Attribute name         | `#BB80B3`  | italic    |
| Markdown H1/H2 (theme's own) | `#c5a5c5` bold | — |
| Markdown bold          | `#5FB3B3`  | bold      |
| Markdown italic        | `#5a9bcf`  | italic    |
| URL / regex / escape   | `#5FB3B3`  | underline |
| Decorator              | `#5a9bcf`  | italic    |
| `variable.language` (this/self) | `#c5a5c5` | italic |
| JSON keys, depth 0–8   | rotates through 8 colors (`#FAC863`, `#c5a5c5`, `#d8dee9`, `#5a9bcf`, `#AB7967`, `#ed6f7d`, `#eb9a6d`, `#FAC863`, `#c5a5c5`) — Zed cannot replicate this |

The plan's note about Danny's H1 cyan / H2 magenta `tokenColorCustomizations`:
- Cobalt Next *itself* colors markdown headings purple (`#c5a5c5`) bold.
- Danny's overrides set H1 → cyan, H2 → magenta on top of that.
- Zed's `title` token does NOT distinguish H1 from H2 (it's a single
  token for any "title"-like thing). So one of the two colors has to
  win at theme level. Default to H1 cyan since H1 is more prominent;
  this is a "nice", not a must.

---

## Go / no-go

**GO**, with the following adjustments to the plan:

1. **Re-frame Approach A**: drop the "patch-onto-Cobalt2" framing.
   Re-purpose the hour to instead build a **Cobalt Next syntax-rule
   inventory** — a categorised dump of every `tokenColors` rule and
   what it targets. This becomes the input for Phase 2's hand-polish
   pass over the converter output.
2. **Demote Approach B**: 10-minute UI-structure scan only. Confirm
   the Zed UI key set, copy nothing wholesale.
3. **Promote Approach C**: now the load-bearing artifact. Run it on
   `CobaltNext.json` with `--warn-on-missing`, capture both the JSON
   and stderr.
4. **Expect Phase 2 to be the heavy lifting**, not Phase 1 — most of
   the per-language and per-language-construct rules in Cobalt Next
   will need manual mapping into Zed's smaller token set.
5. **Multi-variant decision**: Cobalt Next ships three variants (main,
   Dark, Minimal). Defer this choice to after Phase 3 — port the main
   one first, decide whether the others are worth the effort once the
   first is shippable.

No blockers. Recommended next step: kick off Phase 1 in the
**re-ordered priority C → A → B** (Approach B is demoted to a quick
sanity check).
