# 🚀 A015 — Templates 3: If, For, With and Cycle

`📖 Lecture A015` · `🎓 Track: Core Django` · `📶 Level: Beginner` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** built primarily from a **twelfth real artifact** —
> the `myProject7/` project in this very folder (fresh project, single `blog` app). The
> view (`blog/views.py`, 556 bytes) and the template
> (`blog/templates/blog/blog_list.html`, 1971 bytes) are quoted verbatim below;
> `settings.py`, both `urls.py` files, and `apps.py` were read and cross-checked.
> **Every rendered-output claim was verified twice**: by rendering the artifact's exact
> template with its exact context through Django 6.1.1's engine, and by a live `GET`
> through the request path (Django test client, HTTP_HOST `127.0.0.1:8000`) — `GET
> /blog/` returned **200** and all twelve content assertions passed. The root `/` returns
> **404** — this artifact deliberately mounts its page at the `/blog/` prefix only (a
> return of A008's URL-prefix lesson), flagged honestly in the Journey. The command journal
> [`commands.txt`](../commands.txt) adds no new lines (still A007's line 25 — file-editing
> again). Django's official template-docs control-flow reference supplies the exact
> semantics (marked 📌). No transcript exists.

---

## 🧭 What You Will Learn

- [ ] Branch a page with **`{% if %}` / `{% else %}`** — truthiness on real data, with the dot-lookup chain resolving through a *list of dicts* (`blogs.1.is_feature`)
- [ ] Repeat with **`{% for %}`** — iteration over a collection, the **`forloop.counter`** line number, and the **`{% empty %}`** fallback
- [ ] Alias a long expression to a short local name with **`{% with %}`**
- [ ] Alternate row styles with **`{% cycle %}`** — the pattern that bricks alternating tables
- [ ] Pick the first truthy value with **`{% firstof %}`** — including the empty-string trap
- [ ] Suspend template processing with **`{% verbatim %}`**, and the escaping pass with **`{% autoescape off %}`**
- [ ] Trace `GET /blog/` end to end and predict each of the artifact's 9 block tags' outputs

## 🎯 Why This Lecture Matters

A013 made pages *alive* (the context dict fills `{{ }}` blanks) and A014 made values
*presentable* (the filter pipe reshapes them). But a page built only of `{{ }}` prints is
a **flat list** — it renders every row, every branch, every time, in the same order, with
no decisions. Real pages are *not flat*: they show the admin a delete button and hide it
from guests; they print ten rows or zero rows depending on the data; they highlight the
current menu item and stripe every other table line. The tags that make pages *decide and
repeat* are control flow, and that is exactly this lecture.

The artifact — its page title declares `#3 template` (A013's page was `#1 Template Basic`,
A014's `#2 Template`) — is the first in the series' own projects to carry **real block
tags end to end**: `{% if %}`, `{% for %}` with `{% empty %}`, `{% with %}`, `{% cycle %}`,
`{% firstof %}`, `{% verbatim %}`, and `{% autoescape off %}`. Every previous chapter
hinted at this moment — A014 shipped the series' first `{% if %}` (inside `divisibleby`),
and its next-lecture connection literally promised "the *cure* for raw list reprs is
iteration." A015 pays that promise off: what A014's `first`/`join` merely *read*, this
chapter's `{% for %}` *walks*.

Interview-wise this is the highest-yield template lecture so far: control-flow tags are
the words interviewers hear candidates say in every template question, and the
`forloop.counter` / `{% empty %}` / `{% cycle %}` trio is the "list of dicts → striped
table" recipe that appears in every real Django app.

## ✅ Prerequisites

- [ ] **A014** — the first `{% if %}` (in `divisibleby`), filters as *conditions*, `first`/`last`/`length` reads being "list access without iteration" (the need this chapter satisfies)
- [ ] **A013** — `{{ }}` variables, the context dict, dot lookup (dict → attr → list-index), auto-escaping, `|safe`
- [ ] **A011** — namespaced app templates; the lane-2 hit this chapter's page rides
- [ ] **A008** — URL prefixes (`blog/` mounts the app at a subpath; that is where this artifact's page lives)

### 📌 Recap — where A014 left us

A014's `myProject6/` was a *filter shelf*: one `post` dict, twenty pipes, and — almost
hidden in the middle — the series' **first `{% if %}`** wrapping `divisibleby`. Its recall
bank closed with three explicit predictions for A015: the `{% if %}` tag gets the full
treatment; lists get *iterated* instead of printed as reprs; and control-flow/comparison
logic generally becomes first-class. A015's `myProject7/` is a **fresh project** with a
*new* view (`blog_list`) and a page that is the opposite of A014's shelf: instead of
twenty pipes on one value, it stacks **nine block tags** that steer the *flow* of an
entire three-row list. Same two-lane lookup, same `render()` — the new machinery is the
tagger's fork, loop, and underlining pen.

---
## 🏗️ The Artifact — A Page That Thinks (a Control-Flow Shelf)

Ground truth from `myProject7/` on disk (`__pycache__/` and `db.sqlite3` omitted):

```
A015_Templates_3_If_For_With_and_Cycle/
└── myProject7/
    ├── manage.py · db.sqlite3 (0 bytes)
    ├── myProject7/                 ← the config package
    │   ├── settings.py             ← 3372 B: 'blog' registered; pathlib DIRS; inert MAILERS
    │   └── urls.py                 ← 'admin/' + 'blog/' include('blog.urls')   ← the prefix!
    └── blog/
        ├── apps.py                 ← BlogConfig, name='blog'
        ├── views.py                ← 556 B: blog_list builds a 3-item list + 2 extra keys
        ├── urls.py                 ← 117 B: '' → blog_list (mounted under the 'blog/' prefix)
        └── templates/
            └── blog/
                └── blog_list.html  ← 1971 B: 9 block tags — if/for/with/cycle/firstof/verbatim/autoescape
```

The first structural difference to notice: unlike A013's `myProject5` and A014's
`myProject6` (both mounted at root `'' → include → '' → view`), this project uses
**`path('blog/', include('blog.urls'))`** — A008's URL prefix is back. The page lives at
`/blog/`, not `/`. Also unlike its two predecessors, `settings.py` still declares
`'DIRS': [BASE_DIR / 'templates']` but **no outer `templates/` folder exists** (verified:
`myProject7/templates/` is absent) — so the page is found by **lane 2 only** (the app's
private `blog/templates/blog/`), exactly the setup A011 and A013 described.

Here is the view — `blog/views.py`, verbatim (556 bytes):

```python
from django.shortcuts import render
from datetime import datetime

# Create your views here.
def blog_list(request):
    blogs = [
        {"title":"Django Basic", "is_feature":True, "author":"Adnan"},
        {"title":"Django Advanced", "is_feature":False, "author":""},
        {"title":"Django REST Framework", "is_feature":False, "author":"Deo"},
    ]
    context = {
        "blogs":blogs,
        "today":datetime.now(),
        "html_code": "<b>Welcome to my blog</b>"
    }
    return render(request, 'blog/blog_list.html', context)
```

The URL tables — `myProject7/urls.py` (the `urlpatterns` block plus imports), and
`blog/urls.py` (full):

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls'))
]
```

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='home')
]
```
And the template — `blog/templates/blog/blog_list.html`, verbatim (1971 bytes):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>#3 template</title>
</head>
<body>
    <h1>Blog List</h1>
    <p>{{today}}</p>
    {% comment %} If Else {% endcomment %}
    {% if blogs.1.is_feature %}
    <h2>Featured Blog: {{blogs.1.title}}</h2>
    {% else %}
    <h2>No Featured Blog: {{blogs.1.title}}</h2>
    {% endif %}

    {% comment %} For Loop {% endcomment %}
    <ul>
        {% for blog in blogs %}
        <li>{{forloop.counter}}. {{blog.title}} - {{blog.author}}</li>
        {% empty %}
        <li>No blogs available.</li>
        {% endfor %}
    </ul>

    {% comment %} With {% endcomment %}
    {% with total_blogs=blogs|length %}
    <p>Total blogs: {{total_blogs}}</p>
    {% endwith %}

    {% comment %} Cycle {% endcomment %}
    <hr>
    <h2>Blogs in table</h2>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Index</th>
            <th>Title</th>
            <th>Author</th>
            <th>Featured</th>
        </tr>
        {% for blog in blogs %}
        <tr style="background-color: {% cycle 'lightblue' 'lightgreen' %};">
            <td>{{forloop.counter}}</td>
            <td>{{blog.title}}</td>
            <td>{{blog.author}}</td>
            <td>{{blog.is_feature}}</td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="2">No blogs available.</td>
        </tr>
        {% endfor %}
    </table>

    {% comment %} FirstOf {% endcomment %}
    <p>Author:{% firstof blogs.1.author "ABC" %}</p>

    {% comment %} verbatim {% endcomment %}
    {% verbatim  %}
    <p>Author: {{blogs.1.author}}</p>
    {% endverbatim  %}

    {% comment %} autoescape {% endcomment %}
    <h2>Autoescape Example</h2>
    <p>Default(Safe Escaped): {{html_code}}</p>
    <p>Auto escape off: {{html_code|safe}}</p>
    {% autoescape off %}
    <p>autoescape off: {{html_code}}</p>
    {% endautoescape %}
</body>
</html>
```
Five observations set the lecture's agenda:

1. **Nine block tags in 70 lines.** Every one of them — `if`/`else`, `for`/`empty`,
   `with`, `cycle`, `firstof`, `verbatim`, `autoescape off` — is framed by the owner's own
   `{% comment %}` banner: *If Else*, *For Loop*, *With*, *Cycle*, *FirstOf*, *verbatim*,
   *autoescape*. The page is literally a labeled shelf of control flow, matching A014's
   comment-bannered filter shelf.
2. **`blogs.1.is_feature` — the dot chain grows teeth.** A013's dot lookup
   (dict-key → attribute → list-index) is applied here to a **list of dicts**: `blogs.1`
   is list-index, `.is_feature` is dict-key. It resolves to `False` (the second blog is not
   featured), so the `{% if %}` takes its **else** branch. Both branches are real and
   reachable — a decision the page actually makes.
3. **The `{{ }}` and filter vocabulary all comes along.** `blogs|length` (A014's filter)
   feeds `{% with %}`, `forloop.counter` prints line numbers, `{{blog.is_feature}}` prints
   `True`/`False` literally, and `{{html_code}}` gets the full A013 escaping treatment
   (escaped by default, raw through `|safe`, raw inside `autoescape off`).
4. **`{% cycle %}` and `{% firstof %}` are pure template inventions** — there is no
   equivalent concept "in the view." The tagger alternates colors and picks the first
   truthy value entirely at render time; the view only supplied the data.
5. **`{% verbatim %}` proves the tokenizer is real.** Inside it, `{{blogs.1.author}}`
   prints as literal text — the DTL's own parser refuses to parse it, the clearest
   possible demonstration that `{{ }}`, `{% %}`, and `{# #}` are *syntax*, not just
   decorations.

> 🧠 **One sentence for the artifact:** *a three-row list of dicts, walked by a `for`,
> branched by an `if`, numbered by `forloop.counter`, striped by `cycle`, aliased by
> `with`, and shielded by `verbatim`/`autoescape` — nine tags, one view, zero Python.*

---
## 🧠 Core Idea — Control Flow: The Tags That Decide and Repeat

A013's variables *filled* blanks; A014's filters *reshaped* values; A015's tags **steer
the page** — what prints at all, how many times it prints, in what order, in which color,
and whether the parser even looks inside. Every tag in this chapter shares one grammar
family with what you already know:

```html
{% tag … %}                    ← opens a block
{% endtag %}                   ← closes it  (NO other tags may straddle this pair)
```

The scanner (Django's tokenizer) reads these straight-line; the *renderer* obeys them with
if/else forks and for loops. Two levels, one tool chain — which is why the DTL's three
syntaxes (A002) were *syntax*, and this chapter's nine tags are *logic*.

### 1. `{% if %}` / `{% else %}` — truthiness branches

**Definition:** `{% if condition %}…{% else %}…{% endif %}` renders the first block when
the condition is truthy, the second otherwise. The condition is evaluated with the same
truthiness rules Python uses on the template context (📌): `None`, `False`, `0`,
empty strings/collections/empties are falsy; everything else truthy.

**Analogy:** the tagger's **fork** — the train-switch operator. Each request flips the
switch once, and the page's content takes one track or the other. The rails (both
branches) stay in the file; only the *traffic* chooses.

**Why it exists:** a page is not one document — it is a *decision table* rendered as text.
An admin vs a visitor, a full cart vs an empty one, a featured post vs the rest: the view
should hand over the facts, and the template decides what the *reader* should see.

**How it works — this artifact's exact condition:**

```
{% if blogs.1.is_feature %}        ← one dotted resolver, three dots
        │  │  │
        │  │  └─ dict key is_feature (True for blog #1, False for blog #2)
        │  └──── list index 1       ← blogs[1]
        └─────── context key blogs → the list of 3 dicts
```

`blogs.1.is_feature` walks A013's dot order all at once: `blogs` (dict key) → `1`
(list index) → `is_feature` (dict key). Dots compose — **that is the point of A013's
"one rule" framing.** For `blogs = [Basic(True), Advanced(False), REST(False)]`, the
condition is `False`, so the **else** branch prints:

```
No Featured Blog: Django Advanced
```

**Verified:** the render shows exactly that line — and `forloop.counter` in the table
below confirms `blogs[1]` is the *Advanced* row. One condition, one dot chain, two
possible outputs; the page picked the else track.

> ⚠️ **Educational wart (honest note):** the template *tests* index 1 — the one blog
> where `is_feature` is `False` — so the visible output is the "No Featured" branch. The
> *Featured Blog* branch is equally reachable (change the condition to `blogs.0.is_feature`
> and the h2 flips to `Featured Blog: Django Basic`); the owner simply pinned the
> else-track. Both branches exist and both are valid — the test data deliberately shows
> the page *doing its job* on the negative case. (Flip it yourself in Exercise 1.)

**Common confusion:** `{% if %}` does **not** take `==`/`!=` with values unless they are
literals or filters — `{% if blog.is_feature == True %}` works, but the whole point of
truthiness is `{% if blog.is_feature %}` alone. Falsy-but-not-`False` values (`""`, `0`,
`[]`) also take the else track — A014's `yesno` exists precisely because it can tell
`None` from `False`, which a plain `if` cannot (📌).
### 2. `{% for %}` — iteration, `forloop.counter`, and `{% empty %}`

**Definition:** `{% for item in collection %}…{% endfor %}` renders its body once per
element. Inside the loop, the variable name (`blog`) is bound to the current element, and
a special bag named `forloop` exposes per-iteration facts — this artifact uses
`forloop.counter` (1-based line number). If the collection is empty, `{% empty %}`'s body
renders instead (📌 — the whole point of `empty` is you never write a manual
`{% if collection %}` guard in front of a loop).

**Analogy:** the **conveyor belt** — the loop picks each box off the belt, and the body
line is the worker stamping it; `forloop` is the worker's counter clicker. `empty` is the
belt's end-of-line sign: nothing arrived, so print the *empty* notice instead of nothing.

**Why it exists:** A014's `first`/`last`/`join` could only *read* a list; a page must
*repeat* over it — every row of a table, every post in a feed, every item in a cart.
`{% for %}` is the only DTL construct that can turn one collection into N visible rows.

**How it works — the artifact's list:** with
`blogs = [Basic, Advanced, REST]`, this:

```html
{% for blog in blogs %}
<li>{{forloop.counter}}. {{blog.title}} - {{blog.author}}</li>
{% empty %}
<li>No blogs available.</li>
{% endfor %}
```

renders three list items (verified):

```html
<li>1. Django Basic - Adnan</li>
<li>2. Django Advanced - </li>        <!-- author is "" → blank after the dash -->
<li>3. Django REST Framework - Deo</li>
```

Three facts worth the price of admission:

- `blog` is just a **local alias** for the current element — inside the loop `{{blog.title}}`
  is `{{blogs[0].title}}`, `{{blogs[1].title}}`, … (A013's dot issues nothing new; the loop
  *hands you* the element instead of you indexing it).
- `forloop.counter` counts **1, 2, 3** — `forloop` (a dict-like object) lives only inside
  the loop; other counters (`counter0`, `first`, `last`, `revcounter` — 📌 beyond the
  artifact) exist but are unused here.
- Row 2's author prints **blank**, not `None`: `""` is a present-but-empty string, and
  `{{ }}` of a falsy-but-set value is empty output. (`None` would *also* print empty —
  A013's silent-empty rule — but here the key simply holds `""`.)

> 🧠 **The loop is not the list.** `{% for blog in blogs %}` reruns its whole body per
> element; the context outside is untouched; `blog` vanishes when the loop ends.
### 3. `{% with %}` — alias a long expression

**Definition:** `{% with name=value %}…{% endwith %}` binds `name` to `value` for the
block's duration, so the body writes `{{ name }}` instead of repeating the whole
expression. The artifact uses a filter in the binding:

```html
{% with total_blogs=blogs|length %}
<p>Total blogs: {{total_blogs}}</p>
{% endwith %}
```

**Verified output:** `Total blogs: 3`.

**Analogy:** a **sticky note** — you compute `blogs|length` once, write the answer on a
label, and stick it where the paragraph needs it, instead of re-deriving the length every
time you mention it.

**Why it exists:** DRY inside a template. When one expression (`blogs|length`, or worse a
long `post.author.profile.display_name`) appears three times, `{% with %}` lets the
template name it once. It also *freezes* the value at the moment of binding — a boon when
the underlying data could change mid-page (📌 `with` stores a reference at bind time).

**Common confusion:** `{% with %}` is **not** a variable declaration you can mutate later —
there is no re-assignment inside a block; and it does **not** leak outside its block.
`total_blogs` exists only between `{% with %}` and `{% endwith %}`. (Django also allows
the comma form `{% with a=1, b=2 %}` — 📌 beyond this artifact.)

### 4. `{% cycle %}` — alternating values

**Definition:** `{% cycle 'a' 'b' %}` yields its arguments **in turn** on each call,
looping back to the first after the last. It is the template's built-in striping tool —
every other table row gets a different background without any counting in the view. The
artifact wires it into each row's inline style:

```html
{% for blog in blogs %}
<tr style="background-color: {% cycle 'lightblue' 'lightgreen' %};">
```

**Verified output** across the three rows (cycle advances once per call, once per
iteration):

| Row | `forloop.counter` | `{% cycle %}` yields |
|---|---|---|
| 1 (Django Basic) | 1 | `lightblue` |
| 2 (Django Advanced) | 2 | `lightgreen` |
| 3 (Django REST Framework) | 3 | `lightblue` |

So the rendered rows alternate `lightblue → lightgreen → lightblue` — verified in the
request body. The cycle **resets for each new `{% for %}` block** (each cycle tag keeps
its own independent counter), which is exactly why a second loop below would stripe
independently.

**Analogy:** a **revolving door / color wheel** — each push hands you the next color, and
after the last it wraps to the first.

**Why it exists:** zebra-striped tables are the single most common visual pattern on
admin screens, and doing it "by hand" in the view would mean pre-computing a class or
index per row — which is *presentation logic leaking into data*. `{% cycle %}` keeps the
stripe purely a render-time choice (📌 `cycle` also accepts named cycles and
`{% cycle … as name %}` for reuse — beyond this artifact).

> 🧠 **Cycle is per-tag state.** Two `{% cycle %}` tags in the same page are two
> independent wheels; a cycle inside a `for` re-wheels on every loop block.
### 5. `{% firstof %}` — the first truthy value

**Definition:** `{% firstof v1 v2 v3 %}` prints the **first argument that is truthy**,
skipping falsy ones (`None`, `""`, `0`, `[]`…), and prints nothing if all are falsy. The
artifact demonstrates the empty-string trap perfectly:

```html
<p>Author:{% firstof blogs.1.author "ABC" %}</p>
```

`blogs.1.author` is `""` — a falsy *empty string*. Truthy-check fails, so `firstof` moves
on to the literal `"ABC"`. **Verified output:** `Author:ABC`.

**Analogy:** a **flashlight test** — you walk down the line of boxes and pick the first
one that's actually holding something; empty boxes are skipped, and if all are empty you
print nothing.

**Why it exists:** "show this, else that, else that" is a staggeringly common display
idiom (an author name, then "Anonymous", then "—"; a photo, then a silhouette). Writing
it with `{% if %}` chains works but is verbose; `firstof` collapses the whole decision
into one line. Under the hood it is exactly the same truthiness rule `{% if %}` uses —
which is why the series' `yesno` (A014) remains the only tool that can distinguish
`None` from `False`: `firstof` treats both as falsy. (📌 `{% firstof %}` also accepts a
`{% else %}` — not used here.)

> ⚠️ **Tight-writing wart (verbatim):** the artifact writes `Author:{% firstof … %}` with
> no space, so the output is `Author:ABC`. Add a space and it reads `Author: ABC` — pure
> presentation, flagged only so you read the rendered byte-for-byte output correctly.

### 6. `{% verbatim %}` — stop the tokenizer

**Definition:** `{% verbatim %}…{% endverbatim %}` tells Django's *tokenizer* to treat
everything inside as **plain text** — no `{{ }}`, no `{% %}`, no `{# #}` — and copy it
through untouched. (Django ≥5 ships `{% verbatim %}` with `{% verbatim myname %}` named
blocks so an *inner* `{% endverbatim %}` can appear — 📌 beyond this artifact.)

```html
{% verbatim  %}
<p>Author: {{blogs.1.author}}</p>
{% endverbatim  %}
```

**Verified output** — byte-for-byte, the body literally contains
`<p>Author: {{blogs.1.author}}</p>`; the engine never resolved it.

**Analogy:** a **do-not-touch sheet** — you are literally telling the parser "this text
is in a foreign language; don't translate, don't even *try*."

**Why it exists:** the DTL is a *text* language, and sometimes the text itself contains
strings that look like template syntax — documentation pages showing `{{ }}` examples,
templates that must emit client-side template code (Angular `{{ }}`, Vue `{{ }}`),
JavaScript snippets with braces. Without `verbatim`, the scanner would chase `{{` into
misery. It is the escape hatch that makes DTL safe to teach, document, and embed.

> 🧠 **The names in this artifact are do-curious:** `{% verbatim  %}` has a trailing
> double space inside the tag (valid; the tokenizer ignores whitespace) — details, not
> bugs.

### 7. `{% autoescape off %}` — the escaping off-switch

**Definition:** `{% autoescape off %}…{% endautoescape %}` disables auto-escaping for
the block, so `{{html_code}}` emits raw HTML instead of escaped text. Default inside the
block is **off**. This is the *block-level* cousin of A013's `|safe` filter — the filter
exempts one value; the tag exempts a whole region (📌 use is exactly as safe, and exactly
as dangerous).

The artifact shows all **three escaping states side by side** on the same value:

| Template line | What autoescape gives | Verified output |
|---|---|---|
| `{{html_code}}` | **On** (default) — entities | `&lt;b&gt;Welcome to my blog&lt;/b&gt;` |
| `{{html_code\|safe}}` | `safe` marks the value trusted, raw | `<b>Welcome to my blog</b>` |
| `{% autoescape off %}{{html_code}}{% endautoescape %}` | block off — raw | `<b>Welcome to my blog</b>` |

**Analogy:** a **quarantine hatch** — the ink-stain-proof glove (A013) stays on by
default; `|safe` cracks the glove for one stamp, `autoescape off` opens the hatch for the
whole workbench.

**Why it exists:** some legitimate blocks are *meant* to hold rich HTML — a CMS body that
stores `<p><b>…</b></p>` (the real reason the artifact's `html_code` carries markup), or a
markdown render's output. Autoescape off is the legitimate version of that; apps that
instead use it on **user-submitted** data reintroduce XSS on a silver platter (📌 — the
A013 warning stands, loudest here).
### One-sentence mechanism recap

> 🧠 **The whole mechanism in one breath:** *block tags open with `{% … %}` and close with
> `{% end… %}`; the tokenizer reads them as syntax, the renderer obeys them as logic —
> `if` forks on truthiness, `for` walks collections (with `forloop` counting and `empty`
> as the empty-case), `with` labels expressions, `cycle` alternates stored strings,
> `firstof` picks the first truthy, `verbatim` parks text outside parsing, and
> `autoescape off` lowers the escaping hatch for a region.*

---

## 🔄 The Journey — `GET /blog/` Through a Thinking Page

| Step | Actor | What happens |
|---|---|---|
| 1 | Browser → server | `GET /blog/` at `127.0.0.1:8000` |
| 2 | Middleware | default stack passes the request (`127.0.0.1:8000` clears `ALLOWED_HOSTS`) |
| 3 | `ROOT_URLCONF` | `myProject7.urls` consulted |
| 4 | `urlpatterns` | `path('blog/', include('blog.urls'))` — prefix `blog/` consumed, hop into `blog/urls.py` |
| 5 | App URLconf | the remainder is `''`, so `path('', views.blog_list, name='home')` matches |
| 6 | View call | `blog_list(request)` builds the `blogs` list + `context` dict |
| 7 | `render()` | lane-2 hit only: `blog/templates/blog/blog_list.html` (no outer `templates/` dir exists) |
| 8 | Tokenize | the scanner reads 9 block tags + `{{ }}` prints; inside `verbatim` it copies text as-is |
| 9 | Render control flow | `if` evaluates `blogs.1.is_feature` → **False** → else-track; `for` walks the list (3× body, `counter` 1·2·3); `cycle` yields lightblue·lightgreen·lightblue; `with` binds `total_blogs=3`; `firstof` skips `""` → `"ABC"` |
| 10 | Escape + print | `{{html_code}}` escaped (`&lt;b&gt;…`), `|safe` and `autoescape off` output raw; everything written into the response |
| 11 | Response | `200 OK` — the thinking page to the browser |

> ⚠️ **Honesty note — the root 404.** `GET /` on this project returns **404**: the URL
> table maps `admin/` and `blog/` but **no root `''` route**. That is a deliberate
> *structural* difference from A013/A014 (both served the root). It is not an error —
> A008 taught that `blog/` is an honest, common way to mount an app — but if you open
> `http://127.0.0.1:8000/` expecting the page, you will see Django's "The empty path
> didn't match any of these." Navigate to `/blog/`. (The earlier `/` 404 reports in this
> series were fixed by *adding* the `''` route; here the *absence* of one is the
> structure.) Verified: `GET /` → 404, `GET /blog/` → 200, `GET /admin/` → 302 (login).

---

## 🧱 Important Vocabulary

*(New terms are registered in [`docs/MEMORY.md`](../docs/MEMORY.md) — the series-wide
glossary; A013's `{{ }}`/context/escaping terms and A014's filter terms live there too.)*

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **Block tag** | a tag that wraps a region between open and close | `{% tag %}` … `{% endtag %}` — children tags cannot straddle the pair | a box with a lid |
| **`{% if %}` / `{% else %}`** | print one branch or the other | `{% if cond %}A{% else %}B{% endif %}` — truthiness decides; no assignment | the fork |
| **Truthiness** | whether a value counts as "yes" in a condition | `False`·`None`·`0`·`""`·`[]`·`{}` are falsy; everything else truthy (📌) | the switch's "no" list |
| **`{% for %}`** | repeat the body once per element | `{% for x in list %}`…`{% endfor %}`; `x` is bound per iteration | the conveyor belt |
| **`forloop`** | per-loop metadata | a dict-like bag: `forloop.counter` (1-based), `counter0`, `first`, `last` (📌) | the worker's counter clicker |
| **`{% empty %}`** | the empty-collection branch of a loop | `{% for … %}…{% empty %}…{% endfor %}` — renders instead of the body (📌) | the end-of-line sign |
| **`{% with %}`** | alias an expression for a block | `{% with n=v %}…{% endwith %}` — `n` bound to `v` only inside; DRY for repeat reads | the sticky note |
| **`{% cycle %}`** | yield arguments in turn, wrapping | `{% cycle 'a' 'b' %}` → a, b, a, b…; per-tag state, resets per loop (📌) | the revolving door / color wheel |
| **`{% firstof %}`** | print the first truthy argument | `{% firstof a b c %}` — skips falsy, prints first truthy, else nothing | the flashlight test |
| **`{% verbatim %}`** | copy text through untouched | `{% verbatim %}…{% endverbatim %}` — tokenizer disabled inside (📌) | the do-not-touch sheet |
| **`{% autoescape off %}`** | disable escaping for a region | `{% autoescape off %}…{% endautoescape %}` — block-scoped `safe` | the quarantine hatch |

> New terms must also be added to `docs/MEMORY.md` §2 — done in this chapter's ledger pass.
## 💡 Real-World Analogy — The Sorting Office's Tracks

A013's clerk and A014's stamp rack now sit inside a bigger machine: a **sorting office**.
Every piece of mail (each resolved value) travels the office's *tracks*, and this
chapter's tags are the **switches and conveyor belts** the clerk shunts mail across.

- **`{% if %}`** is a **rail switch**: it sees one condition on the label, flips, and the
  mail takes the left track or the right track. The tracks are *already laid* (both
  branches are in the file); the switch just decides which one this parcel rides.
- **`{% for %}`** is a **conveyor belt**: one box at a time, `blog` (the worker's
  clipboard holding the current item) is handed over, the body line stamps it, and the
  next box comes; `forloop` is the counter clicker on the belt. `{% empty %}` is the sign
  at the end that reads *"nothing arrived — print the empty slip."*
- **`{% with %}`** is a **sticky label**: the clerk writes `total_blogs = 3` once and
  slaps it on the clinic's board; anyone glancing at the board reads the count without
  re-counting.
- **`{% cycle %}`** is a **revolving color wheel** at the sorting table: push it once,
  get blue; again, green; again, blue — so every other package gets a different mark,
  with zero counting by the clerk.
- **`{% firstof %}`** is a **flashlight sweep**: shine down the row, grab the first box
  that is actually *holding* something, ignore the empties.
- **`{% verbatim %}`** is the **"do not open — foreign shipment"** crate: the office staff
  don't even try to parse what's inside; it's shipped straight through.
- **`{% autoescape off %}`** is the **quarantine hatch** on the ink-stain-proof glove
  (A013): default on, everything sealed; the hatch opens only for trusted, pre-marked
  cargo (rich HTML the app itself produced).

The office has *one* routing brain and *many* tagged tracks — which is exactly why the
view stays skinny (data in, one `render()`) while the template grows the decision logic
(presentation in, nine tags).

---

## ❌ Common Beginner Mistakes

1. ❌ **Opening a block tag without closing it** — `{% if %}` with no `{% endif %}` (or a
   `{% endif %}` left over from a deleted `if`). *Why:* the tokenizer pairs them by name.
   *Fix:* write open+close in one keystroke habit — `{% if %}` … `{% endif %}` — then fill
   the body.
2. ❌ **Straddling blocks** — `{% if %}` … `{% for %}` … `{% endif %}` — closing the outer
   before the inner. *Why:* block tags nest like parens, and Django reports
   `Unclosed tag` at render. *Fix:* close in exact reverse open order; indent the inner
   block.
3. ❌ **Writing `{% if blog == "x" %}` when truthiness suffices** — or worse, `{% if
   blog.is_feature == True %}` when the value is already a boolean. *Why:* both work, but
   the extra comparison hides the *real* rule — the template already collapses to
   truthiness. *Fix:* write the variable alone; reserve `==` for actual equality against
   literals.
4. ❌ **Forgetting `{% empty %}` and hand-guarding with `{% if list|length > 0 %}`** —
   *Why:* redundant and fragile (and `|length > 0` is wrong anyway — filters don't compare
   that way). *Fix:* put the empty-case *inside* the loop with `{% empty %}` — it exists
   for this.
5. ❌ **Indexing the list instead of looping** — `{% for i in "012" %}` … `blogs.{{i}}` —
   *Why:* `.` can't take `{{ }}` dynamically and that's the whole A013 "one rule" trap.
   *Fix:* loop over the objects, not the indices: `{% for blog in blogs %}` then
   `{{blog.title}}`.
6. ❌ **Expecting `firstof` to rescue falsy-but-set values** — `{% firstof author "X" %}`
   with `author = ""` prints `X` (as the artifact itself shows). *Why:* empty string is
   falsy. *Fix:* know that "empty" ≠ "absent"; for *present but blank*, check the value
   directly with `{% if author %}`…`{% else %}`…`{% endif %}` (or A014's `yesno` when the
   third state matters).
7. ❌ **`autoescape off` on user-submitted text** — *Why:* it is the XSS door A013 warned
   about, thrown wide for a *whole region*. *Fix:* keep `autoescape off` for trusted
   content only; prefer `|safe` (one value) over the tag (a region) — and never trust a
   form field to be safe.
8. ❌ **An orphan `{% empty %}` outside a loop, or a mismatched close** — a stray
   `{% empty %}` is a template error, not a warning; an unmatched `{% endfor %}` raises
   `Unclosed tag`. *Why:* block tags pair by keyword, exactly like parens. *Fix:* count
   opens and closes; indent every nested block.

> 🧠 **One sentence for the section:** *blocks nest by keyword, truthiness follows Python,
> loops carry their own metadata, and the escape hatches (`verbatim`, `autoescape off`)
> must stay shut around anything you don't fully trust.*
---

## 🧠 Common Misconceptions

| ✅ Correct model | ❌ Misconception |
|---|---|
| `{% if %}` evaluates **truthiness** (falsy = `False`/`None`/`0`/`""`/`[]`) | `{% if %}` only works on booleans, or on `==` comparisons |
| `{% for %}` is the **only** way to show N rows from a list | filters like `first`/`join` can replace loops (they *read*, they can't *repeat*) |
| `forloop.counter` is per-loop, available only inside | `forloop` persists after the loop or is global |
| `{% empty %}` renders only when the collection is **empty** | `{% empty %}` runs when the condition is "falsy" somehow (it keys on the list itself) |
| `{% with %}` binds for the block only | `{% with %}` declares a reusable global/updateable variable |
| `{% cycle %}` alternates **per tag call**, resetting per loop block | `{% cycle %}` is page-global and continues across tables |
| `{% firstof %}` picks the first **truthy**, skipping `""` | `{% firstof %}` picks the first *set* variable even if empty |
| `{% verbatim %}` disables the **tokenizer** — nothing inside is parsed | `{% verbatim %}` still resolves `{{ }}` (it does not — that's its point) |
| `{% autoescape off %}` mirrors `\|safe` **at region scope** | `autoescape off` is a filter you can pipe, or safer than `safe` |
| Control flow is **presentation logic that belongs in templates** | all logic should be forced into the view |

> 🧠 **One sentence for the whole mechanism:** *tags steer flow — `if` forks on
> truthiness, `for` repeats over collections, `with` labels, `cycle` stripes, `firstof`
> picks, `verbatim` parks, `autoescape` seals — and the view stays a data provider.*

---

## 🧪 Practical Example — Add Control Flow to the Artifact (Three Live Exercises)

> [!NOTE]
> Everything here is directly runnable in `myProject7/` — each exercise changes the
> template only (Exercise 3 changes the view), then re-serves `/blog/`.

**Exercise 1 — flip the fork.** Change the condition to `{% if blogs.0.is_feature %}` in
`blog_list.html`. Reload `/blog/`: the h2 now reads `Featured Blog: Django Basic` (the
first dict's `is_feature` is `True`). That is the whole fork at work — one token changed,
the else-track becomes the untaken track.

**Exercise 2 — make a row of the table disappear.** Wrap the table's `<tr>` row in
`{% if blog.author %}` … `{% endif %}`. Row 2 (`author = ""`) vanishes — the falsy
`""` hides the whole row. Then use A014's `default` filter to print `Unknown` instead of
the empty author: `{{ blog.author|default:"Unknown" }}` — the single-value cousin of
`firstof`.
**Exercise 3 — trigger `{% empty %}`.** Change the view to `blogs = []` (or delete the
three dicts). Reload `/blog/`: both loop bodies print their empty-branch messages —
`<li>No blogs available.</li>` and `<tr><td colspan="2">No blogs available.</td></tr>`.
The `<ul>` and the `<table>` prove that `{% empty %}` governs each loop independently.

```bash
py .\manage.py runserver        # from myProject7/
# http://127.0.0.1:8000/blog/  →  200 OK, Blog List (the root / stays 404)
```

**Explanation:** each exercise isolates one control-flow concept — the fork's two tracks
(Ex 1), truthiness's reach into row *visibility* plus A014's `default` (Ex 2), and
`{% empty %}` as the loop's own empty-case branch (Ex 3). None of it touched
`settings.py` or the URL table — pure template (plus, in Ex 3, three lines of the view's
list).

---

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. What are block tags, and how do they differ from variables?**
> **Strong answer:** "`{{ variable }}` prints a value; `{% tag %}` executes logic.
> Block tags wrap a region and pair with `{% endtag %}` — `{% if %}`, `{% for %}`,
> `{% with %}`, `{% cycle %}`. The tokenizer reads them as syntax; the renderer obeys
> them as flow control. They don't print their own value; they decide what prints
> inside them."
>
> **Why it works:** starts from the grammar (two syntaxes, one tool chain), not from
> memorized examples — the frame every deeper answer hangs on.

**Q2. Walk me through `{% if blogs.1.is_feature %}`.**
> **Strong answer:** "It's one dotted resolver: `blogs` (context key, the list), then `1`
> (list index), then `is_feature` (dict key) — A013's dot order in a three-step chain.
> On this artifact's data it resolves to `False` (the second blog isn't featured), so the
> `{% else %}` branch renders — 'No Featured Blog: Django Advanced'."
>
> **Why it works:** proves the student can *compose* the dot rule into real nested data
> and read the actual rendered output — not just recite the rule.

**Q3. How would you stripe a table's rows without `{% cycle %}`?**
> **Strong answer:** "You'd have to pre-compute a class or color per row in the view, or
> index the collection — both leak presentation into data. `{% cycle 'lightblue'
> 'lightgreen' %}` keeps the alternation at render time, and it resets per loop block, so
> two tables stripe independently."
>
> **Why it works:** contrasts the alternative (view-side logic) and the reset behavior —
> the two things that separate understanding from usage.

**Q4. `{% empty %}` vs `{% if list %}` — when do you use which?**
> **Strong answer:** "`{% empty %}` is the loop's built-in no-items branch; I'd put it
> inside every `{% for %}` whose body would look silly empty. A separate
> `{% if list %}` around the loop is redundant — the loop *is* the emptiness test."
>
> **Why it works:** names the duplication and the DTL-native replacement — the answer
> senior engineers actually follow.

**Q5. When would you reach for `{% verbatim %}` — and what does it *prove*?**
> **Strong answer:** "Any time the page must emit text that looks like template syntax —
> docs showing `{{ }}`, Angular/Vue braces, JS with braces. It proves the tokenizer is a
> real parser: inside `verbatim`, `{{blogs.1.author}}` came out literally in this very
> artifact."
>
> **Why it works:** pairs purpose with mechanism — and cites the artifact's verified
> literal output as evidence.

---
## 🔁 Active Recall

Retrieval builds memory — answer *in your head first*, then expand each answer.

1. How many block tags does the artifact use, and what are they (by category)?

<details><summary>Answer</summary>

Nine, in the owner's own `{% comment %}` banners: `if`/`else` (branching), `for` with
`empty` (iteration, ×2 — the list and the table), `with` (aliasing), `cycle`
(striping), `firstof` (fallback), `verbatim` (literal text), `autoescape off`
(escaping hatch).</details>

2. The page tests `blogs.1.is_feature`. It resolves to `False`. What exact line does the
browser receive, and which blog does it name?

<details><summary>Answer</summary>

`No Featured Blog: Django Advanced` — the else-branch fired, and `blogs[1]` is the
*Advanced* dict (its `is_feature` key is `False`). The fork took the negative track on
purpose: the data was chosen to exercise the else branch.</details>

3. Why does `{% firstof blogs.1.author "ABC" %}` print `ABC`, not the author?

<details><summary>Answer</summary>

`blogs.1.author` is the empty string `""`, and `""` is *falsy* — the same truthiness
`{% if %}` uses. `firstof` skips it and prints the next truthy argument, the literal
`"ABC"`. Output: `Author:ABC` (no space — verbatim tight-writing).</details>

4. What does `{{html_code}}` produce vs `{{html_code|safe}}` vs the `autoescape off`
block — and why all three on one value?

<details><summary>Answer</summary>

`&lt;b&gt;Welcome to my blog&lt;/b&gt;` (auto-escaped), `<b>Welcome to my blog</b>`
(`|safe` marks it trusted), and the same raw HTML again (block off). Escaping is the
default; `safe`/`autoescape` are the two opt-outs — the artifact demos all three states
of the same string.</details>

5. `forloop.counter` printed 1, 2, 3. What else lives in `forloop`, and where does it
cease to exist?

<details><summary>Answer</summary>

`forloop` is a per-loop bag: `counter0` (0-based), `first`, `last`, `revcounter`,
`parentloop` for nested loops (📌 all beyond the artifact's usage of `counter`). It exists
only inside the loop body — reference it outside and it's an empty variable, the silent
miss of A013.</details>

6. Two loops in one page. `{% cycle 'a' 'b' %}` in the table yields lightblue → lightgreen
→ lightblue. What would a *second* loop's cycle start with, and why?

<details><summary>Answer</summary>

`lightblue` again. `{% cycle %}` keeps per-tag state and resets when its loop block ends;
the second `{% for %}` starts a fresh cycle. Cycles do not share a page-wide pointer.</details>

7. The view passes `blogs` as a list at index `blogs[1]`. Is there any `forloop`-free way
the template saw element 1? Why does the dot form work?

<details><summary>Answer</summary>

Yes — `blogs.1` (as in `blog_list`'s own condition) used A013's dot order directly:
dict-key → attribute → list-index. `blogs[1]` is not template syntax (brackets aren't a
dot); the loop exists precisely so you usually *don't* hand-index.</details>

8. `GET /blog/` → 200, but `GET /` → 404. What single line of `myProject7/urls.py`
explains it — and what does that teach about URL prefixes?

<details><summary>Answer</summary>

`path('blog/', include('blog.urls'))` — the prefix `blog/` consumes the leading
segment before `blog/urls.py` sees `''` as the remainder. Root `/` has no route in this
project (only `admin/` and `blog/`), so it 404s: A008's prefix-stripping, mounted at a
subpath instead of root.</details>

---

## 📝 Quick Revision — A015 in Five Minutes

**The grammar in one breath:**

```html
{% if cond %}A{% else %}B{% endif %}      ← fork on truthiness
{% for x in xs %}…{% empty %}…{% endfor %} ← repeat; empty-branch
{{ forloop.counter }}                     ← line number (1-based, per loop)
{% with name=expr %}…{% endwith %}        ← alias for a block
{% cycle 'a' 'b' %}                       ← alternate, reset per loop
{% firstof v1 v2 v3 %}                    ← first truthy (skips "")
{% verbatim %}…{% endverbatim %}          ← tokenizer OFF
{% autoescape off %}…{% endautoescape %}  ← escaping OFF
```

**Seven-second rules:**

- Truthiness: `False`·`None`·`0`·`""`·`[]`·`{}` are falsy; everything else truthy.
- Blocks nest by keyword; close in exact reverse order.
- `forloop` lives only inside the loop; `counter` = 1, 2, 3…
- `{% empty %}` is the loop's own no-items branch — no `{% if %}` guard needed.
- `{% with %}` binds once, for the block, as a reference.
- `{% cycle %}` alternates per tag, fresh per loop.
- `firstof` follows truthiness: an empty string is skipped, exactly as the artifact proves.
- `verbatim` = no parsing; `autoescape off` = no escaping (only for trusted content).
- The page lives at `/blog/` — the root `/` 404s by design on this artifact.
---

## 🧠 Final Mental Model — The Sorting Office

```mermaid
flowchart LR
    V["View: one context<br>blogs list · today · html_code"] --> R["render() → lane-2 hit<br>blog/templates/blog/blog_list.html"]
    R --> T["Tokenizer reads the page<br>{{ }} prints · 9 block tags"]
    T --> F{"{% if %} fork<br>blogs.1.is_feature = False"}
    F -- "else-track" --> L["{% for %} belt<br>3 rows · forloop.counter 1·2·3"]
    L --> E{"empty?<br>no → body ×3"}
    E --> C["{% cycle %} wheel<br>lightblue·lightgreen·lightblue"]
    E --> W["{% with %} label<br>total_blogs = 3"]
    C --> FO["{% firstof %} sweep<br>\"\" skipped → \"ABC\""]
    FO --> V2["{% verbatim %}<br>{{blogs.1.author}} literal"]
    V2 --> A["{% autoescape off %}<br>html_code raw"]
    A --> P["HttpResponse → browser<br>the thinking page (200)"]
```

*One sentence to carry:* **the view bags data once; the tokenizer reads the page's forks,
belts, labels, wheels, sweeps, crates, and hatches; the renderer runs them — if forks on
truthiness, for walks the list, cycle stripes, firstof picks, verbatim parks,
autoescape seals — and one context produces a deciding, repeating, striped page at
`/blog/`.**

---

## ❓ FAQ

**Q1. The page 404s at `/` — is this a bug in my project?**
A: Not on this artifact. `myProject7/urls.py` mounts `blog/` only (`path('blog/',
include('blog.urls'))`), with no root `''` route. Open `http://127.0.0.1:8000/blog/`.
Compare A013/A014, which mounted at root `''`. Both are legitimate wiring choices; this
one is the A008 URL-prefix route.

**Q2. Can `{% if %}` do `else if`?**
A: Yes — `{% elif %}` (📌) chains conditions in one block. The artifact uses the simple
`if`/`else` form; `elif` short-circuits exactly like Python's.

**Q3. Is there a `{% while %}` loop?**
A: No. DTL has `{% for %}` only; there is no while tag, by design. Any "loop until
something changes" belongs in the view (or a custom template tag, 📌).

**Q4. Does `{% with %}` save performance?**
A: Marginally — it's a reference bind, not a heavy computation. Its real value is
readability (one name instead of a long dotted path repeated) and freezing a value that
could change. Don't micro-optimize with it; use it to write cleaner templates.

**Q5. Why did `{{blog.author}}` print blank instead of `None`?**
A: Because the dict value is the empty string `""` — truthy? No: falsy, but *set*. A013's
rule: missing **or** falsy-but-empty both print empty via `{{ }}`. Only A014's `yesno`
can distinguish `None` from `False`; only `|default`/`firstof` can substitute a visible
fallback.

**Q6. Can I mix `{% cycle %}` with `{% if %}` inside a loop?**
A: Yes — they nest freely, as long as each block closes in reverse order. The table's
`{% cycle %}` sits inside `{% for %}`; an `{% if %}` around the whole row (Exercise 2)
is the same nesting pattern.

**Q7. What exactly does `{% verbatim %}` *not* parse?**
A: Nothing — that's the point. No `{{ }}`, no `{% %}`, no `{# #}`. The DTL tokenizer
skips the entire region and copies text byte-for-byte, which is why the artifact's
`{{blogs.1.author}}` appeared literally in the rendered response (verified).

**Q8. Is `autoescape off` ever the right call?**
A: Yes, for *trusted rich content* — app-authored HTML, sanitized CMS bodies, markdown
output. The artifact's `html_code` is app-authored (`"<b>Welcome to my blog</b>"`), so
its demo is safe. The rule from A013 never moves: never trust user-submitted strings
with `safe` or `autoescape off`.

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Grammar:** I can read `{% tag %}…{% endtag %}` and know why block
  tags pair by keyword — *§Core-Idea intro*
- [ ] **Checkpoint 2 — Fork:** I can predict the exact output of
  `{% if blogs.1.is_feature %}` … `{% else %}` on this artifact's data — *§Core-Idea 1*
- [ ] **Checkpoint 3 — Loop:** I can predict the three `<li>` lines (including the blank
  author) and explain `forloop.counter` + `{% empty %}` — *§Core-Idea 2*
- [ ] **Checkpoint 4 — Labels & stripes:** I can explain what `{% with %}` freezes and
  what `{% cycle %}` yields per row (lightblue/lightgreen/lightblue) — *§Core-Idea 3–4*
- [ ] **Checkpoint 5 — Picking & shielding:** I can explain why `{% firstof %}` skipped
  the empty author, what `{% verbatim %}` refuses to parse, and the three escaping
  states of `html_code` — *§Core-Idea 5–7*
- [ ] **Checkpoint 6 — The tour:** I can trace `GET /blog/` station by station and
  explain the root 404 — *§Journey*
## 🏋️ Exercises

- **Level 1 — Recall:** Without notes: the nine block tags grouped by job (fork /
  repeat / label / stripe / pick / park / seal); the falsy list; the exact output of
  `{% if blogs.1.is_feature %}`; the rendered `<ul>` lines; the three `html_code`
  states.
- **Level 2 — Understanding:** Explain to a rubber duck why the else-branch won on
  `blogs.1`, why `{% firstof %}` printed `ABC`, and why `{% cycle %}` restarts on a new
  loop — while `forloop.counter` keeps counting 1..3 every loop.
- **Level 3 — Application:** In `myProject7/`: flip the fork to `blogs.0.is_feature`
  (watch the h2 change); hide row 2 with `{% if blog.author %}`; set `blogs = []` in the
  view and watch both `{% empty %}` branches; then add a "Featured ★" suffix to the list
  item only when `blog.is_feature` is truthy. Confirm `GET /blog/` stays 200 and the
  root 404 remains.
- **Level 4 — Interview reasoning:** Defend, in three bullets each, "presentation logic
  belongs in templates" vs "all logic belongs in views" — cite nine tags on this
  artifact, and the one case where logic *does* belong in the view (data preparation,
  filtering data vs deciding presentation).

## 🏁 Final Takeaways

1. **Block tags are the DTL's logic.** Variables print; filters reshape; tags *decide and
   repeat* — each pairs with `{% end… %}`.
2. **Truthiness is the one rule.** `False`·`None`·`0`·`""`·`[]`·`{}` falsy — everything
   else truthy. One rule powers `if`, `firstof`, and the loop's behavior.
3. **`{% for %}` turns one list into N rows** — with `forloop.counter` numbering and
   `{% empty %}` as its own empty-case (no `{% if %}` guard needed).
4. **`{% with %}` labels, `{% cycle %}` stripes** — render-time conveniences that keep
   presentation out of the view.
5. **`firstof` is truthiness in a line** — and an empty string *is* falsy, as the
   artifact shows.
6. **`{% verbatim %}` proves the tokenizer** — no parsing inside; **`{% autoescape off
   %}`** lowers the escaping hatch for a region and must stay shut around user content.
7. **The page lives at `/blog/`** — URL prefixes (A008) return; the root `/` 404s by
   design on this artifact.

---

## 🔄 Next Lecture Connection

The page can now *decide* and *repeat* — but look at what it's surrounded by: the
artifact's own `<h1>Blog List</h1>`, `<title>`, and table markup are **copy-pasted page
skeletons waiting to be shared**. Every row, every header, every `<html>`/`<head>` block
would have to be rewritten on the next page. That is the frontier A015 just made
painfully visible: this chapter proved templates can *think*, and the next step is making
them *reusable* so the thinking page's shell is written once.

The next lecture — **A016 · Templates 4: Inheritance, Static Files** (its folder is
already in this repo) — teaches the tags that stop copy-paste: `{% extends %}` and
`{% block %}` (which A012 introduced on A011's `base.html`) so every page inherits one
frame, plus serving **static files** (CSS/JS/images) so the thinking page's styles leave
the template and live in a proper `static/` place. Today's `{% block %}`-less pages
become children of one parent layout; today's inline
`style="background-color:…"` becomes a stylesheet rule — the fork, loop, and stripe you
just learned running inside a shared, styled shell.

---
<div class="doc-footer">

**Sources used:**

| Source | Role | Notes |
|---|---|---|
| `A015_Templates_3_If_For_With_and_Cycle/myProject7/` — twelfth real artifact | **Primary** | `blog/views.py` (556B, 3-item list + `today` + `html_code`), `blog/urls.py` + `myProject7/urls.py` (the `blog/` prefix — A008's lesson back), and `blog/templates/blog/blog_list.html` (1971B, 9 block tags) quoted verbatim; `settings.py` read (single `blog` registration, pathlib `DIRS` with **no outer dir**, inert `MAILERS`) |
| Verified render — Django 6.1.1 engine + request pipeline | Verification | All 9 tags' outputs confirmed by rendering artifact bytes with artifact context, AND `GET /blog/` → 200 (12 assertions), `GET /` → 404, `GET /admin/` → 302 via test client (HTTP_HOST 127.0.0.1:8000) |
| [`commands.txt`](../commands.txt) | Context | No new lines (last entry remains A007's line 25) — file-editing; the artifact outranks the journal |
| [A014](../A014_Templates_2_Filters_Text_Numbers_Date/README.md) · [A013](../A013_Templates_1_Basics_&_Variables/README.md) · [A011](../A011_App_Level_Templates_Setup_HTML_Integration/README.md) · [A008](../A008_Multiple_Apps_with_Views_URLs_%28Blog_Shop_Example%29/README.md) | Context | First `{% if %}` preview + filters-as-conditions; dot lookup/escaping; lane-2 hit; URL-prefix mounting |
| Official Django docs (built-in template tags reference) | 📌 Supplementary | Truthiness, `forloop` bag, `empty` semantics, `cycle` state, `firstof` fallback, `verbatim` named blocks, `autoescape` — flagged 📌 in place |

> 📌 **Scope note:** everything derived from the artifact and its verified render is
> source-grounded; truthiness/`forloop`/`empty`/`cycle`/`verbatim` mechanics come from
> Django's docs and carry the 📌 badge. The `MAILERS` block, the empty `templates/`
> reference in `DIRS`, the tight `Author:{% firstof %}` spacing, and the educational
> pinning of the else-track (test data chose the negative branch) are flagged ⚠️, not
> endorsed — and this artifact's deliberate root-404 is documented honestly in the
> Journey. No transcript exists for A015 — declared per the documentation contract.
>
> **Navigation:** [← A014 · Templates 2: Filters (Text, Numbers, Date)](../A014_Templates_2_Filters_Text_Numbers_Date/README.md) · [📚 Series Hub](../README.md) · [A016 · Templates 4: Inheritance, Static Files →](../A016_Templates_4_Inheritance_Static_Files/README.md)
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
> [A014](../A014_Templates_2_Filters_Text_Numbers_Date/README.md) · **A015** ·
> [Hub](../README.md)

</div>