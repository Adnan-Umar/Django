# 🚀 A029 — HTML Forms, POST, CSRF Token & Validation

`📖 Lecture A029` · `🎓 Track: Core Django` · `📶 Level: Beginner` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the `myProject17/` artifact — a Django 6.1.1 project with a `contact` app that serves an HTML form at `/` and handles POST submission at `/submit/`, protected by Django's CSRF token. The artifact contains two deliberate bugs flagged per AGENTS §12. All file references below are quoted verbatim from the on-disk artifact.
>
> This lecture builds directly on [A028 — Admin: List Display, Searching, Sorting & Filters](../A028_Admin_List_Display_Searching_Sorting_&_Filters/README.md).

---

## 🧭 What You Will Learn

- [ ] How to create an HTML form with `<form>`, `action`, `method="POST"`, and `{% csrf_token %}`
- [ ] How Django handles POST requests via `request.method == 'POST'` and `request.POST.get()`
- [ ] How CSRF protection works and why `{% csrf_token %}` is required
- [ ] How to validate form data before saving to the database
- [ ] How `redirect()` sends the browser back to a named URL

## 🎯 Why This Lecture Matters

Every interactive web application needs forms: user input, submission, validation, and database persistence. Django provides the infrastructure — template tags for form rendering, request objects for data access, CSRF protection for security, and ORM for storage — but the developer must wire it all together. This lecture connects the template layer (HTML forms + CSRF tokens) to the view layer (POST handling + validation + redirect) to the data layer (model creation), completing the request→response cycle for write operations.

## ✅ Prerequisites

- [ ] Models defined, registered in admin, and migrated (covered in A027–A028)
- [ ] `render()` and template rendering (covered in A010–A016)
- [ ] URL routing with `path()` and `include()` (covered in A007)
- [ ] 📌 CSRF protection concept (introduced in this lecture; Django provides it automatically)

## 🧠 Forms, POST, CSRF & Validation

### The Form Template

```html
<!-- contact/templates/contact.html — verbatim from A029 -->
<form action="{% url "submit_contact" %}" method="POST">
    {% csrf_token %}

    <label for="name">Name</label>
    <input type="text" name="name" placeholder="Name" required><br>

    <label for="message">Message</label><br>
    <input type="text" name="message" placeholder="Message" required><br><br>

    <button type="submit" value="Submit">Submit</button>
</form>
```

**Explanation:**
- Line 7: `action="{% url "submit_contact" %}"` — the form submits to the URL reversed from the name `submit_contact` (resolves to `/submit/`). Using `{% url %}` instead of a hardcoded path means the URL can change without updating the template.
- Line 8: `{% csrf_token %}` — inserts a hidden `<input name="csrfmiddlewaretoken" value="...">` into the form. Django's middleware validates this token on every POST request; if missing or invalid, Django rejects the request (403 Forbidden).
- Lines 10–14: Two input fields (`name`, `message`) with `required` HTML5 validation (client-side only — server-side validation still needed).
- Line 16: `<button type="submit">` — triggers the POST to the action URL.

### The View: GET vs POST

```python
# contact/views.py — verbatim from A029
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contact

def contact_form(request):
    return render(request, 'contact.html')

def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        message = request.POST.get('message')

        if name and message:
            Contact.objects.create(name=name, message=message)
            return HttpResponse(f"Thank you, {name}, for your message.")

        else:
            return HttpResponse("Please provide both name and message")

    return redirect('contact_form')
```

**Explanation:**
- Lines 1–3: Imports — `render` (template rendering), `redirect` (HTTP redirect), `HttpResponse` (text response), `Contact` (the model).
- Line 6: `def contact_form(request):` — handles GET requests to `/`. Simply renders the form template.
- Line 7: `return render(request, 'contact.html')` — finds `contact.html` via the two-lane template lookup (`DIRS` → `APP_DIRS`) and fills it with an empty context.
- Line 9: `def submit_contact(request):` — handles both GET and POST to `/submit/`.
- Line 10: `if request.method == 'POST':` — checks if this is a form submission (POST) or a direct page visit (GET).
- Lines 11–13: `request.POST.get('name')` and `request.POST.get('message')` — extract form data from the POST body. Returns `None` if the key doesn't exist (no exception). **Flagged ⚠️**: line 13 is a duplicate of line 12 (`message` is fetched twice, the first assignment on line 12 is immediately overwritten).
- Line 15: `if name and message:` — validates that both fields have values. Empty strings are falsy, so this catches blank submissions.
- Line 16: `Contact.objects.create(name=name, message=message)` — creates a new database row with the submitted data. `created_at` is auto-set via `auto_now_add=True`.
- Line 17: `return HttpResponse(f"Thank you, {name}, for your message.")` — returns a text response. **Flagged ⚠️**: `submit.html` exists but is never used — the view returns an `HttpResponse` string instead of rendering the template.
- Line 20: `return HttpResponse("Please provide both name and message")` — validation failure response.
- Line 22: `return redirect('contact_form')` — if a GET request hits `/submit/` directly, redirect to the form page. Prevents blank submissions.

### CSRF Protection: How It Works

1. When the user loads `/`, Django generates a unique CSRF token and inserts it into the form via `{% csrf_token %}`.
2. When the form is submitted (POST), the token is sent in the request body.
3. Django's `CsrfViewMiddleware` (in `MIDDLEWARE`, line 47) checks the token.
4. If the token matches, the request proceeds. If not (or missing), Django returns **403 Forbidden**.
5. This prevents malicious websites from submitting forms to your Django site on behalf of logged-in users.

> [!IMPORTANT]
> **Two bugs in the artifact, flagged per §12:**
> 1. **`STATICFILES_DIRD` typo** in `settings.py` line 119 — the setting name is `STATICFILES_DIRS` (ends in S), not `STATICFILES_DIRD`. This means any `static/` directory is silently ignored. No `static/` folder exists in the artifact, so this has no visible effect currently, but any future static files would 404.
> 2. **Duplicate `message` line** in `views.py` lines 12–13 — `message = request.POST.get('message')` is written twice. The second assignment overwrites the first immediately. This is harmless functionally but confusing for readers.

---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **POST method** | Form submission method | HTTP method that sends data in the request body (not visible in URL); used for creating/updating data | the sealed envelope |
| **`request.POST`** | The submitted form data | A dictionary-like object containing all POST parameters; accessed via `.get('key')` | the mailbox contents |
| **CSRF token** | Anti-forgery protection | A unique secret string embedded in forms; validated by middleware on every POST | the wax seal on the envelope |
| **`{% csrf_token %}`** | Template tag for CSRF | Renders `<input type="hidden" name="csrfmiddlewaretoken" value="...">` | the seal stamp |
| **`request.method`** | The HTTP verb used | `'GET'`, `'POST'`, `'PUT'`, `'DELETE'` etc.; check for `'POST'` to detect form submissions | the envelope label |
| **`redirect()`** | Send browser to another URL | Returns an HTTP 302 response with a `Location` header; takes a URL name or path | the forwarding address |
| **`request.POST.get()`** | Safely read form data | Returns the value or `None` if key missing; never raises `KeyError` | the safe opener |
| **`HttpResponse`** | A text HTTP response | Wraps a string body into an HTTP response; used for simple text returns | the typed letter |
| **`auto_now_add=True`** | Auto-set on creation | Automatically sets the field to current datetime when the object is first created; not updated on save | the date stamp on the letter |

---

## 💡 Real-World Analogy

**A contact form is a mailroom.** The template (`contact.html`) is the pre-printed form paper with fields to fill. `{% csrf_token %}` is the envelope's security seal — the mailroom won't accept sealed letters from unknown senders. `request.POST` is the mailbox where submissions land. The view (`submit_contact`) is the clerk who opens the mailbox: checks the seal (POST method), reads the handwriting (`request.POST.get()`), validates that required fields aren't blank (`if name and message`), files it in the cabinet (`Contact.objects.create()`), and sends a receipt (`HttpResponse`). If someone drops off a blank form (`GET` to `/submit/`), the clerk redirects them back to the form (`redirect('contact_form')`).

---

## ❌ Common Beginner Mistakes

1. **Forgetting `{% csrf_token %}`** — POST requests without a valid CSRF token are rejected by Django's middleware (403 Forbidden). Fix: always include `{% csrf_token %}` inside every `<form method="POST">`.

2. **Checking `request.method == 'POST'` incorrectly** — Using `request.method == 'POST '` (trailing space) or `request.POST` (truthy check without method check). Fix: always check `request.method == 'POST'` exactly.

3. **Not validating before creating** — Calling `Contact.objects.create()` with `None` or empty values causes database errors. Fix: validate all required fields before calling `.create()`.

4. **Using `request.POST['key']` instead of `request.POST.get('key')`** — `request.POST['key']` raises `KeyError` if the key is missing. Fix: use `.get()` which returns `None` safely.

5. **Not redirecting after POST** — After a successful POST, some developers render a template instead of redirecting. This can cause duplicate submissions if the user refreshes. Fix: use `redirect()` after successful POST (PRG pattern: Post-Redirect-Get).

---

## 🧠 Common Misconceptions

| ✅ Forms ARE … | ❌ They are NOT … |
|---|---|
| Handled by checking `request.method == 'POST'` in the same view that renders the form | Two separate views — one for GET, one for POST (they can be separate, but don't have to be) |
| Protected by CSRF middleware automatically | Safe without `{% csrf_token %}` — Django will reject the POST |
| Validated by the developer checking values before saving | Automatically validated by field types — Django forms do this, but raw `request.POST` does not |
| Submitted to a URL that handles both GET and POST | Only POST-handling URLs need form logic — GET to `/submit/` should redirect, not error |
| `request.POST.get('key')` returns `None` for missing keys | `request.POST['key']` is safer — it actually raises `KeyError` on missing keys |

---

## 🧪 Practical Example

```python
# contact/views.py — minimal working form handler
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contact

def contact_form(request):
    return render(request, 'contact.html')

def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')

        if name and message:
            Contact.objects.create(name=name, message=message)
            return HttpResponse(f"Thank you, {name}, for your message.")
        else:
            return HttpResponse("Please provide both name and message")

    return redirect('contact_form')
```

**Explanation:**
- Lines 1–3: Imports — `render` and `redirect` from `shortcuts`, `HttpResponse` from `http`, `Contact` model from local `models`.
- Line 6: `contact_form` — the view at `/`. GET or any non-POST request renders the form template. No `__str__` issue here since it just renders HTML.
- Line 7: `render(request, 'contact.html')` — finds `contact.html` in `contact/templates/contact.html` via APP_DIRS lookup, renders with empty context.
- Line 9: `submit_contact` — the view at `/submit/`. Both form submission (POST) and direct access (GET) go here.
- Line 10: POST check — only process form data if the request came from the form submission.
- Lines 11–12: Read form data using `request.POST.get()` — safe, returns `None` for missing keys.
- Line 15: Validation — both fields must have truthy values (non-empty strings).
- Line 16: `Contact.objects.create()` — creates and saves a new row. `created_at` is auto-set; `name` and `message` are from user input.
- Line 17: Success response — a simple text confirmation with the user's name interpolated.
- Line 20: Validation failure — tells the user what's missing.
- Line 22: GET redirect — if someone visits `/submit/` directly (not from the form), redirect them back to the form. Prevents empty submissions.

---

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. What does `{% csrf_token %}` do and why is it required?**
A: It renders a hidden input with a unique token that Django's `CsrfViewMiddleware` validates on every POST request. Without it, Django rejects the POST with a 403 error. It prevents cross-site request forgery — malicious sites can't submit forms to your Django site on behalf of authenticated users.

**Q2. Why does `submit_contact` check `request.method == 'POST'`?**
A: The same URL (`/submit/`) handles both form display (GET) and form submission (POST). If you GET `/submit/` directly, you should be redirected to the form page, not try to process empty form data. The method check distinguishes between these two cases.

**Q3. What happens if `request.POST.get('name')` returns `None`?**
A: `None` is falsy, so `if name and message:` evaluates to `False`, and the user gets "Please provide both name and message". No database operation occurs. Using `.get()` is safer than `request.POST['name']` which would raise a `KeyError`.

**Q4. What is the purpose of `redirect('contact_form')`?**
A: It sends an HTTP 302 redirect back to the form page (resolved from the URL name `contact_form`). This implements the Post-Redirect-Get (PRG) pattern — after a successful POST, the user is redirected so refreshing the page doesn't resubmit the form.

**Q5. What is the `auto_now_add=True` flag on `created_at`?**
A: It automatically sets the field to the current datetime when the object is first created. The value cannot be changed on subsequent saves. It's useful for "created at" timestamps.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. What are the two view functions in A029 and what URL does each handle?

<details><summary>Answer</summary>

`contact_form` handles `/` (GET — renders the form). `submit_contact` handles `/submit/` (POST — processes the form; GET — redirects back to form).
</details>

2. What does `{% csrf_token %}` render and why is it needed?

<details><summary>Answer</summary>

It renders `<input type="hidden" name="csrfmiddlewaretoken" value="...">`. Needed because Django's `CsrfViewMiddleware` rejects POST requests without a valid CSRF token (403 Forbidden). Prevents cross-site request forgery attacks.
</details>

3. How does `request.POST.get()` differ from `request.POST['key']`?

<details><summary>Answer</summary>

`.get('key')` returns the value or `None` if missing — never raises an exception. `['key']` raises `KeyError` if the key is not in the POST data. Use `.get()` for optional fields; use `['key']` only when the field must exist (and you want the error to surface).
</details>

4. What happens when a GET request hits `/submit/`?

<details><summary>Answer</summary>

`request.method` is `'GET'`, not `'POST'`, so the `if` block is skipped. The view executes `return redirect('contact_form')` — a 302 redirect to `/`. The user is sent back to the form page.
</details>

5. What are the two bugs in the A029 artifact?

<details><summary>Answer</summary>

1. `STATICFILES_DIRD` in `settings.py` line 119 — should be `STATICFILES_DIRS` (typo, missing S). 2. Duplicate `message = request.POST.get('message')` on lines 12–13 of `views.py` — the first assignment is immediately overwritten by the second.
</details>

---

## 📝 Quick Revision

| Concept | Code | Purpose |
|---|---|---|
| Form tag | `<form action="{% url "name" %}" method="POST">` | Submits to named URL via POST |
| CSRF | `{% csrf_token %}` | Adds hidden token input for security |
| POST check | `if request.method == 'POST':` | Detects form submission |
| Read data | `request.POST.get('key')` | Safely read form field (None if missing) |
| Validate | `if name and message:` | Check required fields before saving |
| Create | `Contact.objects.create(name=name, ...)` | Insert new row into database |
| Redirect | `redirect('url_name')` | 302 redirect to named URL |
| Text response | `HttpResponse("text")` | Return plain text response |
| Auto timestamp | `created_at = models.DateTimeField(auto_now_add=True)` | Auto-set on creation |

---

## 🧠 Final Mental Model

The form submission flow has **four stations**:
1. **Template** (`contact.html`) — the form with `{% csrf_token %}`, fields, and `{% url %}` action
2. **GET view** (`contact_form`) — renders the template at `/`
3. **POST view** (`submit_contact`) at `/submit/` — checks method → reads POST data → validates → creates → responds
4. **Database** (`Contact.objects.create()`) — persists the validated data

Every station must work for the flow to complete. A029 wires all four for the first time.

---

## ❓ FAQ

**Q1. Why does the form use `method="POST"` instead of `method="GET"`?**
A: POST sends data in the request body (not visible in URL) and is the correct method for creating data. GET appends data to the URL (visible, length-limited, cacheable) and should only be used for retrieving data, not creating it.

**Q2. What would happen if `{% csrf_token %}` was removed from the form?**
A: Submitting the form would send a POST request without a CSRF token. Django's `CsrfViewMiddleware` would reject it with a 403 Forbidden error. The user would never reach the "Thank you" response.

**Q3. Why does `submit_contact` use `HttpResponse` instead of rendering a template?**
A: In the A029 artifact, the view returns a simple text confirmation. Using `HttpResponse` is simpler for a one-line message. In a real app, you'd typically render a template (like the empty `submit.html` which exists but is unused) for a better user experience.

**Q4. What does `auto_now_add=True` do differently from `auto_now=True`?**
A: `auto_now_add=True` sets the value once on creation and never changes it (good for "created at"). `auto_now=True` updates the value every time the object is saved (good for "last updated").

**Q5. Why does the `contact_form` view not check `request.method`?**
A: Because `contact_form` only renders the template — it doesn't process data. Whether it's accessed via GET or POST doesn't matter for rendering. The `submit_contact` view needs the method check because it both displays (via redirect) and processes (via POST) at the same URL.

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Form markup:** I can write an HTML form with `action`, `method="POST"`, `{% csrf_token %}`, and named inputs — *§The Form Template*
- [ ] **Checkpoint 2 — POST handling:** I can write a view that checks `request.method == 'POST'`, reads data via `request.POST.get()`, validates, and creates — *§The View: GET vs POST*
- [ ] **Checkpoint 3 — CSRF & redirect:** I can explain why `{% csrf_token %}` is required and when to use `redirect()` — *§CSRF Protection*

---

## 🏋️ Exercises

- **Level 1 — Recall:** Name the two views and their URLs. List the five vocabulary terms from A029. What does `{% csrf_token %}` render?
- **Level 2 — Understanding:** In A029, `submit.html` exists but is never used. Why? What does the view return instead? What is the `STATICFILES_DIRD` typo and why does it matter?
- **Level 3 — Application:** Add a `subject` field (CharField, max_length=200) to the `Contact` model, run `makemigrations` and `migrate`, add it to the form template, update the view to read and store it, and verify the submission flow includes the new field.
- **Level 4 — Interview reasoning:** A junior developer says: "My form POST returns 403." Walk through the four possible causes (missing `{% csrf_token %}`, ` CsrfViewMiddleware` disabled, wrong `request.method` check, missing `name=` on form inputs) and how to fix each.

---

## 🏁 Final Takeaways

1. HTML forms in Django require `method="POST"`, `{% csrf_token %}`, and named inputs.
2. POST handling requires `request.method == 'POST'` check and `request.POST.get()` for safe data access.
3. Validate before creating — check for empty/missing values before `Model.objects.create()`.
4. Use `redirect()` after successful POST (PRG pattern); use `HttpResponse` for simple text responses.
5. Two deliberate bugs in A029: `STATICFILES_DIRD` typo (settings) and duplicate `message` line (views).

## 🔄 Next Lecture Connection

A030 will build on form handling with a complete TODO app — models for tasks, views for CRUD, templates with forms, and full POST/GET handling across multiple pages. See [A030 — Build a Complete TODO App](../A030_Build_a_Complete_TODO_App/README.md).

---

<div class="doc-footer">

**Sources used:** `myProject17/` artifact (Django 6.1.1): `settings.py` (`contact` in `INSTALLETED_APPS`, `DIRS: [BASE_DIR / 'templates']`, `STATICFILES_DIRD` typo flagged), `myProject17/urls.py` (`path('', include('contact.urls'))` root mount, `admin/`), `contact/models.py` (`Contact` model with `name`/`message`/`created_at`, `__str__` returns `name`), `contact/views.py` (`contact_form` + `submit_contact` with POST handling, CSRF, validation, redirect), `contact/urls.py` (`''` → `contact_form`, `submit/` → `submit_contact`), `contact/admin.py` (`admin.site.register(Contact)`), `contact/migrations/0001_initial.py` (`Contact` table). Templates: `contact/templates/contact.html` (form with `{% csrf_token %}`, `{% url "submit_contact" %}`), `contact/templates/submit.html` (empty, unused). No lecture transcript in folder — chapter built from on-disk artifact and official Django documentation.

**Navigation:** ← [A028 — Admin List Display, Searching, Sorting & Filters](../A028_Admin_List_Display_Searching_Sorting_&_Filters/README.md) · [Series hub](../../README.md) · [A030 — Build a Complete TODO App](../A030_Build_a_Complete_TODO_App/README.md) →

</div>
