# RLV Bible

**The New Testament: Real Life Version** — a light-to-moderate re-rendering of the World English Bible into plain modern English.

## Layout

One folder per book, numbered in canonical order so the tree sorts correctly:

```
01-genesis/genesis-ch-001.md
01-genesis/genesis-ch-002.md
...
66-revelation/revelation-ch-022.md
```

Each file holds one chapter. **Verses only** — no book title line, no chapter heading. Verse *V* sits on line *V*, so verse numbers are line numbers.

## Format rules

Every file must satisfy all of these:

- UTF-8 **with BOM** (bytes `EF BB BF`)
- **LF** line endings only, never CRLF
- file ends with a newline
- every line ends with exactly one trailing space
- straight quotes only (`"` and `'`), never curly
- no em dashes or en dashes, ever

## Source

Rendered from the **World English Bible (WEB)**, which is in the public domain.

## Status

- **New Testament: 27 books, 260 chapters, 7,953 verses.** Prose-swept through John and Acts 1–12.
- **Old Testament: 39 books, 929 chapters, 23,145 verses.** Imported, not yet prose-swept.
