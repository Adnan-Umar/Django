# 🚀 Django Lecture Series — The Study Book

`🎓 Track: Core Django` · `📶 Level: Beginner → Advanced` · `📚 Format: one deep chapter per lecture`

Welcome to a structured Django learning series. Each lecture has its own folder with a
**textbook-grade README**: explanations, mental models, diagrams, examples, interview
questions, active recall, exercises and revision sheets — designed for *long-term
retention*, not skim-reading.

> [!NOTE]
> **About the CSS in `docs/styles/global.css`:** GitHub's README rendering does **not**
> load external stylesheets, so this page and every lecture look plain-but-readable here.
> The shared stylesheet is the series' design system and is applied by CSS-aware
> renderers (VS Code preview extensions like *Markdown Preview Enhanced*, pandoc, MkDocs,
> or a future docs site). All content is written to remain fully readable without it.
> See [`docs/AGENTS.md`](docs/AGENTS.md) §CSS.

---

## 🗺️ How to Use This Book

1. **Read one chapter per sitting** — chapters build on each other in order.
2. **Do the active-recall questions before opening the answers** (answers are collapsible).
3. **Keep [`docs/MEMORY.md`](docs/MEMORY.md) open** while revising — it is the whole-series glossary and revision ledger.
4. **Practice in `ChaiAurCode/`** — the repository's real Django project is the playground the chapters reference.
5. **Revision rhythm:** revisit each chapter at Day 1, Day 7, and Day 30 — schedule in [`docs/MEMORY.md`](docs/MEMORY.md).

---

## 📚 The Lectures

| # | Chapter | Focus | Status |
|---|---|---|---|
| A001 | [Introduction to Django — What is Django?](A001_Introduction_What_is_Django/README.md) | What Django is, why it exists, philosophy, architecture at a glance, request/response mental model, project vs app, vocabulary | ✅ Documented |
| A002 | [MVT Architecture Explained](A002_MVT_Architecture_Explained/README.md) | Models, Views, Templates in depth — with the chai app's real code, `render()` & context, template inheritance, the `/chai/3/` trace | ✅ Documented |
| A003 | [Installing Django — Python, pip & Virtual Environments](A003_Install_Python_pip_Django_Virtual_Environment_Setup/README.md) | The toolchain beneath every project: interpreter, pip & PyPI, virtual environments, activation — built on the owner's real command journal (`commands.txt`) | ✅ Documented |
| A004+ | — | *future lectures appear here* | 🗓️ Planned |

---

## 🗂️ Repository Map

```
├── README.md              ← you are here (series hub & table of contents)
├── docs/                  ← documentation system
│   ├── AGENTS.md          ← writing contract for every future lecture
│   ├── MEMORY.md          ← glossary · mental models · recall bank · revisions
│   ├── styles/global.css  ← shared design system (one file, all lectures)
│   └── templates/         ← README skeleton for new lectures
├── A001_…/README.md       ← Lecture A001 chapter
├── A002_…/README.md       ← Lecture A002 chapter
├── A003_…/README.md       ← Lecture A003 chapter (plus its local myenv/ — git-ignored)
└── ChaiAurCode/           ← the real Django project used for practice
    └── chaiaurDjango/     ← (chai shop app: models, views, templates, admin)
```

---

## 📈 Progress

- ✅ **A001 — Introduction to Django** — documented
- ✅ **A002 — MVT Architecture Explained** — documented
- ✅ **A003 — Installing Django: Python, pip & Virtual Environments** — documented
- 🗓️ **A004+** — next up

---

<div class="doc-footer">

**Documentation system:** [`docs/AGENTS.md`](docs/AGENTS.md) (rules) ·
[`docs/MEMORY.md`](docs/MEMORY.md) (ledger) · [`docs/styles/global.css`](docs/styles/global.css) (design) ·
[`docs/templates/README-TEMPLATE.md`](docs/templates/README-TEMPLATE.md) (new lectures)

</div>

