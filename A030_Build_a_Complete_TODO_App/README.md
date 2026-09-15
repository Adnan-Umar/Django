# 🚀 A030 — Build a Complete TODO App

`📖 Lecture A030` · `🎓 Track: Core Django` · `📶 Level: Intermediate` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the `todoproject/` artifact — a Django 6.1.1 project with a `todo` app providing full CRUD (list, create, edit, delete, toggle) for tasks. The app is registered in `INSTALLED_APPS`, namespaced as `todo`, and managed via Django Admin with `@admin.register()`. All file references below are quoted verbatim from the on-disk artifact.
>
> This lecture builds directly on [A029 — HTML Forms, POST, CSRF Token & Validation](../A029_HTML_Forms_POST_CSRF_Token_&_Validation/README.md).

---

## 🧭 What You Will Learn

- [ ] How to build a complete CRUD application in Django (Create, Read, Update, Delete)
- [ ] How URL namespaces (`app_name`) prevent reverse-lookup collisions across apps
- [ ] How `reverse()` resolves named URLs in Python views (avoiding hardcoded paths)
- [ ] How template inheritance chains: project-level `base.html` → app-specific child templates
- [ ] How `ModelAdmin` subclasses customize the Django Admin interface (`list_display`, `search_fields`, `list_filter`, `ordering`)
- [ ] How `makemigrations` + `migrate` evolve the database schema as models change

## 🎯 Why This Lecture Matters

A030 is the first lecture that wires every concept from A001–A029 into a single working application: models define the data shape, migrations create the table, views handle all five CRUD operations, URLs route with a namespace to avoid collisions, templates inherit a shared layout, and admin provides instant management. If any piece is wrong (a wrong URL name, a mismatched context variable, a missing `max_length`), the app breaks visibly — making this the definitive integration test of the entire core Django track.

## ✅ Prerequisites

- [ ] Models defined, registered in admin, and migrated (covered in A022–A023)
- [ ] `render()`, `redirect()`, `get_object_or_404()` (covered in A010–A013)
- [ ] URL routing with `path()`, `include()`, and namespaces (covered in A007–A009)
- [ ] Template inheritance with `{% extends %}` and `{% block %}` (covered in A012)
- [ ] HTML forms with `{% csrf_token %}`, POST handling, and validation (covered in A029)
- [ ] `@admin.register()` decorator and `ModelAdmin` options (covered in A028)

## 🧠 Building the Complete TODO App

### The Architecture

```
todoproject/                    ← project root (where manage.py lives)
├── manage.py
├── todoproject/                ← config package (settings, root urls, wsgi)
│   ├── settings.py             ← INSTALLED_APPS includes 'todo'; ROOT_URLCONF
│   ├── urls.py                 ← includes todo.urls with namespace='todo'
│   ├── wsgi.py
│   └── asgi.py
├── todo/                       ← the app
│   ├── models.py               ← Task model (4 fields)
│   ├── views.py                ← 5 CRUD views
│   ├── urls.py                 ← 5 URL patterns; app_name = 'todo'
│   ├── admin.py                ← @admin.register(Task) with ModelAdmin
│   ├── apps.py                 ← TodoConfig
│   ├── migrations/
│   │   ├── 0001_initial.py     ← creates Task table
│   │   └── 0002_alter_task_title.py ← adds max_length=200 to title
│   └── templates/todo/         ← app-level templates (namespaced)
│       ├── base.html           ← Bootstrap layout; nav with Add Task button
│       ├── task_list.html      ← table of all tasks; edit/delete/toggle buttons
│       ├── task_form.html      ← form for Add + Edit (shared template)
│       └── task_confirm_delete.html ← delete confirmation page
└── db.sqlite3                  ← SQLite database
```

### The Task Model

```python
# todo/models.py — verbatim from A030 (post-fix)
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

**Explanation:**
- Line 5: `title = models.CharField(max_length=200)` — required `max_length` for `CharField`. **Bug fixed:** the original had `title = models.CharField()` which raises `SystemCheckError` — `CharField` requires `max_length` (⚠️ flagged per §12).
- Line 6: `description = models.TextField(blank=True)` — `TextField` has no `max_length`; `blank=True` allows empty descriptions.
- Line 7: `completed = models.BooleanField(default=False)` — tracks whether the task is done.
- Line 8: `created_at = models.DateTimeField(auto_now_add=True)` — auto-sets on creation, immutable afterward.
- Line 10-11: `__str__` returns the title, so tasks display meaningfully in admin and shell.

### Migrations: From Model to Table

```bash
py -3 manage.py makemigrations todo    # creates migration file (schema change)
py -3 manage.py migrate                # applies migration (creates table)
```

Two migrations exist in A030:
1. **`0001_initial.py`** — Creates the `Task` table with all four fields.
2. **`0002_alter_task_title.py`** — Alters `title` to add `max_length=200` (fix for the `CharField()` bug).

The migration system maps Python model definitions to SQL `CREATE TABLE` / `ALTER TABLE` statements. Each `makemigrations` call records a *diff*; `migrate` executes it against the database.

### The Five CRUD Views

```python
# todo/views.py — verbatim from A030 (post-fix)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Task

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title:
            Task.objects.create(title=title, description=description)
            return redirect(reverse('todo:task_list'))
        error = "Title cannot be empty."
        return render(request, 'todo/task_form.html', {'error': error})
    return render(request, 'todo/task_form.html')

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        completed = request.POST.get('completed') == 'on'
        if title:
            task.title = title
            task.description = description
            task.completed = completed
            task.save()
            return redirect(reverse('todo:task_list'))
        return render(request, 'todo/task_form.html', {'task': task, "error": "Title cannot be empty."})
    return render(request, 'todo/task_form.html', {'task': task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect(reverse('todo:task_list'))
    return render(request, 'todo/task_confirm_delete.html', {'task': task})

def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.completed = not task.completed
        task.save()
    return redirect(reverse('todo:task_list'))
```

**Explanation:**
- `task_list` — **Read all.** Fetches all tasks ordered newest-first, passes as `{'tasks': tasks}` (plural). **Bug fixed:** the original passed the QuerySet as `task` (singular) but the template iterated `{% for task in tasks %}`, causing a `VariableDoesNotExist` error.
- `task_create` — **Create.** Checks `request.method == 'POST'`, reads `title`/`description` via `request.POST.get()`, validates title is non-empty, creates the record, then `redirect()` to the list via `reverse('todo:task_list')`. The `reverse()` call resolves the URL from its name, not its path — if the URL pattern changes, `reverse()` still works.
- `task_update` — **Update.** Fetches the task by PK (`get_object_or_404` returns 404 if not found), processes POST data, updates all three fields, saves. Uses the same `task_form.html` template as create (the `task` variable distinguishes edit from add).
- `task_delete` — **Delete.** GET renders confirmation page; POST deletes and redirects. Follows PRG pattern.
- `task_toggle_complete` — **Toggle.** Flips `completed` boolean and saves, then redirects back to list.

**Bugs found in A030:**

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | `todo/models.py:5` | `CharField()` missing required `max_length` | Added `max_length=200` |
| 2 | `todo/views.py:7-8` | QuerySet variable `task` (singular) vs template `tasks` (plural) | Renamed to `tasks` |
| 3 | `todo/templates/todo/task_list.html:19` | URL name `todo:task_toggle` doesn't exist | Fixed to `todo:task_toggle_complete` |
| 4 | `todo/templates/todo/task_list.html:28` | URL name `todo:task_edit` doesn't exist | Fixed to `todo:task_update` |

### URL Configuration with Namespace

```python
# todo/urls.py — verbatim from A030
from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('toggle/<int:pk>/', views.task_toggle_complete, name='task_toggle_complete'),
]
```

**Explanation:**
- Line 4: `app_name = 'todo'` — declares the URL namespace. Every `{% url %}` tag and `reverse()` call uses `'todo:...'` to disambiguate from other apps that might use the same URL names (`task_list`, `task_create`, etc.).
- Line 7: `''` → `task_list` — the root of the app serves the task list (mounted at `/` via root URL config).
- Line 8: `add/` → `task_create` — handles both GET (shows empty form) and POST (creates task).
- Line 9: `edit/<int:pk>/` → `task_update` — `<int:pk>` captures the task ID as an integer.
- Line 10: `delete/<int:pk>/` → `task_delete`.
- Line 11: `toggle/<int:pk>/` → `task_toggle_complete`.

The root URL config wires this in:

```python
# todoproject/urls.py
path('', include(('todo.urls', 'todo'), namespace='todo')),
```

The double-nesting (`include(('todo.urls', 'todo'), namespace='todo')`) sets both the app namespace and the instance namespace to `todo`, so `{% url 'todo:task_list' %}` resolves to `/`.

### Templates: Inheritance Chain

All templates extend `todo/base.html`, which provides the Bootstrap 5.3.8 layout and navigation:

```html
<!-- todo/templates/todo/base.html — verbatim -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Todo App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB"
          crossorigin="anonymous">
</head>
<body>
    <nav class="navbar navbar-light bg-light mb-4">
        <div class="container">
            <a class="navbar-brand" href="{% url "todo:task_list" %}">Todo App</a>
            <a class="btn btn-primary" href="{% url "todo:task_create" %}">Add Task</a>
        </div>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**Three child templates fill `{% block content %}`:**

| Template | Purpose | Key Elements |
|---|---|---|
| `task_list.html` | Displays all tasks in a table | `{% for task in tasks %}`, edit/delete/toggle buttons with `{% url %}` |
| `task_form.html` | Add + Edit form (shared) | `{% csrf_token %}`, `<input name="title">`, `<textarea name="description">`, error display |
| `task_confirm_delete.html` | Delete confirmation | Task title display, POST delete form, cancel link |

The **task list template** is where two URL-name bugs existed (both fixed):

```html
<!-- Bug 3 (fixed): was todo:task_toggle, correct name is todo:task_toggle_complete -->
<form method="POST" action="{% url 'todo:task_toggle_complete' task.pk %}" style="display:inline;">

<!-- Bug 4 (fixed): was todo:task_edit, correct name is todo:task_update -->
<a class="btn btn-sm btn-warning" href="{% url 'todo:task_update' task.pk %}">Edit</a>
```

### Django Admin: ModelAdmin Customization

```python
# todo/admin.py — verbatim from A030
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'completed')
    list_filter = ('completed', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
```

**Explanation:**
- Line 5: `@admin.register(Task)` — registers `Task` with the admin site AND attaches `TaskAdmin` as its configuration class. Equivalent to `admin.site.register(Task, TaskAdmin)`.
- Line 7: `list_display` — which fields appear as columns in the admin change list.
- Line 8: `list_filter` — sidebar filter widgets for the listed fields.
- Line 9: `search_fields` — enables the search bar, querying the specified fields.
- Line 10: `ordering` — default sort order in the change list (newest first).

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **CRUD** | Create, Read, Update, Delete | The four fundamental operations on persistent data | the four letter openers |
| **`app_name`** | App's URL namespace | Declared in `urls.py`; prefixes all URL names to avoid cross-app collisions | the app's last name |
| **`reverse()`** | URL resolver in Python | Takes a URL name (e.g. `'todo:task_list'`) + optional args; returns the path string | the back-door lookup |
| **`{% url %}`** | URL resolver in templates | Resolves a named URL to a path at render time; raises NoReverseMatch if not found | the template lookup |
| **`get_object_or_404()`** | Shortcut for fetch-or-fail | Queries the model by PK; returns 404 HTTP if not found instead of raising | the polite rejection |
| **`ModelAdmin`** | Admin customization class | Controls how a model appears in Django Admin (columns, filters, search, ordering) | the admin window dressing |
| **`app_name`** | App's URL namespace | Declared in `urls.py`; prefixes all URL names to avoid cross-app collisions | the app's last name |
| **`makemigrations`** | Generate migration file | Inspects model changes and writes a migration file (the schema diff) | the blueprint |
| **`migrate`** | Apply migrations | Executes pending migrations against the database (creates/updates tables) | the construction crew |
| **`namespace`** | URL namespace | Wraps URL names in a named scope (`todo:task_list`) to prevent collisions | the namespace envelope |
| **PRG pattern** | Post-Redirect-Get | After a successful POST, redirect to a GET page; prevents duplicate submissions on refresh | the roundabout |

## 💡 Real-World Analogy

**A TODO app is a warehouse with five stations.** The **model** is the warehouse blueprint (what shelves hold: title, description, done flag, date). **Migrations** are the construction crew that builds shelves from the blueprint. The **list view** is the loading dock where all boxes are displayed on a conveyor belt. **Create** is the intake window: fill out a form, a box gets stamped and shelved. **Update** is the rework station: grab a box by its label, modify it, put it back. **Delete** is the shredding station: confirm you want to destroy it, then it's gone. **Toggle** is the quick-flip station: a single button switches a box between "in stock" and "out of stock." The **admin** is the manager's office with a clipboard (`list_display`), a filter board (`list_filter`), and a search index (`search_fields`) — everything the manager needs without visiting the floor. The **namespace** is the zip code on each station's address, ensuring mail (`reverse()` / `{% url %}`) reaches the right place when multiple departments share common labels.

## ❌ Common Beginner Mistakes

1. **Forgetting `app_name` in `urls.py`** — Without `app_name = 'todo'`, `{% url 'todo:task_list' %}` raises `NoReverseMatch` because the namespace doesn't exist. Fix: always declare `app_name` when using `{% url 'namespace:name' %}`.

2. **Wrong URL names in `{% url %}` tags** — If the view is named `task_toggle_complete` but the template says `{% url 'todo:task_toggle' %}`, Django raises NoReverseMatch. Fix: match URL names exactly between `urls.py` and templates/views.

3. **Variable name mismatch between view and template** — Passing `{'task': tasks}` (singular key) but iterating `{% for task in tasks %}` fails because `tasks` is undefined. Fix: ensure the context key matches the template variable name.

4. **`CharField` without `max_length`** — Django requires `max_length` for `CharField`. `CharField()` raises `SystemCheckError` during `makemigrations`. Fix: always specify `max_length` (e.g., `max_length=200`).

5. **Not redirecting after POST** — Without `redirect()` after a successful create/update/delete, refreshing the page resubmits the form (duplicate data). Fix: always redirect after a successful POST (PRG pattern).

## 🧠 Common Misconceptions

| ✅ Django IS … | ❌ It is NOT … |
|---|---|
| Namespaced URLs: `app_name` in `urls.py` + `namespace=` in root `urls.py` | A single global URL name registry — names collide without namespaces |
| `reverse()` in Python and `{% url %}` in templates both resolve names to paths | Two different systems — they both use the same URL name registry |
| `get_object_or_404` returns the model instance or raises Http404 | A query that returns `None` on failure — it raises an exception |
| `ModelAdmin` customizes admin display only | A form for editing data in the admin — it does change how data is displayed, not how it's validated |
| `makemigrations` records schema changes (writes files) | Applies changes to the database — that's `migrate`'s job |

## 🧪 Practical Example

```python
# The complete CRUD flow for a single task — simplified overview

# 1. LIST: GET / → task_list → Task.objects.all() → task_list.html
# 2. CREATE: GET /add/ → task_form.html (empty)
#            POST /add/ → validate → Task.objects.create() → redirect /
# 3. UPDATE: GET /edit/3/ → task_form.html (pre-filled)
#            POST /edit/3/ → validate → task.save() → redirect /
# 4. DELETE: GET /delete/3/ → task_confirm_delete.html
#            POST /delete/3/ → task.delete() → redirect /
# 5. TOGGLE: POST /toggle/3/ → task.completed = !task.completed → redirect /
```

**Explanation:**
- Step 1 (LIST): The view queries all tasks and passes them to the template, which stamps one row per task.
- Step 2 (CREATE): GET shows the empty form; POST validates, creates the record, and redirects back to the list.
- Step 3 (UPDATE): GET pre-fills the form with the existing task's data; POST updates and redirects.
- Step 4 (DELETE): GET shows a confirmation page (never delete on GET); POST performs the deletion.
- Step 5 (TOGGLE): POST flips the completion status without a form — the simplest view in the app.

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. Why does `task_list` pass `tasks` as the context variable but the original code passed `task`?**
A: The template uses `{% for task in tasks %}` — it iterates a collection named `tasks`. Passing `{'task': tasks}` (singular key, QuerySet value) means the template's `tasks` variable is undefined. The variable name in the context dict must match what the template expects. This is a common source of `VariableDoesNotExist` errors.

**Q2. What happens if you reference a URL name that doesn't exist in `{% url %}`?**
A: Django raises `NoReverseMatch` at render time. For example, if the URL pattern is named `task_toggle_complete` but the template says `{% url 'todo:task_toggle' %}`, the page fails to load. Fix: ensure URL names in templates match exactly what's registered in `urls.py`.

**Q3. Why do we need `app_name` and `namespace`?**
A: In a project with multiple apps, URL names can collide (e.g., both `blog` and `todo` might have a `task_list`). The `app_name` in each app's `urls.py` plus the `namespace=` argument in the root `urls.py` creates a two-level naming system (`blog:task_list` vs `todo:task_list`) so every reverse lookup is unambiguous.

**Q4. Why does `CharField` require `max_length`?**
A: `max_length` controls the database column type (`VARCHAR(max_length)` in SQL) and is used for validation. Without it, Django doesn't know how large the field is at the database level. `TextField` doesn't need it because it maps to an unbounded text column (`TEXT` in SQL).

**Q5. What is the difference between `makemigrations` and `migrate`?**
A: `makemigrations` inspects your models and writes migration files (the *plan* — what changed). `migrate` reads those files and executes SQL against the database (the *execution* — creates/updates tables). Running `makemigrations` without `migrate` creates files but changes nothing in the database.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. What are the five views in A030 and which CRUD operation does each handle?

<details><summary>Answer</summary>

`task_list` (Read all), `task_create` (Create), `task_update` (Update), `task_delete` (Delete), `task_toggle_complete` (Toggle completion status).
</details>

2. Why does the template use `tasks` but the view originally passed `task`?

<details><summary>Answer</summary>

The template iterates `{% for task in tasks %}`, expecting a context variable named `tasks`. The view passed `{'task': task}` (singular). The mismatch means `tasks` in the template is undefined. Fixed by renaming both the variable and context key to `tasks`.
</details>

3. What does `app_name = 'todo'` enable?

<details><summary>Answer</summary>

It enables URL namespacing. `{% url 'todo:task_list' %}` resolves to the `task_list` URL within the `todo` app, even if another app also has a `task_list` URL name. Requires `app_name` in the app's `urls.py` and `namespace='todo'` in the root `urls.py`.
</details>

4. What happens when `CharField()` is used without `max_length`?

<details><summary>Answer</summary>

Django's system check raises a `SystemCheckError` during `makemigrations`. The field requires `max_length` to determine the database column type (`VARCHAR`). Fix: `models.CharField(max_length=200)`.
</details>

5. What were the four bugs found in A030?

<details><summary>Answer</summary>

1. `models.py` — `CharField()` missing `max_length`. 2. `views.py` — QuerySet variable `task` vs template `tasks`. 3. `task_list.html` — wrong URL name `task_toggle` (should be `task_toggle_complete`). 4. `task_list.html` — wrong URL name `task_edit` (should be `task_update`).
</details>

6. Why does `task_delete` check `request.method == 'POST'`?

<details><summary>Answer</summary>

The delete view handles two cases at the same URL. GET shows the confirmation page; POST performs the actual deletion. Without the method check, a GET request would delete the task immediately (and search engines/bots could accidentally delete data).
</details>

---

## 📝 Quick Revision

| Concept | Code | Purpose |
|---|---|---|
| Model | `title = models.CharField(max_length=200)` | Define a database field |
| List all | `Task.objects.all().order_by('-created_at')` | Query all rows, newest first |
| Create | `Task.objects.create(title=..., description=...)` | Insert a new row |
| Get or 404 | `get_object_or_404(Task, pk=pk)` | Fetch by PK or return 404 |
| POST check | `if request.method == 'POST':` | Detect form submission |
| Read POST | `request.POST.get('title', '').strip()` | Safely read form data |
| Redirect | `redirect(reverse('todo:task_list'))` | PRG pattern: redirect to named URL |
| Namespace | `app_name = 'todo'` + `namespace='todo'` | Disambiguate URL names across apps |
| Admin register | `@admin.register(Task)` | Register model with ModelAdmin |
| Migration | `makemigrations` → `migrate` | Evolve database schema |

---

## 🧠 Final Mental Model

The TODO app is a **pipeline with five stations**:

```
User ──→ Template (form/table) ──→ View (method check → logic) ──→ Model (CRUD via .objects) ──→ Database (SQLite)
                                    ↑
                              redirect(reverse('todo:...'))
                                    ↓
                              Browser (new URL) ──→ Template (table/form) ──→ ...
```

- **Template** renders the UI, references URLs by name (`{% url 'todo:...' %}`)
- **View** checks method, reads data, validates, calls model, redirects
- **Model** defines the schema; `.objects` provides the query interface
- **URL namespace** (`todo:`) ensures every reverse lookup is unambiguous
- **Admin** provides instant management without custom views

Every station must work for the pipeline to complete. A bug at *any* station breaks the flow visibly — NoReverseMatch, VariableDoesNotExist, SystemCheckError, or a plain 404.

---

## ❓ FAQ

**Q1. Why are there two `todoproject` folders?**
A: The outer `todoproject/` is the project root (contains `manage.py`, the config package, and the app). The inner `todoproject/` (inside it) is the Django config package (contains `settings.py`, `urls.py`, `wsgi.py`). This is a common but confusing naming pattern — the outer folder is the *workspace*, the inner folder is the *configuration*.

**Q2. Can `task_form.html` be used for both Add and Edit?**
A: Yes. For Add, the view passes no `task` variable — the form is empty. For Edit, the view passes `{'task': task}` — the form pre-fills with the task's current data. The template uses `{% if task %}Edit{% else %}Add{% endif %}` to switch the heading.

**Q3. What does `{% csrf_token %}` do in the form?**
A: It renders a hidden `<input>` with a unique CSRF token. Django's `CsrfViewMiddleware` validates this token on every POST request. Without it, Django rejects the POST with 403 Forbidden.

**Q4. Why does `task_toggle_complete` not check for a valid title?**
A: Because it doesn't modify any user-submitted data — it only flips the `completed` boolean. No validation is needed since the value is derived from the existing model instance, not from form input.

**Q5. What would happen if `STATICFILES_DIRS` pointed to a non-existent directory?**
A: Django emits a `staticfiles.W004` warning at startup (not an error). Static files won't be found, but the app still runs. In A030, no `static/` directory exists, so this warning appears — it's harmless for development.

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Model design:** I can define a `Task` model with appropriate field types (`CharField` with `max_length`, `TextField` with `blank=True`, `BooleanField` with `default`, `DateTimeField` with `auto_now_add`) — *§The Task Model*
- [ ] **Checkpoint 2 — CRUD views:** I can write five views covering list, create, update, delete, and toggle — each using `request.method == 'POST'` checks, `redirect()` after POST, and `get_object_or_404()` for single-item lookups — *§The Five CRUD Views*
- [ ] **Checkpoint 3 — URL namespacing:** I can configure `app_name` in an app's `urls.py` and `namespace` in the root `urls.py`, and use `{% url 'namespace:name' %}` and `reverse('namespace:name')` consistently — *§URL Configuration with Namespace*
- [ ] **Checkpoint 4 — Template inheritance:** I can create a `base.html` with `{% block %}`, child templates that `{% extends %}` it, and namepaced template paths (`templates/<app>/page.html`) — *§Templates: Inheritance Chain*
- [ ] **Checkpoint 5 — Admin customization:** I can use `@admin.register(Model)` with a `ModelAdmin` subclass setting `list_display`, `list_filter`, `search_fields`, and `ordering` — *§Admin: ModelAdmin Customization*

---

## 🏋️ Exercises

- **Level 1 — Recall:** Name the five views and their URLs. List the four `ModelAdmin` options used in A030. What does `app_name` do?
- **Level 2 — Understanding:** In A030, why did `task_list` pass `{'task': tasks}` but the template expected `tasks`? What error would you see? Why does `CharField` require `max_length` but `TextField` doesn't?
- **Level 3 — Application:** Add a `priority` field (IntegerField, choices 1–5) to the `Task` model. Run `makemigrations` and `migrate`. Add it to `list_display`, `list_filter`, and `search_fields` in `TaskAdmin`. Add it to `task_form.html` and `task_list.html`. Verify all CRUD operations still work.
- **Level 4 — Interview reasoning:** A user reports "I can see the task list but clicking 'Add Task' gives NoReverseMatch." Walk through the diagnosis: (1) check `app_name` in `todo/urls.py`, (2) check `namespace` in root `urls.py`, (3) check the URL name in `{% url %}` matches `name='...'` in `urlpatterns`, (4) check for typos in the namespace or name.

---

## 🏁 Final Takeaways

1. A complete CRUD app needs: model (schema) → migration (table) → views (logic) → URLs (routing) → templates (UI) → admin (management).
2. Always use `request.method == 'POST'` checks and `redirect()` after successful POST (PRG pattern).
3. URL names must match exactly between `urls.py` and `{% url %}` / `reverse()` — mismatches cause `NoReverseMatch`.
4. Context variable names in views must match template variable names — mismatches cause `VariableDoesNotExist`.
5. `CharField` requires `max_length`; `TextField` does not.
6. `app_name` + `namespace` + `@admin.register()` are the three registration patterns that connect your app to Django's systems.

## 🔄 Next Lecture Connection

No further lecture in this series builds directly on A030 — it is the capstone integration of core Django concepts. For continued learning, explore:
- [Django Forms (model forms)](https://docs.djangoproject.com/en/6.1/topics/forms/modelforms/) — replace manual `request.POST.get()` with `ModelForm` validation
- [Class-Based Views](https://docs.djangoproject.com/en/6.1/topics/class-based-views/) — refactor five function views into a handful of generic CBVs
- [Signals](https://docs.djangoproject.com/en/6.1/topics/signals/) — react to model save/delete events

---

<div class="doc-footer">

**Sources used:** `todoproject/` artifact (Django 6.1.1): `manage.py`, `todoproject/settings.py` (`INSTALLED_APPS` includes `'todo'`, `ROOT_URLCONF = 'todoproject.urls'`, `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']`, `STATICFILES_DIRS = [BASE_DIR / 'static']`), `todoproject/urls.py` (`path('', include(('todo.urls', 'todo'), namespace='todo'))`), `todo/models.py` (Task: title, description, completed, created_at), `todo/views.py` (5 CRUD views), `todo/urls.py` (`app_name='todo'`, 5 routes), `todo/admin.py` (`@admin.register(Task)` with ModelAdmin), `todo/apps.py` (`TodoConfig`), `todo/migrations/0001_initial.py` + `0002_alter_task_title.py`, templates (`base.html` + `task_list.html` + `task_form.html` + `task_confirm_delete.html`). Bugs diagnosed and fixed per AGENTS §12: CharField missing max_length, context variable mismatch, two wrong URL names. No lecture transcript in folder — chapter built from on-disk artifact and official Django documentation.

**Navigation:** ← [A029 — HTML Forms, POST, CSRF Token & Validation](../A029_HTML_Forms_POST_CSRF_Token_&_Validation/README.md) · [Series hub](../../README.md) · A030 is the capstone — no further lecture in this series builds on it directly.

</div>
