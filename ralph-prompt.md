# Ralph Prompt — Revise the `docs/` Knowledge Base

You are running inside a Ralph loop. Every iteration feeds you the same pointer
prompt, and you arrive with no memory of the last one. **This file is your only
memory of intent; the ledger is your only memory of progress.** Read both, in
full, before doing anything else.

Repository: `~/Projects/engx`
Ledger: `.claude/docs-revision.local.md` (gitignored — never commit it)

## Mission

Bring `docs/` to publishable quality: excellent prose, consistent conventions,
ruthless brevity, a structure with no defects, and no gaps in coverage. Then
compose `README.md`, and finally rewrite `CLAUDE.md` so it describes the repo
that now exists.

The content is the product. There is no build, no site generator, no
`package.json`, and you will not add one.

---

## The Loop Contract

Do these five steps, in order, every single iteration.

1. **Orient.** Read this file. Read the ledger. Then check **your surface**:

   ```bash
   git status --porcelain -- docs README.md CLAUDE.md scripts .githooks
   ```

   Everything outside that list — `texts/`, `ralph-prompt.md`, `.claude/` — is
   the user's. They steer you by editing those between iterations. Never commit,
   stage, or revert them. If your surface is dirty, the previous iteration died
   mid-item: inspect the changes, then either finish and commit that item or
   `git checkout --` it away. Never start a new item on a dirty surface.
2. **Claim.** Take the **first unchecked item** in the ledger, in file order.
   Phases are strictly ordered — never start a Phase N item while any Phase N-1
   item is unchecked. If the ledger does not exist, your item is Phase 0.
3. **Do exactly that one item.** Not two. Not "while I'm here". Scope creep is
   the failure mode this loop exists to prevent.
4. **Verify** (see *Verification Gates*), then commit — one commit per item,
   message in `docs(<folder>): <what changed>` form.
5. **Record.** Tick the item's box in the ledger, append a one-line note of what
   you actually did, and append any *new* item the work revealed to the correct
   phase. Then stop the iteration.

**Never re-open a checked item.** If a finished file still bothers you, that is
polish appetite, not a defect — leave it. Endless re-polishing is how Ralph
loops fail to terminate. The only exception is an item a later phase explicitly
names.

### Blocked items — the three-strikes rule

If an item defeats you, append `(strike 1)` to its ledger line and move to the
next item. On the third strike, rewrite the line as
`- [x] BLOCKED — <item> — <one-sentence reason>` and move on permanently.
Blocked items do **not** prevent completion, but they **must** be listed in your
final report. Never silently drop one, and never mark one done to escape.

---

## Ledger Format

Write it once, in Phase 0, to `.claude/docs-revision.local.md`:

```markdown
# Docs Revision Ledger

## Conventions decided in audit
- Heading case: <Title Case | sentence case>
- Folder numbering plan: <old> -> <new>, ...
- <any other repo-wide call the audit made>

## Phase 1 — Structure
- [ ] <one concrete, independently committable change>

## Phase 2 — Content
- [ ] docs/<path>.md — <the specific defects found here>

## Phase 3 — Coverage
## Phase 4 — Cross-cutting
## Phase 5 — Review
## Phase 6 — README.md
## Phase 7 — CLAUDE.md
## Phase 8 — Completion gate
```

Every item must be small enough to finish and commit in one iteration, and
specific enough that a fresh iteration knows what "done" means without
re-deriving it. "Improve architecture docs" is not an item. "docs/03-architecture/
02-architecture.md — H1 restated in lead sentence, three H3s under no H2, two
paragraphs duplicating 03-quality_attributes.md" is.

---

## Phases

### Phase 0 — Audit (runs exactly once, and never again)

Use **`superpowers:dispatching-parallel-agents`**. Dispatch one read-only agent
per top-level folder under `docs/`, plus one cross-cutting agent. Each folder
agent reports, per file: frontmatter defects, heading-hierarchy defects,
concrete prose cuts available, table-convention breaches, dead links, factual
claims that look invented, and content duplicated elsewhere. The cross-cutting
agent reports: numbering collisions, filename-case inconsistencies, terminology
that drifts between folders, concepts explained in more than one place, and
topics the book promises but does not cover.

Then use **`superpowers:writing-plans`** to turn those reports into the ledger.
Decide the repo-wide conventions (heading case, folder numbering plan) here,
once, and write them at the top — later phases obey them without re-litigating.

Commit nothing in Phase 0. The ledger is gitignored.

Known defects to confirm and fold in — this list is a starting point, not the
whole audit:

- `03-architecture` and `03-system_design` share prefix `03`; `09-cloud-aws` and
  `09-cloud-azure` share `09`.
- Four files in `03-system_design/` all claim prefix `04`; two in
  `04-development_process/` both claim `04`.
- Folder and file names mix `snake_case` (`00-software_engineering`,
  `03-quality_attributes.md`) with `kebab-case`.
- `CLAUDE.md` advertises `06-testing` and `40-interview` folders that do not
  exist, while interview material sits in three unrelated folders.
- `README.md` is a one-line stub. `docs/welcome.md` is a front door with no
  table of contents.
- Most folders have no overview doc.
- **`scripts/check_glossary.py` fails today**, before you change anything. As of
  the last baseline run: four mutually-defining term pairs in
  `docs/00-software_engineering/00-glossary.md` (`Solution`/`Stakeholder`,
  `Stakeholder`/`Value`, `Solution`/`State`, `Objectives`/`Requirements`), and
  `Component` in `docs/03-system_design/01-overview.md` both restating itself and
  ending in a period. Re-run the checker yourself to get the current list — do
  not trust this snapshot. Each failure is its own Phase 4 ledger item; fixing a
  mutual definition means redefining one side from first principles, not deleting
  a row.

### Phase 1 — Structure

Fix the shape of the tree. Invariants when this phase closes:

- Every top-level folder under `docs/` has a **unique** two-digit prefix, and
  numeric order is reading order.
- Every file within a folder has a **unique** two-digit prefix.
- Every folder and file name is `kebab-case`.
- Every folder holds exactly one `00-*.md` overview that states what the folder
  covers and links each file in it.
- `docs/` root holds at most one unnumbered file, and it is the book's entry
  point.

Rules: move files with `git mv`, never delete-and-recreate. **Update every
inbound link in the same commit as the move** — a move that strands a link is an
incomplete item. One folder per ledger item. Merging a thin doc into another is
a move of its content plus a `git rm`, recorded as one item; never delete
content that has no new home.

### Phase 2 — Content

One file per iteration, against the *Editorial Bar* below. For files needing
heavy work, use **`superpowers:subagent-driven-development`**: dispatch a
subagent with the file path, the Editorial Bar, and that file's ledger line,
then review its diff yourself before committing. You own the commit.

### Phase 3 — Coverage

Fill the gaps the audit named. A new doc must earn its place: it exists because
the book claims or implies the topic and does not deliver it, not because the
topic is interesting. New docs obey the Editorial Bar and Phase 1 invariants
from their first commit.

### Phase 4 — Cross-cutting

- Every relative link resolves to a real file; every `/images/*.svg` exists in
  `images/`.
- Every concept has exactly one canonical home. Elsewhere it is linked, not
  re-explained.
- Terminology matches `docs/00-software_engineering/00-glossary.md`; where a doc
  and the glossary disagree, fix one of them deliberately.
- Every glossary table obeys the Glossary conventions in `CLAUDE.md`.

**Bounded tooling exception:** you may add exactly one new script,
`scripts/check_links.py`, following the shape of the existing checkers (paths as
argv, human-readable failures, exit 1 on error), and wire it into
`.githooks/pre-commit`. This is the only new tooling permitted anywhere in this
loop. If you add it, write the test first — see
**`superpowers:test-driven-development`** — using a fixture with one good and
one broken link.

### Phase 5 — Review

Use **`superpowers:requesting-code-review`** on the full accumulated diff
(`git diff main...HEAD`), asking specifically for: prose that survived that
should not have, conventions applied inconsistently across folders, claims that
look invented, and structure that is merely different rather than better.

Triage the response with **`superpowers:receiving-code-review`** — verify each
point against the actual file before acting. Reviewers are wrong sometimes;
agreeing with a wrong review is worse than disagreeing with a right one. Append
the points you accept to the ledger as Phase 5 items and work them normally.

### Phase 6 — README.md

Compose the repository front door for someone who just landed on it and has
never seen the book. It states what this repo is, who it is for, how the
numbered-folder structure reads, links the top-level sections, and says how to
contribute (frontmatter convention, `git config core.hooksPath .githooks`).
It is not a copy of `docs/welcome.md` and not a copy of `CLAUDE.md` — README
addresses a human reader arriving cold; `CLAUDE.md` addresses an agent about to
edit. Keep it under roughly 60 lines. It is at the repo root, so it takes no
OKF frontmatter.

### Phase 7 — CLAUDE.md

Rewrite `CLAUDE.md` so every sentence is true of the repo that now exists.
Required work:

- Correct the Structure section to the real folder list, with no invented
  folders. Prefer describing the numbering *rule* over listing folders that will
  drift again.
- Fold in every convention the audit decided and this loop enforced: heading
  case, kebab-case naming, the overview-doc rule, the one-canonical-home rule,
  the Editorial Bar in condensed form.
- Document `scripts/check_links.py` if Phase 4 added it, and the updated hook.
- Delete guidance that no longer applies. Shrinking `CLAUDE.md` is a good
  outcome; it competes for context on every future session, so every line must
  pay for itself.
- Keep the existing Frontmatter and Glossary conventions sections — reconcile
  them with reality rather than rewriting them for style.

### Phase 8 — Completion gate

See *Completion Gate* below. This phase has exactly one item.

---

## Editorial Bar

**Every doc, in this order:** OKF frontmatter → `# H1` byte-identical to the
frontmatter `title` → optional image line → a lead of one to three sentences
saying what the doc covers and who it serves → body.

**Frontmatter** is exactly four fields: `type` (always `Guide`), `title`,
`description` (one sentence, under ~140 chars, no trailing period issues), and
`tags` (lowercase, kebab-case). Never add OKF's optional provenance fields.

**Headings:** exactly one H1. No skipped levels — an H3 never follows an H1
directly. No two sibling headings share text. Heading case follows the
convention the audit recorded in the ledger.

**Brevity — delete on sight:**

- Throat-clearing: "In this section we will", "It is important to note that",
  "As mentioned above", "Let's dive in".
- A first sentence that restates the H1.
- A sentence whose only job is to announce the table or list beneath it.
- Intensifiers that do not change the claim: very, quite, really, simply, just,
  extremely, basically.
- A closing "Summary" or "Conclusion" section that repeats the body.
- Any paragraph a reader could skip without losing the point.

**Prefer structure to prose:** three or more items sharing a shape belong in a
table or list. One idea per paragraph; a paragraph past ~5 lines is a candidate
for splitting.

**Language:** standard English. No rare words, no idioms, no metaphor that a
non-native reader must decode. Say the thing.

**Factual discipline:** no invented numbers, benchmarks, dates, versions, or
citations. A claim that depends on a vendor or version names it. A claim you
cannot support gets cut — not hedged. Hedging a shaky claim keeps the noise and
adds cowardice.

**Tables:** bold the first column's term. No trailing periods in cells. Never a
raw newline inside a cell — use `<br>`. Glossary tables additionally obey the
Glossary conventions in `CLAUDE.md`.

**Links:** relative between docs, resolving to a real file. Link a concept's
canonical home rather than re-explaining it.

---

## Verification Gates

Before **every** commit:

```bash
git config core.hooksPath .githooks   # idempotent; the hook enforces frontmatter
python3 scripts/check_okf_frontmatter.py $(git diff --cached --name-only --diff-filter=ACM -- 'docs/*.md')
python3 scripts/check_glossary.py $(git diff --cached --name-only --diff-filter=ACM -- 'docs/*.md')
```

If a checker fails in a way you did not expect, use
**`superpowers:systematic-debugging`**. Do not "fix" it by loosening the
checker, deleting the table, or skipping the hook. The checkers encode the
repo's rules; when a checker and your edit disagree, your edit is the suspect.

---

## Completion Gate

Before you even consider the promise, run **`superpowers:verification-before-completion`**.
Then produce evidence — actually run these, actually read the output:

```bash
python3 scripts/check_okf_frontmatter.py $(find docs -name '*.md')   # exit 0
python3 scripts/check_glossary.py $(find docs -name '*.md')          # exit 0
python3 scripts/check_links.py $(find docs -name '*.md')             # exit 0, if it exists
git status --porcelain -- docs README.md CLAUDE.md scripts .githooks  # empty
```

Emit `<promise>DONE</promise>` only when **all** of these are true:

1. Every ledger box is ticked — done or explicitly BLOCKED.
2. All three commands above pass, and you have seen their output this iteration.
3. Phase 1's structural invariants hold, verified by listing the tree.
4. `README.md` and `CLAUDE.md` are rewritten, and every factual statement in
   `CLAUDE.md` matches the tree you just listed.
5. Your surface is clean and every change you made is committed. Unrelated
   pending changes elsewhere in the tree are the user's — leave them alone and
   do not let them block you.

With the promise, print a short report: what changed at the top level, and every
BLOCKED item with its reason.

**Do not emit the promise because the loop feels long, because you suspect you
are near the iteration cap, or because you cannot see what is left.** If you
cannot see what is left, that is a signal to re-read the ledger, not to exit. A
false promise is the one unrecoverable failure available to you here.

## Never

- Do more than one ledger item in an iteration.
- Re-run Phase 0 once a ledger exists.
- Re-edit a file whose item is already checked.
- Add tooling, dependencies, or a site generator (the `check_links.py` exception
  above is the whole allowance).
- Delete content that has no new home.
- Commit the ledger or `.claude/*.local.md`.
- Invent a fact to fill a gap. An honest gap beats a confident fabrication.
