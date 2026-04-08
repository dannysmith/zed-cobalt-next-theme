# Zed Cobalt Next Theme Port — Project Plan

> This is a self-contained briefing for a fresh Claude Code session. Read
> the whole file before starting. All the research has been done; the goal
> is execution, not re-discovery.

## Why this project exists

Danny uses **Cobalt Next** (`dline.CobaltNext`) as his primary VS Code
theme. He recently set up Zed as an experimental secondary editor and
wants its visual experience to match VS Code as closely as possible.
Cobalt Next has **no Zed port** — nobody has done it yet. The closest
existing thing is **Wes Bos's Cobalt2**, which is the spiritual ancestor
of Cobalt Next and has both a VS Code version and a Zed version.

### The opportunity
Because Cobalt2 already has a working Zed port, we have a **reference
for how a Cobalt-family theme populates Zed's UI key set**. This gives
us a reasonable UI chrome baseline.

> **Phase 0 correction (2026-04-07):** The Cobalt2 Zed port is NOT a
> careful hand-translation of Cobalt2 — it's "Cobalt2 UI chrome bolted
> onto a Dracula syntax theme" (author "MD. MOHIBUR RAHMAN", LICENSE
> says "Copyright 2023 Dracula Theme", most syntax colors are literal
> Dracula hex values). Its UI block is a valid reference for Zed key
> layout; its syntax block is useless as a translation reference. See
> `phase-0-findings.md` for the full breakdown.

### The goal hierarchy
1. **Must:** a Zed theme that visually matches Cobalt Next at-a-glance.
   Background, foreground, accents, and syntax highlighting in TS / JS /
   CSS / JSON files should feel correct.
2. **Should:** UI elements (sidebar, status bar, terminal, scrollbar)
   match the VS Code source closely.
3. **Nice:** Markdown handling matches — Danny's VS Code spec adds custom
   H1 cyan / H2 magenta heading colours via
   `editor.tokenColorCustomizations`. If we can preserve those in the Zed
   theme's `syntax` block, great. If Zed's smaller token model can't
   express it, accept the loss and move on.
4. **Don't bother:** every TextMate scope from the original perfectly
   preserved. Impossible due to Zed's smaller, more semantic token set.

### The stretch goal
If the result is decent, package it as a Zed extension and submit a PR to
`zed-industries/extensions`. Falling back to "use it locally only" is also
fine. The decision happens at the end based on quality.

---

## Background — How Zed themes work

### Format
- Plain JSON, conforms to schema at
  `https://zed.dev/schema/themes/v0.2.0.json`
- A **theme family** has `name`, `author`, and a `themes` array
- Each **theme** in the family has `name`, `appearance` (`light` or
  `dark`), `style` (UI/editor colours), and `syntax` (token colours)
- One extension can ship multiple themes (light + dark, or multiple
  variants)

### Available syntax tokens
Zed's syntax token set is significantly smaller and more semantic than
VS Code's TextMate scopes. Full list:

`attribute`, `boolean`, `comment`, `comment.doc`, `constant`,
`constant.builtin`, `constructor`, `embedded`, `emphasis`,
`emphasis.strong`, `enum`, `function`, `keyword`, `label`, `link_text`,
`link_uri`, `number`, `operator`, `property`, `punctuation`,
`punctuation.bracket`, `punctuation.delimiter`, `string`, `string.escape`,
`string.regex`, `string.special`, `tag`, `title`, `type`, `type.builtin`,
`variable`, `variable.special`, `variable.parameter`

Each token can specify colour, font weight, and font style
(italic/oblique/normal).

### The token mismatch problem
VS Code themes target hundreds of fine-grained TextMate scopes
(`storage.type.function.ts`, `entity.name.function.member.ts`, etc).
Zed's set above maps many VS Code scopes to a single Zed token. **Any
conversion is necessarily lossy on the syntax side.** This is the central
constraint of the project.

### Two install paths

**Local-only (trivial):** Drop a JSON file in `~/.config/zed/themes/`.
Zed picks it up immediately on next launch. No manifest, no review. This
is the path for personal use and the path we'll use during development.

**Published (more involved):** Package as an extension (with `extension.toml`),
push to a GitHub repo, open a PR against `zed-industries/extensions`. The
extension ID must end in `-theme`. Reviewers approve, it appears in
everyone's in-editor extension gallery.

### Tools
- **Theme Builder** at https://zed.dev/theme-builder — browser UI for
  fine-tuning a theme starting from any existing one. Useful for hand
  polish at the end.
- See "Conversion tools" section below for VS Code → Zed converters.

---

## Background — Available conversion tools

### 1. Official: `zed-industries/zed/crates/theme_importer` (Rust CLI)
**The most authoritative tool.** Lives inside the Zed source tree,
maintained by the Zed team.

```bash
git clone https://github.com/zed-industries/zed
cd zed/crates/theme_importer
cargo run -- convert --warn-on-missing <input.json> -o <output.json>
```

The `--warn-on-missing` flag is important — it prints warnings for
VS Code scopes that didn't have a Zed equivalent, which is exactly the
list we need to hand-fix.

Requires Rust toolchain. Output is canonical Zed JSON.

### 2. `blackmann/theme-to-zed` (VS Code extension)
A VS Code extension that exports the currently-active VS Code theme to
Zed format. https://github.com/blackmann/theme-to-zed

Workflow: install in VS Code, set Cobalt Next as active theme, run
"Export Theme to Zed" from command palette, get JSON. Zero setup beyond
the install.

This is the **easiest path for a baseline** but has the same lossy
conversion issues as #1, possibly worse depending on how recently it's
been updated against the Zed schema.

### 3. `mahi160/vszedthemer` (CLI)
Another community converter. https://github.com/mahi160/vszedthemer
Less popular than #1 and #2; mention only as a third opinion if needed.

### 4. `nexmoe/cursor-themes-for-zed` (reference port)
https://github.com/nexmoe/cursor-themes-for-zed

Not a conversion tool, but it contains a `convert-vscode-to-zed.mjs`
script written for porting Cursor's theme family. Worth reading as a
reference for "what does a real-world manual conversion script look
like". Useful as inspiration if we need to write our own conversion logic.

---

## Background — The themes themselves

### Cobalt Next (`dline.CobaltNext`)
- VS Code Marketplace: https://marketplace.visualstudio.com/items?itemName=dline.CobaltNext
- Description: combines **Cobalt2** (Wes Bos) with **Oceanic Next**
- VS Code-only — no Zed port exists
- **Source repo: needs to be checked in pre-flight (see Phase 0)**
- **Licence: needs to be checked in pre-flight**

Already installed locally for Danny:
- VS Code: `~/.vscode/extensions/dline.cobaltnext-*/`

### Cobalt2 (Wes Bos)
- VS Code repo: https://github.com/wesbos/cobalt2-vscode
- Zed repo: https://github.com/wesbos/cobalt2-zed
- Zed extension page: https://zed.dev/extensions/cobalt2
- VS Code Marketplace: https://marketplace.visualstudio.com/items?itemName=wesbos.theme-cobalt2
- Licence: MIT (Wes Bos themes are typically MIT)
- **Both halves of the conversion blueprint exist as public source files
  in public repos.** This is the win that makes Approach B tractable.

Already installed locally for Danny:
- Zed: `~/Library/Application Support/Zed/extensions/installed/cobalt2/`

### Lineage / signature colours

**Cobalt2** (for reference, NOT what we're targeting):
- Background: `#193549`, Highlights `#1F4662` / `#234E6D`, yellow `#ffc600`

**Cobalt Next** (what we're actually targeting — Phase 0 corrected the
mental model; this is Oceanic Next palette with Cobalt2 *philosophy*,
not Cobalt2 with tweaks):
- Editor bg: `#1b2b34` (slate, NOT deep blue)
- Sidebar bg: `#0f1c23`
- Surface: `#343d46`
- Foreground: `#d8dee9`
- Yellow (cursor, classes): `#fac863` (warm/dim, not electric `#ffc600`)
- Teal / cyan (operators, URLs): `#5fb3b3`
- Red (tags): `#ed6f7d`
- Green (strings): `#99c794`
- Purple (keywords, markdown headings): `#c5a5c5`
- Orange (numbers, constants): `#eb9a6d`
- Blue (functions, links): `#5a9bcf`

These are all Oceanic Next colors. The Cobalt2-ness lives in which
*concepts* get which treatment (angry red tags, italic language
variables, distinct purple attributes), not in the hex values.

---

## Existing local resources to reference

| Resource | Path |
|---|---|
| Danny's VS Code Cobalt Next install | `~/.vscode/extensions/dline.cobaltnext-*/` |
| Danny's Zed Cobalt2 install | `~/Library/Application Support/Zed/extensions/installed/cobalt2/` |
| Danny's Zed config | `~/.config/zed/settings.json` |
| Danny's Zed local themes dir | `~/.config/zed/themes/` (currently empty) |
| Danny's VS Code spec doc (for context) | `~/scratchpad/vscode-setup.md` |

The Cobalt Next install in `~/.vscode/extensions/` will contain the
theme JSON files even if the upstream repo isn't open source — that's
the fallback source. Look for `themes/*.json` inside the extension dir.

---

## Success criteria

Defined upfront so the project knows when to stop:

### Pass / fail bar (must hit all)
- [ ] Background, foreground, and accent colours match Cobalt Next
- [ ] Syntax highlighting in `.ts` / `.js` files looks visually consistent
      with Cobalt Next side-by-side
- [ ] Cobalt Next-specific colour family is recognisable (slate
      `#1b2b34` background with warm-yellow `#fac863`, teal `#5fb3b3`,
      red `#ed6f7d`, green `#99c794`, purple `#c5a5c5` accents — the
      Oceanic Next palette)
- [ ] No glaring errors (white-on-white text, missing string colours,
      etc)

### Stretch (try, accept if not possible)
- [ ] Sidebar, status bar, scrollbar, terminal colours match
- [ ] Markdown H1 cyan / H2 magenta — Danny's VS Code custom heading
      colours, defined in his settings.json under
      `editor.tokenColorCustomizations`. These are NOT part of the
      Cobalt Next theme itself; they're applied on top. Try to bake them
      into the Zed theme's `syntax.title` / equivalent.

### Done means
The theme is in `~/.config/zed/themes/cobalt-next.json`, Zed loads it,
Danny has it active for a real-world side-by-side test against VS Code,
and the result hits the pass/fail bar above.

The publish-as-extension question is a separate decision *after* the
theme passes its visual bar.

---

## Phase 0 — Pre-flight checks

**Goal:** determine the shape of the project before committing to it.
Cheap, ~10 minutes of work, but the answers can change everything.

### 0.1 Verify Cobalt Next source availability
Check the VS Code Marketplace listing
(https://marketplace.visualstudio.com/items?itemName=dline.CobaltNext)
for a "Repository" link in the sidebar. Common possibilities:
- **Best case:** open GitHub repo with theme JSON in `themes/*.json`.
  Use that as canonical source.
- **Acceptable case:** no repo linked, but the installed extension at
  `~/.vscode/extensions/dline.cobaltnext-*/` contains the theme JSON
  (it always does — VS Code themes ship JSON, not compiled assets).
  Use that as source for personal use; flag licensing as TBD for
  publishing.
- **Worst case:** none of the above. Should not happen with VS Code
  themes — they're always shipped as JSON.

### 0.2 Check Cobalt Next licence
- Look in the GitHub repo (if found in 0.1) for `LICENSE` or `LICENSE.md`
- Or check the `package.json` of the installed extension for a `license`
  field
- If MIT, BSD, or similarly permissive: free to derive and republish
  (with attribution)
- If something restrictive (CC-BY-NC, proprietary, no licence stated):
  flag this. Personal use is fine; publishing is murky and may need a
  courtesy ping to `dline`.

### 0.3 Verify Cobalt2 access (should be trivial)
- `https://github.com/wesbos/cobalt2-vscode` and
  `https://github.com/wesbos/cobalt2-zed` should both be accessible
- Confirm both are MIT licensed (expected)
- Clone or fetch both repos to a working dir within this project

### 0.4 Verify the official Zed converter builds
- `git clone https://github.com/zed-industries/zed` (this is a large
  repo — Zed's full source). Consider `git clone --depth 1` to save
  bandwidth, since we only need the `crates/theme_importer` directory.
- `cd zed/crates/theme_importer`
- `cargo build` (or just `cargo run -- --help`)
- Confirm Rust toolchain is present. If not, `brew install rust` or
  install via rustup.

### 0.5 Decide
Based on the above, write a short "go / no-go" note in
`phase-0-findings.md` in this directory. Include:
- Cobalt Next source location and licence
- Cobalt2 repos confirmed accessible
- Converter builds yes/no
- Any blockers found

If the answer is "go", proceed to Phase 1. If "no-go", explain why and
present alternatives to Danny before continuing.

---

## Phase 1 — Three approaches (re-ordered after Phase 0)

**Goal:** produce candidate theme output and the *understanding* needed
to hand-polish it in Phase 2.

> **Phase 0 changed the shape of this phase.** The original plan
> imagined three roughly equal-weight approaches feeding into a synthesis
> step. Phase 0 found:
>
> 1. The Cobalt2 Zed port is a Dracula reskin, so Approach B can't
>    extract translation rules from a careful hand-port (because there
>    isn't one). Demoted from "highest-value learning" to a 10-min
>    UI-structure sanity check.
> 2. Cobalt Next isn't "Cobalt2 + tweaks" — it's a different palette
>    entirely (Oceanic Next colors). Approach A's "diff against Cobalt2,
>    decide whether patching is viable" framing is moot — patching
>    is not viable. Re-purposed to **build a syntax-rule inventory**
>    of Cobalt Next itself, which becomes Phase 2's hand-polish input.
> 3. The official converter (Approach C) is the only viable
>    *automated* baseline and is now load-bearing.
>
> **Revised order: C → A → B** (C is the artifact; A is the manual
> understanding that Phase 2 needs; B is a quick reality check).

### Approach C — Run the official converter (do first, load-bearing)

**Question it answers:** What does the official automated converter
produce, and which Zed tokens does it fail to fill?

**Steps:**
1. Source JSON is at `source/cobaltnext-vscode/themes/CobaltNext.json`
   (cloned in Phase 0).
2. Run the built `theme_importer` binary (already compiled in Phase 0
   to `source/zed-theme-importer/target/debug/theme_importer`):
   ```bash
   ./source/zed-theme-importer/target/debug/theme_importer \
     --warn-on-missing \
     -o approach-c-output.json \
     source/cobaltnext-vscode/themes/CobaltNext.json \
     2> approach-c-warnings.txt
   ```
   The converter logs to stderr at Trace level — the file will be
   noisy. The interesting lines are `WARN` entries ("No matching token
   color found for '<token>'") and `INFO Matched '<zed-token>' to
   '<vscode-rule-name>'" which shows what each Zed token got mapped to.
3. Copy the output to `~/.config/zed/themes/cobalt-next-approach-c.json`,
   launch Zed, switch to it, and take screenshots of a real `.ts` file
   alongside the same file in VS Code Cobalt Next.
4. Also run the converter on the two other variants
   (`CobaltNext-Dark.json`, `CobaltNext-Minimal.json`) for completeness
   — decision on which to ship is deferred to after Phase 3.

**Output:**
- `approach-c-output.json` — the converted theme
- `approach-c-warnings.txt` — list of unmapped scopes
- `approach-c-screenshot-comparison.png` — visual diff
- `approach-c-notes.md` — what's wrong with it, how close it is to the
  pass bar

### Approach B — Cobalt2 Zed UI-structure sanity check (demoted)

**Question it answers:** Does the converter's UI block look structurally
right compared to another working Cobalt-family Zed theme?

> Phase 0 established that `wesbos/cobalt2-zed`'s *syntax* block is
> Dracula hex values, not a careful Cobalt2 translation. But its
> *`style`* (UI) block does use real Cobalt2 UI colors, so it's still
> a valid reference for "what keys does a Cobalt-family Zed theme
> populate in the UI section".

**Steps (quick, ~10 min):**
1. Open `source/cobalt2-zed/themes/cobalt2.json` and the Approach C
   output side by side.
2. Scan for Zed UI keys Cobalt2 Zed defines but Approach C's output
   doesn't (or vice versa). The converter may miss keys the Cobalt Next
   VS Code JSON doesn't explicitly set; note any gaps.
3. Note the schema version difference (Cobalt2 Zed is `v0.1.0`,
   current Zed uses `v0.2.0`).
4. Save findings as `approach-b-notes.md` — short, bullet-point
   observations only.

**Output:**
- `approach-b-notes.md` — structural gaps in the converter output's
  UI section, if any, plus any keys worth copying patterns from.

**Do not:**
- Don't build a VS Code → Zed translation table from Cobalt2 Zed.
- Don't use its syntax block as reference for anything.

### Approach A — Cobalt Next syntax-rule inventory (re-purposed)

**Question it answers:** What does each `tokenColors` rule in Cobalt
Next target, and which Zed token (if any) is the right home for it?
This is the worksheet Phase 2 will lean on.

> Phase 0 established that Cobalt Next is Oceanic Next palette + Cobalt2
> philosophy, not Cobalt2 + tweaks. The original "diff against Cobalt2
> to see if patching is viable" framing is moot (it's not viable).
> This approach is re-purposed to produce the hand-polish input that
> Phase 2 needs.

**Steps:**
1. Read `source/cobaltnext-vscode/themes/CobaltNext.json` end to end.
2. Build a table of every `tokenColors` rule with columns:
   - VS Code scope(s) — the raw scope strings from the JSON
   - Intent — one-line description of what it targets (e.g. "JS
     storage.type.function", "Markdown H2 heading", "JSON key depth 3")
   - Colour + style
   - Proposed Zed token — closest match from the 40-token set, or
     `N/A` if nothing fits (e.g. JSON-key-by-depth rules)
   - Notes — collision warnings, fallback chain implications, etc.
3. Group rules by proposed Zed token. Where multiple VS Code rules
   collapse into one Zed token, pick a canonical colour and note the
   conflict (e.g. "Cobalt Next has `source.ts keyword` purple AND
   `source.js keyword` teal — Zed can't distinguish, picking purple
   because keywords are purple in the language-agnostic rule too").
4. Call out rules Zed cannot express at all (JSON-key-by-depth rotation,
   `variable.language` italic-specific, per-language scope
   overrides). These become "accepted losses".
5. Compare the proposed Zed tokens against Approach C's actual output —
   wherever they disagree, that's a manual fix for Phase 2.

**Output:**
- `approach-a-inventory.md` — the categorised rule table
- `approach-a-phase2-worklist.md` — delta between proposed mapping and
  Approach C's output; this is Phase 2's starting checklist

---

## Phase 2 — Synthesis

**Goal:** combine the outputs of A, B, and C into a single best-effort
Zed theme.

Likely shape (decide based on Phase 1 outcomes):
- Start from Approach C's converter output as the baseline structure
- Apply Approach B's translation rules to fix the worst syntax mappings
  the converter got wrong (look at the warnings list)
- Apply Approach A's colour deltas to shift the result from "looks like
  Cobalt Next-converted" to "looks like Cobalt Next"
- Manually polish anything that's still wrong using the Zed Theme Builder
  at https://zed.dev/theme-builder

Output: `cobalt-next.json` in `~/.config/zed/themes/`. Switch to it in
Zed and walk through the success criteria checklist.

---

## Phase 3 — Polish & validation

Side-by-side comparison with VS Code Cobalt Next on real files:
- `.ts` / `.tsx` files (function declarations, imports, JSX)
- `.css` files (selectors, properties, values)
- `.json` files (keys, values, strings)
- `.md` files (headings, code blocks, links — and the H1/H2 custom
  colours from Danny's spec, if reachable)
- The Zed UI itself (sidebar, terminal, command palette, status bar)

For each, capture screenshots and document any remaining gaps in
`phase-3-findings.md`.

Iterate until the success criteria's pass/fail bar is hit.

---

## Phase 4 — Optional publish

Only if the result is decent and Danny decides he wants to make it
available to others.

Rough shape:
1. Create a standalone GitHub repo (`cobalt-next-zed` or similar)
2. Add `extension.toml` manifest, `themes/cobalt-next.json`, README,
   LICENSE (matching Cobalt Next's licence — verify in Phase 0)
3. Attribution: explicitly credit `dline` for Cobalt Next, Wes Bos for
   Cobalt2, and the Oceanic Next authors
4. Open a PR against `zed-industries/extensions` adding the theme as a
   submodule
5. Respond to review feedback

If Phase 4 doesn't happen, the theme still lives at
`~/.config/zed/themes/cobalt-next.json` for Danny's personal use. That's
a fully valid endpoint — local install is a first-class path in Zed.

---

## Recommended order

**C → A → B → Phase 2 hand-polish.** (Revised from C → B → A after
Phase 0.) Reasons:

- **C is the load-bearing artifact.** Run the converter, get the
  baseline JSON and the missing-token warning list. Everything else
  in Phase 1 either fills gaps in C or validates it.
- **A feeds Phase 2.** Building the Cobalt Next inventory gives Phase 2
  a concrete worklist: "for each Zed token C got wrong or didn't fill,
  here's what the source rule wanted and the right colour to use".
- **B is a quick sanity check.** Confirm C's UI block structure
  against Cobalt2 Zed's UI block. ~10 minutes, not a day.
- **Phase 2 is now where most of the work lives**, not Phase 1.

---

## Things to watch out for

### Cobalt2 Zed is not actually a Cobalt2 port (resolved in Phase 0)
We checked. It's 5 commits, most of the syntax colors are Dracula, and
the author isn't Wes Bos. Treat it strictly as a UI-key-layout reference,
nothing more. See `phase-0-findings.md` for the full write-up.

### Token-system ceiling
Some of Cobalt Next's TextMate scope distinctions simply cannot be
expressed in Zed's smaller token set. When you hit those, accept the
loss and move on — don't try to be cleverer than the schema.

### The markdown heading colours specifically
Danny's VS Code H1 cyan / H2 magenta is applied via
`editor.tokenColorCustomizations` *on top of* whatever theme is active.
It's not part of Cobalt Next per se (Cobalt Next itself colors H1/H2
purple `#c5a5c5` bold).

Phase 0 confirmed Zed's `title` syntax token does NOT distinguish H1
from H2 — it's a single token covering "title-like things". So in the
Zed theme we can pick exactly one heading colour. Default to **H1 cyan
`#9cecfb`** since H1 is the more prominent of the two and Danny's spec
emphasises H1 first. Alternative: leave it at Cobalt Next's own purple
`#c5a5c5` and let Danny decide. This is a "nice" goal — if it's
controversial, drop it.

### The hand-crafting fallback
If all three approaches plus Phase 2 synthesis still leaves us at 60%
visual fidelity instead of 90%, the fallback is **hand-authoring from
scratch in the Zed Theme Builder** with VS Code Cobalt Next open in
another window as reference. Slow, but always works as a last resort.
Danny is fine with Claude doing this part with screenshot input from
him if needed.

---

## Quick reference — useful URLs

### Documentation
- Zed Theme docs: https://zed.dev/docs/themes
- Zed Theme Extension docs: https://zed.dev/docs/extensions/themes
- Zed Theme Builder: https://zed.dev/theme-builder
- Zed schema: https://zed.dev/schema/themes/v0.2.0.json

### Tools
- Official converter (in Zed source): https://github.com/zed-industries/zed/tree/main/crates/theme_importer
- blackmann/theme-to-zed: https://github.com/blackmann/theme-to-zed
- mahi160/vszedthemer: https://github.com/mahi160/vszedthemer
- nexmoe/cursor-themes-for-zed (reference port): https://github.com/nexmoe/cursor-themes-for-zed

### Source themes
- Cobalt Next (VS Code marketplace): https://marketplace.visualstudio.com/items?itemName=dline.CobaltNext
- Cobalt2 VS Code repo: https://github.com/wesbos/cobalt2-vscode
- Cobalt2 Zed repo: https://github.com/wesbos/cobalt2-zed
- Cobalt2 Zed extension page: https://zed.dev/extensions/cobalt2

### Distribution (if Phase 4 happens)
- zed-industries/extensions: https://github.com/zed-industries/extensions

---

## Working directory

This project lives in `~/scratchpad/zed-cobalt-next-theme/`. Suggested
structure as the work progresses:

```
~/scratchpad/zed-cobalt-next-theme/
├── plan.md                    # this file
├── phase-0-findings.md        # pre-flight check results
├── source/                    # cloned repos for offline reference
│   ├── cobaltnext-vscode/     # from extension dir or repo
│   ├── cobalt2-vscode/        # cloned from wesbos
│   ├── cobalt2-zed/           # cloned from wesbos
│   └── zed-theme-importer/    # cloned from zed-industries
├── approach-a-diff.md
├── approach-a-verdict.md
├── approach-b-mapping.md
├── approach-b-history.md
├── approach-c-output.json
├── approach-c-warnings.txt
├── approach-c-notes.md
├── phase-2-synthesis.md
├── phase-3-findings.md
└── cobalt-next.json           # the final theme (also symlinked or
                               # copied to ~/.config/zed/themes/)
```

---

## How to start

1. Read this file end-to-end
2. Run Phase 0 pre-flight checks
3. Write `phase-0-findings.md` with the go / no-go decision
4. If go, start Phase 1 in the recommended order (C → B → A)
5. Check in with Danny at the end of Phase 1 before Phase 2 synthesis —
   he wants to see the three approach outputs and decide direction
   together
