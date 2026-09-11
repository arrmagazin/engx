# reference/

Source material, not part of the book.

These three handbooks are the single-cloud catalogs the Clouds chapter was distilled
from. Together they are around 68,000 words — roughly half the book, all of it vendor
reference. Keeping them here preserves the detail without letting one chapter outweigh
the other nine.

| File | What it is |
|---|---|
| `aws-handbook.md` | The AWS service catalog, its vocabulary, and the competency areas an infrastructure role is interviewed against. |
| `azure-handbook.md` | The same for Azure, with the differences from AWS called out rather than glossed over. |
| `gcp-handbook.md` | The same for Google Cloud. |

## What this folder is outside of

- **Outside `docs/`** — so it is not a chapter and has no place in the reading order.
- **Outside the checkers** — `.githooks/pre-commit` and the three `scripts/check_*.py`
  only ever see `docs/*.md`. Frontmatter, glossary and link conventions are not
  enforced here.
- **Outside the build** — `scripts/build_book.py` assembles `docs/` only. Nothing here
  reaches the EPUB or the PDF.

## The one rule

**No file under `docs/` may link into this folder.** Such a link would resolve in the
repository and be dead in the rendered book, and `check_links.py` would not catch it:
the checker verifies that a relative target exists on disk, which it does. Links in the
other direction are fine — these handbooks point into `../docs/` freely.

What `docs/07-clouds/` offers instead is a comparison: the same concept across all three
providers, in one table. That is the chapter's job. Exhaustive per-provider detail is
this folder's.
