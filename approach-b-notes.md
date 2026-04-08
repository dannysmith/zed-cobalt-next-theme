# Approach B — Cobalt2 Zed UI-structure sanity check

> Demoted from Phase 1 mainstay after Phase 0 found Cobalt2 Zed is a
> Dracula-syntax reskin (see `phase-0-findings.md`). This is a 10-minute
> structural scan only — no syntax mappings extracted.

## What Cobalt2 Zed populates that Approach C doesn't

Most of these are **legacy v0.1 status keys** that the current v0.2
schema may not need:

| Key set                                          | Notes |
|--------------------------------------------------|-------|
| `info`, `info.border`, `info.background`         | v0.1 only — replaced by `hint`/info-via-`text` semantics in v0.2. Skip. |
| `success`, `success.*`                           | v0.1 only. Skip. |
| `unreachable`, `unreachable.*`                   | v0.1 only. Skip. |
| `renamed`, `renamed.*`                           | v0.1 only. Skip. |
| `predictive`, `predictive.*`                     | v0.1 only — `predictive` is now a syntax token in v0.2. Skip. |
| `players` (5 populated entries)                  | **Worth copying the pattern.** Approach C has `players: []`. See Phase 2 worklist. |
| Multiple `*.border` and `*.background` siblings  | Cobalt2 Zed defines border/background siblings for `conflict`, `created`, `deleted`, `error`, `modified`, `warning`. Approach C only fills some. Worth checking which v0.2 actually accepts. |

## What Approach C has that Cobalt2 Zed doesn't

| Key                                          | Notes |
|----------------------------------------------|-------|
| `border`, `border.variant`                   | v0.2 additions. Approach C has them. |
| `editor.document_highlight.bracket_background` | v0.2 addition. |
| `vim.yank.background`                        | v0.2 addition. |
| `scrollbar.thumb.active_background`          | v0.2 addition. |

## Schema version

- Cobalt2 Zed: `v0.1.0`
- Approach C output: `v0.2.0` ← use this. v0.1 is end-of-life.

## Pattern Cobalt2 Zed gets right that we should imitate

The `players` array has the right shape:

```json
"players": [
    { "cursor": "<accent1>", "selection": "<accent1+88>", "background": "<accent1>" },
    { "cursor": "<accent2>", "selection": "<accent2+33>", "background": "<accent2>" },
    ...
]
```

For Cobalt Next we can populate this with the syntax palette
(`#fac863`, `#c5a5c5`, `#99c794`, `#5a9bcf`, `#ed6f7d`) — see Phase 2
worklist.

## Conclusion

No structural surprises. Approach C's UI block is in good shape against
the Cobalt2 Zed reference. The only meaningful gaps to fill manually
are `players` and `accents`. The legacy v0.1 keys can be ignored.
