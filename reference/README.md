# Reference — building and understanding the Cobalt Next Zed port

This directory contains everything needed to rebuild the Cobalt Next Zed theme from the upstream VS Code source, plus evergreen reference material about Cobalt Next, Zed's theme system, and the specific decisions that shaped the port.

## Layout

```
reference/
├── README.md                    # this file
├── build-theme.py               # synthesis script (the whole port logic)
├── syntax-rules.md              # Cobalt Next rule inventory + palette + accepted losses
├── notes.md                     # Zed theme quirks + port-specific decisions
├── vscode/                      # upstream Cobalt Next VS Code source
│   ├── CobaltNext.json          #   main variant (input)
│   ├── CobaltNext-Dark.json     #   dark variant (input)
│   ├── CobaltNext-Minimal.json  #   minimal variant (input)
│   └── LICENSE                  #   upstream licence (MIT, David Leininger)
└── converter-output/            # Zed theme_importer output (intermediate)
    ├── cobalt-next.json         #   from theme_importer on CobaltNext.json
    ├── cobalt-next-dark.json    #   from theme_importer on CobaltNext-Dark.json
    └── cobalt-next-minimal.json #   from theme_importer on CobaltNext-Minimal.json
```

## How the build works

The port is a two-stage pipeline:

1. **Automated conversion.** Zed's own `theme_importer` CLI (from the `zed-industries/zed` source tree) reads a VS Code theme JSON and produces a Zed theme JSON. This does the bulk of the work: UI chrome mapping, terminal ANSI colours, and a reverse-weighted-match from Zed's 40-token syntax set to VS Code's scope vocabulary. See [notes.md](notes.md#how-the-zed-converter-works) for details.

2. **Hand-polish.** `build-theme.py` loads the three converter outputs, applies fixes for the tokens the converter got wrong or missed, wraps them as a Zed theme family, and writes the final `themes/cobalt-next.json` at the repo root (and installs a copy at `~/.config/zed/themes/cobalt-next.json` for live testing).

All of the port's opinionated logic lives in `build-theme.py` — the converter outputs in `converter-output/` are mechanical artifacts that only need regenerating if the upstream VS Code theme or Zed's converter changes. See [syntax-rules.md](syntax-rules.md) for what Cobalt Next's rules look like and where each one ends up, and [notes.md](notes.md) for *why* specific fixes exist.

## Rebuilding

### Fast path: just re-run the synthesis

If you only want to tweak the palette or the fix dictionaries:

```bash
python3 reference/build-theme.py
```

This rewrites `themes/cobalt-next.json` and `~/.config/zed/themes/cobalt-next.json` from the existing `converter-output/` files. Reload themes in Zed (command palette → `zed: reload themes` or restart).

### Full path: regenerate converter outputs from upstream

Do this if the upstream VS Code theme changes, or if you want to rebase on a newer version of Zed's converter.

**1. Clone Zed.**

```bash
git clone https://github.com/zed-industries/zed.git /tmp/zed
cd /tmp/zed
```

**2. Build `theme_importer`.**

```bash
cargo build -p theme_importer
```

First build takes a few minutes — Zed's workspace has hundreds of crates. Subsequent builds are fast.

**3. Run the converter on each of the three VS Code files.** From this repo's root, with `/tmp/zed` containing the Zed source:

```bash
/tmp/zed/target/debug/theme_importer \
  --warn-on-missing \
  -o reference/converter-output/cobalt-next.json \
  reference/vscode/CobaltNext.json

/tmp/zed/target/debug/theme_importer \
  --warn-on-missing \
  -o reference/converter-output/cobalt-next-dark.json \
  reference/vscode/CobaltNext-Dark.json

/tmp/zed/target/debug/theme_importer \
  --warn-on-missing \
  -o reference/converter-output/cobalt-next-minimal.json \
  reference/vscode/CobaltNext-Minimal.json
```

`--warn-on-missing` logs every token the converter couldn't match to stderr; pipe it through `2> warnings.txt` if you want to review.

**4. Run the synthesis.**

```bash
python3 reference/build-theme.py
```

That's the whole chain. If the converter's behaviour has changed, the synthesis fixes in `build-theme.py` may need adjusting — diff `converter-output/cobalt-next.json` against git to see what moved.

## Refreshing the upstream VS Code theme

The `reference/vscode/` files are verbatim copies of `cobaltnext-vscode/themes/*.json` from [davidleininger/cobaltnext-vscode][upstream]. To pick up upstream changes:

```bash
git clone --depth 1 https://github.com/davidleininger/cobaltnext-vscode /tmp/cn
cp /tmp/cn/themes/CobaltNext*.json reference/vscode/
cp /tmp/cn/LICENSE reference/vscode/LICENSE
```

Then re-run the converter + synthesis steps above.

## Licence note on Zed's `theme_importer`

`theme_importer` is part of the `zed-industries/zed` source tree and is GPL-licensed. Using it as a build-time CLI tool is fine — its JSON output is data, not a derivative work in any meaningful sense, and nothing from the Zed source tree is shipped in the final theme.

[upstream]: https://github.com/davidleininger/cobaltnext-vscode
