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
| A004 | [Create Django Project](A004_Create_Django_Project/README.md) | `django-admin startproject` file-by-file, the two-`myProject` confusion, `manage.py` vs `django-admin`, `settings.py` anatomy, `runserver` & the dev server — built on the journal + the real generated `myProject/` | ✅ Documented |
| A005 | [Django Files & Folders](A005_Django_Files_Folders/README.md) | The complete project map: every file & folder incl. `db.sqlite3` & `__pycache__`, edit-vs-never-edit, where future apps/templates live, custom ports (`runserver 8080`) | ✅ Documented |
| A006 | [Django startapp Command](A006_Django_startapp_Command_Explained/README.md) | The command that creates an app: generated files, `apps.py` & `AppConfig`, `INSTALLED_APPS` registration — built on journal line 17 + the real generated `blog/` app | ✅ Documented |
| A007 | [Views & URLs Basics](A007_Views_URLs_Basics/README.md) | First views (`HttpResponse`), the app-level `urls.py` startapp doesn't make, `include()` wiring, `ROOT_URLCONF`, URL→view→response journey — built on journal lines 19–25 + the `dj1/` artifact (views + urls already written) | ✅ Documented |
| A008 | [Multiple Apps with Views & URLs (Blog/Shop)](A008_Multiple_Apps_with_Views_URLs_%28Blog_Shop_Example%29/README.md) | Two apps in one project (`blog` + `shop`): URL prefixes & prefix-stripping, name-collision avoidance (`blog-home`), and how to read the artifact's real duplicate-route bug — built on the fifth artifact `myProject1/` | ✅ Documented |
| A009 | [URL Parameters — path, re_path, kwargs](A009_URL_Parameters_%28path_re_path_kwargs%29/README.md) | Captured URL segments as typed view arguments: path converters (`<int:post_id>`), multi-segment routes, `re_path` regex groups (strings), `**kwargs` views — built on the sixth artifact `myProject2/` | ✅ Documented |
| A010 | [Templates Folder Setup — Project Level](A010_Templates_Folder_Setup_Project_Level/README.md) | The T of MVT hands-on: the project-level `templates/` folder, `TEMPLATES['DIRS']` vs `APP_DIRS`, lookup order & shadowing, `render()` as find-fill-wrap, `TemplateDoesNotExist` debugging — built on the seventh artifact `myProject3/` (zero apps, first executed `render()`) | ✅ Documented |
| A011+ | — | *future lectures appear here* | 🗓️ Planned |

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
├── A004_…/                ← Lecture A004 chapter (plus myProject/ — the real generated project it dissects)
├── A005_…/                ← Lecture A005 chapter (plus myproject/ — a second generated project, lowercase this time)
├── A006_…/                ← Lecture A006 chapter (plus myproject/ — now holding the blog/ app startapp created)
├── A007_…/                ← Lecture A007 chapter (plus dj1/ — project whose blog/ app got its first views & urls)
├── A008_…/                ← Lecture A008 chapter (plus myProject1/ — the project now running blog AND shop apps)
├── A009_…/                ← Lecture A009 chapter (plus myProject2/ — the app that reads values from URLs: converters, re_path, kwargs)
├── A010_…/                  ← Lecture A010 chapter (plus myProject3/ — zero apps: project-level templates/, config-level views.py, the DIRS edit)
├── A011_…/                  ← planned lecture (App-Level Templates Setup — HTML Integration)
└── ChaiAurCode/           ← the real Django project used for practice
    └── chaiaurDjango/     ← (chai shop app: models, views, templates, admin)
```

---

## 📈 Progress

- ✅ **A001 — Introduction to Django** — documented
- ✅ **A002 — MVT Architecture Explained** — documented
- ✅ **A003 — Installing Django: Python, pip & Virtual Environments** — documented
- ✅ **A004 — Create Django Project** — documented
- ✅ **A005 — Django Files & Folders** — documented
- ✅ **A006 — Django startapp Command** — documented
- ✅ **A007 — Views & URLs Basics** — documented
- ✅ **A008 — Multiple Apps with Views & URLs (Blog/Shop)** — documented
- ✅ **A009 — URL Parameters (`path`, `re_path`, `kwargs`)** — documented
- ✅ **A010 — Templates Folder Setup (Project Level)** — documented
- 🗓️ **A011+** — next up

---

<div class="doc-footer">

**Documentation system:** [`docs/AGENTS.md`](docs/AGENTS.md) (rules) ·
[`docs/MEMORY.md`](docs/MEMORY.md) (ledger) · [`docs/styles/global.css`](docs/styles/global.css) (design) ·
[`docs/templates/README-TEMPLATE.md`](docs/templates/README-TEMPLATE.md) (new lectures)

</div>

