# 📘 Documentation Contract — Django Lecture Series

> **Status:** Active · **Scope:** every lecture folder (`A###_…`) and everything under `docs/`
> **Audience:** any agent or human who writes, edits, or reviews documentation in this repository.
>
> This file is the **permanent documentation contract**. It defines *how* documentation is
> written so that 50 lectures from now, the series still reads like one coherent book.
> Do not duplicate these rules inside lecture files — link here instead.

---

## 1. Repository Documentation Map

```
repo-root/
├── README.md                        # Series hub: about, learning path, TOC, progress
├── docs/                            # Shared documentation infrastructure
│   ├── AGENTS.md                    # ← this contract (how to write)
│   ├── MEMORY.md                    # Learning ledger: glossary, mental models,
│   │                                #   recall bank, revision schedule, progress
│   ├── styles/
│   │   └── global.css               # The ONLY stylesheet — shared by all lectures
│   └── templates/
│       └── README-TEMPLATE.md       # Skeleton every new lecture starts from
├── A001_Introduction_What_is_Django/
│   └── README.md                    # One lecture = one folder = one README
├── A002_.../
└── ChaiAurCode/                     # ⛔ The actual Django project — NEVER edited
    └── ...                          #   by documentation work (read-only reference)
```

**Hard rule:** documentation work never modifies `ChaiAurCode/**`, `.venv/**`, or any
application source code. The Django project is a *learning artifact we document about*,
referenced by path, never rewritten.

---

## 2. Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Lecture folder | `A###_Title_Case_With_Underscores` | `A001_Introduction_What_is_Django` |
| Lecture README | always `README.md` inside the folder | `A001_…/README.md` |
| Lecture code | `A` + 3-digit zero-padded number | `A001`, `A002` |
| Headings | Sentence case after the emoji | `## 🧠 What Is Django?` |
| Terms | Use the exact spelling recorded in `docs/MEMORY.md` glossary | `URL dispatcher` |
| Internal links | Relative paths between chapters | `../A002_…/README.md` |

The `A` prefix reserves the namespace; a future practical/lab track could use `B`.

---

## 3. Source-of-Truth Rules (the honesty contract)

Priority order when writing a lecture:

1. **Lecture source material** — transcript/notes if present in the lecture folder
   (look for `_source/` or any material the owner dropped in). Primary source.
2. **The owner's stated topic list** for that lecture (chat request / plan).
3. **Official Django documentation** (`djangoproject.com`) — authoritative for all
   general Django claims (philosophy, features, architecture).
4. **This repository's own code** (`ChaiAurCode/`) — for concrete, verified examples.

Derived rules:

- Never present supplementary knowledge as if it came from the lecture. Mark it with
  the **📌 Beyond the lecture** badge.
- Never contradict the lecture source silently. If a source seems factually wrong,
  keep the source's framing, add a `> ⚠️ **Discrepancy note:** …` explaining the
  correction explicitly.
- Every lecture README ends with a **"Sources used"** footer listing what was actually used.
- If no lecture source exists (as was the case for A001), say so openly in the
  chapter's opening note and in the footer. No pretending.

---

## 4. README Structure Contract

Every lecture README follows the canonical section order below. Sections come from
`docs/templates/README-TEMPLATE.md`. Omit a section only with a good reason
(e.g. no code in a pure-theory lecture) — never reorder, never invent new top-level
sections casually.

```
# 🚀 A### — Title            ← H1 exactly once, with lecture code
badge line                   ← Lecture no. · track · difficulty · status
opening source note          ← when source material is absent/partial
## 🧭 What You Will Learn    ← outcomes as a checklist
## 🎯 Why This Lecture Matters
## ✅ Prerequisites             ← honest, minimal; optional items marked 📌
## 🧠 <Core concept sections>   ← 1–n main teaching sections (the body)
## 🗺️ diagrams                  ← embedded within body sections, not dumped at the end
## 🧱 Important Vocabulary    ← glossary table w/ memory hooks
## 💡 Real-World Analogy
## ❌ Common Beginner Mistakes
## 🧠 Common Misconceptions
## 🧪 Practical Example
## 🎯 Interview Perspective
## 🔁 Active Recall          ← <details> answers
## 📝 Quick Revision
## 🧠 Final Mental Model
## ❓ FAQ
## 🏁 Learning Checkpoints   ← self-test gates ("I can …" checkboxes), referenced by the revision schedule
## 🏋️ Exercises              ← 4 levels: recall → understanding → application → interview
## 🏁 Final Takeaways
## 🔄 Next Lecture Connection
--- Sources used + chapter navigation footer
```

---

## 5. Explanation Depth Standards

The bar is **textbook depth**, not cheat-sheet depth:

- **Why before how.** Every concept answers "why does this exist / what problem does
  it solve" before showing mechanics.
- **Concept formula:** definition → analogy → cause → effect → minimal example →
  common confusion. A section missing most of these is too shallow.
- Beginner-friendly sentence first, technically precise restatement second.
- No buzzword lists. Each feature gets: name, simple explanation, why it exists,
  how it helps, small example, analogy, caveat/misconception.
- Code shown in a lecture README must not exceed what that lecture has introduced.

---

## 6. CSS Usage Rules (read the truth before styling anything)

- **GitHub fact:** README rendering on github.com **cannot load external or per-file
  CSS**. Never claim otherwise in documentation, and never add `<style>` blocks or
  inline styles to lecture READMEs expecting GitHub to honor them (GitHub strips them).
- **Design strategy — two layers, one visual language:**
  1. **GitHub-native layer (primary):** GFM alerts (`> [!NOTE]`, `> [!TIP]`,
     `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`), tables, task lists,
     `<details>/<summary>`, Mermaid fenced blocks, emoji hierarchy. Renders everywhere,
     no CSS required.
  2. **CSS enhancement layer (secondary):** `docs/styles/global.css` styles the same
     vocabulary for CSS-aware renderers (VS Code preview extensions, pandoc, MkDocs,
     future docs site): design tokens, headings, tables, code, callout classes
     (`.note`, `.tip`, `.warning`, `.important`, `.caution`), cards (`.learning-card`,
     `.example-card`, `.interview-card`, `.remember`, `.misconception`, `.checkpoint`,
     `.revision`), `.badge*`, `.diagram`, `.doc-footer`, `<details>`, dark mode, print.
- **One stylesheet only.** Style improvements happen in `global.css`; never create
  per-lecture CSS files.
- **Markdown must stand alone.** Every lecture reads perfectly with CSS disabled —
  meaning is carried by words, structure, tables and alerts, never by styling alone.
- **Class hooks are optional sugar.** Wrap content in `<div class="…">` sparingly
  (remember-boxes, interview cards) only where a plain GFM alert would lose meaning.

---

## 7. Emoji Conventions (fixed vocabulary — do not improvise)

| Emoji | Meaning | Typical place |
|---|---|---|
| 🚀 | lecture / major topic | H1, major openings |
| 🧭 | guidance, learning outcomes | "What You Will Learn" |
| 🎯 | objectives; interview section | outcomes, interview |
| 🧠 | mental model, memory, misconceptions | mental-model sections |
| 💡 | insight / tip | tips (with `[!TIP]`) |
| ⚠️ | warning / caveat | warnings (with `[!WARNING]`) |
| ❌ | mistake / wrong idea | mistakes, misconception tables |
| ✅ | correct / checklist item | checklists, IS/IS-NOT tables |
| 🔄 | process / flow | lifecycle, next-lecture |
| 🗺️ | diagram / visual map | Mermaid sections |
| 📌 | beyond-the-lecture (supplementary) | labeled extras |
| 📝 | revision | quick revision |
| ❓ | FAQ | FAQ |
| 🏋️ | exercises | exercises |
| 🏁 | finish / takeaways | final takeaways |
| 🧪 | practical example | examples |
| 🧷 | memory hook | glossary entries |
| 📚 | series / hub | hub README |

Rules: emojis mark **structure**, not sentences. Never emoji-per-sentence; never use an
emoji outside this table's meaning without first updating this contract.

---

## 8. Mermaid Diagram Rules

- Add a diagram **only** when a process, hierarchy, flow or relationship is genuinely
  easier to grasp visually. Diagrams are never decoration.
- Prefer `flowchart TD/LR` and `sequenceDiagram`. Keep ≤ 12 nodes. Label edges with
  what *moves* along them (`-- "HTTP request" -->`), not with vague arrows.
- **Syntax safety (the #1 breakage source):** quote every node label containing
  spaces, parentheses, colons or slashes: `A["Browser (client)"]`. Never leave
  unquoted `() : /` inside labels.
- Consistent reading direction across the series: inputs top/left, outputs bottom/right.
- Every diagram gets one sentence before it saying what the reader should *see* in it.
- Verify rendering (GitHub preview or mermaid.live) before marking a chapter done.

---

## 9. Code Block Standards

- Always fenced **with a language identifier** (```python, ```bash, ```text).
- Code must be **syntactically correct** and runnable within what the lecture has
  taught, or explicitly marked as simplified/pseudo.
- Comments explain *why*, not restate *what*.
- Every code block is followed by an explanation of the load-bearing lines.
- Prefer examples connected to this repository's `ChaiAurCode/` project where natural.
- Terminal commands: no `$` prompts inside the fence; one fence per flow.
- No giant dumps: examples over ~25 lines get split and narrated between parts.

---

## 10. Terminology & Consistency Rules

- `docs/MEMORY.md` §2 glossary is the **single source of truth** for term spelling and
  wording. Check it before writing; add new terms *while* writing a chapter, never "later".
- Mental models/analogies are registered in `MEMORY.md` §3 and **reused**, not
  reinvented — consistent analogies compound retention.
- Cross-lecture consistency: when a later chapter builds on an earlier one, open with a
  2–4 line **recap box** linking the earlier chapter
  (`[A001](../A001_Introduction_What_is_Django/README.md)`), then move on.

---

## 11. Avoiding Duplication Between Lectures

- A concept gets its **full explanation exactly once** — in the lecture that introduces it.
- Later lectures **link** to it; they may summarize in ≤ 3 lines, never re-derive.
- Glossary definitions live in `MEMORY.md` (short form) and in the introducing chapter
  (deep form). No third copy anywhere.
- If you notice duplication while editing: extract to the earliest owning chapter and
  replace the copy with a link.

---

## 12. Updating Existing Documentation Safely

- Read the chapter (and its "Sources used" footer) before touching it.
- Preserve structure: the §4 canonical order is stable; improvements happen *inside* sections.
- Content corrections are allowed when accuracy demands them, but add a
  `> ⚠️ **Discrepancy note:**` if they contradict a lecture source.
- Never delete another chapter's cross-links; repoint them if targets moved.
- Renaming/moving files: search the repo for inbound links to the old path and update
  them, plus the hub table, in the same change.
- After editing a lecture: update `MEMORY.md` if terms/mental models changed, and the
  hub status column if the lecture status changed.

---

## 13. New-Lecture Lifecycle (follow in order)

1. **Folder** — create `A###_Title_Underscores/` at repo root (zero-padded number).
2. **Skeleton** — copy `docs/templates/README-TEMPLATE.md` → `README.md` inside it.
3. **Source check** — look for lecture transcript/notes in the folder; declare the
   source situation in the opening note (§3).
4. **Write** — follow §4 structure and §5 depth standards; diagrams per §8, code per §9.
5. **Register** — add glossary terms (MEMORY §2), mental models (§3), recall questions
   (§4), revision schedule row (§5).
6. **Hub** — add the lecture row to the root `README.md` table and progress section.
7. **Checklist** — run §14; only then is the chapter done.
8. **Publish** — commit the change and `git push origin main`. A chapter is only "done"
   when it is on origin — never leave finished work committed locally.

---

## 14. Quality Checklist (gate before any chapter is "done")

- [ ] H1 exactly once; lecture code correct; badge line present
- [ ] Source situation honestly declared; 📌 on every beyond-lecture item
- [ ] Canonical §4 section order followed (omissions justified)
- [ ] Every concept: why-before-how; definition → analogy → cause→effect → example → confusion
- [ ] Mermaid diagrams only where they truly clarify; syntax verified (labels quoted)
- [ ] Code blocks: language tag, correct, commented, explained after
- [ ] Emojis match §7 table; no emoji-per-sentence
- [ ] All new terms in the MEMORY glossary; spellings match it
- [ ] Active recall uses `<details>`; exercises cover 4 levels
- [ ] Quick-revision sheet present; final mental model connects all chapter concepts
- [ ] "Sources used" footer + prev/next navigation links valid (relative paths)
- [ ] Renders on GitHub (GFM-only constructs) and reads fine without CSS
- [ ] `ChaiAurCode/**` untouched; only documentation files changed
- [ ] Change committed and pushed to `origin` (`git push origin main`) — done means shipped

---

*This contract evolves only by explicit edit to this file; such edits are announced at
the top of the `docs/MEMORY.md` update log.*


