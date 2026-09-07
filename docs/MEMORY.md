# 🧠 MEMORY — Learning Ledger

> **Status:** Active · **Scope:** the whole series
>
> Two jobs in one file:
> **1) Agent memory** — accumulated terminology, mental models and facts, so any
> future documentation agent stays consistent with earlier lectures without
> re-reading every chapter.
> **2) Student revision index** — one place to find every glossary term, analogy,
> recall question and revision schedule across all lectures.
>
> Rules: definitions here are **the single source of spelling/wording** for all
> lecture READMEs. New terms learned in a lecture get added here by that lecture's
> documentation pass. Keep entries one-to-three lines; deep explanation lives in
> the lecture chapters — this file links, it does not re-teach.
> Writing rules live in [`AGENTS.md`](AGENTS.md).

---

## 1. Series Progress Tracker

| Code | Folder | Title | Status | Sources available? |
|---|---|---|---|---|
| A001 | `A001_Introduction_What_is_Django` | Introduction to Django / What is Django? | ✅ Documented | ❌ No transcript — built from topic list + official docs |
| A002 | `A002_MVT_Architecture_Explained` | MVT Architecture Explained | ✅ Documented | ❌ No transcript — built from title + official docs + the chai app's real code (quoted verbatim) |
| A003 | `A003_Install_Python_pip_Django_Virtual_Environment_Setup` | Installing Django: Python, pip & Virtual Environments | ✅ Documented | ⚠️ Partial — primary source is the owner's command journal `commands.txt` (5 commands, quoted verbatim); mechanics filled from official Python/pip docs, marked 📌 |

---

## 2. Glossary (accumulated across lectures)

> Format: **term** — simple meaning · *technical meaning* · 🧷 memory hook.
> Spelling here is canonical for the whole series.

### A001 — Introduction to Django

- **Django** — a high-level Python web framework for building database-driven websites quickly and securely · *a full-stack, batteries-included server-side framework maintained by the Django Software Foundation; publicly released July 2005, created at the Lawrence Journal-World newspaper, named after guitarist Django Reinhardt* · 🧷 "perfectionists with deadlines."
- **Web framework** — a pre-built toolkit of code that handles the repeated plumbing of every website (routing, requests, databases, security) so developers write only app-specific logic · *a reusable software skeleton implementing inversion of control: your code is called by the framework, not the other way round* · 🧷 buying a furnished house vs. stacking bricks.
- **Framework vs library** — a library is called by your code; a framework calls your code · *inversion of control is the dividing line* · 🧷 "you call a plumber (library); a general contractor runs your site and calls you (framework)."
- **Batteries included** — Django ships nearly everything a web app needs in the box: ORM, admin, authentication, forms, templates, routing, security, i18n, testing · *monolithic full-stack framework philosophy* · 🧷 moving into a furnished apartment.
- **MTV pattern** — Django's architecture: Model (data), Template (presentation), View (request logic) · *Django's naming for MVC: Django's "view" describes which data is presented; the "template" describes how it looks* · 🧷 MTV = Django's dialect of MVC.
- **Model** — the Python class that describes one kind of stored data and talks to the database for you · *a class mapping to a database table via the ORM* · 🧷 the app's memory.
- **Template** — the HTML skeleton with placeholders that turns data into a visible page · *presentation layer with Django Template Language* · 🧷 the page's stencil.
- **View** — a Python function (or class) that receives a web request and returns a response · *request-handler layer: request in → HttpResponse out* · 🧷 the waiter: takes the order, returns the dish.
- **URL dispatcher** — the router that matches the requested URL path to a view · *URLconf: `urls.py` maps path patterns to views* · 🧷 the building's reception desk.
- **ORM (Object-Relational Mapper)** — lets you read/write database rows as Python objects instead of writing SQL · *maps classes→tables, instances→rows, attributes→columns* · 🧷 "Python in, SQL hidden."
- **Project (Django)** — one website instance: settings, root `urls.py`, and its collection of apps · *created by `django-admin startproject`; the configured container* · 🧷 the shopping mall.
- **App (Django)** — a self-contained module that does one job (blog, payments, accounts) and can be reused across projects · *a Python package registered in `INSTALLED_APPS`* · 🧷 the shops inside the mall.
- **Middleware** — hooks that process every request/response as it passes through Django · *the onion layers around the view* · 🧷 airport security lanes.
- **WSGI** — the standard Python interface between web servers and Django · *Web Server Gateway Interface; `runserver` is a development server only* · 🧷 the kitchen door standard.
- **CSRF / XSS / SQL injection** — the classic web attacks Django defends against by default (tokens, auto-escaping, parameterized ORM queries) · 🧷 Django locks the doors before you ask.
- **ASGI** — the async-capable sibling of WSGI: the interface between web servers and Django · *Asynchronous Server Gateway Interface; enables async views/WebSockets* · 🧷 WSGI's faster sibling.
- **HTTP request / response** — the browser's question and the server's answer · *Django models them as `HttpRequest` (in) and `HttpResponse` (out) objects* · 🧷 order ticket in, dish out.
- **Server-side / backend** — code that runs on the server, not in the browser · *receives HTTP, applies logic, returns responses — Django's territory* · 🧷 the kitchen, not the dining table.
- **`manage.py`** — the per-project command-line helper for Django tasks · *wraps `django-admin` with your project's settings: runserver, migrate, startapp, test* · 🧷 the mall's intercom.
- **Migrations** — version control for the database schema · *Python files generated from model changes, applied with `migrate`* · 🧷 renovation permits for the storeroom.
- **Admin (Django admin)** — the auto-generated back-office UI for managing models · *built from `admin.py` registrations; for staff, not the public site* · 🧷 the staff-only back office.
- **DRY (Don't Repeat Yourself)** — say everything exactly once · *every piece of knowledge has one authoritative representation; duplication breeds disagreement* · 🧷 one price tag per item.

### A002 — MVT Architecture Explained

- **QuerySet** — the object a model query returns: "all chais", "chais under ₹100" · *a chainable, lazy description of a database question; iterating it runs the query* · 🧷 the question you hand the storeroom.
- **View contract** — every view takes one `request` and returns one response object · *uniform signature is what lets the dispatcher call any view* · 🧷 request in, response out — no exceptions.
- **`render()`** — the standard way a view produces a page · *combines request + template file + context into a filled `HttpResponse`* · 🧷 "fill that file with this data."
- **Context** — the dictionary a view hands to a template · *its keys become the template's variable names; the only official view→template data channel* · 🧷 the handoff brief.
- **DTL (Django Template Language)** — the mini-language inside templates · *three syntaxes: `{{ variable }}`, `{% tag %}`, `{{ value\|filter }}` — intentionally not full Python* · 🧷 three shapes, read any template.
- **Template inheritance** — a parent template declares the shared skeleton; children fill its blocks · *`{% extends %}` + `{% block %}`; one navbar definition, N pages* · 🧷 letterhead & blank fields.
- **Path converter** — the typed part of a URL pattern, e.g. `<int:chai_id>` · *captures the URL segment, converts it, passes it as a view argument* · 🧷 the receptionist writes the room number on the ticket.
- **`get_object_or_404()`** — fetch one row or raise a 404 page · *replaces manual try/except around `.get()` for missing records* · 🧷 "find it — or politely say not found."
- **`pk` (primary key)** — the unique id of a row · *Django auto-adds an `id` pk to every model; `pk=chai_id` is the generic spelling* · 🧷 every row wears a badge number.
- **`__str__()`** — the human-readable name of a model object · *used by the admin, shell and logs; without it: `ChaiVarity object (1)`* · 🧷 the shelf label on the crate.
- **URL name & `{% url %}`** — patterns get a `name=`; templates build links from the name · *links survive URL restructuring — no hardcoded paths* · 🧷 call the room by its nickname, never its street address.
- **Single source of truth (model)** — one model declaration governs table, forms, admin, validation · *DRY applied to data definitions* · 🧷 one declaration, many obeying behaviors.

---
### A003 — Installing Django: Python, pip & Virtual Environments

- **pip** — Python's package installer: downloads and installs packages into the active environment's `site-packages` · *the standard tool for consuming PyPI; bound to whichever interpreter/environment is currently active* · 🧷 packages land wherever you're standing.
- **PyPI** — the Python Package Index: the public online registry pip fetches packages from · *the default package repository of the Python ecosystem* · 🧷 the app store for Python.
- **Virtual environment (venv)** — an isolated per-project Python package space in a normal folder · *an interpreter + its own `site-packages`, so projects don't share dependencies* · 🧷 your own room in a shared house.
- **virtualenv** — the classic third-party tool that creates virtual environments; the journal uses it · *predates and inspired Python 3's built-in `venv` module; still faster for some workflows* · 🧷 venv's famous older sibling.
- **Activation** — pointing your terminal shell at an environment so `python`/`pip`/installed tools run from it · *a session-scoped shell configuration, visible as the `(myenv)` prompt prefix; ends with `deactivate` or the terminal* · 🧷 walking into the room (the prefix is the door).
- **site-packages** — the folder inside an environment where installed packages physically live · *the per-environment package directory the interpreter searches at import time* · 🧷 the room's storage shelf.
- **Global installation** — packages installed while no environment is active, going to the base interpreter · *shared by every project on the machine; the source of version conflicts* · 🧷 standing outside the room when you drop the package.
- **`django-admin`** — Django's global command-line utility, installed *by* the Django package · *proof-of-install and project-scaffolding tool (`--version`, `startproject`)* · 🧷 it exists only because Django put it there.

---

## 3. Mental-Model Registry (registered analogies — reuse, don't reinvent)

| Model | Maps to | Introduced | Use for |
|---|---|---|---|
| **Furnished house vs loose bricks** | framework vs library (inversion of control) | A001 | framework-nature questions |
| **Furnished apartment** | "batteries included" | A001 | feature-scope questions |
| **Shopping mall & shops** | project vs app | A001 | structure questions |
| **Restaurant** | request cycle: waiter = view, kitchen = model/ORM, plating & menu = template, order ticket = request, dish = response | A001 | architecture & lifecycle questions |
| **Reception desk** | URL dispatcher | A001 | routing questions |
| **Airport security lanes** | middleware | A001 | request-pipeline questions |
| **Letterhead & blank fields** | template inheritance: parent layout declares blocks, children fill them | A002 | template reuse questions |
| **The room & where you're standing** | virtual environments: venv = room (a folder), activate = walking in (the `(myenv)` prefix is the door), `pip install` = dropping the package where you stand, deactivate = stepping out | A003 | environment/isolation questions |

**One-breath model (A001):** *Python is the language; Django is the furnished framework
built on it; a project is the mall; apps are its shops; a request enters, the reception
desk (URL dispatcher) routes it to the right waiter (view), the kitchen (model/ORM)
fetches the data, the plating (template) presents it, and the finished dish (HTTP
response) goes back to the guest (browser).*

---

## 4. Active-Recall Bank (cumulative across lectures)

**From A001:** What is Django in one sentence? · Framework vs library? · Why does
"batteries included" matter? · Name 5 major features + the problem each removes ·
MTV vs MVC? · Trace a request through Django · Project vs app (two concrete
differences) · What Django does NOT do · Why Python + Django works well · What you
would have to build by hand without a framework.

**From A002:** Name the three MVT layers, their files, and the one question each
answers · The three model mappings (class/field/object → ?) · What are `render()`'s
three arguments? · What is a context dictionary and why do its keys matter? · The DTL's
three syntaxes? · What problem does template inheritance solve, and how? · What does
`get_object_or_404` prevent? · Why do templates build URLs with `{% url %}` instead of
hardcoding them? · Walk `/chai/3/` file by file · Map a symptom to its layer.

**From A003:** What does pip do and where does it install? · The one visible sign of an
active venv? · What does `virtualenv myenv` physically create? · The professional setup
order — and what the journal reordered? · Why isn't a fresh venv "Python from scratch"?
· `deactivate` vs closing the terminal? · What never gets committed to git, and what
does this repo's `.gitignore` do about it? · One machine, two Django versions — what
breaks and what fixes it?

---

## 5. Spaced-Revision Schedule

| Chapter | Day 1 | Day 7 | Day 30 |
|---|---|---|---|
| A001 | Re-read 📝 Quick Revision; answer 🔁 recall questions | Redraw the 5 Mermaid diagrams from memory; explain project vs app aloud | Do the Level-4 exercise; deliver 🎯 interview answers aloud |
| A002 | Re-read 📝 Quick Revision; recite the three layers + their files | Redraw the `/chai/3/` journey table from memory; annotate `views.py` aloud | Trace a fresh URL (e.g. `/chai/chai_stores/`) through every file; answer the interview set aloud |
| A003 | Re-read 📝 Quick Revision; recite the 6-command chain | On a fresh folder: create → activate → install → verify, without notes; explain aloud why the order matters | Set up a new project's venv from scratch; answer the interview set aloud |

---

## 6. Update Log

- **A001 documented; system created** — `docs/` infrastructure built (contract, ledger,
  global CSS, template, hub README). Glossary seeded with 15 A001 terms; 6 mental
  models registered. No lecture transcript existed for A001 — declared in-chapter;
  chapter grounded in the owner's topic list + official Django docs.
- **A001 audit pass** — 16-dimension audit of A001 + system. Glossary completed
  (15 → 22 A001 terms: ASGI, HTTP request/response, server-side, `manage.py`,
  migrations, admin, DRY added). Revision row corrected (5 Mermaid diagrams, not 4).
  Learning Checkpoints formalized in AGENTS §4 + template. Template checklist pointer
  fixed (§10 → §14). A001: `include()` wiring note added to the practical example,
  2 FAQ items added (configuration ≠ automatic; request ≠ response), memory-palace
  diagram flow corrected (WHY now motivates Django instead of following the response),
  trailing blank lines trimmed. CSS: inline-code `white-space: nowrap` removed (mobile
  overflow risk) and `.diagram` selector simplified. `ChaiAurCode/**` untouched.
- **A002 documented** — MVT deep dive built from title + official docs + the chai app's
  real code (models/views/urls/templates quoted and annotated verbatim). 12 glossary
  terms added; "Letterhead & blank fields" mental model registered; recall bank and
  revision schedule extended; hub TOC updated to ✅. Key teaching artifacts: the
  `/chai/3/` file-by-file trace and the symptom→layer debugging table.
- **A003 documented** — first chapter built from an in-repo primary source: the
  `commands.txt` lecture journal (quoted verbatim; its install-before-venv ordering
  preserved and dissected as a lesson rather than silently corrected). 8 glossary terms
  added; "The room & where you're standing" mental model registered; recall bank and
  revision schedule extended; hub TOC updated to ✅. `commands.txt` committed alongside
  the chapter so its cited primary source lives in the repo.

