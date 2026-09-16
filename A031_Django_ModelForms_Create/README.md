# 🚀 A031 — Django ModelForms Create

`📖 Lecture A031` · `🎓 Track: Core Django` · `📶 Level: Intermediate` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the `myProject18/` artifact — a Django 6.1.1 project with a `student` app that demonstrates creating database records using `ModelForm` instead of manual `request.POST.get()` handling. The `Student` model has `name`, `age`, and `email` fields; the `StudentForm` ModelForm maps to all three fields and includes custom `clean_age()` validation. All file references below are quoted verbatim from the on-disk artifact.
>
> This lecture builds directly on [A030 — Build a Complete TODO App](../A030_Build_a_Complete_TODO_App/README.md).

---

## 🧭 What You Will Learn

- [ ] How `ModelForm` maps a model's fields to a form automatically
- [ ] How `form.is_valid()` runs field-level and custom validation
- [ ] How `form.save()` persists form data to the database
- [ ] How `form.as_p()` renders form fields with minimal template code
- [ ] How custom `clean_<fieldname>()` methods enforce field-specific rules
- [ ] How `forms.ValidationError` signals validation failures to the user

## 🎯 Why This Lecture Matters

A030 built a complete CRUD app using `request.POST.get()` and `Model.objects.create()` — the raw approach. A031 replaces that plumbing with `ModelForm`: a single class that auto-generates form fields from a model, validates input against field constraints, and saves valid data in one line. This is the Django-recommended way to handle forms tied to models, and it eliminates entire categories of bugs (missing fields, wrong types, omitted validation).

## ✅ Prerequisites

- [ ] Models defined and migrated (covered in A022–A023)
- [ ] HTML forms with `{% csrf_token %}`, POST handling, and validation (covered in A029)
- [ ] `render()`, `redirect()`, and `request.method == 'POST'` (covered in A029–A030)
- [ ] URL routing with `path()` and `include()` (covered in A007–A009)

## 🧠 ModelForms in Django

### The Architecture

```
myProject18/                    ← project root (manage.py lives here)
├── manage.py
├── myProject18/                ← config package (settings, urls, wsgi, asgi)
│   ├── settings.py             ← INSTALLED_APPS includes 'student'
│   ├── urls.py                 ← includes student.urls at ''
│   ├── wsgi.py
│   └── asgi.py
├── student/                    ← the app
│   ├── models.py               ← Student model (name, age, email)
│   ├── forms.py                ← StudentForm (ModelForm)
│   ├── views.py                ← student_create view
│   ├── urls.py                 ← path('', student_create, name='student_create')
│   ├── admin.py                ← (empty — Student not registered)
│   ├── apps.py                 ← StudentConfig
│   ├── migrations/
│   │   └── 0001_initial.py     ← creates student_student table
│   └── templates/
│       ├── student_form.html   ← form with {{ form.as_p }}
│       └── student_success.html ← success confirmation
└── db.sqlite3                  ← SQLite database
```

### The Student Model

```python
# student/models.py — verbatim from A031
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
```

**Explanation:**
- Line 5: `name = models.CharField(max_length=100)` — a required string field with a length cap.
- Line 6: `age = models.IntegerField()` — an integer field with no constraints (accepts any integer, including negatives). Validation for age ≥ 18 is handled in the form, not the model (📌 — the model allows any integer; business rules live in the form).
- Line 7: `email = models.EmailField(unique=True)` — a validated email field; `unique=True` prevents duplicate emails at the database level.
- Line 9-10: `__str__` returns the student's name for admin and shell display.

### The StudentForm ModelForm

```python
# student/forms.py — verbatim from A031 (bug noted below)
from django.forms import ModelForm
from .models import Student

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'age', 'email']  # Specify the fields you want to include in the form
        # fields = '__all__'

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError("Age must be 18 or older.")
        return age
```

**Explanation:**
- Line 1: `from django.forms import ModelForm` — imports the base class.
- Line 2: `from .models import Student` — imports the model the form maps to.
- Lines 4-5: `class StudentForm(ModelForm)` — the form class, inheriting from `ModelForm`.
- Lines 6-9: The `Meta` inner class configures the form:
  - `model = Student` — which model this form maps to.
  - `fields = ['name', 'age', 'email']` — which model fields appear as form fields. The alternative `fields = '__all__'` would include all fields automatically.
- Lines 10-15: `clean_age()` — custom validation for the `age` field:
  - `self.cleaned_data.get('age')` — retrieves the validated age value (after Django's default type conversion).
  - `if age < 18: raise forms.ValidationError(...)` — **Bug:** `forms` is not imported. The module only imports `ModelForm` from `django.forms`, but uses `forms.ValidationError` which doesn't exist. Fix: `from django.forms import ModelForm, ValidationError` and change to `raise ValidationError("Age must be 18 or older.")`, or `from django.core.exceptions import ValidationError`.
  - `return age` — required; `clean_<fieldname>()` must return the cleaned value.

### How ModelForm Works

```
Student(model) → StudentForm(ModelForm) → form fields auto-generated
                  ↓
              form.is_valid() → runs field validation + clean_age()
                  ↓
              form.save() → creates Student row in database
```

1. **`StudentForm()`** (GET request) — creates an empty bound form. `form.as_p()` renders three form fields (`<p>`-wrapped) with labels and input widgets automatically derived from the model field types.
2. **`StudentForm(request.POST)`** (POST request) — creates a data-bound form with submitted values.
3. **`form.is_valid()`** — runs all validations in order:
   - Field-level: `CharField` (required, max 100 chars), `IntegerField` (must be integer), `EmailField` (must be valid email format, unique at DB level)
   - Form-level: `clean_age()` runs after field-level validation
   - If any fails: `form.errors` populates with error messages; returns `False`
4. **`form.save()`** — creates and saves a `Student` instance with the cleaned form data. Equivalent to `Student.objects.create(name=..., age=..., email=...)` but using the form's validated data.

### The View

```python
# student/views.py — verbatim from A031
from django.shortcuts import render
from .forms import StudentForm

def student_create(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'student_success.html')
    else:
        form = StudentForm()

    return render(request, 'student_form.html', {'form': form})
```

**Explanation:**
- Line 1-2: Imports — `render` for template rendering, `StudentForm` for the form class.
- Line 6: `form = StudentForm()` — creates an empty form for initial display.
- Lines 7-12: POST handling:
  - Line 8: `form = StudentForm(request.POST)` — binds form to submitted data.
  - Line 9: `if form.is_valid():` — validates all fields + `clean_age()`.
  - Line 10: `form.save()` — persists the new Student record.
  - Line 11: `return render(request, 'student_success.html')` — shows confirmation. **Bug:** This renders a template instead of redirecting. After a successful POST, `redirect('student_success')` would be the PRG pattern. Rendering directly means refreshing the success page resubmits the form data (📌 — same issue as A029's `submit.html` which exists but is unused).
- Lines 13-14: GET handling — re-creates an empty form (redundant since `form = StudentForm()` on line 6 already did this, but harmless).
- Line 16: Renders the form template with the form object.

### Templates

#### Student Form

```html
<!-- student/templates/student_form.html — verbatim -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Student Add</title>
</head>
<body>
    <h2>Add Student Here</h2>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Add Student</button>
    </form>
</body>
</html>
```

**Explanation:**
- Line 9: `{% csrf_token %}` — required for all POST forms in Django.
- Line 10: `{{ form.as_p }}` — renders the entire form as `<p>` elements, one per field. Each field includes its label, input widget, and any validation errors. This single tag replaces ~15 lines of manual HTML for three fields.
- Line 11: Submit button.
- **No `{% extends %}`** — this is a standalone page, not part of a template inheritance chain (📌 — departs from the A012-A030 convention of a shared `base.html`).

#### Student Success

```html
<!-- student/templates/student_success.html — verbatim -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Student Added</title>
</head>
<body>
    <h2>Student Added Successfully</h2>
    <a href="/">Add Another Student</a>
</body>
</html>
```

**Explanation:**
- Line 8: `<a href="/">` — **Bug:** hardcoded path instead of `{% url 'student_create' %}`. If the URL pattern changes, this link breaks. Fix: `<a href="{% url 'student_create' %}">Add Another Student</a>`.

### URL Configuration

```python
# student/urls.py — verbatim from A031
from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_create, name='student_create'),
]
```

**Explanation:**
- No `app_name` declared — no URL namespace. `{% url 'student_create' %}` works because there's no namespace collision, but it also means the URL name isn't scoped. Best practice: add `app_name = 'student'` and use `{% url 'student:student_create' %}` (📌).
- `path('', views.student_create, name='student_create')` — the empty path means this view handles the app's root URL, mounted via `path('', include('student.urls'))` in the project `urls.py`.

The project root configures this:

```python
# myProject18/urls.py
path('', include('student.urls')),
```

### Admin

`student/admin.py` is empty — `Student` is **not registered**. To enable admin management:

```python
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```

### Migration

```bash
py -3 manage.py makemigrations student   # generates 0001_initial.py
py -3 manage.py migrate                  # applies: creates student_student table
```

The migration creates the `student_student` table (following the `appname_modelname` convention):

| Column | Type | Constraints |
|---|---|---|
| `id` | BigAutoField | PK |
| `name` | VARCHAR(100) | NOT NULL |
| `age` | INTEGER | NOT NULL |
| `email` | VARCHAR(254) | NOT NULL, UNIQUE |

---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **`ModelForm`** | A form that knows its model | A `forms.Form` subclass that auto-generates fields from a model's fields via `Meta.model` and `Meta.fields` | a model-shaped form |
| **`form.is_valid()`** | Does this form pass validation? | Runs field validators + `clean_<field>()` methods + `clean()`; populates `form.errors` on failure; returns `True`/`False` | the quality gate |
| **`form.save()`** | Persist this form's data | Creates or updates a model instance from `form.cleaned_data` and saves it to the database | the filing cabinet |
| **`form.as_p()`** | Render form as paragraphs | Template tag outputting each field as a `<p>` element with label, widget, and errors | one tag, three fields |
| **`clean_<fieldname>()`** | Custom field validator | A method named `clean_<field>()` that receives the raw value via `self.cleaned_data.get('<field>')`, returns the cleaned value or raises `ValidationError` | the field's guard |
| **`ValidationError`** | "This input is bad" | Exception raised in `clean_*()` methods; displayed to the user as a form error | the stop sign |
| **`form.cleaned_data`** | Validated form values | A dictionary of field names → validated/coerced values, available after `is_valid()` returns `True` | the clean output |
| **`Meta` class** | Form configuration inner class | Inner class on a `ModelForm` specifying `model`, `fields`, `exclude`, widgets, etc. | the form's blueprint |

## 💡 Real-World Analogy

**A `ModelForm` is a customs declaration form for a model.** The model (Student) defines what data exists (name, age, email — the cargo manifest). The `ModelForm` is the form you fill out to declare that cargo. `form.is_valid()` is the customs officer checking that every field matches the manifest rules (age ≥ 18, email format valid, no duplicate emails). `form.save()` is when the officer stamps the form and the cargo enters the country (database). `clean_age()` is a specific regulation ("you must be 18 to enter") that goes beyond the manifest's basic field types. `{{ form.as_p }}` is the pre-printed blank form — the officer doesn't design the form; it's auto-generated from the manifest.

## ❌ Common Beginner Mistakes

1. **Forgetting to import `ValidationError`** — Using `forms.ValidationError` when only `ModelForm` was imported causes a `NameError`. Fix: `from django.forms import ModelForm, ValidationError` or `from django.core.exceptions import ValidationError`.

2. **Not checking `form.is_valid()` before `form.save()`** — Calling `form.save()` on an invalid form raises an error. Fix: always check `is_valid()` first: `if form.is_valid(): form.save()`.

3. **Rendering instead of redirecting after POST** — `render(request, 'success.html')` after a successful POST means refreshing the page resubmits the data. Fix: use `redirect()` after successful POST (PRG pattern).

4. **Forgetting `{% csrf_token %}`** — POST requests without a valid CSRF token are rejected (403 Forbidden). Fix: always include `{% csrf_token %}` inside `<form method="POST">`.

5. **Hardcoded URLs in templates** — Using `<a href="/">` instead of `{% url 'student_create' %}` means URL changes break the link. Fix: always use `{% url %}` for reverse lookups.

6. **Using `fields = '__all__'` when you need to exclude sensitive fields** — `__all__` includes every field. If the model has a `password` or `is_admin` field, it appears in the form. Fix: explicitly list fields: `fields = ['name', 'age', 'email']`.

## 🧠 Common Misconceptions

| ✅ ModelForm IS … | ❌ It is NOT … |
|---|---|
| Auto-generates form fields from model fields | A database query tool — it creates forms, not queries |
| `is_valid()` runs both field and form-level validation | The same as `form.data` — `cleaned_data` only exists after validation passes |
| `form.save()` creates a model instance from validated data | A substitute for model validation — model-level constraints (`unique`, `null`) are still enforced independently |
| `clean_<field>()` runs for that specific field | A replacement for `request.POST.get()` — it's a higher-level abstraction |
| `{{ form.as_p }}` renders all fields at once | Styleable directly — you can render individual fields as `{{ form.name }}` instead |

## 🧪 Practical Example

```python
# student/views.py — the complete ModelForm create flow
from django.shortcuts import render
from .forms import StudentForm

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)          # 1. Bind form to POST data
        if form.is_valid():                        # 2. Validate (fields + clean_age)
            form.save()                            # 3. Save to database
            return redirect('student_create')      # 4. Redirect (PRG pattern)
    else:
        form = StudentForm()                       # 5. Empty form for GET

    return render(request, 'student_form.html', {'form': form})  # 6. Render
```

**Explanation:**
- Step 1 (Bind): `StudentForm(request.POST)` packages submitted data into the form.
- Step 2 (Validate): `is_valid()` checks all field constraints (`CharField` max 100, `IntegerField` must be int, `EmailField` must be valid email + unique) plus custom `clean_age()` (≥ 18).
- Step 3 (Save): `form.save()` creates a `Student` row from `form.cleaned_data` — no manual `Student.objects.create(name=..., age=..., email=...)` needed.
- Step 4 (Redirect): After successful POST, redirect to prevent duplicate submissions.
- Step 5 (Empty): For GET requests, create an unbound form for the user to fill out.
- Step 6 (Render): Pass the form to the template; `{{ form.as_p }}` renders all three fields.

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. What is the difference between `ModelForm` and `forms.Form`?**
A: `forms.Form` is a standalone form with manually defined fields. `ModelForm` is tied to a model — it auto-generates fields from the model's fields via the `Meta` class, and `form.save()` creates a model instance. `ModelForm` is for CRUD operations tied to models; `Form` is for arbitrary input (contact forms, search boxes).

**Q2. What does `form.is_valid()` do internally?**
A: It runs in this order: (1) each field's built-in validators (required, type, max_length, email format, etc.), (2) each `clean_<fieldname>()` method for the specific field, (3) the form's `clean()` method for cross-field validation. If any fails, `form.errors` populates and it returns `False`. If all pass, `form.cleaned_data` is populated and it returns `True`.

**Q3. What is `cleaned_data` and when is it available?**
A: `form.cleaned_data` is a dictionary of validated, coerced field values. It's only available AFTER `is_valid()` returns `True`. Before that, accessing it raises an `AttributeError`. It contains the Python-native types (e.g., `age` is an `int`, not a string).

**Q4. Why does `clean_age()` use `self.cleaned_data.get('age')` instead of `self.data['age']`?**
A: `self.data` contains raw POST strings (e.g., `"25"`). `cleaned_data` contains already-validated and coerced values (e.g., `25` as an `int`). By the time `clean_age()` runs, Django has already validated that `age` is an integer — so `cleaned_data.get('age')` gives us a real integer to compare against 18.

**Q5. What happens if `form.save()` is called without `is_valid()`?**
A: Django raises an error because `save()` requires cleaned data from a valid form. You must always call `is_valid()` first and check its return value.

**Q6. What is the bug in `forms.py` line 13?**
A: `forms.ValidationError` is used but `forms` is never imported. The module imports `from django.forms import ModelForm` only. Fix: `from django.core.exceptions import ValidationError` and change the raise to `raise ValidationError(...)`.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. What are the three steps in the ModelForm create pattern?

<details><summary>Answer</summary>

1. Instantiate the form with POST data: `form = StudentForm(request.POST)`. 2. Validate: `if form.is_valid():`. 3. Save: `form.save()`.
</details>

2. What is the difference between `form.data` and `form.cleaned_data`?

<details><summary>Answer</summary>

`form.data` is the raw POST data (all strings). `form.cleaned_data` is the validated, coerced data (correct Python types) available only after `is_valid()` returns `True`.
</details>

3. What does `{{ form.as_p }}` render?

<details><summary>Answer</summary>

Each form field as a `<p>` element containing the label, input widget, and any validation errors. For a 3-field form, it renders 3 `<p>` blocks.
</details>

4. When does `clean_<fieldname>()` run in the validation order?

<details><summary>Answer</summary>

After the field's built-in validators but before the form's `clean()` method. It runs per-field, so `clean_age()` runs specifically for the `age` field.
</details>

5. What is the bug in A031's `forms.py`?

<details><summary>Answer</summary>

`forms.ValidationError` on line 13 — `forms` is not imported. The module only does `from django.forms import ModelForm`. Fix: import `ValidationError` from `django.core.exceptions` or `django.forms`.
</details>

6. Why should you `redirect()` instead of `render()` after a successful POST?

<details><summary>Answer</summary>

Redirecting implements the PRG (Post-Redirect-Get) pattern. Without it, refreshing the page resubmits the form data (duplicate records). After a redirect, refreshing the page re-issues the GET request, which is safe.
</details>

---

## 📝 Quick Revision

| Concept | Code | Purpose |
|---|---|---|
| ModelForm | `class StudentForm(ModelForm): Meta: model = Student` | Auto-generate form from model |
| Fields | `fields = ['name', 'age', 'email']` | Which model fields appear in form |
| Validate | `if form.is_valid():` | Run field + custom validation |
| Clean data | `form.cleaned_data` | Validated, coerced values |
| Save | `form.save()` | Create model instance from form |
| Render | `{{ form.as_p }}` | Auto-render all fields as `<p>` |
| Custom validate | `def clean_age(self):` | Field-specific validation rule |
| ValidationError | `raise ValidationError(...)` | Signal invalid input to user |
| CSRF | `{% csrf_token %}` | Anti-forgery token in POST forms |

---

## 🧠 Final Mental Model

The ModelForm flow has **four stations**:

```
User ─→ Template ({{ form.as_p }}) ─→ View (POST: bind → validate → save → redirect) ─→ Model (Student row in DB)
                                    ↑
                             form.is_valid() gate
                                    ↓
                             form.errors (displayed in {{ form.as_p }})
```

- **Template** renders the auto-generated form with one tag (`{{ form.as_p }}`)
- **View** binds, validates, saves, redirects — no manual field extraction
- **Model** defines the schema and `save()` persists the data
- **Validation gate** (`is_valid()`) ensures only clean data reaches the model

`ModelForm` collapses three layers (form definition, validation, persistence) into one class.

---

## ❓ FAQ

**Q1. Can I use `ModelForm` for models with relationships (ForeignKey, ManyToMany)?**
A: Yes. `ModelForm` auto-generates `<select>` dropdowns for `ForeignKey` and multi-select for `ManyToManyField`. Use `fields = '__all__'` or explicitly list fields including the relationship field.

**Q2. What's the difference between `fields = ['name', 'age', 'email']` and `exclude = ['email']` in `Meta`?**
A: `fields` is an allowlist — only listed fields appear. `exclude` is a blocklist — listed fields are hidden. Use `fields` (explicit) for security; use `exclude` only for adding fields to an existing form.

**Q3. Why does `age = models.IntegerField()` in the model accept any integer, while the form rejects ages < 18?**
A: The model defines the database schema (any integer fits an `IntegerField`). The form defines user-facing validation rules (age ≥ 18). Business rules belong in the form or a dedicated validator, not in the model's field definition.

**Q4. Can I customize how each field is rendered instead of `{{ form.as_p }}`?**
A: Yes. Render individual fields: `{{ form.name }}` for a single field, `{{ form.name.label_tag }}` for just the label, `{{ form.name.errors }}` for just errors. Or use custom HTML with `{{ form.name }}` inside your own markup.

**Q5. What happens if `email` is duplicated and `form.is_valid()` is called?**
A: `EmailField(unique=True)` checks the database during validation. If a matching email exists, `is_valid()` returns `False` and `form.errors['email']` contains an error message about the duplicate.

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — ModelForm definition:** I can define a `ModelForm` with `Meta.model` and `Meta.fields`, and explain how fields auto-generate from the model — *§The StudentForm ModelForm*
- [ ] **Checkpoint 2 — Validation flow:** I can explain the three-step validation order (field validators → `clean_<field>()` → `clean()`) and the difference between `is_valid()` and `cleaned_data` — *§How ModelForm Works*
- [ ] **Checkpoint 3 — Create pattern:** I can write the complete ModelForm create view (bind → validate → save → redirect) and explain why each step exists — *§The View*
- [ ] **Checkpoint 4 — Custom validation:** I can write a `clean_<fieldname>()` method that enforces a business rule and raises `ValidationError` — *§The StudentForm ModelForm*
- [ ] **Checkpoint 5 — Bug diagnosis:** I can identify `forms.ValidationError` NameError, hardcoded URLs, and missing PRG redirect — *§Common Beginner Mistakes*

---

## 🏋️ Exercises

- **Level 1 — Recall:** Name the three steps of the ModelForm create pattern. What does `is_valid()` return? What is `cleaned_data`?
- **Level 2 — Understanding:** Why is `forms.ValidationError` a bug? Why does the model accept any integer but the form rejects age < 18? What happens if you call `form.save()` without `is_valid()`?
- **Level 3 — Application:** Add a `clean_email()` method to `StudentForm` that rejects email addresses from a blocklist (e.g., `@tempmail.com`). Add `app_name = 'student'` to `urls.py`. Register `Student` in `admin.py`. Change the success template to use `{% url 'student:student_create' %}`.
- **Level 4 — Interview reasoning:** A junior developer writes `form = StudentForm(request.POST); form.save(); return redirect(...)` without calling `is_valid()`. Walk through what happens: the database receives invalid data, or an exception is raised. How do you fix it? Why does `ModelForm` exist instead of just using `request.POST.get()` and `Model.objects.create()`?

---

## 🏁 Final Takeaways

1. `ModelForm` auto-generates form fields from a model — no manual field definition needed.
2. Always call `form.is_valid()` before `form.save()` — never skip validation.
3. `form.cleaned_data` contains validated, type-coerced values after `is_valid()` passes.
4. Custom validation lives in `clean_<fieldname>()` methods, which must return the cleaned value or raise `ValidationError`.
5. `{{ form.as_p }}` renders the entire form in one template tag.
6. After successful POST, always `redirect()` (PRG pattern).
7. Always import `ValidationError` if you use it in `clean_*()` methods.

## 🔄 Next Lecture Connection

A031 introduces ModelForms for creation. A032 — now documented ([Django ModelForms Read](../A032_Django_ModelForms_Read/README.md)) — added the **read** half over the same table: a list view and a detail view. The remaining progression:

- [ ] **A033 — ModelForms Update (Edit) Data** — editing an existing record by reusing `StudentForm` with `instance=` (*next lecture*)
- [ ] ModelForms with `ChoiceField` and `ModelChoiceField` for relationships
- [ ] Formsets (multiple ModelForms at once)

> 📌 **Correction (per §12):** this section previously described A032 as "ModelForms for Update (editing existing records with `instance=` parameter)". That is the **A033** lecture; A032 is **ModelForms Read**. The mislabel is corrected here rather than silently overwritten.

---

<div class="doc-footer">

**Sources used:** `myProject18/` artifact (Django 6.1.1): `manage.py`, `myProject18/settings.py` (`INSTALLED_APPS` includes `'student'`, `ROOT_URLCONF = 'myProject18.urls'`, `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']` (directory does not exist — W004 ghost shelf), `STATICFILES_DIRS = [BASE_DIR / 'static']`), `myProject18/urls.py` (`path('', include('student.urls'))`, no namespace), `student/models.py` (Student: name CharField max_length=100, age IntegerField, email EmailField unique=True), `student/forms.py` (StudentForm ModelForm with clean_age), `student/views.py` (student_create: bind → validate → save → render), `student/urls.py` (no app_name), `student/admin.py` (empty — Student not registered), `student/migrations/0001_initial.py` (creates student_student table), `student/templates/student_form.html` (`{% csrf_token %}`, `{{ form.as_p }}`), `student/templates/student_success.html` (hardcoded `/` link). Bugs flagged per AGENTS §12: `forms.ValidationError` NameError (forms not imported), render vs redirect in student_create view, no `app_name` in student/urls.py, hardcoded `/` in success template, Student not registered in admin, no template inheritance (no base.html). No lecture transcript in folder — chapter built from on-disk artifact and official Django documentation.

**Navigation:** ← [A030 — Build a Complete TODO App](../A030_Build_a_Complete_TODO_App/README.md) · [Series hub](../../README.md) · [A032 — Django ModelForms Read →](../A032_Django_ModelForms_Read/README.md)

</div>
