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
| A002 | `A002_MVT_Architecture_Explained` | MVT Architecture Explained | 🗓️ Planned | — |

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

---

## 5. Spaced-Revision Schedule

| Chapter | Day 1 | Day 7 | Day 30 |
|---|---|---|---|
| A001 | Re-read 📝 Quick Revision; answer 🔁 recall questions | Redraw the 5 Mermaid diagrams from memory; explain project vs app aloud | Do the Level-4 exercise; deliver 🎯 interview answers aloud |

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

