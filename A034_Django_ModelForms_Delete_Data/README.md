# 🗑️ A034 — Django ModelForms: Delete Data

`📖 Lecture A034` · `🎓 Track: Core Django` · `📶 Level: Intermediate` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the `myProject18/` artifact — the same Django project evolved across A031–A033 — extended here with a `student_delete` view that implements the confirm-then-delete pattern. The `Student` model (name, age, city, email) and `StudentForm` ModelForm are **unchanged**; this lecture adds only a view, a URL, and a confirmation template. All file references below are quoted verbatim from the on-disk artifact.
>
> This lecture builds directly on [A033 — Django ModelForms Update (Edit) Data](../A033_Django_ModelForms_Update_(Edit)_Data/README.md).

---

## 🧭 What You Will Learn

- [ ] How Django's delete pattern differs from create and update — no `ModelForm` needed
- [ ] Why deletion requires a **confirmation step** (GET shows confirm page, POST executes delete)
- [ ] How to fetch a row safely with `get_object_or_404` before deleting
- [ ] How `instance.delete()` removes a row from the database
- [ ] How to wire a delete route carrying a **primary key in the URL** (`delete/<int:pk>/`)
- [ ] How to add a Delete link to each row of a list page using `{% url %}` with an argument
- [ ] How the **Post/Redirect/Get pattern** applies to delete operations

## 🎯 Why This Lecture Matters

A031–A033 covered Create, Read, and Update. Delete is the final letter of CRUD. Unlike the other three, delete needs **no form** — there is nothing to fill in. But it still needs a guard: a single accidental click on a delete link must not destroy data. The solution is a **confirm page**: a GET request shows a "Are you sure?" page, and only a POST request actually deletes. This two-step pattern is so universal that Django's own `DeleteView` class-based view is built on exactly the same GET/POST split. Understanding the function-based version here prepares you to recognise and use `DeleteView` later.

## ✅ Prerequisites

- [ ] `Student` model + `StudentForm` defined and migrated (A031)
- [ ] `get_object_or_404`, pk-carrying URL patterns, `<int:pk>` converter (A009, A033)
- [ ] `render()`, `redirect()`, `request.method == 'POST'` (A029–A031)
- [ ] List view with `{% for %}` and `{% url %}` links per row (A032–A033)

## 🧠 The Delete Pattern in Django

### The Architecture

```
myProject18/                    ← project root (unchanged)
├── manage.py
├── myProject18/
│   ├── settings.py             ← unchanged
│   └── urls.py                 ← unchanged: includes student.urls
└── student/
    ├── models.py               ← Student — unchanged
    ├── forms.py                ← StudentForm — unchanged
    ├── views.py                ← ➕ student_delete view
    ├── urls.py                 ← ➕ delete/<int:pk>/ route
    └── templates/
        ├── student_form.html      ← unchanged (create/edit)
        ├── student_list.html      ← ➕ Delete link per row
        ├── student_detail.html    ← unchanged
        ├── student_success.html   ← unchanged
        └── student_confirm_delete.html  ← ➕ new confirmation page
```

**Two files the diff does not touch are the most important ones:** `models.py` and `forms.py`. Deleting a record needs no new model field and no form class. No migration is required. Like A033's edit feature, this is pure wiring.

The model being deleted (unchanged from A031):

```python
# student/models.py — verbatim, unchanged
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name
```

### How Delete Differs from Create / Update

| Step | Create (A031) | Update (A033) | Delete (A034) |
|---|---|---|---|
| Form needed? | ✅ `StudentForm` | ✅ `StudentForm(instance=)` | ❌ No form |
| GET shows | Blank form | Pre-filled form | Confirm page |
| POST does | `form.save()` → INSERT | `form.save()` → UPDATE | `student.delete()` → DELETE |
| After POST | `redirect()` | `redirect()` | `redirect()` |
| New migration? | ✅ (A031 only) | ❌ | ❌ |

The delete view is the **simplest** CRUD view: fetch the row, show confirmation, delete on POST, redirect.

### The View

```python
# student/views.py — the new student_delete view
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})
```

**Explanation:**
- Line 1: `from django.shortcuts import render, get_object_or_404, redirect` — all three utilities are needed: `get_object_or_404` to fetch safely, `render` for the confirm page (GET), `redirect` after deletion (POST).
- Line 4: `def student_delete(request, pk):` — `pk` comes from the URL pattern `delete/<int:pk>/`, exactly as `student_edit(request, pk)` received it in A033.
- Line 5: `student = get_object_or_404(Student, pk=pk)` — fetch the row first. If the `pk` doesn't exist (already deleted, wrong URL), the user gets a 404 — not a 500 crash. **Identical first line to `student_edit`** (📌 — fetching safely is a habit across all pk-based views).
- Lines 6-8: POST branch — **this is the actual delete**:
  - `student.delete()` — calls Django's ORM `delete()` method on the instance, executing `DELETE FROM student_student WHERE id = pk`.
  - `return redirect('student_list')` — PRG pattern: after deletion, redirect to the list so refresh doesn't attempt a second delete on a now-missing row.
- Line 9: Implicit GET branch (no `else:` needed because POST returns early) — renders the confirmation template, passing the `student` object so the template can display the student's name in the "Are you sure?" message.

### How `instance.delete()` Works

```
student = get_object_or_404(Student, pk=3)
                    ↓
           SELECT … WHERE id = 3
                    ↓
student.delete()
                    ↓
           DELETE FROM student_student WHERE id = 3
```

- `instance.delete()` is **not** `form.save()` — there is no form involved. It is called directly on the model instance.
- It returns a tuple: `(1, {'student.Student': 1})` — the count of deleted rows and a breakdown by model. For a simple delete, this is rarely used but useful for cascade debugging.
- If the `Student` model had related objects with `on_delete=CASCADE`, those would also be deleted. Always check related models before deleting in production.

### The URL

```python
# student/urls.py — full file with delete route added
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.student_create, name='student_create'),
    path('', views.student_list, name='student_list'),
    path('details/<int:pk>/', views.student_detail, name='student_detail'),
    path('edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
]
```

**Explanation:**
- `delete/<int:pk>/` follows the same pattern as `edit/<int:pk>/` directly above it — a pk-carrying route that the browser cannot guess or enumerate safely (a user has to know the id). Compare all three pk routes: `details/`, `edit/`, `delete/` — three verbs, one identity mechanism.
- `name='student_delete'` — the URL name used in `{% url 'student_delete' s.id %}` in the list template.

### Templates

#### Confirmation Page

```html
<!-- student/templates/student_confirm_delete.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Delete Student</title>
</head>
<body>
    <h2>Delete Student</h2>
    <p>Are you sure you want to delete <strong>{{ student.name }}</strong>?</p>
    <form method="POST">
        {% csrf_token %}
        <button type="submit">Yes, Delete</button>
        <a href="{% url 'student_list' %}">Cancel</a>
    </form>
</body>
</html>
```

**Explanation:**
- `{{ student.name }}` — displays the student's name so the user knows exactly what they are about to delete. The `student` context variable comes from `render(request, 'student_confirm_delete.html', {'student': student})` in the view.
- `<form method="POST">` — the actual delete is a POST request. A GET request to this URL only shows the page; it never deletes. This is the safety gate.
- `{% csrf_token %}` — required for all POST forms in Django. A delete form without CSRF protection is vulnerable to cross-site request forgery (an attacker could trick a logged-in user's browser into sending a delete request).
- `<button type="submit">Yes, Delete</button>` — submits the POST to `delete/<pk>/`.
- `<a href="{% url 'student_list' %}">Cancel</a>` — a plain link (GET, no POST). Clicking Cancel navigates away without triggering the delete. The student record is untouched.
- **No `{% extends %}`** — standalone page, consistent with the A031–A033 convention for this project (📌 — departs from the A012–A030 base.html convention).

#### List Template — Delete Link Per Row

```html
<!-- student/templates/student_list.html — the Delete link column (new) -->
<a href="{% url 'student_detail' s.id %}">{{ s.name }} - {{ s.email }}</a> |
<a href="{% url 'student_edit' s.id %}">Edit</a> |
<a href="{% url 'student_delete' s.id %}">Delete</a>
```

Each row now has **three doors**: view, edit, and delete. `{% url 'student_delete' s.id %}` reverses the `delete/<int:pk>/` pattern with that row's id — no hardcoded URLs.

> [!WARNING]
> **Never make a delete link a plain `<a>` that performs the delete directly** (i.e., a GET that deletes). Search crawlers, browser prefetchers, and link previewers all issue GET requests automatically. A plain delete-on-GET link would let a crawler silently wipe your table. Always require a POST for destructive actions.

### The Delete Round Trip (GET → Confirm → POST → Delete → Redirect)

```
LIST page
  │  user clicks Delete on row #3  → GET /delete/3/
  ▼
CONFIRM page (/delete/3/)
  │  get_object_or_404(Student, pk=3) → row #3
  │  render student_confirm_delete.html with student=row
  │
  ├─ user clicks Cancel → GET /  (student_list, row intact)
  │
  └─ user clicks "Yes, Delete" → POST /delete/3/
       │  get_object_or_404(Student, pk=3) → row #3
       │  student.delete() → DELETE FROM student_student WHERE id=3
       └─ redirect('student_list') → 302 → GET /
```

Two things to note:

1. **The row is fetched twice** — once per request, just like the edit view. HTTP is stateless; the POST request has no memory of the GET. Each request independently fetches the row, so each is safe in isolation.
2. **The 302 redirect after delete** — if the user refreshes after deletion, they refresh a harmless GET to the list, not a re-POST that would try to delete an already-deleted row (which would 404 anyway, but the redirect is cleaner).

### What SQL Actually Runs

| Step | ORM call | SQL |
|---|---|---|
| Fetch (GET + POST) | `get_object_or_404(Student, pk=3)` | `SELECT … FROM student_student WHERE id = 3` |
| Delete | `student.delete()` | `DELETE FROM student_student WHERE id = 3` |
| Create (A031) | `form.save()` (no instance) | `INSERT INTO student_student (…) VALUES (…)` |
| Update (A033) | `form.save()` (with instance) | `UPDATE student_student SET … WHERE id = 3` |

All four CRUD operations on a single table — one model, four ORM methods.

---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **`instance.delete()`** | Remove this record | ORM method that issues `DELETE FROM … WHERE pk = …` and cascades if configured | The eraser — one call, one (or more) rows gone |
| **Confirm page** | "Are you sure?" | A GET-rendered template with a POST form; the GET shows, the POST acts | See then decide |
| **`get_object_or_404`** | Fetch or fail cleanly | Shortcut that calls `Model.objects.get()` and raises `Http404` if not found | Safe fetch — 404 not 500 |
| **POST-only delete** | Delete via form, not link | The pattern of requiring a POST request to perform destructive actions | A form is a guard |
| **`{% csrf_token %}`** | Anti-forgery token | A hidden form field Django validates to ensure the POST originated from your own site | The bouncer on the POST door |
| **PRG (Post/Redirect/Get)** | Refresh-safe saving | After any successful POST (create, update, delete), respond with a 302 redirect so refresh issues a harmless GET | Save → send away → show |
| **Cascade delete** | Related rows deleted too | When `on_delete=CASCADE` is set on a ForeignKey, deleting the parent also deletes all related child rows | Pulling one thread unravels others |

## 💡 Real-World Analogy

**Deleting a student record is like shredding a paper form at a school office.** The clerk doesn't shred on the spot the moment you ask — they first pull the form from the drawer (`get_object_or_404`), show it to you and say "You're about to destroy Asha's enrolment record — are you sure?" (the confirm page). Only after you sign the authorisation slip (POST) do they run it through the shredder (`student.delete()`). The Cancel button is the clerk putting the form back. `{% csrf_token %}` is the authorisation slip itself — without it, someone could forge your signature from outside the office.

## ❌ Common Beginner Mistakes

1. **Deleting on GET instead of POST** — wiring `path('delete/<int:pk>/', ...)` to a view that deletes immediately, without a confirm page. Any link prefetcher or bot that crawls your site will silently delete records. Fix: always require a POST for destructive operations.

2. **Forgetting `{% csrf_token %}` in the confirm form** — the POST is rejected with a 403 Forbidden. The user sees an error and thinks delete is broken. Fix: add `{% csrf_token %}` inside every `<form method="POST">`.

3. **Rendering instead of redirecting after delete** — if the view `render`s a success page instead of `redirect`-ing, refreshing that page issues a new POST to `delete/<pk>/`. Since the row is already gone, Django raises a 404. Fix: always `redirect()` after a successful delete.

4. **Not passing the `student` object to the confirm template** — the template can't show "Are you sure you want to delete *Asha*?" without it. Fix: include `{'student': student}` in the `render()` context.

5. **Using `Student.objects.filter(pk=pk).delete()` without a confirm step** — this works technically but bypasses the confirmation UI entirely. Fine for scripts; never acceptable in a user-facing view.

6. **Forgetting to add the Delete link to the list template** — the view and URL are wired but the user has no way to reach the confirm page. Fix: add `<a href="{% url 'student_delete' s.id %}">Delete</a>` inside the `{% for %}` loop.

## 🧠 Common Misconceptions

| ✅ Delete IS … | ❌ It is NOT … |
|---|---|
| Called via `instance.delete()` on the fetched row | Called via `form.delete()` — no such method |
| A two-step GET/POST (confirm then act) | A single-step GET that destroys data immediately |
| A view that needs no `ModelForm` | Something that requires a form class |
| Reversed by URL name: `{% url 'student_delete' s.id %}` | A hardcoded href like `/delete/3/` |
| Always followed by `redirect()` (PRG) | Followed by `render('success.html')` |
| Safe from CSRF via `{% csrf_token %}` | Safe without the token |

## 🧪 Practical Example

```python
# student/views.py — the complete delete flow
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)   # 1. Fetch safely
    if request.method == 'POST':                   # 2. Confirm received
        student.delete()                           # 3. Delete from DB
        return redirect('student_list')            # 4. Redirect (PRG)
    return render(                                 # 5. Show confirm page
        request,
        'student_confirm_delete.html',
        {'student': student}
    )
```

**Explanation:**
- Step 1 (Fetch): `get_object_or_404` retrieves the row or returns 404 — no crash on bad ids.
- Step 2 (Guard): `if request.method == 'POST'` — delete only executes when the user deliberately submits the confirm form. A GET request (link click, prefetch, crawler) never reaches the delete line.
- Step 3 (Delete): `student.delete()` issues `DELETE FROM student_student WHERE id = pk`. One method call, one SQL statement.
- Step 4 (Redirect): `redirect('student_list')` issues a 302. The browser follows with a fresh GET, so refresh doesn't try to re-delete.
- Step 5 (Confirm page): For GET requests, renders the confirm template with the student's details so the user can review before committing.

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. Why does the delete view have a GET branch at all?**
A: To show a confirmation page. If deletion happened on GET, any link click — including from a browser prefetcher or search crawler — would silently destroy data. The GET branch is the safety gate; the POST branch is the actual action.

**Q2. What ORM method deletes a row, and what SQL does it issue?**
A: `instance.delete()` — issues `DELETE FROM <table> WHERE id = <pk>`. It also cascades if related models are configured with `on_delete=CASCADE`.

**Q3. Does delete need a `ModelForm`?**
A: No. There is nothing to validate or fill in. The view fetches the row and deletes it. A form would add complexity without benefit.

**Q4. Why redirect after deletion instead of rendering a success page?**
A: The PRG pattern. After `redirect()`, a browser refresh issues a harmless GET to the list. Without the redirect, refreshing would re-POST the delete request — which fails with a 404 (row is gone) and confuses the user.

**Q5. What happens if `{% csrf_token %}` is missing from the confirm form?**
A: Django rejects the POST with 403 Forbidden. The delete never executes. Always include `{% csrf_token %}` in every POST form.

**Q6. How do you make a Delete link for each row in a list template?**
A: `<a href="{% url 'student_delete' s.id %}">Delete</a>` inside the `{% for s in students %}` loop. The `{% url %}` tag reverses the `delete/<int:pk>/` URL pattern using the row's id.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. What are the two steps in the delete pattern?

<details><summary>Answer</summary>

Step 1 — GET: fetch the row with `get_object_or_404`, render the confirm page. Step 2 — POST: fetch the row again, call `instance.delete()`, redirect to the list.
</details>

2. Why must deletion be triggered by a POST, not a GET?

<details><summary>Answer</summary>

GET requests can be issued automatically by browsers (prefetch, link preview) and crawlers. A GET-triggered delete would let bots silently wipe records. POST requires deliberate form submission.
</details>

3. What ORM method removes a row, and what is the equivalent SQL?

<details><summary>Answer</summary>

`instance.delete()` — equivalent to `DELETE FROM student_student WHERE id = <pk>`.
</details>

4. What does the confirm template need from the view's context?

<details><summary>Answer</summary>

The `student` object — so the template can display the student's name in the "Are you sure?" message and include `{% csrf_token %}` in the POST form.
</details>

5. What happens if you refresh the page after a successful delete?

<details><summary>Answer</summary>

If the view `redirect`s (PRG), refresh issues a harmless GET to the list. If the view `render`s a success page instead, refresh re-POSTs the delete request, resulting in a 404 (row is already gone).
</details>

6. What is the difference between `instance.delete()` and `form.save()`?

<details><summary>Answer</summary>

`form.save()` creates or updates a model instance (INSERT or UPDATE). `instance.delete()` removes the row (DELETE). Delete has no form; it operates directly on the fetched instance.
</details>

---

## 📝 Quick Revision

| Concept | Code | Purpose |
|---|---|---|
| Fetch safely | `get_object_or_404(Student, pk=pk)` | 404 not 500 on bad id |
| Guard | `if request.method == 'POST':` | Only delete on deliberate POST |
| Delete | `student.delete()` | `DELETE FROM … WHERE id = pk` |
| Redirect | `return redirect('student_list')` | PRG — refresh-safe |
| Confirm page | `render(request, 'student_confirm_delete.html', {'student': student})` | Show before act |
| CSRF | `{% csrf_token %}` | Anti-forgery on POST form |
| Delete link | `{% url 'student_delete' s.id %}` | One link per row, no hardcoding |
| Cancel link | `<a href="{% url 'student_list' %}">Cancel</a>` | Exit without deleting |

---

## 🧠 Final Mental Model

The complete CRUD cycle on `Student`:

```
CREATE (/add/)          → StudentForm() → form.save()       → INSERT
READ   (/, /details/)   → Student.objects.all() / .get()    → SELECT
UPDATE (/edit/<pk>/)    → StudentForm(instance=row)          → UPDATE
DELETE (/delete/<pk>/)  → student.delete()                  → DELETE
```

The delete flow specifically:

```
User ─→ List page ─→ clicks Delete link (GET /delete/3/)
                           │
                    student_delete view (GET branch)
                           │  get_object_or_404
                           │  render confirm page
                           ▼
                    Confirm page — "Delete Asha?"
                           │
          ┌────────────────┴────────────────┐
          │ Cancel (GET /)                  │ Yes, Delete (POST /delete/3/)
          ▼                                 ▼
       List page                    student_delete (POST branch)
       (unchanged)                        │  get_object_or_404
                                          │  student.delete()
                                          │  redirect('student_list')
                                          ▼
                                       List page (row gone)
```

- **GET** shows, **POST** acts — always.
- `get_object_or_404` guards both branches independently.
- `redirect()` after POST closes the PRG loop.
- No `ModelForm`, no `cleaned_data`, no `save()` — delete is pure instance-level ORM.

---

## ❓ FAQ

**Q1. Can I delete without a confirm page for non-sensitive data?**
A: You can, but you should not. Even for low-stakes data, the confirm page is a standard UX convention. Users click Delete by accident; "Are you sure?" saves support requests. Always include it.

**Q2. What happens to related records when a student is deleted?**
A: It depends on `on_delete` in the ForeignKey definition. `CASCADE` deletes related rows automatically. `PROTECT` raises a `ProtectedError` and blocks the delete. `SET_NULL` nullifies the foreign key. The `Student` model as defined has no inbound ForeignKeys — deletion is clean.

**Q3. How does Django's `DeleteView` (CBV) relate to this?**
A: `DeleteView` implements exactly the same GET/POST split — GET renders a confirm template (defaults to `<model>_confirm_delete.html`), POST calls `object.delete()` and redirects to `success_url`. Understanding this function-based version makes `DeleteView` trivial to read.

**Q4. Can one URL name be used for both the confirm page and the delete action?**
A: Yes — `delete/<int:pk>/` handles both GET (confirm) and POST (delete). One URL, two request methods, two behaviours. This is standard Django/HTTP design: the URL identifies the resource; the method identifies the action.

**Q5. Should I add an `app_name` to `urls.py`?**
A: Yes — adding `app_name = 'student'` namespaces all URL names, so `{% url 'student:student_delete' s.id %}` won't collide with a `student_delete` in another app. A031 flagged this as a best-practice note (📌); it applies here equally.

**Q6. What is the return value of `student.delete()`?**
A: A tuple `(n, {model_label: n})` where `n` is the number of rows deleted. For a simple student without cascades: `(1, {'student.Student': 1})`. Rarely used in views but useful for logging.

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Pattern:** I can describe the two-step delete pattern (GET → confirm, POST → delete → redirect) and explain why GET must never delete — *§The View*
- [ ] **Checkpoint 2 — ORM:** I can state that `instance.delete()` issues a `DELETE` SQL statement and requires no `ModelForm` — *§How `instance.delete()` Works*
- [ ] **Checkpoint 3 — CSRF:** I can explain why `{% csrf_token %}` is required in the confirm form and what error appears without it — *§Templates*
- [ ] **Checkpoint 4 — PRG:** I can explain why `redirect()` is used after deletion and what goes wrong if `render()` is used instead — *§Common Beginner Mistakes*
- [ ] **Checkpoint 5 — Wiring:** I can write the complete delete URL, view, and confirm template from memory — *§The URL / The View / Templates*

---

## 🏋️ Exercises

- **Level 1 — Recall:** Name the four CRUD operations and the ORM call used for each in this project.
- **Level 2 — Understanding:** Why is the confirm page GET and the actual delete POST? What would break if you swapped them? Why does the view call `get_object_or_404` twice (once per request)?
- **Level 3 — Application:** Add an `app_name = 'student'` namespace to `urls.py` and update all `{% url %}` tags in every template to use `student:student_delete`, `student:student_edit`, etc. Add a "Delete" column to `student_detail.html` as well.
- **Level 4 — Interview reasoning:** A teammate writes a delete view where the link `<a href="/delete/{{ s.id }}/">Delete</a>` performs the deletion on GET with no confirm page. List every problem with this approach and explain how to fix each one.

---

## 🏁 Final Takeaways

1. Delete requires **no `ModelForm`** — call `instance.delete()` directly on the fetched row.
2. Always use a **two-step confirm pattern**: GET shows the confirm page, POST performs the delete.
3. Never delete on a GET request — crawlers, prefetchers, and accidental clicks will destroy data.
4. Always include `{% csrf_token %}` in the confirm form's POST request.
5. Always `redirect()` after a successful delete — the PRG pattern makes the result refresh-safe.
6. `get_object_or_404` is the correct fetch method in all pk-based views — 404, not 500.
7. No model change means **no migration** — delete is pure view, URL, and template wiring.

## 🔄 Series Connection

A034 closes the CRUD loop on the `Student` model:

| Lecture | CRUD | ORM call | Form? |
|---|---|---|---|
| A031 | **C**reate | `form.save()` → INSERT | ✅ `StudentForm` |
| A032 | **R**ead | `.all()` / `.get()` → SELECT | ❌ |
| A033 | **U**pdate | `form.save(instance=)` → UPDATE | ✅ `StudentForm` |
| **A034** | **D**elete | `instance.delete()` → DELETE | ❌ |

The progression after CRUD:

- [ ] **A035 — Debug Info Success Warning & Error** — using Django's messages framework for user feedback (*next lecture*)
- [ ] Authentication & permissions (A036)
- [ ] Class-based views (`CreateView`, `ListView`, `UpdateView`, `DeleteView`) — the CBV equivalents of A031–A034

---

<div class="doc-footer">

**Sources used:** `myProject18/` artifact (Django 6.1.1): `student/models.py` (Student: name CharField, age IntegerField, city CharField, email EmailField), `student/forms.py` (StudentForm ModelForm — unchanged), `student/views.py` (student_delete: get_object_or_404 → confirm/delete → redirect), `student/urls.py` (delete/<int:pk>/ route), `student/templates/student_confirm_delete.html` (confirm page with POST form and Cancel link), `student/templates/student_list.html` (Delete link per row). No lecture transcript in folder — chapter built from on-disk artifact, A031–A033 README conventions, and official Django documentation. Bugs and best-practice notes flagged per AGENTS §12: no `app_name` namespace in `urls.py`, no `{% extends %}` in confirm template, hardcoded Cancel `<a>` should use `{% url %}`.

**Navigation:** ← [A033 — Django ModelForms Update (Edit) Data](../A033_Django_ModelForms_Update_(Edit)_Data/README.md) · [Series hub](../../README.md) · [A035 — Debug Info Success Warning & Error →](../A035_Debug_Info_Success_Warning_&_Error/README.md)

</div>
