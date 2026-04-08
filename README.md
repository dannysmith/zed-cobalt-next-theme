# Cobalt Next for Zed

A port of [David Leininger's Cobalt Next][upstream] VS Code theme to Zed.

Cobalt Next is *not* Cobalt2. It's the Oceanic Next palette (slate `#1b2b34` background, warm `#fac863` yellow, `#5fb3b3` teal, `#ed6f7d` red, `#99c794` green, `#c5a5c5` purple, `#eb9a6d` orange) used in the Cobalt2 *spirit* — italic comments and language variables, angry-red tags, yellow types, blue functions.

## Variants

The family ships three variants, all dark:

- **Cobalt Next** — main variant; slate editor background
- **Cobalt Next Dark** — darker editor background with teal-tinted selections
- **Cobalt Next Minimal** — as Dark, with a slightly lower-contrast tab bar

Switch between them via Zed's theme selector (`cmd-k cmd-t` or `theme selector: toggle`).

## Install

### Via Zed's extension index (once published)

Open the extensions panel (`cmd-shift-x`), search for "Cobalt Next", install, then pick it from the theme selector.

### Manually (before publishing, or to iterate)

Copy `themes/cobalt-next.json` into `~/.config/zed/themes/` and reload Zed's themes.

```bash
cp themes/cobalt-next.json ~/.config/zed/themes/cobalt-next.json
```

Running `reference/build-theme.py` also writes the file directly to `~/.config/zed/themes/cobalt-next.json` for fast iteration.

## Credits and licence

- **Original theme:** [Cobalt Next][upstream] by David Leininger (MIT, 2017). A copy of the upstream licence is preserved at [`reference/vscode/LICENSE`](reference/vscode/LICENSE).
- **Zed port:** Danny Smith, MIT.
- The `reference/vscode/` directory contains unmodified copies of the three upstream VS Code theme JSON files, used as input to the port.

## Development

See [`reference/README.md`](reference/README.md) for how the theme is built, the Cobalt Next rule inventory, and the specific decisions and trade-offs that shaped the Zed port.

[upstream]: https://github.com/davidleininger/cobaltnext-vscode
