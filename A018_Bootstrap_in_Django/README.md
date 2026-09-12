# 🚀 A018 — Bootstrap in Django

`📖 Lecture A018` · `🎓 Track: Core Django` · `📶 Level: Beginner` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** no lecture transcript or notes exist for A018 — this
> chapter is built from the repo's own fifteenth artifact, `myProject10/` (all files quoted
> verbatim), plus the owner's command-journal line `pip install django-bootstrap5`
> (`commands.txt`). Bootstrap-version facts and CDN/test-client mechanics come from the
> installed third-party package `django-bootstrap5 26.3` and official Django docs, marked 📌.

---

## 🧭 What You Will Learn

- [ ] Explain what Bootstrap gives Django templates that raw CSS does not — ready-made
  components (`btn btn-primary` et al.) plus a grid/utilities system shipped as CSS + JS
- [ ] Wire **three different Bootstrap delivery channels** in one parent: a
  `django-bootstrap5` template tag, a commented-out CDN fallback, and project-local
  `{% static %}` asset links
- [ ] Read a parent (`templates/base.html`) that stacks all three channels and say, for each
  line, which channel serves the line and what it resolves to
- [ ] Trace `GET /blog/` end to end: mount → `blog` view → un-namespaced child →
  cross-lane `{% extends %}` → `corecss` block override → final 1,368-byte page
- [ ] Diagnose the artifact's **dead asset label** from first principles: why
  `/static/js/bootstrap.bundle.min.js` misses while the page itself returns 200
- [ ] Reproduce every number in this chapter with the engine render and the
  live request path on Django 6.1.1 + `django-bootstrap5 26.3`

## 🎯 Why This Lecture Matters

Every template lecture so far built the *skeleton*: inheritance gave pages one shared shell
(A016), the specialist tags gave them a working shelf (A017) — but the pages still *look*
like wireframes. The moment a teacher says "now make it pretty," beginners reach for a CSS
framework, and in a Django classroom that framework is almost always **Bootstrap**: a
vocabulary of class names (`btn`, `btn-primary`, `alert`, `container`) whose styling and
behavior arrive as plain CSS + JS files the browser must download.

This lecture is the series' first **third-party bridge**: Django itself never changes — the
same `render()`, the same two-lane lookup, the same `{% static %}` label system — but the
page gains two new kinds of suppliers: a **template-tag bridge** (`django_bootstrap5`,
installed via `pip install django-bootstrap5`) that *prints* the Bootstrap `<link>` /
`<script>` elements for you, and a **CDN fallback** (commented out in the artifact, kept as
a museum piece). The artifact keeps all three wiring styles side by side — tag bridge, CDN
comment, and local `{% static %}` links — which makes it a perfect specimen for learning
*which* channel serves *which* line, and what happens when a warehouse shelf stands empty.

What breaks if you skip it: the next time a page looks unstyled you'll blame Django, the
template, or the browser — when the actual failure mode (this artifact proves it live) is a
**silent asset 404 beside a healthy page 200**. A016 taught that four-link static chain;
A018 is the lecture where you watch one of its links miss and learn to read page source
like a supply manifest.

## ✅ Prerequisites

---

## 🏗️ The Artifact — A Styled Shell With Three Supply Channels (Fifteenth Artifact)

The pattern is familiar by now: a fresh single-app project — `myProject10/`, app `blog`,
project-level `templates/`, `blog/`-prefixed URLs, one view, one child page. What is new
is everything around that skeleton:

| # | File | Size | Role in this lecture |
|---|---|---|---|
| 1 | `myProject10/templates/base.html` | 1,779 B | **The specimen.** A parent wiring *three* Bootstrap channels at once: `django_bootstrap5` tags (live), CDN links (commented museum), local `{% static %}` links (live labels, one dead target) |
| 2 | `myProject10/blog/templates/blog.html` | 252 B | The child. Un-namespaced (⚠️, like A017), extends across lanes, overrides **two** blocks: `title` and `corecss` |
| 3 | `myProject10/blog/views.py` | 125 B | One view, `blog`, context-free `render(request, 'blog.html')` |
| 4 | `myProject10/blog/urls.py` | 112 B | One pattern, `''` → `blog`, `name='blog'` |
| 5 | `myProject10/myProject10/urls.py` | 839 B | `blog/` prefix include + admin (the A008 mount, fifth artifact running) |
| 6 | `myProject10/myProject10/settings.py` | 3,443 B | Two firsts: `'django_bootstrap5'` in `INSTALLED_APPS`, and the first *populated* `STATICFILES_DIRS` of the `STATIC_URL`-only era — pointing at an **empty warehouse** |
| 7 | `myProject10/blog/static/styles.css` | 24 B | The only real stylesheet in the repo: `h1 { color: red; }` — sitting in the *app* lane while the parent's label points elsewhere |
| 8 | `myProject10/static/{css,js}/` | 0 files | Two **empty directories** — the warehouse shelves the settings point at |
| 9 | `myProject10/venv/` | — | The project's own interpreter: Django 6.1.1 + `django-bootstrap5 26.3` (the bridge lives here, nowhere else) |
| 10 | `myProject10/db.sqlite3` | 0 B | Sixth artifact running — still an empty promise, forms/database still pending |

Two things to notice before we open anything. First, this is the first artifact whose
*interesting* behavior comes from a package that is **not Django**: `django_bootstrap5`
sits in `venv/Lib/site-packages/` and is registered in `INSTALLED_APPS` like any app —
that's the whole installation story (`pip install django-bootstrap5`, journal line 27).
Second, the artifact is a *wiring museum*: commented-out CDN `<link>` / `<script>` on lines
5 and 32, live `{% bootstrap_css %}` / `{% bootstrap_javascript %}` on lines 7–8, and live
`{% static %}` labels on lines 12 and 33. Three eras of "how do I get Bootstrap into my
page" preserved in one 35-line file. The chapter's first job is to date each exhibit.

### The artifact tree (nothing cached, nothing generated)

```text
myProject10/
├── manage.py
├── db.sqlite3                      # 0 bytes — sixth artifact running
├── blog/
│   ├── admin.py  apps.py  models.py  tests.py  views.py  urls.py  __init__.py
│   ├── migrations/__init__.py
│   ├── static/
│   │   └── styles.css              # 24 B — the ONLY real CSS file
│   └── templates/
│       └── blog.html               # 252 B — un-namespaced child (⚠️)
├── myProject10/
│   ├── settings.py                 # 3,443 B — bridge registration + STATICFILES_DIRS
│   ├── urls.py                     # 839 B — blog/ prefix + admin
│   └── asgi.py  wsgi.py  __init__.py
├── templates/
│   └── base.html                   # 1,779 B — the three-channel parent
├── static/
│   ├── css/                        # EMPTY — the warehouse shelf
│   └── js/                         # EMPTY — the warehouse shelf
└── venv/                           # project interpreter (Django 6.1.1, bootstrap5 26.3)
```

---

## 🧠 Core Idea 1 — Bootstrap Is a Costume Shipped as Files

**Definition.** Bootstrap is a front-end component library: a set of CSS classes
(`btn btn-primary`, `btn-success`, …) plus companion JavaScript, versioned and
distributed as static files (or a CDN mirror of those files). Django never "runs"
Bootstrap — the browser downloads the files referenced by the page's `<link>` / `<script>`
elements and applies them. Django's only job is to *print the right references*.

**Why it exists.** Hand-writing "a blue button with hover, focus ring, disabled state, and
dark-mode variant" is slow and inconsistent; nine such buttons (the artifact's parent has
exactly nine) is a design system. Bootstrap sells the finished system: you write
`class="btn btn-primary"` and the framework's CSS does the rest — *if* the CSS file
actually arrives.

**The artifact proof.** Open the parent and count the costume rack — nine buttons, lines
17–26, each wearing two classes:

```html
<button type="button" class="btn btn-primary">Primary</button>
<button type="button" class="btn btn-secondary">Secondary</button>
<button type="button" class="btn btn-success">Success</button>
<button type="button" class="btn btn-danger">Danger</button>
<button type="button" class="btn btn-warning">Warning</button>
<button type="button" class="btn btn-info">Info</button>
<button type="button" class="btn btn-light">Light</button>
<button type="button" class="btn btn-dark">Dark</button>

<button type="button" class="btn btn-link">Link</button>
```

**Explanation.** Every button says the same thing in two words: `btn` ("I am a Bootstrap
button") and one variant (`btn-primary`, `btn-danger`, … — "paint me this color"). No
Django tag anywhere in these lines: pure HTML waiting for CSS. The verified render carries
all nine words (`btn btn-primary` asserted HIT) — the *markup* is present. Whether the
*paint* arrives is a static-files question.

> **Confusion to pre-empt:** "I installed `django-bootstrap5`, so Bootstrap works." No —
> installation only stocks the *bridge* (template tags). The paint still travels by
> `<link>` / `<script>`, each a separate delivery with its own failure mode. The artifact's

## 🧠 Core Idea 2 — The Bridge: `django_bootstrap5` Prints Your Link Tags

**Definition.** `django-bootstrap5` (version 26.3 in this project's venv) is a third-party
Django app whose template tags render Bootstrap's `<link>` / `<script>` elements for you,
pointing at a pinned CDN build. You `{% load django_bootstrap5 %}` and write
`{% bootstrap_css %}` / `{% bootstrap_javascript %}`; the tags expand to full elements
with `href`/`src`, `integrity` hashes, and `crossorigin` attributes.

**Why it exists.** Bootstrap's CDN URLs are long, version-pinned, and integrity-hashed —
exactly the kind of string humans mistype. The bridge centralizes them: upgrade the
package, and every page's references move together. (📌 Version 26.3 of the package
emits Bootstrap **5.3.8** URLs — bridge version ≠ Bootstrap version.)

**The wiring.** `settings.py` registers the bridge as an app (line 40 — the *only*
`INSTALLED_APPS` delta vs every previous artifact):

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'blog',
]
```

**Explanation.** Registration is what makes `{% load django_bootstrap5 %}` resolvable —
same mechanism as any app's template tags. Without line 40, line 6 of the parent raises
at parse time; with it, lines 7–8 expand. Then the parent spends the bridge:

```html
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
```

**Explanation.** Line 6 unlocks the library (A016's "signing the register"). Lines 7–8
*spend* it: each tag renders one element. Verified byte-for-byte through the engine:

```html
<link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" rel="stylesheet">
<script crossorigin="anonymous" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
```

Two facts worth memorizing: the URLs point at **jsdelivr.net** (a public CDN — the
browser fetches paint from the internet, not from your `runserver`), and the
`integrity="sha384-…"` hashes match the artifact's commented-out CDN lines *character
for character* — the museum piece and the live bridge agree on Bootstrap 5.3.8.

## 🧠 Core Idea 3 — The Museum: Commented-Out CDN Lines

**Definition.** Lines 5 and 32 of the parent are `{% comment %}…{% endcomment %}`
regions wrapping hand-written Bootstrap CDN `<link>` / `<script>` elements — the
pre-bridge way of dressing a page. They render to **nothing**: the DTL strips the whole
region before the browser ever sees it.

```html
{% comment %} <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous"> {% endcomment %}
```

```html
{% comment %} <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script> {% endcomment %}
```

**Why keep them.** They are the fossil record: *this* is what lines 7–8 replaced. Same CDN
host, same version, same integrity hashes — only attribute order differs (HTML doesn't
care) and authorship (a human typed the fossil; the package prints the live one).

**Why comment, not delete.** `{% comment %}` (A013's "never served" syntax) keeps the
alternative visible without costing the browser a byte — the verified 1,368-byte page

## 🧠 Core Idea 4 — The Warehouse, Stocked on Paper

**Definition.** `STATICFILES_DIRS = [BASE_DIR / 'static']` (settings line 120) tells the
staticfiles app: "besides every app's `static/` folder, also serve files from the
project-level `static/` directory." It is the warehouse stock list — and in this
artifact, the warehouse is real but both shelves are empty.

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**Explanation.** Line 119 is the *address scheme* (`{% static 'x' %}` → `/static/x`);
line 120 is the *stock list* (look for `x` under `myProject10/static/`). Contrast the
`STATIC_URL`-only era (A009–A017, where line 120 didn't exist and only app lanes could
serve): this is the first artifact that *could* serve project-level static. The lookup
order per label: app-`static/` lanes first (in `INSTALLED_APPS` order), then each
`STATICFILES_DIRS` entry. A miss everywhere is a 404, served *by the same dev server*
that returned the page 200.

**The empty shelves, inventoried.** `myProject10/static/css/` and `myProject10/static/js/`
exist as directories and contain **zero files**. That emptiness is load-bearing: it turns
the parent's `js/bootstrap.bundle.min.js` label into a live 404.

## 🧠 Core Idea 5 — The Mislabeled Crate and the Dead Label

**Definition.** A `{% static %}` label resolves a name to a URL (`/static/…`) at render
time; the *file* behind that URL is found (or not) at request time by searching the
lanes above. A label can resolve perfectly and still 404 — resolution and existence are
different stations.

**Exhibit A — the CSS label (parent line 12, inside the `corecss` block).**

```html
{% block corecss %}
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
{% endblock %}
```

**Explanation.** Renders to `<link rel="stylesheet" href="/static/css/styles.css">`.
The search: `blog/static/css/styles.css`? No (`blog/static/` holds only `styles.css`
at its root — note the missing `css/` middle). `myProject10/static/css/styles.css`?
The directory exists; the file does not → **404** on the parent-alone render. The
element is correct; the warehouse has no such crate.

**Exhibit B — the JS label (parent line 33, wrapped in no block).**

```html
<script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
```

**Explanation.** Renders to `<script src="/static/js/bootstrap.bundle.min.js">`
(verified HIT). The search ends the same way: `myProject10/static/js/` is an empty
directory → **404**, and no child block can swap it (see §Core Idea 6). No local
Bootstrap JS exists anywhere in the repo — the only Bootstrap JS that *arrives* comes
from the bridge's CDN script.

**Exhibit C — the crate in the wrong aisle (the 24-byte stylesheet).**

```css
h1 {
    color: red;
}
```

**Explanation.** `blog/static/styles.css` is real CSS — red `h1`s — sitting in the *app*
lane at the path `styles.css`. And the child *labels exactly that path* (line 6:
`{% static 'styles.css' %}`) — which resolves to an existing file. But the child's label
only renders because of the override mechanism below.

contains **zero** bytes of these lines. Shipping them uncommented would *double-load*
Bootstrap (bridge CSS + fossil CSS — same version, wasted download).


## 🧠 Core Idea 6 — The Override That Swaps: `corecss`

**Definition.** `corecss` is an ordinary block — parent ships a default (lines 11–13: the
`css/styles.css` label), the child overrides it (lines 5–7: the `styles.css` label).
Override semantics are total: the winner's text replaces the loser's; nothing merges.

The parent's default slot vs the child's winning graft (note the load the child carries):

```html
{% block corecss %}
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
{% endblock %}
```

```html
{% load static %}
{% block corecss %}
    <link rel="stylesheet" href="{% static 'styles.css' %}">
{% endblock %}
```

```html
{% block title %} Blog page {% endblock %}
```

```html
{% block content %}
    <h1>Blog Page</h1>
{% endblock %}
```

**Explanation.** Three overrides ride in this 252-byte child: `title` (`Blog page` —
note the artifact's own leading/trailing spaces, verified in the `<title>` repr),
`corecss` (the swap), and `content` (`<h1>Blog Page</h1>` — which is why `My Site` is
correctly *absent* from the verified render). The `{% load static %}` on line 4 is
*load-bearing* here, unlike A017's inert load — remove it and the child's `{% static %}`
raises `TemplateSyntaxError` at parse (A016's loads-don't-inherit rule).

**The swap's net effect, stated plainly.** The parent's `css/styles.css` label (which
404s) is *replaced* by the child's `styles.css` label (which resolves to the real
24-byte app file). So the final 1,368-byte page wears: bridge CDN CSS (live paint),
the child's `styles.css` (red `h1`s, live), bridge CDN JS (live behavior), and the
parent's `js/bootstrap.bundle.min.js` label (404 — no block wraps it, no child can
swap it). One 404 fixed by grafting, one 404 permanent.

## 🔄 The Journey — `GET /blog/` Through Three Channels and One Swap

| # | Station | What happens | Evidence |
|---|---|---|---|
| 1 | Project URLs | `blog/` prefix matches → strips to `''`, includes `blog.urls` (A008's mount) | `myProject10/urls.py` line 22 |
| 2 | App URLs | `''` matches the single pattern → `views.blog`, `name='blog'` | `blog/urls.py` line 5 |
| 3 | View | `blog(request)` → `render(request, 'blog.html')`, no context (evidence-bag arrives empty) | `views.py` line 5 |
| 4 | Child lookup | `'blog.html'` → lane 1 (`DIRS`) misses → lane 2 (`APP_DIRS`) hits `blog/templates/blog.html` (un-namespaced ⚠️) | 252 B file |
| 5 | Parent lookup | `{% extends "base.html" %}` → lane 1 hits `templates/base.html` (cross-lane graft) | 1,779 B file |

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| Bootstrap | A ready-made costume rack for pages | CSS + JS component library: class vocabulary (`btn`, `btn-primary`) + behavior scripts, versioned as files | the costume rack |
| `django-bootstrap5` | The bridge between Django and the rack | Third-party app (26.3 here) exposing `{% bootstrap_css %}` / `{% bootstrap_javascript %}` tags that print version-pinned CDN elements | the bridge |
| `{% bootstrap_css %}` / `{% bootstrap_javascript %}` | "Print the Bootstrap link/script for me" | Template tags expanding to `<link>` / `<script>` with jsdelivr URL + `integrity` + `crossorigin` | the printer |
| CDN | Paint delivered by the internet, not your server | Content Delivery Network — the browser fetches Bootstrap files from `cdn.jsdelivr.net` | the mail-order catalog |
| `integrity` hash | A tamper seal on a CDN file | Subresource Integrity: the browser verifies the fetched bytes against `sha384-…` before applying | the wax seal |
| `STATICFILES_DIRS` | The warehouse stock list | Settings list of project-level directories searched for `{% static %}` names, after app lanes | the stock list |
| App-`static/` lane | Each app's own crate shelf | `<app>/static/` directories served by the staticfiles app in `INSTALLED_APPS` order | the shop shelves |
| Label-vs-file | The name resolves; the file may not exist | `{% static %}` resolution (render time) vs file lookup (request time) — a 404 needs only the second to fail | the label vs the crate |
| `corecss` | A swappable stylesheet slot | An ordinary block whose override *replaces* the parent's `<link>` wholesale — no merging | the costume slot |
| Silent asset 404 | Broken paint, healthy page | Asset miss returns 404 while the page returns 200 — styling absent, no Django error | the missing delivery |

> New terms must also be added to `docs/MEMORY.md` §2.

## 💡 Real-World Analogy — The Theater Company's Costume Department

A theater company (your Django project) stages a play (the page). The actors already know
their lines (templates, variables, control flow) and share one stage design (the parent
shell) — but opening night needs costumes, and nobody sews them in-house.

Three suppliers serve the company. **The bridge** (`django_bootstrap5`) is the contracted
costume house: you phone two item numbers and finished costumes arrive by courier (CDN)
with wax seals (integrity hashes) — sewn to the season's pattern (5.3.8). **The museum
drawer** is last season's mail-order catalog (the commented CDN lines): the same house,
the same pattern, the same seals — kept in a drawer so the new stage manager can see what
the contract replaced. **The warehouse** (`static/`) is the company's own storage: shelves
labeled `css/` and `js/`, but the shelves are bare — the requisition slips come back
stamped *not in stock* (404), while one mislabeled crate (`blog/static/styles.css`, filed
under the shop shelf) actually holds the red paint.

And the **costume slot** (`corecss`) is the dresser's standing instruction — "hang
whatever's on this hook" — where the touring actor (the child) swaps the company's dead
requisition for their own live one. The audience (the browser) sees a dressed cast and
never knows a delivery failed backstage: the show returns 200 while the manifest shows a
404. Check the manifest (page source), then the shelves (finders), before blaming the play.

## ❌ Common Beginner Mistakes

1. **`pip install` in the wrong interpreter** — the bridge lives in `myProject10/venv/`,
   not the system Python. `py -c "import django_bootstrap5"` fails globally *by design*;
   only the project's interpreter imports it. Symptom: `ModuleNotFoundError`. Fix: activate
   the venv (journal lines 21–23) or prefix with its `python.exe`.
2. **Forgetting the `INSTALLED_APPS` line** — installed but unregistered, so
   `{% load django_bootstrap5 %}` raises at parse. The artifact's settings line 40 is the
   exhibit: one line, and the bridge resolves.
3. **Reading a 200 page as "static works"** — the artifact's page is 200 with a 404
   asset riding along. Check status codes per asset, not per page.
4. **Labeling a file that lives in the wrong lane** — `css/styles.css` is labeled but the
   bytes sit at `styles.css` (no `css/` middle) in the app lane. The label is a path, not
   a search query: every segment must match. Fix: move the file *or* fix the label.
5. **Editing the parent's `corecss` default and wondering why nothing changes** — the
   child overrides the block, so the parent's default never renders on this route.
   Edit the winner (child lines 5–7), not the loser.
6. **Uncommenting the CDN fossils "to be safe"** — double-loading Bootstrap (bridge +
   fossil, same 5.3.8): wasted bytes and a specificity coin-flip. One channel per asset.

| 6 | Bridge expansion | `{% bootstrap_css %}` → jsdelivr CSS `<link>` (5.3.8, integrity hash); `{% bootstrap_javascript %}` → jsdelivr `<script>` | verified HIT `bootstrap` |

## 🧠 Common Misconceptions

| ✅ Django/Topic IS … | ❌ It is NOT … |
|---|---|
| Bootstrap is files the browser downloads; Django only prints references | A Django feature — Django never styles anything itself |
| `django-bootstrap5` is a printer for `<link>`/`<script>` elements | A theme engine or a replacement for `{% static %}` |
| Bridge version (26.3) and Bootstrap version (5.3.8) are independent numbers | The same thing — upgrading the package moves the pinned CDN build |
| `{% static %}` resolving proves the label is spelled right | Proof the file exists — existence is decided lanes later, per request |
| An empty `static/css/` directory is a configured warehouse with bare shelves | A misconfiguration — `STATICFILES_DIRS` is correct; the shelves just hold nothing |
| A block override merges with the parent default | Total replacement — the child's `corecss` erases the parent's `<link>` |
| Page 200 means assets loaded | Any guarantee at all — assets have independent status codes |

## 🧪 Practical Example — Extend the Artifact (Three Live Exercises)

> All three run from `myProject10/` with its venv interpreter. None edits the artifact —
> copy patterns into scratch files or answer from the verified outputs.

**Exercise 1 — Read the manifest.** From the verified 1,368-byte render, list the four
asset references (2 CDN, 2 local) with their full URLs, then for each local one state
the lane search and its verdict. *Answers:* `…/bootstrap.min.css` (CDN, live) ·
`…/bootstrap.bundle.min.js` (CDN, live) · `/static/styles.css` (child's label →
`blog/static/styles.css` HIT, live) · `/static/js/bootstrap.bundle.min.js` (parent's
label → all lanes miss, 404).

**Exercise 2 — Fix the 404 twice.** (a) Warehouse fix: create
`static/js/bootstrap.bundle.min.js` (any bytes) and re-request — which status flips and
why does the page byte-count not change? (b) Label fix: change the parent's line 33 to
point at an existing file — what breaks the moment a second child overrides nothing?
*Goal:* feel the label-vs-file split and the override asymmetry from both sides.

**Exercise 3 — Prove the swap.** Render `base.html` *alone* (no child — A016/A017's
parent-as-page trick) and diff its `<head>` against the child's 1,368 bytes: the
`css/styles.css` label appears only in the alone-render, `styles.css` only in the
child render, `My Site` only alone, `Blog Page` only grafted. *Goal:* the override is
total — defaults are content, and losers vanish completely.

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q: "How do you add Bootstrap to a Django project — and what are the trade-offs of each
way?"**
A: Three channels, and the artifact shows all three. (1) The `django-bootstrap5` bridge:
`pip install`, register in `INSTALLED_APPS`, `{% load %}` + `{% bootstrap_css %}` /
`{% bootstrap_javascript %}` — pinned versions and integrity hashes managed for you,
but a third-party dependency and CDN-bound by default. (2) Hand-written CDN links (the
artifact's fossils): zero dependencies, same CDN reliance, and you own version bumps +
hashes. (3) Local files via `{% static %}`: works offline, versioned with your repo,
but you vendor + serve the bytes yourself. Never run two channels for one asset.

**Q: "The page returns 200 but looks unstyled. Walk me through the diagnosis."**
A: Page status tells me nothing about assets — I open the page source (the manifest)
and list every `<link>` / `<script>` URL, then check each asset's own status. For local
ones I chain the A016 machinery: does `{% static %}` resolve (render-time), then does
the file exist in any lane — app-`static/` in `INSTALLED_APPS` order, then each
`STATICFILES_DIRS` entry (request-time)? This artifact is my worked example: page 200,
`/static/js/bootstrap.bundle.min.js` 404, because the label is well-formed but every
lane misses — the warehouse shelves are empty.

**Q: "`{% static 'css/styles.css' %}` renders fine but 404s. Is the tag broken?"**
A: No — the tag did its whole job (name → `/static/css/styles.css`). Resolution and
existence are separate stations. Here the bytes live at `blog/static/styles.css` (no
`css/` segment) while the label asks for `css/styles.css` — a path mismatch, not a tag
bug. The fix is one move: file to label, or label to file.

**Q: "What does overriding `corecss` do to the parent's stylesheet — combine or
replace?"**
A: Replace, totally. Blocks are grafts, not merges: on this route the parent's
`css/styles.css` `<link>` never renders — the child's `styles.css` `<link>` stands
alone in the 1,368 bytes. That's why editing the parent's default changes nothing on
the blog route, and why the child's swap silently *fixed* one 404 while the unwrapped
JS label stayed broken.

**Q: "Why does the child say `{% load static %}` when the parent already did?"**
A: Because loads don't inherit (A016's rule, verified by `TemplateSyntaxError` there):
each template file signs its own register. The child's `{% static %}` on line 6 needs
the child's line 4 — delete it and parsing fails before rendering starts.

| 7 | Fossils stripped | Both `{% comment %}` regions → zero bytes in the response | absent from 1,368 B |
| 8 | `corecss` swap | Child's `styles.css` label replaces parent's `css/styles.css` label | verified HIT `styles.css` |
| 9 | `title` + `content` grafts | `<title> Blog page </title>`; `<h1>Blog Page</h1>`; `My Site` gone | `Blog Page` HIT, `My Site` MISS |
| 10 | Response | **200**, 1,368 bytes. The browser then fetches 4 assets: 2 CDN (live) + `/static/styles.css` (live — child's label) + `/static/js/bootstrap.bundle.min.js` (**404** — empty shelf) | 5/5 request-path assertions |

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. Name the three Bootstrap supply channels visible in `base.html`, with line numbers —
   and which ones cost the browser bytes.

<details><summary>Answer</summary>

Live bridge: lines 6–8 (`{% load django_bootstrap5 %}`, `{% bootstrap_css %}`,
`{% bootstrap_javascript %}`) — costs two CDN downloads. Museum: lines 5 and 32
(`{% comment %}`-wrapped CDN link/script) — costs **zero** bytes (stripped at render).
Local labels: lines 12 and 33 (`{% static 'css/styles.css' %}`,
`{% static 'js/bootstrap.bundle.min.js' %}`) — cost whatever the lanes can serve
(one 404 here).

</details>

2. What does `{% bootstrap_css %}` expand to — host, version, and what travels with the URL?

<details><summary>Answer</summary>

A full `<link>` to `https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css`
with matching `integrity="sha384-sRIl4…LB"` and `crossorigin="anonymous"` (verified
byte-for-byte). Bridge 26.3 prints Bootstrap 5.3.8 — the two version numbers are
independent.

</details>

3. The page is 200 but `/static/js/bootstrap.bundle.min.js` is 404 — chain every lane
   that was searched.

<details><summary>Answer</summary>

`{% static %}` resolved the name to the URL (render-time, correct). At request time:
app-`static/` lanes in `INSTALLED_APPS` order (no such path in any app), then
`STATICFILES_DIRS` → `myProject10/static/js/` — directory exists, file absent → 404.
Resolution ≠ existence; the label was well-formed, the shelves were bare.

</details>

4. What did the child's `corecss` override change — and what did it leave broken?

<details><summary>Answer</summary>

Replaced the parent's `css/styles.css` `<link>` (404 — wrong path) with the child's
`styles.css` `<link>` (live — matches `blog/static/styles.css`). Total replacement:
the parent's label never renders on this route. Left broken: the parent's
`js/bootstrap.bundle.min.js` label (line 33, no wrapping block, no override) — still
404.

</details>

5. Why does `GET /` 404 while `GET /blog/` 200 — which single line decides it?

<details><summary>Answer</summary>

`myProject10/urls.py` line 22: `path('blog/', include('blog.urls'))` — the A008 mount.
Only the `blog/` prefix is wired; root has no pattern, so `/` 404s by design (verified).
Same mount as A008/A015–A017.

</details>

6. Where does `django_bootstrap5` live, and what single settings line makes its tags loadable?

<details><summary>Answer</summary>

In the project's venv (`venv/Lib/site-packages/django_bootstrap5/`, version 26.3) —
invisible to the system interpreter. Settings line 40 (`'django_bootstrap5'` in
`INSTALLED_APPS`) registers the app, which exposes its `templatetags/` module to
`{% load django_bootstrap5 %}`. No line 40 → parse-time failure.

</details>

7. Name the artifact's ⚠️-flagged quirks a reviewer should catch.

<details><summary>Answer</summary>

(1) The un-namespaced child `blog/templates/blog.html` (A011 convention departed from,
like A017); (2) the parent CSS label / app file path mismatch (`css/styles.css` vs
`styles.css`); (3) the `title` block's own spacing (` Blog page `) quoted verbatim;
(4) the empty `static/css/` + `static/js/` shelves behind a populated
`STATICFILES_DIRS`; (5) the inert `MAILERS` block — sixth artifact running; (6) the
0-byte `db.sqlite3` — forms/database still pending.

</details>

## 📝 Quick Revision — A018 in Five Minutes

| Concept | One line | Artifact proof |
|---|---|---|
| Bootstrap | Costume rack: classes + JS shipped as files | nine `btn btn-*` buttons, lines 17–26 |
| The bridge | `django_bootstrap5` prints CDN link/script | lines 6–8 → jsdelivr 5.3.8 + `sha384` seals |
| The museum | commented CDN lines cost zero bytes | lines 5, 32 → absent from 1,368 B |
| The warehouse | `STATICFILES_DIRS` lists shelves that are bare | `static/css/`, `static/js/` — 0 files |
| Label vs file | Resolve (render) ≠ exist (request) | `/static/js/…` HIT in HTML, 404 on wire |
| The swap | `corecss` override replaces, never merges | child `styles.css` in, parent `css/styles.css` out |
| The journey | mount → view → child → parent → bridge → 200 | `GET /blog/` 200, 1,368 B, 5/5 assertions |
| By-design 404s | `/` unwired; JS shelf empty | `/` → 404, `/admin/` → 302 |

Verified numbers to memorize: page **1,368 B** · `GET /blog/` → **200** (5/5) ·
`GET /` → **404** · `GET /admin/` → **302** · bridge **26.3** prints Bootstrap
**5.3.8** · title repr `' Blog page '` · nine buttons · one live local CSS
(`styles.css`, 24 B, red `h1`s), one dead local JS.

## 🧠 Final Mental Model — The Costume Department

```mermaid
flowchart TD

## ❓ FAQ

**Q1. I installed `django-bootstrap5` globally — why does the project still fail?**
A: The bridge must live where the project runs. This artifact's project interpreter is
`myProject10/venv/` (Django 6.1.1 + bridge 26.3); the system `py` has neither. Either
activate the venv (journal: `py -m venv venv`, `venv/Scripts/activate`,
`pip install django-bootstrap5`) or run everything through `venv/Scripts/python.exe`.
`ModuleNotFoundError: No module named 'django_bootstrap5'` always means wrong
interpreter, never broken Django.

**Q2. Do I need the internet for this page?**
A: For the Bootstrap paint and behavior, yes — both bridge elements point at
`cdn.jsdelivr.net`. Offline, the buttons fall back to unstyled native controls while
everything Django does (routing, rendering, the local `styles.css`) keeps working.

**Q3. Why do the bridge and the fossil carry the *same* integrity hash?**
A: Because they're the same file release: Bootstrap 5.3.8's `bootstrap.min.css` has one
canonical `sha384` digest, and both authors (the package maintainer, the artifact's
author) pinned it. Matching hashes prove the bridge is a printer, not a re-implementation.

**Q4. Should `STATICFILES_DIRS` point at `static/` when app-`static/` already works?**
A: They serve different owners: app lanes hold reusable per-app assets, `STATICFILES_DIRS`
holds project-wide assets (site CSS, vendor JS). This artifact needs both concepts because
its labels point at both lanes. In production 📌 both are *collected* by `collectstatic` —
dev serving is a convenience, not the deployment story.

**Q5. The child override "fixed" a 404 — is that a legitimate pattern?**
A: Accidentally, not architecturally. The swap worked because the child's label happened
to match a real file. Relying on overrides to repair mislabeled parents is backwards —
fix the label or stock the shelf. Blocks repair *presentation*, not *inventory*.

**Q6. Port 8000 shows a stale/unstyled page again — same trap?**
A: Same trap as A016 Q7 / A017 Q7: a stale `runserver` from an earlier chapter's project
owning port 8000, or a cached tab. Stop the old server, run
`venv/Scripts/python.exe manage.py runserver` (venv interpreter!) from `myProject10/`,
hard-refresh (`Ctrl+F5`). Server-side truth: `GET /blog/` → 200 (1,368 B).

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — The rack:** I can name what `btn` vs `btn-primary` each contribute and count the artifact's nine buttons — *§Core Idea 1*
- [ ] **Checkpoint 2 — The bridge:** I can install, register, load, and spend `django_bootstrap5`, and state both version numbers — *§Core Idea 2*
- [ ] **Checkpoint 3 — The museum:** I can explain why commented CDN lines cost zero bytes and why uncommenting them double-loads — *§Core Idea 3*
- [ ] **Checkpoint 4 — Label vs file:** I can chain the full lane search for any `{% static %}` name and predict 200 vs 404 — *§Core Ideas 4–5*
- [ ] **Checkpoint 5 — The swap:** I can predict a `corecss` diff (parent-alone vs child render) before running it — *§Core Idea 6*
- [ ] **Checkpoint 6 — The journey:** I can trace `GET /blog/` station by station with byte counts and status codes — *§Journey*

## 🏋️ Exercises

- **Level 1 — Recall:** List the three supply channels with parent line numbers; quote
  the bridge versions (package vs Bootstrap); quote the verdicts (`/` 404, `/blog/`
  200, `/admin/` 302).
- **Level 2 — Understanding:** Explain to a peer why installation ≠ delivery, using the
  200-page-with-404-asset as the exhibit — and why the browser, not Django, is the
  party that "notices" a missing stylesheet.
- **Level 3 — Application:** Do the three Practical-Example exercises from §🧪 above:
  read the manifest, fix the JS 404 both ways, and prove the `corecss` swap by rendering
  the parent alone.
- **Level 4 — Interview reasoning:** Your team must ship an offline kiosk (no
  internet) running this page. Which channel survives, what do you vendor, how does
  `collectstatic` 📌 change the story — and what breaks first if you just delete the
  bridge lines?

## 🏁 Final Takeaways

1. **Bootstrap is files; Django prints references.** Nine `btn` buttons are markup
   waiting for paint — the paint travels by `<link>` / `<script>`, each with its own
   status code.
2. **The bridge is a printer with a version of its own.** `django-bootstrap5 26.3`
   emits Bootstrap 5.3.8 CDN elements with integrity seals — install it in the
   *project* interpreter, register one line, spend two tags.
3. **Comments cost nothing; duplicates cost double.** The CDN fossils render to zero
   bytes; un-commenting them double-loads the same release.
4. **Labels resolve, files exist — different stations.** `/static/js/…` rendered
   correctly and 404d honestly: well-formed label, bare shelves.

---

<div class="doc-footer">

**Sources used:**

| Source | Role | Notes |
|---|---|---|
| `A018_Bootstrap_in_Django/myProject10/` — fifteenth real artifact | **Primary** | `templates/base.html` (1,779 B) and `blog/templates/blog.html` (252 B) quoted verbatim; `blog/views.py` (125 B), both `urls.py` (839 B / 112 B), `settings.py` (3,443 B — bridge registration + populated `STATICFILES_DIRS`) read and cross-checked; `blog/static/styles.css` (24 B) and the empty `static/css/` + `static/js/` inventoried |
| Verified render — Django 6.1.1 engine + request pipeline | Verification | Engine render of artifact bytes (1,368 B; 8/8 assertions incl. byte-exact bridge expansion + `styles.css`/`bootstrap.bundle.min.js` label HITs + `My Site` absence) AND live `GET`s via test client (HTTP_HOST `127.0.0.1:8000`): `/blog/` 200 (5/5 assertions), `/` 404, `/admin/` 302 |
| [`commands.txt`](../commands.txt) | Context | New line 27 (`pip install django-bootstrap5`, quoted verbatim) + venv lines 21–23 — environment rebuild; the artifact outranks the journal |
| [A016](../A016_Templates_4_Inheritance_Static_Files/README.md) · [A008](../A008_Multiple_Apps_with_Views_URLs_%28Blog_Shop_Example%29/README.md) · [A011](../A011_App_Level_Templates_Setup_HTML_Integration/README.md) · [A013](../A013_Templates_1_Basics_&_Variables/README.md) | Context | Static chain + loads-don't-inherit; the `blog/` mount; the namespace convention (departed from, ⚠️); comment fates + context-free render |
| Installed `django-bootstrap5 26.3` (`templatetags/django_bootstrap5.py`, dist METADATA) · official Django staticfiles docs | 📌 Supplementary | Tag-expansion mechanics, bridge-vs-Bootstrap version split, lane search order — flagged 📌 in place |

> 📌 **Scope note:** everything derived from the artifact and its verified render is
> source-grounded; bridge internals, `collectstatic`, and offline-vendoring guidance come
> from package/Django docs and carry the 📌 badge. The un-namespaced child
> (`blog/templates/blog.html`), the empty warehouse shelves, the `title` block's own
> spacing (` Blog page `), the inert `MAILERS` block (sixth artifact running), and the
> 0-byte `db.sqlite3` are flagged ⚠️, not endorsed — and the models/forms frontier stays
> honestly pending. No transcript exists for A018 — declared per the documentation
> contract.
>
> **Navigation:** [← A017 · Templates 5: Advanced Tags](../A017_Templates_5_Advanced_Tags/README.md) · [📚 Series Hub](../README.md) · A019 · the next lecture — its folder drops with it →
>
> **Series:** [A001](../A001_Introduction_What_is_Django/README.md) ·
> [A002](../A002_MVT_Architecture_Explained/README.md) ·
> [A003](../A003_Install_Python_pip_Django_Virtual_Environment_Setup/README.md) ·
> [A004](../A004_Create_Django_Project/README.md) ·
> [A005](../A005_Django_Files_Folders/README.md) ·
> [A006](../A006_Django_startapp_Command_Explained/README.md) ·
> [A007](../A007_Views_URLs_Basics/README.md) ·
> [A008](../A008_Multiple_Apps_with_Views_URLs_%28Blog_Shop_Example%29/README.md) ·
> [A009](../A009_URL_Parameters_%28path_re_path_kwargs%29/README.md) ·
> [A010](../A010_Templates_Folder_Setup_Project_Level/README.md) ·
> [A011](../A011_App_Level_Templates_Setup_HTML_Integration/README.md) ·
> [A012](../A012_Manage_HTML_Files/README.md) ·
> [A013](../A013_Templates_1_Basics_&_Variables/README.md) ·
> [A014](../A014_Templates_2_Filters_Text_Numbers_Date/README.md) ·
> [A015](../A015_Templates_3_If_For_With_and_Cycle/README.md) ·
> [A016](../A016_Templates_4_Inheritance_Static_Files/README.md) ·
> [A017](../A017_Templates_5_Advanced_Tags/README.md) · **A018** ·
> [Hub](../README.md)

</div>

5. **Overrides replace, never merge.** The child's `corecss` erased the parent's dead
   label and hung a live one — presentation repaired, inventory untouched.
6. **A 200 page can carry 404s.** Check the manifest, then the shelves, before blaming
   the play.

## 🔄 Next Lecture Connection

The shell is now dressed — variables (A013), filters (A014), control flow (A015),
inheritance + static (A016), specialist tags (A017), and styled components (A018). What
the artifact *still* doesn't have is anything to be dynamic about: no models, no forms,
no persistence — the 0-byte `db.sqlite3` is now six artifacts old, and the painted-on
doors stay shut. That frontier — **models, the ORM, and forms** — is where the series
must go next; when its folder drops, today's pigeonholes become querysets and the
costume department finally dresses real data.

    V["view: context-free render<br>blog()"] --> C["child: touring actor<br>blog.html, lane 2"]
    C -->|extends| P["parent: stage design<br>base.html, lane 1"]
    B["bridge: costume house<br>django_bootstrap5 26.3"] -->|prints| CDN["courier delivery<br>jsdelivr 5.3.8 + seals"]
    CDN --> PAGE["opening night<br>1,368 B · 200"]
    M["museum drawer<br>commented CDN lines"] -.->|zero bytes| PAGE
    C -->|corecss swap| SLOT["costume slot<br>styles.css LIVE"]
    SLOT --> PAGE
    P -->|unwrapped label| SHELF["bare shelf<br>js/*.js → 404"]
    SHELF -.->|missing delivery| PAGE
    W["warehouse stock list<br>STATICFILES_DIRS"] --> SHELF
```

One sentence to carry: **the bridge prints the courier's address, the museum keeps
last season's catalog for free, the child swaps one dead requisition for a live one —
and the show returns 200 while a delivery 404s backstage, because pages and assets
have independent status codes.**


**The one-line journey:** mount → view → child (lane 2) → parent (lane 1) → bridge
prints CDN paint → fossils vanish → child swaps one dead label for a live one → 200.

> page returns **200** while one asset returns **404** — installation succeeded, delivery
> partially failed, page stayed healthy.


> ⚠️ **Discrepancy note (artifact vs convention):** the child is
> `blog/templates/blog.html`, **not** `blog/templates/blog/blog.html` — the A011
> `<app>/` namespacing convention is departed from again (A017 did the same). It works
> because a single-app project has no collision to prevent; it is flagged, not endorsed.
> A second ⚠️ of the same family: the parent's CSS label says `css/styles.css` while the
> only real file sits at app-lane `styles.css` (no `css/` middle) — a path mismatch the
> chapter diagnoses rather than silently fixes.


- [ ] A013 — what `render(request, name)` does and how the third-argument context works
- [ ] A016 — the franchise model: parent shell, child grafts, `{% load static %}` +
  `{% static %}` labels, `STATICFILES_DIRS` as the warehouse stock list
- [ ] A010/A011 — the two template lanes (`DIRS` first, then `APP_DIRS`) and the
  `<app>/` namespacing convention (the artifact *departs* from it — flagged ⚠️)
- [ ] A008 — the `blog/` URL prefix (root `/` 404s by design, again)
- [ ] 📌 A terminal that can run the project's own interpreter
  (`myProject10/venv/Scripts/python.exe`) — the third-party bridge only exists inside it

