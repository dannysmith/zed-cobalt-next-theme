#!/usr/bin/env python3
"""
Build the Cobalt Next Zed theme family from the Zed theme_importer's
raw converter output by applying hand-polish fixes.

Re-run after editing this file to regenerate the theme.

Inputs (alongside this script):
  converter-output/cobalt-next.json
  converter-output/cobalt-next-dark.json
  converter-output/cobalt-next-minimal.json

Outputs:
  ../themes/cobalt-next.json              (in-repo extension artifact)
  ~/.config/zed/themes/cobalt-next.json   (local install for live testing)

See reference/README.md for how to regenerate the converter outputs.
See reference/syntax-rules.md for the Cobalt Next palette and token inventory.
See reference/notes.md for port-specific decisions and trade-offs.
"""

import json
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).parent
REPO_ROOT = HERE.parent
CONVERTER_OUTPUT_DIR = HERE / "converter-output"
REPO_THEME_FILE = REPO_ROOT / "themes" / "cobalt-next.json"
ZED_THEMES_DIR = Path.home() / ".config" / "zed" / "themes"

# ---------------------------------------------------------------------------
# Cobalt Next palette (distilled from Cobalt Next's VS Code tokenColors)
# ---------------------------------------------------------------------------

PALETTE = {
    # backgrounds
    "bg":            "#1b2b34",  # main editor / panel background (slate)
    "bg_dark":       "#0f1c23",  # sidebar / darker variant editor background
    "bg_darker":     "#0b151b",  # dropdown bg, tab border (very dark)
    "surface":       "#343d46",  # tab.active, line highlight, raised surfaces
    "surface_high":  "#4f5b66",  # selection, line numbers, muted ruler
    "surface_higher":"#65737e",  # comments, inactive sidebar text, indent active
    # foregrounds
    "fg":            "#d8dee9",  # default text (sidebar, ui labels)
    "fg_bright":     "#ffffff",  # editor foreground
    "fg_var":        "#CDD3DE",  # plain variables
    # accents
    "yellow":        "#fac863",  # cursor, classes, types, JSON keys lvl0
    "teal":          "#5fb3b3",  # operators, punctuation, URLs, regex, escapes
    "red":           "#ed6f7d",  # tags, errors
    "green":         "#99c794",  # strings, link text
    "purple":        "#c5a5c5",  # keywords, language vars, native md headings
    "purple_dim":    "#BB80B3",  # attributes
    "blue":          "#5a9bcf",  # functions, link URLs, markdown italic
    "orange":        "#eb9a6d",  # numbers, constants, parameters, md inline code
    # markdown heading override
    "h2_magenta":    "#e255a1",  # H2 magenta override; H1/H2 share Zed's `title` token
}

# ---------------------------------------------------------------------------
# Syntax fixes — applied to all 3 variants (they share one syntax block).
# Each entry overrides whatever the Zed converter produced for that token.
# Commentary explains the specific converter bug being corrected.
# ---------------------------------------------------------------------------

SYNTAX_FIXES = {
    # converter chose "Other Variable, String Link" (red) — should be markdown
    # link title green for link text...
    "link_text":         {"color": PALETTE["green"]},
    # ...and markdown link address blue for link URI
    "link_uri":          {"color": PALETTE["blue"]},
    # Cobalt Next uses `string.regexp` (extra `p`); converter looks for
    # `string.regex`. Fallback to `string` gives wrong green. Should be teal.
    "string.regex":      {"color": PALETTE["teal"]},
    # Converter's StringEscape fallback chain hit `constant.character` (orange)
    # before finding `constant.character.escape` (teal).
    "string.escape":     {"color": PALETTE["teal"]},
    # Cobalt Next has an explicit author override on `variable.language` to
    # purple italic (see syntax-rules.md rule 12). Converter picked the later
    # JS-specific red rule instead — this brings `this`/`self`/`super` back
    # to purple italic to match Cobalt Next's intent.
    "variable.special":  {"color": PALETTE["purple"], "font_style": "italic"},
    # Converter latched onto "[CSS] - Entity Tag Name" (red) incidentally.
    # Constructors are type-like — match the `type` color (yellow).
    "constructor":       {"color": PALETTE["yellow"]},
    # `property` is the most contested token because multiple languages use
    # it for different concepts (see notes.md "Property token split"):
    #   YAML keys        → @property       (bare)     — red in VS Code
    #   CSS property     → @property       (bare)     — yellow in VS Code
    #   TS/JS `foo.bar`  → @property       (bare)     — white in VS Code
    #   Rust/Go fields   → @property       (bare)     — white in VS Code
    #   JSON keys        → @property.json_key         — yellow (preferred)
    #   TS object keys   → @property.name             — yellow
    # Zed's theme resolver walks dot-prefixes, so subscopes override.
    # Base set to red (YAML priority); subscopes overridden to yellow below.
    # Trade-off: TS `foo.bar` field access and Rust/Go struct fields become
    # red. Method calls (`.foo()`) are `@function.method`, unaffected.
    "property":            {"color": PALETTE["red"]},
}

# Tokens the converter leaves unfilled, plus subscope overrides for
# `property` handled above.
SYNTAX_ADDITIONS = {
    # markdown italic — blue italic (Cobalt Next markup.italic.markdown rule)
    "emphasis":          {"color": PALETTE["blue"], "font_style": "italic"},
    # markdown bold — teal bold (markup.bold.markdown rule)
    "emphasis.strong":   {"color": PALETTE["teal"], "font_weight": 700},
    # markdown headings — H2 magenta override wins (H1/H2 share `title`)
    "title":             {"color": PALETTE["h2_magenta"], "font_weight": 700},
    # TS/JS object literal keys and labeled statements — yellow
    "property.name":     {"color": PALETTE["yellow"]},
    # JSON keys specifically — yellow (overrides the red `property` base)
    "property.json_key": {"color": PALETTE["yellow"]},
    # parameter names — orange italic (Number/Constant/Parameter rule + italicsify)
    "variable.parameter":{"color": PALETTE["orange"], "font_style": "italic"},
    # JSX text / embedded blocks — foreground
    "embedded":          {"color": PALETTE["fg"]},
    # enum types — match classes/types yellow
    "enum":              {"color": PALETTE["yellow"]},
    # Rust enum variants and similar — match enum/type yellow
    "variant":           {"color": PALETTE["yellow"]},
    # loop labels and similar — match function blue
    "label":             {"color": PALETTE["blue"]},
    # preprocessor directives — keyword-adjacent purple
    "preproc":           {"color": PALETTE["purple"]},
}

# Tokens left intentionally empty: hint, predictive, primary
# (Zed's converter has no scope mapping for these; none of the source
# theme's rules semantically fit them.)


# ---------------------------------------------------------------------------
# UI tweaks shared across all variants
# ---------------------------------------------------------------------------

def shared_ui_polish(style):
    """In-place modifications to a variant's `style` block."""

    # --- Border overhaul --------------------------------------------------
    # The converter mapped most border keys to VS Code's `panel.border`
    # which Cobalt Next sets to teal `#5fb3b3`. In VS Code this only shows
    # on the panel separator and active tab underline; in Zed these keys
    # are the *ubiquitous* panel/pane dividers, so teal lines appear
    # between every panel. Override to a dark subtle border and reserve
    # teal for actual selection emphasis.
    style["border"] = PALETTE["bg_darker"]            # general borders — very dark
    style["border.variant"] = PALETTE["bg_darker"]
    style["border.transparent"] = PALETTE["bg_darker"]
    style["border.disabled"] = PALETTE["surface"]
    style["border.focused"] = PALETTE["surface"]      # focus rings
    style["border.selected"] = PALETTE["teal"]        # selection emphasis only
    style["pane_group.border"] = PALETTE["bg_darker"]

    # Muted wrap guides (converter set these to teal from panel.border;
    # Cobalt Next's actual ruler is `editorRuler.foreground: #4f5b66`)
    style["editor.wrap_guide"] = PALETTE["surface_high"]
    style["editor.active_wrap_guide"] = PALETTE["surface_higher"]

    # --- Sidebar background ----------------------------------------------
    # Cobalt Next's actual sideBar.background is `#0f1c23` — darker than
    # the editor `#1b2b34`. The converter read from `panel.background`
    # which Cobalt Next sets equal to the editor. Override.
    # (terminal.background is a separate key, so the terminal panel keeps
    # its `#1b2b34` background.)
    style["panel.background"] = PALETTE["bg_dark"]
    style["surface.background"] = PALETTE["bg_dark"]

    # --- Indent guides ---------------------------------------------------
    # Cobalt Next defines these but converter ignored them
    style["editor.indent_guide"] = PALETTE["surface"]
    style["editor.indent_guide_active"] = PALETTE["surface_higher"]

    # Word/symbol highlight — from editor.wordHighlightBackground/Strong
    style["editor.document_highlight.read_background"] = PALETTE["surface_high"]
    style["editor.document_highlight.write_background"] = PALETTE["surface_higher"]

    # Hint colour — converter default is `#969696`, replace with palette grey
    style["hint"] = PALETTE["surface_higher"]

    # --- Text states ------------------------------------------------------
    # text.accent: search match characters, active filter chips, link colour
    # in the agent panel. Reuse the function/link blue.
    style["text.accent"] = PALETTE["blue"]
    # text.placeholder: input placeholder text (search bars, command palette
    # empty state). Without this, falls back to `text` and reads as real
    # content rather than a hint.
    style["text.placeholder"] = PALETTE["surface_higher"]
    # text.disabled: disabled menu items, disabled buttons.
    style["text.disabled"] = PALETTE["surface_high"]

    # --- Element states ---------------------------------------------------
    # element.active: pressed-state background for buttons/inputs (mouse
    # button held down). Distinct from `element.selected`, which is a
    # persistent toggle state.
    style["element.active"] = PALETTE["surface_high"]
    # element.disabled: disabled button/input background.
    style["element.disabled"] = PALETTE["bg_dark"]
    # ghost_element.*: same logic as `element.*` but for transparent
    # buttons (e.g. toolbar icon buttons). The base background is fully
    # transparent so the underlying surface shows through until a state
    # change tints it.
    style["ghost_element.background"] = "#00000000"
    style["ghost_element.active"] = PALETTE["surface_high"]
    style["ghost_element.disabled"] = PALETTE["bg_dark"]

    # --- Editor extras ----------------------------------------------------
    # editor.invisible: rendered whitespace colour (`show_whitespaces: all`).
    # Match the wrap guide so invisibles read as muted indentation marks.
    style["editor.invisible"] = PALETTE["surface_high"]
    # editor.highlighted_line.background: line that flashes when you use
    # `editor: go to line` or jump from the outline view. Distinct from
    # the regular active line highlight.
    style["editor.highlighted_line.background"] = PALETTE["surface"]
    # editor.subheader.background: section headers in multi-buffer views
    # (project search results, "find all references", etc.).
    style["editor.subheader.background"] = PALETTE["surface"]
    # editor.debugger_active_line.background: line currently paused on by
    # the debugger. Tinted yellow so it's distinct from the regular active
    # line. NOTE: this key isn't enumerated in the v0.2.0 schema but does
    # exist in Zed's Rust source — if a future Zed rejects it as unknown,
    # drop this line.
    style["editor.debugger_active_line.background"] = PALETTE["yellow"] + "33"

    # --- Project panel indent guides --------------------------------------
    # Sidebar file-tree indent guides — separate from `editor.indent_guide`.
    # Mirror the editor guide colours so the file tree matches.
    style["panel.indent_guide"] = PALETTE["surface"]
    style["panel.indent_guide_active"] = PALETTE["surface_higher"]
    style["panel.indent_guide_hover"] = PALETTE["surface_high"]

    # --- Title bar inactive ----------------------------------------------
    # Title bar background when the window loses focus. Subtle, but a nice
    # visual cue. One shade darker than the active title bar.
    style["title_bar.inactive_background"] = PALETTE["bg_dark"]

    # --- Status colour family --------------------------------------------
    # Zed has 14 status families: each ideally has a foreground colour, a
    # tinted background pill, and a darker border. Pattern (from Zed One):
    #   foreground = palette colour at full opacity
    #   .background = same colour at ~10% alpha (`+ "1a"`)
    #   .border     = `surface` grey
    # Used in the agent panel diff view, git status sidebar, inline
    # diagnostics, and assistant panel mentions.
    #
    # Already set elsewhere: warning + error foregrounds + borders come
    # from the converter; the family pattern below adds their backgrounds.

    # warning + error — diagnostic pill backgrounds (the original gap that
    # motivated this whole block).
    style["warning.background"] = PALETTE["yellow"] + "1a"
    style["error.background"] = PALETTE["red"] + "1a"

    # info: informational diagnostics, agent panel hint icons.
    style["info"] = PALETTE["blue"]
    style["info.background"] = PALETTE["blue"] + "1a"
    style["info.border"] = PALETTE["surface"]
    # success: agent panel success states, test pass indicators.
    style["success"] = PALETTE["green"]
    style["success.background"] = PALETTE["green"] + "1a"
    style["success.border"] = PALETTE["surface"]
    # predictive: AI / Copilot ghost text colour. Without this, ghost text
    # falls back to a value that fights with comment colour. Use the muted
    # comment grey so suggestions read as ghostly but legible.
    style["predictive"] = PALETTE["surface_higher"]
    style["predictive.background"] = PALETTE["surface_higher"] + "1a"
    style["predictive.border"] = PALETTE["surface"]
    # renamed: git "renamed" status in the project panel.
    style["renamed"] = PALETTE["blue"]
    style["renamed.background"] = PALETTE["blue"] + "1a"
    style["renamed.border"] = PALETTE["surface"]
    # unreachable: dead-code dimming (LSP unreachable diagnostic). Should
    # read as faded — dimmer than comments.
    style["unreachable"] = PALETTE["surface_high"]
    style["unreachable.background"] = PALETTE["surface_high"] + "1a"
    style["unreachable.border"] = PALETTE["surface"]

    # Add .background and .border to families that already have a foreground
    # set by the converter. The agent panel + project diff views are where
    # these matter most — they pill changed/added/removed regions using
    # these backgrounds.
    style["conflict.background"] = PALETTE["purple"] + "1a"
    style["conflict.border"] = PALETTE["surface"]
    style["created.background"] = PALETTE["green"] + "1a"
    style["created.border"] = PALETTE["surface"]
    style["deleted.background"] = PALETTE["red"] + "1a"
    style["deleted.border"] = PALETTE["surface"]
    style["hidden.background"] = PALETTE["surface_higher"] + "1a"
    style["hidden.border"] = PALETTE["surface"]
    style["hint.background"] = PALETTE["surface_higher"] + "1a"
    style["hint.border"] = PALETTE["surface"]
    style["ignored.background"] = PALETTE["surface_high"] + "1a"
    style["ignored.border"] = PALETTE["surface"]
    style["modified.background"] = PALETTE["yellow"] + "1a"
    style["modified.border"] = PALETTE["surface"]

    # --- Icons -----------------------------------------------------------
    # Most icon colours can inherit from text, but icon.accent is what
    # tints toggled-on icon buttons (active filter indicators, selected
    # toolbar tools).
    style["icon"] = PALETTE["fg"]
    style["icon.muted"] = style.get("text.muted", PALETTE["surface_higher"])
    style["icon.disabled"] = PALETTE["surface_high"]
    style["icon.accent"] = PALETTE["blue"]

    # Accents — used for multi-buffer headers, mention highlights, etc.
    # Use the syntax palette for visual consistency.
    style["accents"] = [
        PALETTE["yellow"],
        PALETTE["teal"],
        PALETTE["red"],
        PALETTE["green"],
        PALETTE["purple"],
        PALETTE["blue"],
        PALETTE["orange"],
        PALETTE["purple_dim"],
    ]

    # Players — primary cursor + multi-cursor palette.
    # Player 0 is the local cursor: yellow per Cobalt Next's editorCursor.foreground.
    # Selection background: editor.selectionBackground = #4f5b66.
    # Other players use distinct accent colours for collaborative cursors.
    style["players"] = [
        {  # local cursor — Cobalt Next signature yellow
            "cursor":     PALETTE["yellow"],
            "selection":  PALETTE["surface_high"] + "80",  # 50% alpha
            "background": PALETTE["yellow"],
        },
        {
            "cursor":     PALETTE["teal"],
            "selection":  PALETTE["teal"] + "33",
            "background": PALETTE["teal"],
        },
        {
            "cursor":     PALETTE["green"],
            "selection":  PALETTE["green"] + "33",
            "background": PALETTE["green"],
        },
        {
            "cursor":     PALETTE["purple"],
            "selection":  PALETTE["purple"] + "33",
            "background": PALETTE["purple"],
        },
        {
            "cursor":     PALETTE["red"],
            "selection":  PALETTE["red"] + "33",
            "background": PALETTE["red"],
        },
        {
            "cursor":     PALETTE["blue"],
            "selection":  PALETTE["blue"] + "33",
            "background": PALETTE["blue"],
        },
        {
            "cursor":     PALETTE["orange"],
            "selection":  PALETTE["orange"] + "33",
            "background": PALETTE["orange"],
        },
    ]


# ---------------------------------------------------------------------------
# Apply fixes to one variant
# ---------------------------------------------------------------------------

def apply_fixes(theme):
    """Apply syntax fixes, additions, and UI polish to a single theme dict."""
    style = theme["style"]
    syntax = style.setdefault("syntax", {})

    for token, value in SYNTAX_FIXES.items():
        # Replace wholesale (not merge), so wrong style flags get cleared.
        syntax[token] = deepcopy(value)

    for token, value in SYNTAX_ADDITIONS.items():
        syntax[token] = deepcopy(value)

    # Sort syntax tokens alphabetically for predictable diffs.
    style["syntax"] = dict(sorted(syntax.items()))

    shared_ui_polish(style)
    return theme


# ---------------------------------------------------------------------------
# Build the family
# ---------------------------------------------------------------------------

def load_variant(filename):
    with open(CONVERTER_OUTPUT_DIR / filename) as f:
        theme = json.load(f)
    # Strip the per-variant $schema; the family-level one wins.
    theme.pop("$schema", None)
    return theme


def main():
    main_theme = apply_fixes(load_variant("cobalt-next.json"))
    dark_theme = apply_fixes(load_variant("cobalt-next-dark.json"))
    minimal_theme = apply_fixes(load_variant("cobalt-next-minimal.json"))

    family = {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Cobalt Next",
        "author": "David Leininger (Cobalt Next, MIT) — Zed port",
        "themes": [main_theme, dark_theme, minimal_theme],
    }

    payload = json.dumps(family, indent=2) + "\n"

    REPO_THEME_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPO_THEME_FILE.write_text(payload)

    ZED_THEMES_DIR.mkdir(parents=True, exist_ok=True)
    zed_theme_file = ZED_THEMES_DIR / "cobalt-next.json"
    zed_theme_file.write_text(payload)

    print(f"wrote {REPO_THEME_FILE}  ({REPO_THEME_FILE.stat().st_size} bytes)")
    print(f"wrote {zed_theme_file}  ({zed_theme_file.stat().st_size} bytes)")
    print(f"{len(family['themes'])} variants in family")
    print(f"syntax tokens per variant: {len(main_theme['style']['syntax'])}")


if __name__ == "__main__":
    main()
