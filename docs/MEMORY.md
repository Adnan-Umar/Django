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
| A004 | `A004_Create_Django_Project` | Create Django Project | ✅ Documented | ⚠️ Partial — primary sources are the command journal's new lines (11 & 13, quoted verbatim) and the generated `myProject` artifact itself (settings/manage/urls/wsgi/asgi quoted verbatim) |
| A005 | `A005_Django_Files_Folders` | Django Files & Folders | ✅ Documented | ⚠️ Partial — primary sources are the journal's new line 15 (`runserver 8080`, quoted verbatim) and the second generated artifact `myproject/` (lowercase — the case-sensitivity case study) |
| A006 | `A006_Django_startapp_Command_Explained` | Django startapp Command | ✅ Documented | ⚠️ Partial — primary sources are the journal's new line 17 (`startapp blog`, quoted verbatim) and a third artifact: the generated `blog/` app inside A006's `myproject/` (stub files + user-edited `INSTALLED_APPS` quoted verbatim) |
| A007 | `A007_Views_URLs_Basics` | Views & URLs Basics | ✅ Documented | ⚠️ Partial — primary sources are the journal's lines 19–25 (environment rebuild, quoted verbatim) and a fourth artifact: the `dj1/` project whose `blog/` app now contains written views and URLs (all quoted verbatim) |
| A008 | `A008_Multiple_Apps_with_Views_URLs_(Blog_Shop_Example)` | Multiple Apps with Views & URLs (Blog/Shop) | ✅ Documented | ⚠️ Partial — primary source is a fifth artifact: `myProject1/` running `blog` AND `shop` apps (all views/urls/settings quoted verbatim, including a REAL duplicate-`''` bug in `shop/urls.py`, dissected per AGENTS §12); journal (`startapp blog` + env rebuild) is context |
| A009 | `A009_URL_Parameters_(path_re_path_kwargs)` | URL Parameters (path, re_path, kwargs) | ✅ Documented | ⚠️ Partial — primary source is a sixth artifact: `myProject2/` whose `blog` app reads values from URLs (views/urls quoted verbatim: `path()` converters, multi-segment routes, a `re_path` regex route, and a `**kwargs` view that superseded a commented-out explicit signature); journal adds no lines (file-editing lecture) |
| A010 | `A010_Templates_Folder_Setup_Project_Level` | Templates Folder Setup (Project Level) | ✅ Documented | ⚠️ Partial — primary source is a seventh artifact: `myProject3/`, the first with **no app** (project-level `templates/home.html`, config-level `views.py` calling `render()`, `settings.py` with the `DIRS` edit + `import os` + an inert `MAILERS` block — all quoted verbatim); A004's pristine `settings.py` serves as the in-repo "before" diff; journal adds no lines (file-editing lecture) |
| A011 | `A011_App_Level_Templates_Setup_HTML_Integration` | App-Level Templates Setup (HTML Integration) | ✅ Documented | ⚠️ Partial — primary source is an eighth artifact: `myProject4/` running `blog` + `shop`, each owning a namespaced `templates/<app>/` folder with a tag-free page (`views.py`/`urls.py`/templates + `settings.py` quoted verbatim: both apps registered, pathlib `DIRS`, orphaned `base.html`, inert `MAILERS` block carried over); A010's `settings.py` is the "before" diff; journal adds no lines (file-editing lecture) |
| A012 | `A012_Manage_HTML_Files` | Manage HTML Files | ✅ Documented | ⚠️ Partial — primary source is a ninth artifact: the same `myProject4/` with **zero Python changed** (all `.py` files diffed vs A011 — identical); three rewritten templates (`base.html` now a parent with `title`/`content` blocks at outer `templates/` — moved from A011's inner path, flagged in a §12 discrepancy note — plus two `{% extends %}` children); journal adds no lines (file-editing lecture) |
| A013 | `A013_Templates_1_Basics_&_Variables` | Templates 1: Basics & Variables | ✅ Documented | ⚠️ Partial — primary source is a tenth artifact: `myProject5/`, a fresh single-app project (`blog`) whose `home.html` is the first template in the series' own projects with live `{{ }}` variables (`views.py` holds a 7-key context dict + an in-file `User` class; `home.html` carries 12 `{{ }}` prints + 3 comment syntaxes — both quoted verbatim; `settings.py`/`urls.py`/`apps.py` read for config: single `blog` registration, pathlib `DIRS`, minimal URL table); all 12 outputs + comment fates + datetime self-format verified by rendering artifact bytes through Django 6.1.1's engine; journal adds no lines (file-editing lecture) |
| A014 | `A014_Templates_2_Filters_Text_Numbers_Date` | Templates 2: Filters (Text, Numbers, Date) | ✅ Documented | ⚠️ Partial — primary source is an eleventh artifact: `myProject6/`, a fresh single-app project (`blog`) whose `blog_details.html` is a filter shelf — 20 distinct filters spanning the text, number, date/time, collection, and three-state families, plus the series' first `{% if %}` tag (`views.py` holds one 8-key `post` dict incl. `author=None`, a `datetime`, a `tags` list; template + views + urls + settings quoted verbatim); every output verified twice — rendering artifact bytes through Django 6.1.1's engine AND a live `GET /` (200) through the request path, closing the owner's early-404; journal adds no lines (file-editing lecture) |
| A015 | `A015_Templates_3_If_For_With_and_Cycle` | Templates 3: If, For, With and Cycle | ✅ Documented | ⚠️ Partial — primary source is a twelfth artifact: `myProject7/`, a fresh single-app project (`blog`) whose `blog_list.html` is the series' first true control-flow page — 9 block tags (`if`/`else`, `for` ×2 with `empty`, `with`, `cycle`, `firstof`, `verbatim`, `autoescape off`) walking a 3-item list of dicts (`views.py` holds `blogs`, `today`, `html_code`; template + views + urls + settings quoted verbatim; the `blog/`-prefix mount returns A008's lesson — root `/` 404s by design, `GET /blog/` 200); all 9 tag outputs verified twice — engine render of artifact bytes AND live request path (12 assertions); journal adds no lines (file-editing lecture) |
| A016 | `A016_Templates_4_Inheritance_Static_Files` | Templates 4: Inheritance, Static Files | ✅ Documented | ⚠️ Partial — primary source is a thirteenth artifact: `myProject8/`, a fresh single-app project (`blog`) whose `templates/base.html` (505 B) is the series' first *formal* parent — `title`/`content` blocks (title ships the default `My Title`), `{% include "navbar.html" %}` partial with `{% url %}`-reversed links, css+js via `{% static %}`; two children — outer `home.html` (572 B, img via `{% static %}`, inert login form + onclick button) and app-level `about.html` (168 B, cross-lane extends); `settings.py` adds exactly one non-default line (`STATICFILES_DIRS = [BASE_DIR / 'static']`) plus a real `static/` tree (css 308 B, js 73 B, logo.png 24,890 B valid PNG); template + views + urls + settings quoted verbatim; all outputs verified twice — engine render (17/17 assertions, incl. the parent-alone default and the loads-don't-inherit TemplateSyntaxError) AND live request path (`GET /blog/` 200 with 10 assertions, `GET /blog/about/` 200 with 7, three assets 200 byte-identical, `/` 404, `/admin/` 302 → login 200); journal adds no lines (file-editing lecture) |
| A017 | `A017_Templates_5_Advanced_Tags` | Templates 5: Advanced Tags | ✅ Documented | ⚠️ Partial — primary source is a fourteenth artifact: `myProject9/`, a fresh single-app project (`blog`) whose `blog/templates/blog.html` (865 B, **un-namespaced** — departs from A011's `templates/<app>/` convention, flagged ⚠️) is a shelf of 4 specialist tags over a 3-student list of dicts (`views.py` holds `students_list` + a `home` view that renders the parent `base.html` (279 B) **directly**; template + views + urls + settings quoted verbatim; `settings.py` is `STATIC_URL`-only — no `STATICFILES_DIRS`, no `static/` tree; inert `{% load static %}` in base, inert `MAILERS` block carried over); all outputs verified twice — engine render of artifact bytes (13/13 assertions: regroup order `10th → 9th → 8th`, widthratio `50`, byte-exact spaceless block, `<P>…</P>` region, lower/add pairs) AND live request path (`GET /blog/` 200 defaults-as-page, `GET /blog/blog/` 200 13/13 assertions, `/` 404, `/admin/` 302); journal adds no lines (file-editing lecture) |

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

### A004 — Creating the Django Project

- **`startproject`** — the scaffolding command that generates a project skeleton · *`django-admin` runs its project template: `manage.py` + an inner configuration package named after your argument* · 🧷 the mall stamped from one blueprint.
- **Inner vs outer project folder** — the duplicated name `startproject` creates · *outer folder = a renameable container; inner package = the Python config root (`myProject.settings`) that imports come from* · 🧷 the box vs the label on it.
- **Development server (`runserver`)** — Django's built-in web server for development only · *serves the site at `127.0.0.1:8000` with auto-reload; never for production* · 🧷 the rocket page is a dev-only elevator.
- **`INSTALLED_APPS`** — the project's app registry in `settings.py` · *the list that switches apps on; Django's own admin/auth ship as apps (`django.contrib.*`)* · 🧷 the mall's directory of open shops.
- **`settings.py`** — the project's constitution: one Python module configuring everything · *module-level constants: `SECRET_KEY`, `DEBUG`, `DATABASES`, `INSTALLED_APPS`, `TEMPLATES`* · 🧷 city hall's rulebook.
- **DEBUG mode** — the verbose-error/development switch · *`True` shows tracebacks and enables auto-reload; must be `False` in production* · 🧷 construction lights — great for building, dangerous left on.
- **`SECRET_KEY`** — the cryptographic seed Django generates per project · *feeds sessions, CSRF and signing; must stay secret and unique per deployment* · 🧷 the mall's master key — never copy between malls.
- **`db.sqlite3`** — the auto-created SQLite database file · *appears on first `runserver`/`migrate`; it is your data, so it stays out of version control* · 🧷 the storeroom's goods — not the blueprints.
- **`__pycache__`** — Python's compiled-bytecode cache folder · *auto-generated next to imported packages; excluded from version control* · 🧷 scratch paper — redrawn automatically, never filed.
- **WSGI/ASGI entry points** — `wsgi.py` / `asgi.py`: the doors production servers use · *each exposes the `application` callable a real server imports; unused on dev days* · 🧷 staff entrances, not the customer door.

### A005 — Django Files & Folders

- **SQLite / `db.sqlite3`** — your app's data file · *file-backed relational database; Django's default `ENGINE`, written only via ORM + migrations — never by hand* · 🧷 the filing cabinet in the office.
- **`__pycache__/`** — Python's scratch copies · *directory of compiled `.pyc` bytecode, auto-regenerated on import; fully disposable* · 🧷 the photocopier room.
- **Bytecode** — pre-chewed Python · *intermediate compiled form CPython caches to speed up imports* · 🧷 pre-chewed food.
- **`__init__.py`** — the "this is a package" flag · *makes a directory importable as a Python package* · 🧷 the shop's "OPEN" sign.
- **Port** — which door on the machine · *numbered endpoint (1–65535) one program listens on at a time; chosen at launch (`runserver 8080`), not stored in settings* · 🧷 the doorbell number.
- **localhost / `127.0.0.1`** — "this machine itself" · *loopback address — traffic never leaves the computer* · 🧷 talking to yourself in the mirror.
- **Case sensitivity** — `myProject` ≠ `myproject` (to Python) · *Windows file system is case-insensitive; Python imports are case-sensitive everywhere* · 🧷 name tags must match exactly.

### A006 — Django startapp Command

- **`startapp`** — Django's command that creates a new app package · *`python manage.py startapp <name>` renders Django's app template next to `manage.py`; it does **not** register the app* · 🧷 a key that cuts a new shop's shell.
- **App scaffolding** — the ready-made skeleton a new app starts with · *template-generated stubs (`apps`/`models`/`views`/`admin`/`tests` + `migrations/`), importable but empty* · 🧷 a shelved-but-empty shop unit.
- **`AppConfig`** — the class that represents the app to Django · *lives in `apps.py`; its `name` attribute points at the app package; class derived from the app name (`blog` → `BlogConfig`)* · 🧷 the shop's nameplate.
- **Stub comment** — the `# Create your … here` lines in generated files · *scaffolding's explicit "your code goes here" markers that you replace* · 🧷 shelf labels marked "stock me".
- **App registration** — adding the app's name to `INSTALLED_APPS` · *the setting that switches an app on; without it the folder is inert (`INSTALLED_APPS` itself defined in A004)* · 🧷 adding the shop to the mall's directory.

### A007 — Views & URLs Basics

- **View function** — the Python function that answers one URL · *takes `request`, returns a response object; the dispatcher calls it per request* · 🧷 the counter that makes the dish.
- **`HttpResponse`** — the object a view hands back · *wraps body text/bytes, status code and headers into the HTTP reply* · 🧷 the finished dish on its tray.
- **`path()`** — one row in the URL table · *`path(route, view, name=…)` — a path string, a callable view, an optional name; never call the view (`views.home()`) at import time* · 🧷 one address-book entry.
- **App-level URLconf** — the app's own `urls.py` · *`startapp` does NOT create it; a `urlpatterns` list with `from . import views`; connected to the project by `include()`* · 🧷 the shop's own menu.
- **`include()`** — delegates a URL prefix to another URLconf · *`path('', include('blog.urls'))` hands the remainder of the path to the app's table* · 🧷 mall directory → shop's menu.
- **`ROOT_URLCONF`** — the setting naming the project's root URLconf · *a string like `'dj1.urls'` in `settings.py`; the first table Django consults* · 🧷 the front-door directory.
- **URL pattern** — the mapping of a path to a view · *a `path()` object inside `urlpatterns`; matched in order; `<converter:…>` segments capture values* · 🧷 a line in the reception ledger.

### A008 — Multiple Apps with Views & URLs

- **URL prefix** — the path segment that claims an app · *the `route` argument of `include()` — `path('shop/', include('shop.urls'))`; Django strips it and hands the remainder down* · 🧷 the shop's street address.
- **Prefix stripping** — the app never sees its own prefix · *matches `shop/`, passes `products/` into `shop.urls`; the project mounts, the app defines* · 🧷 the mall signs it, the shop doesn't wear it.
- **Name collision** — two routes sharing a `name=` · *ambiguous `{% url 'home' %}` when `blog` and `shop` both define `home`; the fix is app-prefixed names* · 🧷 two shops, one "home" in the directory.
- **Name prefixing** — manual namespacing by convention · *`blog-home`, `shop-home` — unique names with no framework machinery* · 🧷 labels with the shop's initials.
- **Dead route** — a pattern that can never win · *shadowed by an earlier identical/overlapping pattern; the artifact's second `path('')` in `shop/urls.py`* · 🧷 the menu line printed but never served.
- **First-match-wins** — the resolver stops at the first matching pattern · *`urlpatterns` scanned in order; later same-path patterns are unreachable* · 🧷 first menu line a guest sees.

### A009 — URL Parameters (path, re_path, kwargs)

- **URL parameter** — a value embedded in the path · *a variable segment like `<int:post_id>` the dispatcher captures and passes to the view as a keyword argument* · 🧷 the blank on the form letter.
- **Path converter** — the typed part of a placeholder · *`<type:name>` — matches a segment shape, converts it, hands it by keyword (`<int:post_id>` → `post_id=73`, an `int`); non-matching values → 404* · 🧷 a bouncer who also translates.
- **Converter → keyword contract** — captured values become view keyword arguments · *`path('post/<int:post_id>/', …)` calls `views.post_details(request, post_id=…)`; the view signature must accept the same name or a `TypeError` fires* · 🧷 the URL whispers, the view answers by name.
- **`re_path()`** — URL patterns written as regex · *matches the whole path against a regex; `(?P<name>…)` named groups become keyword args — always **strings*** · 🧷 `path`'s older, sharper-edged sibling.
- **Named regex group** — regex capture with a name · *`(?P<year>[0-9]{4})` captures 4 digits as `year`; arrives as `'2024'` (str), unlike `<int:year>`'s int* · 🧷 `(?P<name>pattern)` ⇒ `name` the keyword.
- **`**kwargs` view** — a view accepting any captured keywords · *`def view(request, **kwargs)` collects all URL-keyword arguments into a dict — one view, many URL shapes; superseded a commented-out explicit signature in the artifact* · 🧷 the catch-all funnel.

### A010 — Templates Folder Setup (Project Level)

- **Project-level templates folder** — one `templates/` directory at the project root, shared by the whole site · *convention home for site-wide templates (layouts, home, error pages), found via `DIRS`* · 🧷 the building's central print room.
- **`TEMPLATES['DIRS']`** — the engine's "look here too" list · *a list of template directories searched **first** by the `DjangoTemplates` loader; default `[]` = a fresh project cannot find project-level templates* · 🧷 the signpost to the print room.
- **`APP_DIRS`** — the "also look inside apps" flag · *`True` makes each installed app's `templates/` subfolder a lookup location, in `INSTALLED_APPS` order; a no-op with zero apps* · 🧷 also check every open shop's printer.
- **Template lookup order** — where the engine searches, in sequence · *`DIRS` directories first, then app dirs; **first match wins**, so `DIRS` can shadow an app's template* · 🧷 A008's URL rule, now a file rule.
- **Template engine / loader** — the machinery that finds, reads, and fills templates · *the `'BACKEND'` in `TEMPLATES` (`DjangoTemplates`) resolves a name to a file, parses, fills from context* · 🧷 the clerk of the print room.
- **`TemplateDoesNotExist`** — Django's "I looked everywhere; no file" error · *raised when no configured location contains the requested name; the `DEBUG` page lists every location tried — read it first* · 🧷 the clerk's receipt of every room checked.

### A011 — App-Level Templates Setup (HTML Integration)

- **App-level templates folder** — an app's own `templates/` directory inside the app package · *searched by the `APP_DIRS` lane when the app is registered; location = `app/templates/`* · 🧷 each shop's private printer.
- **`<app>/` namespacing convention** — putting app templates in a subfolder named after the app · *`app/templates/<app>/page.html`; every `render()` call uses the namespaced name — prevents cross-app name collisions* · 🧷 label every form with the shop's name.
- **Namespaced template name** — the call-side half of the convention · *`'blog/post_list.html'` — a relative path resolved against every configured location; the prefix aims the match* · 🧷 the call rhymes with the file.
- **Two-lane lookup (populated)** — both search locations active · *`DIRS` (project) first, then registered apps' folders in `INSTALLED_APPS` order; first match wins* · 🧷 the checklist walks both rooms.
- **Registration precondition** — the `APP_DIRS` lane only walks registered apps · *an unregistered app's template folder is invisible to the engine — the A006 step matters for templates too* · 🧷 not in the mall directory → its printer isn't on the checklist.
- **Orphaned template** — a staged file no view renders yet · *present on disk, wired lane-wise, but referenced by no `render()` call — reserved (here: `base.html`, for inheritance)* · 🧷 letterhead printed; nobody's holding it.

### A012 — Manage HTML Files

- **Parent template** — the shared skeleton other pages build on · *a template containing `{% block %}` regions; never rendered directly here — reached via `{% extends %}`* · 🧷 the letterhead itself.
- **`{% extends %}`** — the line where a child names its parent · *must be the child's first tag (📌); its string resolves through the normal two-lane lookup* · 🧷 "print this on that letterhead."
- **`{% block %}`** — a named, fillable region of the parent · *`{% block name %}default{% endblock %}` — declares the slot and its fallback content* · 🧷 a labeled blank field.
- **Block default** — what shows when a child stays silent · *the content between `{% block %}` and `{% endblock %}` in the parent; replaced entirely when a child fills the block* · 🧷 the pre-printed line.
- **Child template** — a page that fills a parent's blanks · *contains `{% extends %}` + `{% block %}` fills; stray text outside blocks is dropped (📌)* · 🧷 the filled-in letter.
- **Cross-lane inheritance** — child and parent found in different lanes · *e.g. lane-2 child extends a lane-1 parent — one lookup mechanism, two searches* · 🧷 two rooms, one checklist, twice.

### A013 — Templates 1: Basics & Variables

- **Context dictionary** — the labeled bag of data the view hands the template · *the third argument of `render()`; keys become top-level template names* · 🧷 the evidence bag.
- **`{{ }}` variable** — a print-this-value placeholder · *outputs the resolved value, auto-escaped, as a string* · 🧷 the blank on the form.
- **Dot lookup order** — how dotted names resolve (one rule, every shape) · *dict-key → attribute → list-index (📌); on a miss the variable renders empty* · 🧷 try each door in order.
- **`{% comment %}`** — a template-author note, never served · *block comment stripped server-side (📌)* · 🧷 the margin note.
- **`{# #}`** — a one-line template-author note, never served · *single-line comment stripped server-side (📌)* · 🧷 the sticky note.
- **Auto-escaping** — values print HTML-safe by default · *`<`, `>`, quotes render as entities unless a value is `safe` (📌)* · 🧷 ink that can't stain.
### A014 — Templates 2: Filters (Text, Numbers, Date)

- **Filter** — a print-time reshape of a value · *`{{ value\|filter }}` — the filter receives the resolved value and returns a transformed one; output is auto-escaped; the context is never mutated* · 🧷 a stamp pressed before the ink dries.
- **Filter argument** — a value plugged into a filter · *`{{ value\|filter:arg }}`; quoted `"…"` when it contains commas/spaces (`date:"D,d,M,Y"`, `slice:":2"`, `join:" , "`)* · 🧷 the stamp's dial setting.
- **Format string** — a pattern of date/time one-letter codes · *`"D,d,M,Y"` joined by literal punctuation, consumed by `date`/`time`; codes are case-sensitive (`D` dayname vs `d` daynumber, `M` monthname vs `m` monthnumber)* · 🧷 the letter-pattern for a date stamp.
- **Collection filter** — list access without iteration · *`first`/`last`/`length`/`slice`/`join` — one card, a count, a cut, a strand; `slice` returns a list (repr when printed), `join` returns a string* · 🧷 one card, a count, a cut, a strand.
- **`floatformat`** — round to N decimals · *`{{ 123.4568\|floatformat:2 }}` → `123.46` (round-half-to-even, 📌)* · 🧷 the decimal dial.
- **`divisibleby`** — exact-division test · *returns `True`/`False` — a boolean usable as an `{% if %}` condition* · 🧷 the "is it even?" stamp.
- **`pluralize`** — plural suffix by count · *`Comment{{ count\|pluralize:"s" }}` → `Comments`/`Comment`; the argument appends only when count ≠ 1* · 🧷 the "s" stamp.
- **`yesno`** — three-state truth to words · *`{{ author\|yesno:"Yes,No,Maybe" }}` → `Maybe` when author is `None`; a plain `{% if %}` can't express the explicit-`None` state* · 🧷 the true/false/unknown stamp.
- **`safe` filter** — "I trust this HTML — render it raw" · *marks a value exempt from escaping; owner-authored strings only, never raw user input* · 🧷 the trusted stamp.
### A015 — Templates 3: If, For, With and Cycle

- **Block tag** — a tag that wraps a region · *`{% tag %}` … `{% endtag %}` — the DTL's logic syntax: `if`, `for`, `with`, `cycle`, `firstof`, `verbatim`, `autoescape`* · 🧷 a box with a lid.
- **`{% if %}` / `{% else %}`** — print one branch or the other · *`{% if cond %}A{% else %}B{% endif %}` — truthiness decides; a variable can stand alone as the condition* · 🧷 the fork.
- **Truthiness** — whether a value counts as "yes" in a condition · *`False` · `None` · `0` · `""` · `[]` · `{}` are falsy; everything else truthy (📌)* · 🧷 the switch's "no" list.
- **`{% for %}`** — repeat the body once per element · *`{% for x in xs %}…{% endfor %}` — `x` bound per iteration; the only iteration tag (no `while`)* · 🧷 the conveyor belt.
- **`forloop`** — per-loop metadata · *a dict-like bag: `forloop.counter` (1-based), `counter0`, `first`, `last`, `parentloop` (📌)* · 🧷 the worker's counter clicker.
- **`{% empty %}`** — the empty-collection branch of a loop · *`{% for … %}…{% empty %}…{% endfor %}` — renders instead of the body when the list is empty (📌)* · 🧷 the end-of-line sign.
- **`{% with %}`** — alias an expression for a block · *`{% with name=value %}…{% endwith %}` — binds for the block only; DRY for long repeats* · 🧷 the sticky note.
- **`{% cycle %}`** — yield arguments in turn, wrapping · *`{% cycle 'a' 'b' %}` → a, b, a, b…; per-tag state resets per loop (📌)* · 🧷 the revolving door / color wheel.
- **`{% firstof %}`** — print the first truthy argument · *`{% firstof a b c %}` — skips falsy (`""` included), prints the first truthy, else nothing* · 🧷 the flashlight test.
- **`{% verbatim %}`** — stop the tokenizer · *`{% verbatim %}…{% endverbatim %}` — nothing inside is parsed, not even `{{ }}` (📌)* · 🧷 the do-not-touch sheet.
- **`{% autoescape off %}`** — disable escaping for a region · *`{% autoescape off %}…{% endautoescape %}` — block-scoped `safe` (📌)* · 🧷 the quarantine hatch.


### A016 — Templates 4: Inheritance, Static Files

- **Template inheritance** — one frame, many pages · *a parent declares `{% block %}` slots; children `{% extends %}` it and fill the slots — the parent's skeleton renders with the child's blocks grafted in* · 🧷 blueprint & furnished rooms.
- **`{% extends %}`** — build on a parent · *a child's first tag names the parent; only blocks may follow; the parent renders wearing the child's blocks* · 🧷 the foundation stamp.
- **`{% block %}`** — a named, overridable slot · *`{% block title %} My Title {% endblock %}` — the child's version wins; the parent's in-block content is the default* · 🧷 an empty picture frame.
- **Block default** — shipped filler · *the parent's in-block content, rendered when no child overrides (verified: `'  My Title  '` on a parent-alone render)* · 🧷 showroom furniture.
- **`{% include %}` (template tag)** — paste an organ in place · *`{% include "navbar.html" %}` renders the partial with the current context; identical on every page, not overridable (distinct from URLconf `include()`)* · 🧷 prefab wall.
- **Partial** — a reusable organ · *a small template (nav, card) included by others; never extended, never routed* · 🧷 one organ, many bodies.
- **`{% load %}`** — unlock a tag library, per file · *loads are compile-time and per-template; a parent's load never covers the child's own tags (verified `TemplateSyntaxError`)* · 🧷 the toolbox sign-in sheet.
- **`{% static %}`** — the warehouse address stamp · *joins `STATIC_URL` + asset path → `/static/css/style.css`; computes a URL, never checks the file exists* · 🧷 the warehouse's street sign.
- **`STATIC_URL`** — the public static prefix · *`'static/'` — what the browser asks for; a `startproject` default* · 🧷 the storefront address.
- **`STATICFILES_DIRS`** — the dev warehouse list · *project folders the static finders search (`[BASE_DIR / 'static']`); the one non-default line A016's settings added* · 🧷 the warehouse inventory list.
- **Cross-lane inheritance** — app child, project parent · *an `APP_DIRS` template extends a `DIRS` template because lane 1 is searched first* · 🧷 the tenant borrowing the lobby.
### A017 — Templates 5: Advanced Tags

- **`{% regroup %}`** — pigeonhole a list by a shared value · *`{% regroup students by class as grouped %}` yields `grouper` (the shared value) + `list` (every item sharing it) objects in **first-appearance order — never sorted** (📌); the original list is untouched* · 🧷 mailroom pigeonholes.
- **`group.grouper` / `group.list`** — the hole's label / the hole's contents · *the artifact prints `Class {{ group.grouper }}` and walks members with a nested `{% for student in group.list %}`* · 🧷 the hole label / the hole tray.
- **`{% widthratio %}`** — compute a ratio in markup · *`{% widthratio v m w %}` = `(v/m)·w`, integer-rounded — `50 100 100` → `50`; for percentages/bar widths, not precision* · 🧷 the mailroom calculator.
- **`{% spaceless %}`** — strip pure inter-tag whitespace · *removes whitespace runs that contain *only* whitespace and sit *between two tags*; text-adjacent spaces survive (verified byte-exact)* · 🧷 the gap-filler.
- **`{% filter %}`** — one filter across a whole region · *`{% filter upper %}…{% endfilter %}` stamps the entire region — text **and tags** (`<p>` → `<P>`, verified); region scope vs the pipe's single-value scope* · 🧷 the region stamp.
- **Region vs value** — scope of a transform · *a pipe (`|lower`, `|add`) formats one value; `{% filter %}` applies one filter chain to a whole region* · 🧷 the stamp vs the pen.
- **Parent as page** — defaults are content · *rendering a parent directly serves pure defaults (`' My Title '`, `My Site`); blocks with no child are the page* · 🧷 the unfurnished showroom.
- **Inert load** — unlocked but unused · *`{% load %}` without any use renders fine, because loads only unlock libraries — they demand nothing* · 🧷 the idle register.

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
| **The print shop's stamp rack** | filters: the rack = the filter shelf (text/number/date/collection/logic stamps), each stamp has a dial (`:arg`), the clerk (engine) presses resolve → filter → escape → print per value, the case file (context) is never marked — `date:"D,d,M,Y"` = a date-format stamp, `yesno` = a three-state stamp, `slice` vs `join` = a cut vs a strand | A014 | filters / pipe / date-codes / escaping / list-read questions |
| **The room & where you're standing** | virtual environments: venv = room (a folder), activate = walking in (the `(myenv)` prefix is the door), `pip install` = dropping the package where you stand, deactivate = stepping out | A003 | environment/isolation questions |
| **One command, a skeleton mall** | startproject scaffolding: one command stamps the entire project blueprint (the config skeleton) — you furnish it with apps later; `runserver` opens the doors | A004 | scaffolding / what-was-generated questions |
| **The zoning map** | file ownership: "who writes this — me or the tooling?" — every skeleton item gets a verdict (yours to edit / tooling owns / your data / disposable scratch) | A005 | file-map & edit-vs-never-edit questions |
| **The empty shop unit** | startapp's scaffold = a bare shop shell (files) + nameplate (`apps.py`); registration in `INSTALLED_APPS` = the mall directory lists it; models/views/urls stock it (A007) | A006 | what-was-created / why-is-it-invisible questions |
| **The menu chain / directory-to-menu** | routing hierarchy: `ROOT_URLCONF` = which front door; project `urls.py` = mall directory (keeps `admin/`, delegates everything else); app `urls.py` = the shop's own menu; view = kitchen; `HttpResponse` = the dish; `include()` = "from here, the app is in charge" | A007 | routing / wiring / where-does-a-URL-go questions |
| **Many shops, one directory** | multi-app scale: project = mall directory listing each shop at its own *prefix*; each shop = its own package (views/urls menu); prefixed names (blog-home) = unique dish labels; first-match-wins = only the first identical menu line is served | A008 | multi-app / prefix / name-collision / dead-route questions |
| **The ellipsis address** | URL parameters: pattern = address template with typed blanks (`<int:post_id>` = house-number blank), converter = postal sorting rule (shape-check + type-stamp), view = the resident who answers by keyword name, `re_path` = registered mail with strict format (strings), `**kwargs` = a resident who lists every parcel that arrived | A009 | converters / re_path / kwargs / URL-detail questions |
| **The central print room** | project-level templates: the folder = the building's print room (site-wide forms), `DIRS` = the signpost in the staff handbook (`settings.py`) saying where it is, `APP_DIRS` = the rule "also check every open shop's printer", `render()` = the clerk who finds the form by name and fills it from a brief (context — empty today), `TemplateDoesNotExist` = the receipt listing every room checked | A010 | template setup / DIRS / lookup-order / render questions |
| **Private printers, labeled forms** | app-level templates: each `templates/<app>/` folder = a shop's private printer installed at registration, the `<app>/` subfolder = the shop's name stamped on every form it prints, checklist order = central room then registered shops in `INSTALLED_APPS` order (first labeled match wins), `base.html` = the shared letterhead waiting in the central room, `TemplateDoesNotExist` = the receipt (unregistered shops' trays aren't even listed) | A011 | namespacing / app-vs-project placement / cross-app collision / receipt-reading questions |
| **The company letterhead** | template inheritance: parent = pre-printed letterhead (fixed skeleton + named blanks with defaults), children = filled-in sheets (`{% extends %}` first line + fills, stray text dropped), extends string resolves through the same two-lane lookup (cross-lane here), block-name typos fail silently | A012 | inheritance / extends / block / parent-child / silent-failure questions |
| **The form letter** | templates + variables: the view = the clerk, context = the case file (labeled data), the template = pre-printed form with blanks (`{{name}}`), dots copy file-into-blank through one ordered lookup (dict → attr → index, misses empty), auto-escaping = the clerk copies literally (`<b>` stays text), `safe` = the supervisor's trusted stamp, `default` = the printed fallback — data flows one way, structure never moves | A013 | variables / context / dot-lookup / escaping / render-third-arg questions |
| **The sorting office's tracks** | control-flow tags: `if` = rail switch (fork on truthiness), `for` = conveyor belt (walk collection, per-item box = the loop variable, `forloop` = counter clicker, `empty` = end-of-line sign), `with` = sticky label (alias), `cycle` = revolving color wheel (striping), `firstof` = flashlight sweep (first truthy), `verbatim` = do-not-touch crate (no parsing), `autoescape off` = quarantine hatch (region-safe) — one routing brain, many tagged tracks; the view stays a data provider | A015 | control-flow / truthiness / loop / stripe / verbatim / autoescape questions |
| **The franchise restaurant** | inheritance = the construction blueprint (one shell: walls, wiring, entrance), block = a room the outlet furnishes, block default = showroom furniture, include = the prefab entrance hung identically everywhere, `{% url %}` = ordering by catalog number, `static/` = the central warehouse (`STATICFILES_DIRS` = stock list, `STATIC_URL` = address scheme, `{% static %}` = item label), `{% load %}` = signing the warehouse register yourself — one blueprint, many outlets | A016 | inheritance / include / url / static / load questions |
| **The mailroom's pigeonholes** | advanced tags = the specialist shelf: `{% regroup %}` = the pigeonhole wall (labels = `grouper`, contents = `group.list`, arrival order — never sorted), `{% widthratio %}` = the ratio calculator (integer-rounded), `{% spaceless %}` = the gap-filler (inter-tag gaps only), `{% filter %}` = the region stamp (stamps text and tags) — plus the bare blueprint (`base.html`) served directly as a complete page of pure defaults | A017 | regroup / widthratio / spaceless / filter / region-vs-value questions |

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

**From A004:** What two things did `startproject myProject` create, and what is each
for? · Why do the two `myProject` folders share a name — and which one do imports use?
· Name the inner package's files and each one's job · `django-admin` vs `manage.py` —
when does the journal use each, and why? · What does `runserver` print, where does it
serve, and what must it never be used for? · Which four settings did we read and why
does each matter? · The 5.2.7-vs-6.1.1 story — which Django lesson does it prove? ·
What did the rocket page prove beyond "the command exited 0"?

**From A005:** Draw the complete project map — all 10 items · Which items may you edit, and which must you never touch? · What is `db.sqlite3`, and what manages it? · What is `__pycache__/`, and why is it disposable? · Outer vs inner folder — which one do Python imports use? · What did `runserver 8080` prove about ports? · The case-sensitivity rule — and the one place it bites · Where will your own files live from A006 onward?

**From A006:** What does `startapp` create — name all the files? · What is in `apps.py`, and where does the class name come from? · The four things `startapp` does NOT do · Why was the app invisible right after the command ran? · Where does the app land, and what are the naming rules? · Which artifact line proves registration is manual — and why can't `startapp` write it?
**From A014:** The four pipeline stages between a `{{ }}` and the browser — and which stage never mutates the context? · Verify the `D`/`d`, `M`/`m`, `Y`/`y` date-code case distinctions. · Why does `truncatechars:10` output `My Second…` (9 chars + the counted ellipsis)? · Why must comma-bearing args be quoted (`date:"D,d,M,Y"`)? · `slice:":2"` prints a list repr while `join:" , "` prints clean text — what type difference causes it? · `yesno:"Yes,No,Maybe"` → `Maybe` for `None`; what would `""` and `0` print, and why can't a plain `{% if %}` say "explicit None"? · The artifact hosts the series' first `{% if %}` — which lecture formally owns control flow?
**From A015:** How many block tags does the artifact use, and what are they (by category)? · `{% if blogs.1.is_feature %}` resolves how, and which branch wins? · Why does `{% firstof blogs.1.author "ABC" %}` print `ABC`? · The three escaping states of one `{{html_code}}` — which tag/filter makes each? · `forloop.counter` printed 1,2,3 — what else lives in `forloop` and where does it end? · Two loops, two `{% cycle %}`s — does the second start fresh, and why? · The dot chain `blogs.1.is_feature` — which A013 order rule does it exercise? · `GET /blog/` → 200 but `GET /` → 404 — which single line explains it?
**From A016:** Which file owns `<html>`, and what exactly do the children own? · What prints when a child skips the title block — and where was that verified? · `{% include %}` vs `{% block %}` — what can a child never change? · Name the four dev static links in order; what breaks visually if `STATICFILES_DIRS` is missing? · Derive both verified title reprs (`'  Home Page  '` vs `' About Page '`) from source · Why can an app-lane child extend a `DIRS` parent, and which lane wins a clash? · What error — at which phase — does a missing `{% load static %}` produce?
**From A017:** What two things live inside each `{% regroup %}` object — and which one did the artifact print as the hole's label? · `10th → 9th → 8th` — whose order is that, and where would you sort instead? · `{% widthratio 50 100 100 %}` prints what, and why is it for bars not money? · Quote the byte-exact spaceless div block — what vanished, what survived? · How did `{% filter upper %}` prove its region scope (which two characters changed)? · Why does `/blog/` show `My Site` while `/blog/blog/` shows the shelf — same `base.html`? · Name the artifact's three ⚠️ quirks a reviewer must catch · Pipe vs `{% filter %}` — when each?

**From A007:** Name the three files a request crosses, in order · The three `path()` arguments, and the `views.home()` bug · Why `startapp` makes no `urls.py` — evidence from A006's artifact · What do the commented-out lines in `dj1/urls.py` teach? · 404 on `/about/` — which file opens first? · Where and when does `a = 10 + 50` run? · What did journal lines 19–25 add to the environment? · Why does `name=` matter even before any template exists?

**From A008:** The two mechanisms A008 adds over A007, and what each prevents · Trace `/shop/products/` through both URL tables · What makes the artifact's second `shop` route dead? · Why must `blog` and `shop` route names differ? · Where does the `blog/` prefix live, and who strips it? · Is a `name=` enough to make a URL work — why? · The three essentials of a multi-app project · Why is a third app "mechanical"?

**From A009:** What does `/blog/post/73/` deliver to the view, exactly? · Why does `<int:post_id>` reject `/blog/post/abc/`? · The one type difference between `path` converters and `re_path` groups · Why did the artifact replace an explicit `article_details(year, month)` signature with `**kwargs`? · Name the five default converters · Where do converters live — app or project file? · Decode `r'^article/(?P<year>[0-9]{4})/$'` piece by piece · Path parameter vs query string — when each?

**From A010:** The two lookup locations, in order — and who can be shadowed? · The three touches that set up project-level templates, proven against A004's default settings · What `render()`'s missing third argument means for the artifact's page · Why does `myProject3/` work with zero apps? · Why is `import os` needed with `os.path.join` (and what breaks without it)? · Why does `render(request, 'templates/home.html')` fail? · The three failure stages on the `/` journey (404 / startup `NameError` / `TemplateDoesNotExist`) · What does the `MAILERS` block in the artifact's settings actually do?

**From A011:** Trace `'blog/post_list.html'` through both lanes — every miss and the hit · Why the doubled folder (`blog/templates/blog/`) — what collision does it prevent? · What happens if the app is never registered in `INSTALLED_APPS`? · The artifact's one asymmetry (`blog` first in registration, `shop/` first in URLs) — why harmless, when not? · A010's vs A011's `DIRS` spelling — what changed and what proves it? · Why is `base.html` an orphan, and what lecture gives it a job? · Where does `GET /shop/` differ from A010's `GET /` journey? · What breaks / survives if `DIRS` empties to `[]`?
**From A012:** How does the engine find the parent named in `{% extends %}` — new mechanism or reused? · What renders when a child skips a block, and is there an error? · The two silent failures (typo'd block name, stray outside-block text) — symptom and fix for each · Trace `GET /shop/` stations 9–11: what is new vs byte-identical? · Why did `base.html`'s move from the inner config package to the outer root matter? · Shop's child shrank 321→221 bytes — where did the bytes go, and why is blog's delta tiny? · What is still missing from every template (zero `{{ }}`) — and which lecture supplies it?
**From A013:** What does `render()`'s third argument do, and what silently happens without it? · Dots resolve in what order — and what does `{{skills.0}}` walk through? · Why do missing names render empty instead of raising an error? · What does auto-escaping do to `<b>` — and how does `|safe` (safely) change it? · Which two comment syntaxes never reach the browser, and which comment always does? · The datetime `{{ }}` self-format — where does it come from? · Why does printing a whole list produce `['a', &#x27;b&#x27;]`? · What still needs the `{{ }}` variables to be useful together (iteration, filter family) — and which lecture?



---

## 5. Spaced-Revision Schedule

| Chapter | Day 1 | Day 7 | Day 30 |
|---|---|---|---|
| A001 | Re-read 📝 Quick Revision; answer 🔁 recall questions | Redraw the 5 Mermaid diagrams from memory; explain project vs app aloud | Do the Level-4 exercise; deliver 🎯 interview answers aloud |
| A002 | Re-read 📝 Quick Revision; recite the three layers + their files | Redraw the `/chai/3/` journey table from memory; annotate `views.py` aloud | Trace a fresh URL (e.g. `/chai/chai_stores/`) through every file; answer the interview set aloud |
| A003 | Re-read 📝 Quick Revision; recite the 6-command chain | On a fresh folder: create → activate → install → verify, without notes; explain aloud why the order matters | Set up a new project's venv from scratch; answer the interview set aloud |
| A004 | Re-read 📝 Quick Revision; recite the 2-command chain and what each created | Redraw the `myProject` artifact tree from memory; explain inner vs outer folder aloud | `startproject` a fresh project and `runserver` it; answer the interview set aloud |
| A005 | Re-read 📝 Quick Revision; recite the complete project map | Redraw the zoning/ownership map from memory; classify all 10 items without notes | Run the A005 artifact's server on 8080, then 8000; answer the interview set aloud |
| A006 | Re-read 📝 Quick Revision; recite the 7 generated files and the 4 silences | Redraw the `blog/` tree from memory; explain registration + the artifact's `# Custom app created by user` comment aloud | Create + register a fresh app and run `check`; answer the interview set aloud |
| A007 | Re-read 📝 Quick Revision; recite the three-file wiring + the `path()` formula | Redraw the `/about/` journey (files in order) from memory; explain the commented-out lines in `dj1/urls.py` aloud | Wire a fresh app: write two views + app urls + one `include()` and serve them; answer the interview set aloud |
| A008 | Re-read 📝 Quick Revision; recite the multi-app `urls.py` shape + the three uniqueness rules | Redraw the two-shop tree + `/blog/about/` prefix-strip flow from memory; explain the `shop/urls.py` dead route aloud | Add a third app (startapp → register → view → urls → include) and serve it; answer the interview set aloud |
| A009 | Re-read 📝 Quick Revision; recite the converter→keyword contract + the `re_path` string-trap | Redraw the `/blog/post/73/` journey from memory; explain why the artifact uses `**kwargs`; decode the `re_path` regex aloud | Add a `product/<int:product_id>/` route to the artifact and watch 404/`TypeError` behavior; answer the interview set aloud |
| A010 | Re-read 📝 Quick Revision; recite the `DIRS`→`APP_DIRS` order + the edit trio | Redraw the `/` render journey from memory; explain `render()` as find-fill-wrap aloud; diff A010's `settings.py` against A004's | Add an about page to `myProject3/`, then deliberately break and fix a `TemplateDoesNotExist` via the tried-list; answer the interview set aloud |
| A011 | Re-read 📝 Quick Revision; recite the stamp convention + the two-lane checklist | Redraw the two-lane trace of `'blog/post_list.html'` from memory; explain the doubled folder and the registration precondition aloud | Add the stamped shop about page, then break it three ways (bare name / missing stamp / unregistered) and restore; answer the interview set aloud |
| A012 | Re-read 📝 Quick Revision; recite the two block names + the extends string | Redraw the `/shop/` parent+child journey (stations 9–11) from memory; explain defaults vs fills aloud | Add the about child, break it two silent ways, change the banner once and confirm propagation; answer the interview set aloud |
| A013 | Re-read 📝 Quick Revision; recite render's third arg + the dot order | Redraw the form-letter flow (context → lane-2 hit → fill → response) from memory; explain a missing-key miss — silent empty string, and why | Extend the artifact with an about page (context + `{{ }}` + a `safe`/`default` touch), then break the handshake three ways (no context arg / key typo / `[0]` brackets); answer the interview set aloud |
| A014 | Re-read 📝 Quick Revision; recite the pipeline + the six filter families | Redraw the stamp-rack flow (dict → pipeline → 20 filters → response) from memory; explain why `slice` prints a repr and `join` prints text; decode `date:"D,d,M,Y"` aloud | Add a chained filter row, break the `join:" "` quotes (watch the error), flip `author` through `None`/`""`/`"Adnan"` and read the `yesno` output each time; answer the interview set aloud |
| A015 | Re-read 📝 Quick Revision; recite the nine block tags + the falsy list | Redraw the sorting-office flow (fork → belt → stripes → response) from memory; explain why `firstof` skipped the empty string and why `{% cycle %}` restarts per loop | Add a Featured ★ suffix via `{% if blog.is_feature %}`, hide row 2 with `{% if blog.author %}`, empty `blogs` in the view and watch both `{% empty %}` branches; answer the interview set aloud |
| A016 | Re-read 📝 Quick Revision; recite the static chain + the load rule | Redraw the franchise flow (blueprint → slots → organs → warehouse) from memory; explain both title reprs and why the nav cannot vary | Do the three Practical-Example exercises (footer slot, contact child + load-crash, `blog:` namespace); answer the interview set aloud |
| A017 | Re-read 📝 Quick Revision; recite the four specialist tags + region-vs-value | Redraw the mailroom flow (tray → holes → calculator → shelf) from memory; explain regroup's first-appearance order and the `<P>` proof | Do the three Practical-Example exercises (re-order the list, add the duplicate student, build the `progress.html` widthratio page); answer the interview set aloud |

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
- **A004 documented** — chapter built from two in-repo sources: the command journal's
  new lines (11 & 13, quoted verbatim) and the actual generated `myProject` artifact
  (`settings.py`, `manage.py`, `urls.py`, `wsgi.py`/`asgi.py` quoted verbatim). The
  journal-vs-artifact Django version difference (5.2.7 vs 6.1.1) preserved as a formal
  discrepancy note — a live demonstration of A003's isolation lesson. 10 glossary terms
  added; "One command, a skeleton mall" mental model registered; recall bank and
  revision schedule extended; hub TOC updated to ✅; A003's next-lecture bridge now
  points here.
- **A005 documented** — chapter built from the journal's new line 15 (`runserver 8080`)
  and the second real artifact `myproject/` (lowercase — the case-sensitivity teachable).
  Differentiated from A004's file tour per AGENTS §11: complete map (incl. `db.sqlite3`
  & `__pycache__/`), four-verdict ownership/zoning split, launch-time port lesson.
  7 glossary terms added; "The zoning map" mental model registered; recall bank and
  revision schedule extended (A004's isolated table rows repaired); hub TOC updated to ✅.
- **A006 documented** — chapter built from the journal's line 17 (`startapp blog`, quoted
  verbatim) and a third real artifact: the generated `blog/` app inside A006's
  `myproject/` (all stub files quoted verbatim; `INSTALLED_APPS` shows the user's
  hand-written `'blog', # Custom app created by user` — on-disk evidence that
  registration is a manual step; `urls.py` remains admin-only and `db.sqlite3` 0-byte,
  captured as "the four silences"). 5 glossary terms added; "The empty shop unit"
  mental model registered; recall bank and revision schedule extended; hub TOC updated
  to ✅.
- **A007 documented** — chapter built from the journal's lines 19–25 (the environment
  rebuild: `pip install vern` as written, `py -m venv venv`, `venv/Scripts/activate`,
  `django-admin --version`) and a fourth real artifact: the `dj1/` project whose `blog/`
  app now contains written views and URLs (all quoted verbatim). Core teaching: the
  three-file wiring (view → app `urls.py` → project `include()` + `ROOT_URLCONF`),
  URL↔view separation, `path(route, view, name=…)`, and the owner's commented-out
  direct-import attempts preserved as on-disk evidence of the workflow (with `render`
  imported-but-unused signaling templates are next). 7 glossary terms added; "The menu
  chain / directory-to-menu" mental model registered; recall bank and revision schedule
  extended; hub TOC updated to ✅. A008's actual topic (Multiple Apps with Views & URLs —
  its folder now exists in the repo) is named in the bridge, and the next-lecture nav
  link points at it.
- **A008 documented** — chapter built from the journal's lines 19–25 (the environment
  rebuild) and a fifth real artifact: `myProject1/` running TWO apps (`blog` + `shop`),
  views/urls/settings quoted verbatim. Core teaching: URL prefixes + prefix-stripping
  (project mounts, app defines), name-collision avoidance via manual name prefixing
  (`blog-home`/`shop-home`; formal `app_name` flagged 📌), and — the star lesson — a
  REAL duplicate-`''` bug in `shop/urls.py` dissected per AGENTS §12 (first-match-wins,
  dead routes, "a name labels a path but never creates one"). 6 glossary terms added;
  "Many shops, one directory" mental model registered; recall bank and revision schedule
  extended; hub TOC updated to ✅. A009's actual topic (URL Parameters: path, re_path,
  kwargs — its folder now exists in the repo) is named in the bridge and nav link.
- **A009 documented** — chapter built from a sixth real artifact: `myProject2/` whose
  `blog` app reads values from URLs (`blog/views.py` + `blog/urls.py` quoted verbatim).
  Core teaching: the converter→keyword contract (`<int:post_id>` → `post_id=73`),
  `path` vs `re_path` (regex groups arrive as strings — the type trap), multi-segment
  routes, and the `**kwargs` view that superseded a commented-out explicit signature
  (the "two routes, one view" story). The artifact's shared `name='article_details'`
  flagged as fragile per A008's lesson. 6 glossary terms added; "The ellipsis address"
  mental model registered; recall bank and revision schedule extended; hub TOC updated
  to ✅. Next lecture (A010 Templates Folder Setup — its folder already exists) linked
  in the bridge and nav footer.
- **A010 documented** — chapter built from a seventh real artifact: `myProject3/`, the
  first with **no app** — a project-level `templates/home.html`, a config-package
  `views.py` calling `render()` for the first time in the series' own projects (A007's
  imported-but-unused `render` debt paid), and a `settings.py` whose three manual edits
  (folder, `import os`, `'DIRS': [os.path.join(BASE_DIR, 'templates')]`) are proven
  against A004's pristine same-Django-6.1.1 settings in an in-repo diff. Two honest flags
  per §12: the legacy `os.path.join` style (vs `BASE_DIR / 'templates'`, 📌) and an inert
  `MAILERS` block Django's core never reads (the core setting is `EMAIL_BACKEND`). Core
  teaching: call-by-name/configure-the-search, the `DIRS`→`APP_DIRS` lookup order with
  first-match shadowing, find-fill-wrap `render()` mechanics, the 8-station `/` journey,
  and `TemplateDoesNotExist` as diagnostic output. 6 glossary terms added; "The central
  print room" mental model registered; recall bank and revision schedule extended; hub
  TOC updated to ✅. Next lecture (A011 App-Level Templates Setup — HTML Integration; its
  folder already exists with the `myProject4/` artifact) named and linked in the bridge
  and nav footer.
- **A011 documented** — chapter built from an eighth real artifact: `myProject4/` running
  TWO registered apps (`blog` + `shop`), each owning a namespaced `templates/<app>/`
  folder with a tag-free page — the `APP_DIRS` lane A010 left as a no-op now populated
  and dissected. Core teaching: the `<app>/` namespacing convention (A008's prefixing
  lesson applied to files; the doubled folder prevents cross-app collisions), the
  populated two-lane trace (`DIRS` misses, `INSTALLED_APPS` order hits), registration as
  a twice-over precondition, ownership-based placement (project room = shared letterhead,
  private printers = app pages), and the artifact's honest asymmetries (pathlib `DIRS`
  arriving — A010's 📌 prediction paid off; `blog`-first registration vs `shop/`-first
  URLs, harmless because disjoint; `base.html` orphaned, staged for inheritance; the
  inert `MAILERS` block carried over verbatim). 6 glossary terms added; "Private
  printers, labeled forms" mental model registered; recall bank and revision schedule
  extended; hub TOC updated to ✅. A010's nav footer repointed at this chapter. Next
  lecture (A012 Manage HTML Files — its folder already exists) named and linked in the
  bridge and nav footer.
- **A012 documented** — ninth artifact, same myProject4, zero Python changed: three rewritten templates (parent base.html with title/content blocks plus two extends children); teaches cross-lane lookup, defaults, silent failures, ownership; inner-to-outer base.html move flagged per section 12; 6 terms, letterhead model, recall/revision extended, hub updated, A011 nav repointed, A013 linked.
- **A013 documented** — chapter built from a tenth real artifact: `myProject5/`, a fresh single-app project (`blog`) whose `home.html` is the first template in the series' own projects to carry live `{{ }}` variables. Core teaching: the context dictionary as `render()`'s third argument (the evidence-bag handshake — keys become template names), the dot-lookup order (dict-key → attribute → list-index; misses silently empty, 📌), `{{ }}` printed escaped-by-default with `|safe` as the opt-out, the three comment syntaxes' fates (`{% comment %}`/`{# #}` never served vs HTML comments always), and the structure-vs-data divide (A012 blocks shape, A013 variables fill). Verified by rendering the artifact's bytes through Django 6.1.1's template engine (all 12 outputs, comment fates, datetime self-format confirmed). 7 glossary terms added; "The form letter" mental model registered; recall bank and revision schedule extended; hub TOC updated to ✅; A012's nav footer repointed at this chapter (folder → README.md). The in-`views.py` `User` class, `MAILERS` block carried over, and A002's "loop" terminology are flagged ⚠️ per §12. Next lecture (A014 Templates 2: Filters — its folder already exists) named and linked in the bridge and nav footer.
- **A014 documented** — chapter built from an eleventh real artifact: `myProject6/`, a fresh single-app (`blog`) project whose `blog_details.html` is literally a filter shelf — 20 distinct filters across the text (upper/lower/capfirst/title/truncatechars/truncatewords/linebreaks/urlencode), number (floatformat/add/divisibleby + pluralize), date/time (date:"D,d,M,Y", time:"H:i"), collection (first/last/length/slice/join), and three-state-logic (yesno) families, plus the series' first `{% if %}`. Core teaching: the resolve→filter→escape→print pipeline (context never mutated), case-sensitive date codes (D/d, M/m, Y/y), quote-args-with-commas, slice's list-repr vs join's string output, yesno's explicit-`None` third state. Verified twice: engine render of artifact bytes with artifact context AND a live `GET /` → 200 (the owner's early-404 is resolved by the current `''→include→''→blog_details` wiring). 8 glossary terms added; "The print shop's stamp rack" mental model registered; recall bank and revision schedule extended; hub TOC updated to ✅; A013's nav footer repointed at this chapter (folder → README.md). The `"web devlopment"` typo, `Float formate` label, nested-`<p>` linebreaks output, and inert `MAILERS` block are flagged ⚠️ per §12. Next lecture (A015 Templates 3: If/For/With and Cycle — its folder already exists) named and linked in the bridge and nav footer.
- **A015 documented** — chapter built from a twelfth real artifact: `myProject7/`, a fresh single-app (`blog`) project whose `blog_list.html` is the series' first true control-flow page — nine block tags under the owner's own `{% comment %}` banners: `if`/`else` (forking on `blogs.1.is_feature` → False → else-track), `for` ×2 with `forloop.counter` and `{% empty %}` (the `<ul>` list and the `<table>`), `{% with total_blogs=blogs|length %}`, `{% cycle 'lightblue' 'lightgreen' %}` (rows lightblue→lightgreen→lightblue), `{% firstof blogs.1.author "ABC" %}` (empty string is falsy → `ABC`), `{% verbatim %}` (prints `{{blogs.1.author}}` literally), and `{% autoescape off %}` (raw `html_code` — while default escaping and `|safe` show the other two states). Core teaching: truthiness is the one rule; block tags pair by keyword; dots compose through list-of-dicts (`blogs.1.is_feature`); `forloop` and `empty` are per-loop; the page mounts at `/blog/` (A008's prefix) so root `/` 404s by design. Verified twice: engine render of artifact bytes with artifact context AND a live request path — `GET /blog/` → 200 with 12 content assertions, `GET /` → 404, `GET /admin/` → 302. 11 glossary terms added; "The sorting office's tracks" mental model registered; recall bank and revision schedule extended; hub TOC updated to ✅; A014's nav footer repointed at this chapter (folder → README.md). The inert `MAILERS` block, `DIRS` pointing at a nonexistent outer `templates/`, the tight `Author:{% firstof %}` spacing, and the educational else-track pinning are flagged ⚠️ per §12. Next lecture (A016 Templates 4: Inheritance, Static Files — its folder already exists) named and linked in the bridge and nav footer. Contract amended (§13 step 8 + §14 checklist): every chapter ends with a commit and `git push origin main` — done means shipped.
- **A016 documented** — chapter built from a thirteenth real artifact: `myProject8/`, a fresh single-app (`blog`) project that finally shares one shell and wears real styles: `templates/base.html` (505 B) is the parent — `<title>` block shipping the default `My Title`, `{% load static %}` + css/js via `{% static %}`, `{% include "navbar.html" %}` (144 B) whose links are `{% url %}` reversals, a `content` block, and a hard-coded footer — with two children: outer `home.html` (572 B; overrides both blocks, loads static for its `<img>`, inert login form with `{% csrf_token %}`, `onclick="showAlert()"` wired by the parent's script) and app-level `blog/about.html` (168 B; the cross-lane child extending the `DIRS` parent). `settings.py` adds exactly one non-default line — `STATICFILES_DIRS = [BASE_DIR / 'static']` — beside a real warehouse: css 308 B, js 73 B, logo.png 24,890 B (valid PNG). Core teaching: inheritance is *grafting* (child blocks into the parent skeleton); block content is *verbatim text* (verified title reprs `'  Home Page  '` / `' About Page '` / `'  My Title  '`); includes are organs not slots; `{% url %}` reverses names at render (⚠️ flat names — `app_name` is the 📌 cure); the dev static chain is four links (staticfiles app → `STATICFILES_DIRS` → `STATIC_URL` → `{% load static %}`+`{% static %}`) and fails *silently* (asset 404, page 200; 📌 `collectstatic` in production); loads don't inherit — verified by a parse-time `TemplateSyntaxError: Invalid block tag 'static'`. Verified twice: engine render of the artifact's templates (17/17 assertions, incl. parent-alone default) AND live request path — `GET /blog/` 200 (10 assertions), `GET /blog/about/` 200 (7), three assets 200 byte-identical, `GET /` 404 (A008's prefix), `GET /admin/` 302 → login 200 (0-byte db flagged ⚠️). 11 glossary terms added; "The franchise restaurant" mental model registered; recall bank and revision schedule extended; hub TOC updated to ✅; A015's nav footer repointed at this chapter (folder → README.md). The inert `MAILERS` block (fourth artifact running), the hard-coded `© 2023` footer, the namespace-less `{% url %}` names, the inert login form, and the unmigrated admin are flagged ⚠️ per §12. Next lecture: Django's forms/database layer (the artifact's
  painted-on doors) — A017's folder (which already exists) drops with its lecture.
- **A017 documented** — chapter built from a fourteenth real artifact: `myProject9/`, a fresh
  single-app (`blog`) whose `blog/templates/blog.html` (865 B, un-namespaced) shelves four
  specialist tags — `{% regroup %}` (students → `10th → 9th → 8th` holes, first-appearance order),
  `{% widthratio 50 100 100 %}` → `50`, `{% spaceless %}` (byte-exact joined spans), and
  `{% filter upper %}` (`<p>` → `<P>`, region scope) — plus the parent `base.html` (279 B) rendered
  directly as a complete page of pure defaults (`' My Title '` + `My Site`). Verified twice:
  engine render of artifact bytes (13/13 assertions) AND live request path (`GET /blog/` 200
  defaults-as-page, `GET /blog/blog/` 200 13/13, `/` 404, `/admin/` 302). 8 glossary terms added;
  "The mailroom's pigeonholes" mental model registered; recall bank and revision schedule
  extended; hub TOC updated to ✅; A016's nav footer repointed at this chapter (README.md → README.md).
  The un-namespaced child, inert `{% load static %}`, artifact typos ("Blog Us", "a upper case"),
  inert `MAILERS` block, and the `/blog/blog/` double-prefix wiring are flagged ⚠️ per §12.
  Next lecture: A018 Bootstrap in Django — its folder already exists.
