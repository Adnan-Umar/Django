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
| A011 | [App-Level Templates Setup — HTML Integration](A011_App_Level_Templates_Setup_HTML_Integration/README.md) | Templates inside apps: the `templates/<app>/` namespacing convention, the populated two-lane lookup (`DIRS` → `INSTALLED_APPS` order), registration as precondition, ownership-based placement — built on the eighth artifact `myProject4/` (`blog` + `shop`, orphaned `base.html`) | ✅ Documented |
| A012 | [Manage HTML Files](A012_Manage_HTML_Files/README.md) | Template inheritance in practice: parent `base.html` with `{% block %}` regions, children that `{% extends %}` it, cross-lane parent lookup, block defaults, silent-failure diagnosis, ownership-based placement — built on the ninth artifact (same `myProject4/`, zero Python changed, three rewritten templates) | ✅ Documented |
| A013 | [Templates 1: Basics & Variables](A013_Templates_1_Basics_&_Variables/README.md) | `{{ }}` variables + the context dictionary: `render()`'s data argument, the dot-lookup order, auto-escaping & `|safe`, DTL comments — built on the tenth artifact `myProject5/` (fresh single-app project, first living `home.html`, all 12 outputs verified by rendering) | ✅ Documented |
| A014 | [Templates 2: Filters (Text, Numbers, Date)](A014_Templates_2_Filters_Text_Numbers_Date/README.md) | The filter shelf: 20 distinct filters (text / number / date / collection / three-state) reshaping values at print time, the resolve→filter→escape pipeline, case-sensitive date codes, first `{% if %}` — built on the eleventh artifact `myProject6/` (all outputs verified by rendering + live 200 on `GET /`) | ✅ Documented |
| A015 | [Templates 3: If, For, With and Cycle](A015_Templates_3_If_For_With_and_Cycle/README.md) | The control-flow shelf: 9 block tags (`if`/`else`, `for` with `empty` & `forloop.counter`, `with`, `cycle`, `firstof`, `verbatim`, `autoescape off`) that make a page decide and repeat — built on the twelfth artifact `myProject7/` (list-of-dicts page at `/blog/`, render-verified + live 200) | ✅ Documented |
| A016 | [Templates 4: Inheritance, Static Files](A016_Templates_4_Inheritance_Static_Files/README.md) | The blueprint + the warehouse: one `base.html` parent with `title`/`content` block defaults, two children (one per template lane), an included navbar reversing named URLs, and a real `static/` tree (`STATICFILES_DIRS` + `{% load static %}` + `{% static %}`) — built on the thirteenth artifact `myProject8/` (render-verified 17/17 + live 200s on both pages and all three assets) | ✅ Documented |
| A017 | [Templates 5: Advanced Tags](A017_Templates_5_Advanced_Tags/README.md) | The specialist shelf: `{% regroup %}` (pigeonholes in first-appearance order), `{% widthratio %}`, `{% spaceless %}`, `{% filter %}` (region form of the pipe) — plus the parent rendered directly as a page of pure defaults — built on the fourteenth artifact `myProject9/` (render-verified 13/13 + live 200s on `/blog/` and `/blog/blog/`) | ✅ Documented |
| A018 | [Bootstrap in Django](A018_Bootstrap_in_Django/README.md) | The costume department: nine `btn` buttons dressed by three supply channels — the `django-bootstrap5 26.3` bridge (prints 5.3.8 CDN link/script), commented-out CDN fossils, and local `{% static %}` labels — plus the `corecss` swap that trades one dead label for a live one — built on the fifteenth artifact `myProject10/` (render-verified + live 200 with a diagnosed asset 404) | ✅ Documented |
| A019 | [Tailwind Setup in Django](A019_Tailwind_Setup_in_Django/README.md) | The print shop with two floors: one `<h1>` wearing three utilities (`bg-sky-200 text-center p-4`), woven by the Tailwind v4.3.3 CLI (`input.css` 22 B → `output.css` 4,889 B via `npm run dev`) and served from the app lane — plus the ghost `STATICFILES_DIRS` (`W004`) and the test-client 404 that proves nothing — built on the sixteenth artifact `myProject11/` (286 B page, 200; asset 404-by-design vs `runserver` 200) | ✅ Documented |
| A020 | [Portfolio Website in Django](A020_Portfolio_Website_in_Django/README.md) | The capstone-start: a **root-mounted** `portfolio` app owns `/` (`/blog/` → 404), three pages under one base with hard-coded `<title>` (⚠️), an `includes/` partials folder, a real project-level `static/` tree (3,760 B css + 7 byte-identical assets), the series' first `{% csrf_token %}` form (empty + verbatim `UserWarning` bare vs live hidden input), plus **dormant CSS** (`.hero h1`, `.contact h2`) — built on the seventeenth artifact `myProject12/` (render-verified 1,452/794/994 B pages, live 200s incl. `POST /contact/` re-render) |
| A022 | [Create Model, Migration Files & SQLite DB](A022_Create_Model_Migration _iles_&_SQLite_DB/README.md) | The blueprint and the migration ledger: define a `Student` model with `name`, `age`, `email`, and `enrollment_date` fields, then generate the migration skeleton (`0001_initial.py`) and let Django create the SQLite table — plus the `blog` app wiring (model, view, URL, template, admin) — built on the eighteenth artifact `myProject13/` | ✅ Documented |
| A021+ | — | *future lectures appear here* | 🗓️ Planned |

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
├── A011_…/                  ← Lecture A011 chapter (plus myProject4/ — blog + shop apps, each owning templates/<app>/; orphaned base.html)
├── A012_…/                  ← Lecture A012 chapter (plus myProject4/ — same blog + shop project, zero Python changed; base.html now a parent, both app pages children)
├── A013_…/                  ← Lecture A013 chapter (plus myProject5/ — the fresh single-app project whose home.html got live {{ }} variables, render-verified against artifact context)
├── A014_…/                  ← Lecture A014 chapter (plus myProject6/ — the fresh single-app project whose blog_details.html is a 20-filter shelf, render-verified + 200 on GET /)
├── A015_…/                  ← Lecture A015 chapter (plus myProject7/ — the fresh single-app project whose blog_list.html is a 9-tag control-flow shelf at /blog/, render-verified + live 200)
├── A016_…/                  ← Lecture A016 chapter (plus myProject8/ — the fresh single-app project whose pages inherit one base.html parent and wear a real static/ tree, render-verified + live 200s)
├── A017_…/                  ← Lecture A017 chapter (plus myProject9/ — the fresh single-app project whose blog.html is a specialist-tag shelf (`regroup`/`widthratio`/`spaceless`/`filter`), render-verified + live 200s)
├── A018_…/                  ← Lecture A018 chapter (plus myProject10/ — the fresh single-app project whose base.html wires django-bootstrap5 26.3 + CDN fossils + static labels, render-verified + live 200)
├── A019_…/                  ← Lecture A019 chapter (plus myProject11/ — the fresh single-app project whose blog.html wears Tailwind utilities woven by the v4.3.3 CLI, 286 B page + 4,889 B bolt)
├── A020_…/                  ← Lecture A020 chapter (plus myProject12/ — the fresh three-page portfolio whose root-mounted `portfolio` app ships a hard-coded tab, real static/ tree, and a csrf form)
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
- ✅ **A011 — App-Level Templates Setup (HTML Integration)** — documented
- ✅ **A012 — Manage HTML Files** — documented
- ✅ **A013 — Templates 1: Basics & Variables** — documented
- ✅ **A014 — Templates 2: Filters (Text, Numbers, Date)** — documented
- ✅ **A015 — Templates 3: If, For, With and Cycle** — documented
- ✅ **A016 — Templates 4: Inheritance, Static Files** — documented
- ✅ **A017 — Templates 5: Advanced Tags** — documented
- ✅ **A018 — Bootstrap in Django** — documented
- ✅ **A019 — Tailwind Setup in Django** — documented
- ✅ **A020 — Portfolio Website in Django** — documented
- ✅ **A022 — Create Model, Migration Files & SQLite DB** — documented
- 🗓️ **A021+** — next up (ORM — folder already in repo)

---

<div class="doc-footer">

**Documentation system:** [`docs/AGENTS.md`](docs/AGENTS.md) (rules) ·
[`docs/MEMORY.md`](docs/MEMORY.md) (ledger) · [`docs/styles/global.css`](docs/styles/global.css) (design) ·
[`docs/templates/README-TEMPLATE.md`](docs/templates/README-TEMPLATE.md) (new lectures)

</div>

