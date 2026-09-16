# 🚀 A035 — Django Messages Framework: Debug, Info, Success, Warning & Error

`📖 Lecture A035` · `🎓 Track: Core Django` · `📶 Level: Intermediate` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the `myProject19/` artifact — a Django 6.1.1 project with a `msg_demo` app that demonstrates all five message levels using `django.contrib.messages`. The project has no model and no form; its sole purpose is to show how messages are queued in a view and consumed in a template. All file references below are quoted verbatim from the on-disk artifact.
>
> This lecture builds directly on [A034 — Django ModelForms Delete Data](../A034_Django_ModelForms_Delete_Data/README.md).

---

## 🧭 What You Will Learn

- [ ] What Django's messages framework is and why it exists
- [ ] The five built-in message levels: `debug`, `info`, `success`, `warning`, `error`
- [ ] How to add messages in a view with `messages.<level>(request, text)`
- [ ] How to display messages in a template with `{% if messages %}` and `{{ message.tags }}`
- [ ] How `MESSAGE_LEVEL` in `settings.py` controls which levels are shown
- [ ] How `MessageMiddleware` and `django.contrib.messages.context_processors.messages` wire the framework together
- [ ] Why messages are a one-time display — consumed on render, never repeated

## 🎯 Why This Lecture Matters

Every CRUD operation from A031–A034 ends with a `redirect()`. After that redirect, the original request is gone — you cannot `return render(...)` with an error message because the response cycle is already over. The messages framework solves exactly this problem: it lets a view **queue** a message before redirecting, and the *next* page (after the redirect) **consumes and displays** it. Without this, the only way to communicate "Student added successfully" or "That email already exists" after a redirect is to encode it in the URL (fragile) or use a session manually (error-prone). `django.contrib.messages` handles both the storage and the display cleanly, and it ships with Django — no installation needed.

## ✅ Prerequisites

- [ ] `render()`, `redirect()`, and the POST/Redirect/Get pattern (A029–A031)
- [ ] Django template tags: `{% if %}`, `{% for %}`, `{{ variable }}` (A013–A015)
- [ ] `INSTALLED_APPS`, `MIDDLEWARE`, and `TEMPLATES['OPTIONS']['context_processors']` (A004, A010)
- [ ] `ModelForm` create/delete pattern (A031, A034) — the CRUD context that makes messages necessary

---

## 🧠 The Django Messages Framework

### Why Messages Exist: The PRG Gap

The Post/Redirect/Get pattern (introduced in A031) prevents duplicate form submissions. But it creates a communication gap:

```
POST /add/ → form.save() → redirect('/') → GET /
                                              ↑
                              How does this page know "Student added"?
```

A `render()` can pass context — but after a `redirect()`, the original view's context is lost. The messages framework bridges this gap with a **server-side message queue** stored in the session (or cookie). The view queues a message; the next GET request's template consumes it.

```
POST /add/ → messages.success(request, "Student added!") → redirect('/') → GET /
                      ↑                                                        ↑
                 stored in session                              displayed and cleared
```

### The Architecture

```
myProject19/
├── manage.py
├── myProject19/
│   ├── settings.py     ← MESSAGE_LEVEL = DEBUG; MessageMiddleware; messages context processor
│   └── urls.py         ← path('', include('msg_demo.urls'))
└── msg_demo/
    ├── views.py         ← show_msg: queues all 5 message levels
    ├── urls.py          ← path('', views.show_msg, name='show_msg')
    ├── models.py        ← empty — no model needed
    └── templates/
        └── message.html ← {% for message in messages %} + {{ message.tags }}
```

No model. No form. No migration. The messages framework is pure middleware + context processor — it requires no database table of its own (📌 — by default messages are stored in session cookies, not the database).

### The Three Infrastructure Pieces

Django's messages framework needs three things configured. All three are present in `myProject19/settings.py` by default:

**1. `django.contrib.messages` in `INSTALLED_APPS`:**

```python
# myProject19/settings.py — verbatim
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',   # ← the messages app
    'django.contrib.staticfiles',
    'msg_demo',
]
```

**2. `MessageMiddleware` in `MIDDLEWARE`:**

```python
# myProject19/settings.py — verbatim (relevant excerpt)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',   # ← required
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

`MessageMiddleware` processes messages on every request/response cycle — it reads queued messages from the session and makes them available to the template engine.

**3. The messages context processor in `TEMPLATES`:**

```python
# myProject19/settings.py — verbatim (relevant excerpt)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  # ← required
            ],
        },
    },
]
```

The context processor injects the `messages` variable into every template's context automatically — you never pass it manually from the view.

> [!IMPORTANT]
> All three pieces ship in Django's default project template. They are already present unless someone removed them. If messages don't appear, check this list first.

### The Five Message Levels

Django defines five levels, each with a numeric constant and a convenience function:

| Level | Constant | Integer | `messages.<function>()` | Default CSS tag |
|---|---|---|---|---|
| DEBUG | `messages.DEBUG` | 10 | `messages.debug(request, text)` | `debug` |
| INFO | `messages.INFO` | 20 | `messages.info(request, text)` | `info` |
| SUCCESS | `messages.SUCCESS` | 25 | `messages.success(request, text)` | `success` |
| WARNING | `messages.WARNING` | 30 | `messages.warning(request, text)` | `warning` |
| ERROR | `messages.ERROR` | 40 | `messages.error(request, text)` | `error` |

The integer values matter for filtering: `MESSAGE_LEVEL` in `settings.py` sets the minimum level that is stored and displayed. Any message with a level **below** `MESSAGE_LEVEL` is silently discarded.

### The View

```python
# msg_demo/views.py — verbatim from A035
from django.shortcuts import render
from django.contrib import messages

def show_msg(request):
    messages.debug(request, 'This is a debug message.')
    messages.info(request, 'This is an info message.')
    messages.success(request, 'This is a success message.')
    messages.warning(request, 'This is a warning message.')
    messages.error(request, 'This is an error message.')
    return render(request, 'message.html')
```

**Explanation:**
- Line 2: `from django.contrib import messages` — imports the messages module. All five level functions live here.
- Lines 5–9: Five `messages.<level>(request, text)` calls — each **queues** one message into the request's session storage. No message is displayed yet; they are held until the template iterates over `messages`.
- Line 10: `return render(request, 'message.html')` — renders the template. The messages context processor automatically injects the queued messages as the `messages` variable. **Note:** This view queues messages and renders in the same request — which works for demonstration purposes but is not the real-world pattern. In production, messages are queued before a `redirect()` and consumed by the *next* request's template (📌 — the PRG pattern is the real use case; this lecture uses a single-request demo for simplicity).

### `MESSAGE_LEVEL` — The Visibility Gate

```python
# myProject19/settings.py — verbatim
from django.contrib.messages import constants as messages_constants

MESSAGE_LEVEL = messages_constants.DEBUG  # Set the message level to DEBUG
```

**Explanation:**
- Without this line, Django's default `MESSAGE_LEVEL` is `messages.INFO` (integer 20). That means `messages.debug()` calls are silently discarded — debug messages never appear in production unless you explicitly lower the level.
- `messages_constants.DEBUG` sets the level to 10, so all five levels (10, 20, 25, 30, 40) pass the filter.
- The import: `from django.contrib.messages import constants as messages_constants` — the `constants` module holds `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR` as integers. Using the named constant (not the raw integer `10`) makes the intent clear and immune to typos.

> [!TIP]
> In production, keep `MESSAGE_LEVEL` at `INFO` or higher. `DEBUG` messages expose internal state that end users should never see.

### The Template

```html
<!-- msg_demo/templates/message.html — verbatim from A035 -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>All Messages Data</title>
    <style>
        .debug { color: blue; }
        .info { color: green; }
        .success { color: green; }
        .warning { color: orange; }
        .error { color: red; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
    </style>
</head>
<body>
    <h1>All Messages Data</h1>
    {% if messages %}
        <ul>
            {% for message in messages %}
                <li class="{{ message.tags }}">{{ message }}</li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No messages available.</p>
    {% endif %}
</body>
</html>
```

**Explanation:**
- Lines 6–12: Inline `<style>` — maps each message tag to a colour. Per AGENTS §6, inline styles in templates do not render on GitHub, but they work fine in a running Django app. For a production project, these styles belong in `static/css/` and loaded with `{% static %}`.
- `{% if messages %}` — guards the list. If no messages are queued (e.g. on a fresh GET with no prior POST), the `{% else %}` branch renders "No messages available."
- `{% for message in messages %}` — iterates over the `messages` context variable (injected by the context processor). **This iteration consumes the messages** — after the template renders, the messages are cleared from the session and will not appear on the next page load.
- `{{ message.tags }}` — outputs the level name as a CSS class string (e.g. `debug`, `info`, `success`). This is how the CSS colours are applied per level.
- `{{ message }}` — outputs the message text itself.

### How `message.tags` Is Built

Each message object has two relevant attributes:

| Attribute | Value for `messages.success(request, "Saved!")` | Description |
|---|---|---|
| `message.message` | `"Saved!"` | The text string |
| `message.level` | `25` | The integer level constant |
| `message.level_tag` | `"success"` | The level name as a lowercase string |
| `message.tags` | `"success"` | `level_tag` + any extra tags added via `extra_tags=` |

`{{ message.tags }}` typically equals `{{ message.level_tag }}` unless you add custom tags. In this lecture's template, it is used directly as the CSS class name — which only works because the CSS classes (`.debug`, `.info`, etc.) are intentionally named after the level tags.

### The URL Configuration

```python
# msg_demo/urls.py — verbatim
from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_msg, name='show_msg'),
]
```

```python
# myProject19/urls.py — verbatim (relevant excerpt)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('msg_demo.urls')),
]
```

Root-mounted at `''` — `GET /` hits `show_msg` directly.

### The Message Lifecycle

The diagram below shows a real-world POST → redirect → display cycle, which is the intended production pattern for messages (the A035 demo compresses this into one request for simplicity):

```
View (POST handler)                   Session storage           Template (next GET)
─────────────────────────────────────────────────────────────────────────────────
messages.success(request, "Saved!")──▶ [queued in session]
redirect('student_list') ────────────────────────────────▶ GET /
                                                               │
                                                       MessageMiddleware reads session
                                                               │
                                                       context processor injects `messages`
                                                               │
                                                       {% for message in messages %}
                                                               │
                                                       messages cleared from session
```

**Key point:** messages are stored in the **session** (by default using cookies), not in the database. They survive the redirect because the session persists across requests for the same browser. They are cleared the moment the template iterates over them — each message is a one-time display.

---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **Messages framework** | Django's one-time notification system | `django.contrib.messages`: a middleware + context processor system that queues messages in the session and injects them into the next template | The sticky note on the fridge — seen once, then thrown away |
| **Message level** | How urgent is this message? | An integer constant (`DEBUG=10`, `INFO=20`, `SUCCESS=25`, `WARNING=30`, `ERROR=40`) controlling whether a message is stored and shown | Higher number = louder alarm |
| **`MESSAGE_LEVEL`** | The volume dial | The `settings.py` constant that sets the minimum level to store; messages below this level are silently dropped | The door height — shorter messages can't get in |
| **`messages.<level>()`** | Queue this message | A convenience function that calls `messages.add_message(request, LEVEL, text)` under the hood | Posting a note on the board |
| **`message.tags`** | The CSS class hint | A string combining the level tag (`debug`, `info`, `success`, `warning`, `error`) and any `extra_tags`; used as HTML class names in templates | The colour label on the sticky note |
| **`MessageMiddleware`** | The message postman | Middleware at `django.contrib.messages.middleware.MessageMiddleware` that reads queued messages from the session on each request | The postman who delivers and collects |
| **Messages context processor** | Auto-injector | `django.contrib.messages.context_processors.messages` — injects the `messages` iterable into every template's context automatically | The automatic refill |
| **One-time display** | Seen once, gone forever | Messages are consumed (cleared from session) when the template iterates over them; a page refresh shows no messages | A self-destructing sticky note |

> New terms must also be added to `docs/MEMORY.md` §2.

## 💡 Real-World Analogy

**The messages framework is the "order ready" buzzer at a fast-food counter.** When you place your order (POST request), the cashier hands you a buzzer (the message is queued in the session). You sit down (the redirect happens). When the buzzer goes off (the next page loads and the template iterates over `messages`), you collect your tray ("Student added successfully!") and the buzzer is handed back to be used for the next customer (the message is cleared from the session). Without the buzzer, the cashier would have to run over to you personally after the redirect — but they can't, because the POST cycle is already over.

The five levels are the buzzer's intensity: a `debug` buzzer barely vibrates (internal dev note), an `info` buzzer gives a gentle ping, `success` lights up green, `warning` blinks yellow, and `error` buzzes red and loud. `MESSAGE_LEVEL` is the setting that decides which buzzers the restaurant uses at all — a production counter leaves the `debug` buzzers in the drawer.

## ❌ Common Beginner Mistakes

1. **Calling `messages.<level>()` after `redirect()`** — messages must be queued *before* the redirect. After `redirect()` is returned, the view has ended; there is no request object to attach the message to. Fix: always call `messages.*` then `return redirect(...)`.

2. **Forgetting `MESSAGE_LEVEL = messages_constants.DEBUG` in dev** — debug messages are silently dropped by the default `INFO` level. The view appears to work (no error) but `messages.debug()` calls are invisible. Fix: add `MESSAGE_LEVEL = messages_constants.DEBUG` to `settings.py` while developing.

3. **Missing `MessageMiddleware` or the context processor** — messages never appear in templates; no error is raised. Fix: verify both are present in `MIDDLEWARE` and `TEMPLATES['OPTIONS']['context_processors']`.

4. **Iterating `messages` twice in the same template** — the second loop produces nothing; messages are consumed on first iteration. Fix: iterate once and store in a variable if multiple uses are needed, or use `{% for message in messages %}` exactly once.

5. **Using inline `<style>` in the `message.html` template for production** — the artifact does this for demo convenience, but styles should live in `static/css/` and be loaded via `{% static %}` in a real app. Fix: move the CSS to the stylesheet and use `{% load static %}` + `<link>`.

6. **Hardcoding message text instead of using `message.tags` for the CSS class** — if the class name doesn't match the level tag, the colour mapping breaks. Fix: always use `class="{{ message.tags }}"` and define CSS classes named after the level tags.

## 🧠 Common Misconceptions

| ✅ Messages framework IS … | ❌ It is NOT … |
|---|---|
| A session-based one-time notification queue | A database log — messages are not stored in any table |
| Automatically available in every template via context processor | Something you pass manually in `render()`'s context dict |
| Cleared the moment the template iterates over them | Persistent — they do not re-appear on page refresh |
| Controlled by `MESSAGE_LEVEL` — levels below it are dropped | A filter applied at render time — filtering happens at queue time |
| Framework-level (works across apps and views) | Per-view — you don't need to configure it per view |
| Used for one-time user feedback (after save, delete, login) | Used for permanent status or data display (use model fields for that) |

## 🧪 Practical Example

The real-world messages pattern — adding a success message to the `student_delete` view from A034:

```python
# student/views.py — practical usage of messages after delete
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages           # 1. Import messages
from .models import Student

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name                   # 2. Capture before delete
        student.delete()
        messages.success(                     # 3. Queue the message
            request,
            f'"{name}" was deleted successfully.'
        )
        return redirect('student_list')       # 4. Redirect (message survives in session)
    return render(request, 'student_confirm_delete.html', {'student': student})
```

```html
<!-- student/templates/student_list.html — consuming the message -->
{% if messages %}
    <ul>
        {% for message in messages %}
            <li class="{{ message.tags }}">{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
```

**Explanation:**
- Step 1 (Import): `from django.contrib import messages` — one import, access to all five levels.
- Step 2 (Capture): The student's name is saved to a local variable *before* `student.delete()` removes the object from the database.
- Step 3 (Queue): `messages.success()` stores "Asha was deleted successfully." in the session before the redirect. The session persists to the next request.
- Step 4 (Redirect): `redirect('student_list')` issues a 302. The browser GETs `/`, the template renders, and the context processor injects the queued message.
- Template: `{% if messages %}` guards the block. `{{ message.tags }}` applies the CSS class; `{{ message }}` prints the text. After iteration the message is cleared — refresh shows no message.

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. What problem does `django.contrib.messages` solve?**
A: After a `redirect()`, a view's context is lost — there is no way to pass data to the next page via `render()`. The messages framework bridges this gap by storing one-time notifications in the session, so they survive the redirect and are displayed by the next page's template.

**Q2. What are the five message levels and their integer values?**
A: `DEBUG=10`, `INFO=20`, `SUCCESS=25`, `WARNING=30`, `ERROR=40`. The integers allow `MESSAGE_LEVEL` to act as a minimum-threshold filter.

**Q3. What is `MESSAGE_LEVEL` and why does it matter?**
A: It is a `settings.py` constant that sets the minimum level a message must reach to be stored. Messages below `MESSAGE_LEVEL` are silently discarded at queue time. Default is `INFO` (20), which drops `DEBUG` messages. In development, set it to `DEBUG` (10) to see all levels.

**Q4. Why are messages "consumed" after display?**
A: Messages are stored in the session (or a cookie). When a template iterates over `messages`, Django marks them as read and removes them from the session. This is the one-time-display guarantee — a page refresh does not re-show old messages.

**Q5. What two infrastructure pieces must be in `settings.py` for messages to work?**
A: `MessageMiddleware` in `MIDDLEWARE`, and `django.contrib.messages.context_processors.messages` in `TEMPLATES['OPTIONS']['context_processors']`. Plus `django.contrib.messages` in `INSTALLED_APPS` — three pieces total.

**Q6. What is `message.tags` and how is it used in templates?**
A: A string combining the level tag (e.g. `success`) and any `extra_tags` passed to the message. It is typically used as an HTML `class` attribute (`class="{{ message.tags }}"`) to apply level-specific CSS styling.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. What problem does the messages framework solve that `render()` with context cannot?

<details><summary>Answer</summary>

After a `redirect()`, the view's response cycle is over — context passed to `render()` is gone. Messages are stored in the session before the redirect and survive to the next request, where they are consumed by the template.
</details>

2. What are the five message levels in order from lowest to highest?

<details><summary>Answer</summary>

`DEBUG` (10) → `INFO` (20) → `SUCCESS` (25) → `WARNING` (30) → `ERROR` (40).
</details>

3. What does `MESSAGE_LEVEL = messages_constants.DEBUG` do in `settings.py`?

<details><summary>Answer</summary>

Sets the minimum message level to 10 (DEBUG), so all five levels pass the filter and are stored/displayed. Without it, the default level is INFO (20) and `messages.debug()` calls are silently dropped.
</details>

4. What three settings infrastructure pieces does the messages framework need?

<details><summary>Answer</summary>

1. `'django.contrib.messages'` in `INSTALLED_APPS`. 2. `'django.contrib.messages.middleware.MessageMiddleware'` in `MIDDLEWARE`. 3. `'django.contrib.messages.context_processors.messages'` in `TEMPLATES['OPTIONS']['context_processors']`.
</details>

5. What does `{{ message.tags }}` render, and how is it used in the template?

<details><summary>Answer</summary>

It renders the level name as a lowercase string (e.g. `success`, `warning`). Used as an HTML class attribute (`class="{{ message.tags }}"`) to apply level-specific CSS colours.
</details>

6. What happens to messages after the template iterates over them?

<details><summary>Answer</summary>

They are cleared from the session. A page refresh will not show them again — one-time display is the core guarantee of the framework.
</details>

---

## 📝 Quick Revision

| Concept | Code | Purpose |
|---|---|---|
| Import | `from django.contrib import messages` | Access all level functions |
| Queue debug | `messages.debug(request, text)` | Stored only if `MESSAGE_LEVEL ≤ 10` |
| Queue info | `messages.info(request, text)` | Stored only if `MESSAGE_LEVEL ≤ 20` |
| Queue success | `messages.success(request, text)` | Stored only if `MESSAGE_LEVEL ≤ 25` |
| Queue warning | `messages.warning(request, text)` | Stored only if `MESSAGE_LEVEL ≤ 30` |
| Queue error | `messages.error(request, text)` | Stored only if `MESSAGE_LEVEL ≤ 40` |
| Consume | `{% for message in messages %}` | Iterates and clears all queued messages |
| CSS class | `class="{{ message.tags }}"` | Applies level-based style |
| Text | `{{ message }}` | Renders message text |
| Level gate | `MESSAGE_LEVEL = messages_constants.DEBUG` | Show all levels in dev |

---

## 🧠 Final Mental Model

```
settings.py (MESSAGE_LEVEL = DEBUG)
      │
      │  only messages with level ≥ MESSAGE_LEVEL are stored
      ▼
View  →  messages.debug()   ─┐
         messages.info()    ─┤
         messages.success() ─┼──▶ session storage (cookie/db)
         messages.warning()  ─┤
         messages.error()   ─┘
              │
         redirect() / render()
              │
              ▼
Template (next request)
   context processor injects `messages`
              │
   {% if messages %}
      {% for message in messages %}
         <li class="{{ message.tags }}">{{ message }}</li>   ← displayed
      {% endfor %}
              │
   messages cleared from session                            ← gone
```

Five levels, one queue, one consumer, one clearing. `MESSAGE_LEVEL` is the gate at the entrance; `{% for message in messages %}` is the gate at the exit.

---

## ❓ FAQ

**Q1. Where are messages physically stored?**
A: By default in the session, which is stored in a cookie (`FallbackStorage` tries cookies first, then falls back to session storage). No database table is involved. You can configure this via `MESSAGE_STORAGE` in `settings.py` (📌 — beyond this lecture).

**Q2. Can I add extra CSS classes to a message beyond the level tag?**
A: Yes — use the `extra_tags` parameter: `messages.success(request, "Saved!", extra_tags='fade-in')`. The template then sees `class="success fade-in"` in `{{ message.tags }}`.

**Q3. Can I use messages without the context processor?**
A: Yes — call `get_messages(request)` from `django.contrib.messages` directly in the view and pass it as context. But the context processor eliminates this boilerplate for every template — use it.

**Q4. What is the difference between `message.level_tag` and `message.tags`?**
A: `level_tag` is always just the level name (`success`). `tags` is `level_tag` plus any `extra_tags` you added, joined by a space. For simple usage without `extra_tags` they are identical.

**Q5. Will messages appear if I `render()` instead of `redirect()` after saving?**
A: Yes — the context processor injects messages into any template rendered in the same request. But the reason messages exist is specifically to survive a `redirect()`. Using both in the same request is valid for demos (as in this lecture's artifact) but the real-world pattern is always queue → redirect → consume.

**Q6. What happens if `MessageMiddleware` is missing from `MIDDLEWARE`?**
A: Django raises `MessageFailure: You cannot add messages without installing django.contrib.messages.middleware.MessageMiddleware` at the point where `messages.<level>()` is called. The error is loud and specific.

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Purpose:** I can explain why `django.contrib.messages` is needed after a `redirect()` and what problem it solves — *§Why Messages Exist: The PRG Gap*
- [ ] **Checkpoint 2 — Levels:** I can list all five message levels in order with their integer values and explain what `MESSAGE_LEVEL` does — *§The Five Message Levels*
- [ ] **Checkpoint 3 — Infrastructure:** I can name the three `settings.py` pieces required for messages to work and what each one does — *§The Three Infrastructure Pieces*
- [ ] **Checkpoint 4 — Template:** I can write the `{% if messages %}` / `{% for message in messages %}` template block and explain `{{ message.tags }}` — *§The Template*
- [ ] **Checkpoint 5 — Lifecycle:** I can trace a message from `messages.success()` in a view through session storage, redirect, context processor injection, template consumption, and session clearing — *§The Message Lifecycle*

---

## 🏋️ Exercises

- **Level 1 — Recall:** Name all five message levels and their integer constants. What is the default `MESSAGE_LEVEL`? What happens to `messages.debug()` if you don't override it?
- **Level 2 — Understanding:** Why does the artifact's `show_msg` view queue messages and then `render()` in the same request? Is this the intended real-world pattern? What is the real pattern and why?
- **Level 3 — Application:** Integrate messages into the `myProject18` student CRUD app: add `messages.success()` after a successful create (A031), update (A033), and delete (A034). Add the `{% if messages %}` block to `student_list.html` with CSS classes matching the level tags. Add `MESSAGE_LEVEL = messages_constants.DEBUG` to `settings.py`.
- **Level 4 — Interview reasoning:** A teammate says "I just use the URL query string to pass status messages after a redirect — `?status=saved`. Why bother with `django.contrib.messages`?" Explain the drawbacks of the query-string approach (XSS exposure, visible in history, must be manually cleared) and the advantages of the messages framework (session-backed, one-time display, level-based filtering, no template URL-parsing code).

---

## 🏁 Final Takeaways

1. `django.contrib.messages` solves the PRG gap: it lets views queue notifications that survive a `redirect()` and are displayed once by the next template.
2. Five built-in levels — `debug` (10), `info` (20), `success` (25), `warning` (30), `error` (40) — each maps to a convenience function `messages.<level>(request, text)`.
3. `MESSAGE_LEVEL` in `settings.py` is the minimum-level gate; messages below it are silently dropped. Default is `INFO` — set to `DEBUG` in development to see all levels.
4. Three infrastructure pieces are required: `django.contrib.messages` in `INSTALLED_APPS`, `MessageMiddleware` in `MIDDLEWARE`, and the messages context processor in `TEMPLATES`. All ship in Django's default project template.
5. The context processor injects `messages` into every template automatically — no manual context dict needed.
6. `{{ message.tags }}` gives the level name as a CSS class string; `{{ message }}` gives the text.
7. Messages are consumed (cleared from session) when the template iterates over them — one-time display is the core guarantee.

## 🔄 Next Lecture Connection

A035 adds one-time feedback to CRUD operations. A036 — [Authentication & Permissions](../A036_Authentication_&_Permissions/README.md) — adds the access control layer: login, logout, `@login_required`, user permissions, and protecting views so only authenticated users can reach the CRUD operations from A031–A034.

---

<div class="doc-footer">

**Sources used:** `myProject19/` artifact (Django 6.1.1): `manage.py`, `myProject19/settings.py` (`INSTALLED_APPS` includes `django.contrib.messages` and `msg_demo`; `MIDDLEWARE` includes `MessageMiddleware`; `TEMPLATES['OPTIONS']['context_processors']` includes messages processor; `MESSAGE_LEVEL = messages_constants.DEBUG`; `STATICFILES_DIRS` ghost shelf W004), `myProject19/urls.py` (`path('', include('msg_demo.urls'))`), `msg_demo/views.py` (`show_msg`: queues all five levels → `render('message.html')`), `msg_demo/urls.py` (root path), `msg_demo/models.py` (empty — no model), `msg_demo/templates/message.html` (`{% if messages %}` / `{% for message in messages %}` with `{{ message.tags }}` CSS class). No lecture transcript in folder — chapter built from on-disk artifact and official Django messages documentation. Practical Example (§) extends the A034 delete view per series-internal convention; marked 📌 where it exceeds the artifact.

**Navigation:** ← [A034 — Django ModelForms Delete Data](../A034_Django_ModelForms_Delete_Data/README.md) · [Series hub](../README.md) · [A036 — Authentication & Permissions →](../A036_Authentication_&_Permissions/README.md)

</div>
