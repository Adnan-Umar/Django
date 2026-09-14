# 🚀 A028 — Admin: List Display, Searching, Sorting & Filters

`📖 Lecture A028` · `🎓 Track: Core Django` · `📶 Level: Beginner` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the `myProject16/` artifact — a fresh Django 6.1.1 project with a `students` app, a `Student` model, and a `StudentAdmin` class registered via the `@admin.register()` decorator with four customizations: `list_display`, `search_fields`, `list_filter`, and `ordering`. All file references below are quoted verbatim from the on-disk artifact.
>
> This lecture builds directly on [A027 — Register & Manage Models in Django Admin](../A027_Register_&_Manage_Models_in_Django_Admin/README.md).

---

## 🧭 What You Will Learn

- [ ] How to create a `ModelAdmin` class to customize the admin interface
- [ ] How `@admin.register(Model)` decorator differs from `admin.site.register()`
- [ ] How `list_display` controls which columns appear in the admin list view
- [ ] How `search_fields` adds a search box to the admin
- [ ] How `list_filter` adds sidebar filter panels
- [ ] How `ordering` sets the default sort order of records

## 🎯 Why This Lecture Matters

The default admin registration (`admin.site.register(Model)`) gives you a functional but generic interface — every field is shown, there's no search, no filters, and no control over sort order. For any real project, the admin needs to be tailored to how staff actually work. `ModelAdmin` is the gateway to all admin customization: every admin feature (date hierarchy, inlines, actions, form customization, export) builds on the same `ModelAdmin` class. This lecture covers the four most common customizations that immediately make the admin usable.

## ✅ Prerequisites

- [ ] Models defined and registered in admin (covered in A027)
- [ ] Admin site accessible with a superuser (covered in A026)
- [ ] Understanding of `INSTALLED_APPS` and app registration (covered in A006)
- [ ] 📌 `ModelAdmin` class concept (introduced in this lecture; A027 used plain `admin.site.register()`)

## 🧠 ModelAdmin Customization

### The Problem with Plain Registration

In A027, both models were registered with `admin.site.register(Student)` and `admin.site.register(Profile)`. This works but shows every field in a long vertical form, has no search, no filters, and no control over ordering. For a model with 20 fields, this is unusable.

### `ModelAdmin` — The Customization Class

`ModelAdmin` is a Django class that defines how a model appears and behaves in the admin. You create a subclass, set attributes on it, and register it instead of using the bare `admin.site.register()`.

### Two Ways to Register with `ModelAdmin`

**Method 1: `admin.site.register()` with class argument**

```python
from django.contrib import admin
from students.models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'city')

admin.site.register(Student, StudentAdmin)
```

**Method 2: `@admin.register()` decorator (used in A028 artifact)**

```python
# students/admin.py — A028 artifact verbatim
from django.contrib import admin
from students.models import Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'city')
    search_fields = ('name', 'city')
    list_filter = ('age', 'city')
    ordering = ('name',)
```

**Explanation:**
- Line 1: Import `admin` from `django.contrib.admin`.
- Line 2: Import the model. The import path uses the app name (`students.models`) — the app's Python package path, not the project name.
- Line 5: `@admin.register(Student)` — a decorator that registers the model with the admin site. It's equivalent to `admin.site.register(Student, StudentAdmin)` but more concise. The decorator returns the class unchanged, so it can be used as a decorator.
- Line 6: `class StudentAdmin(admin.ModelAdmin)` — the customization class. All attributes below control admin behavior.

### The Four Customizations in A028

| Attribute | Purpose | Value in A028 |
|---|---|---|
| `list_display` | Which fields show as columns in the admin list view | `('name', 'age', 'city')` — three columns instead of all fields |
| `search_fields` | Which fields get a search box at the top of the list | `('name', 'city')` — search by name or city |
| `list_filter` | Which fields get sidebar filter panels | `('age', 'city')` — filter by age range or city |
| `ordering` | Default sort order of records | `('name',)` — alphabetical by name |

### How Each Customization Works

**`list_display`** — A tuple of field names that become table columns in the admin list view. Without it, Django shows the `__str__` representation (or raw object reference if `__str__` is missing). With it, each field becomes its own clickable column. Fields can also be methods on the `ModelAdmin` class, not just model fields.

**`search_fields`** — A tuple of field names that Django will search with `LIKE '%query%'` (case-insensitive in SQLite). A search box appears at the top of the admin list. Only fields in `search_fields` are searchable — this keeps the search fast and relevant.

**`list_filter`** — A tuple of field names that add sidebar filter panels on the right of the admin list. For `CharField` and `DateField`, Django shows a dropdown with distinct values. For `IntegerField` and `DateField`, it shows range filters (e.g., "Any age", "0-10", "11-20", etc.). Only fields in `list_filter` get filter panels.

**`ordering`** — A tuple of field names (with optional `-` prefix for descending) that sets the default sort. `('name',)` sorts A→Z. `('-age',)` would sort by age descending. Without `ordering`, records appear in insertion order (unpredictable).

### The Commented-Out `__str__`

In the A028 artifact, `__str__` is commented out in `models.py`:

```python
# def __str__(self):
#     return self.name
```

This is deliberate — it demonstrates that `list_display` works independently of `__str__`. Even without `__str__`, the admin list view shows meaningful columns because `list_display` explicitly names which fields to show. If neither `__str__` nor `list_display` were set, the admin would show `Student object (1)` in the name column (raw object reference).

> [!NOTE]
> **Both registration methods work the same way.** The decorator `@admin.register(Model)` and the function call `admin.site.register(Model, AdminClass)` are interchangeable. The decorator is more concise; the function call is more explicit. A027 used `admin.site.register()`; A028 uses `@admin.register()`.

---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **`ModelAdmin`** | Controls model's admin appearance | A class subclassing `admin.ModelAdmin`; set attributes like `list_display`, `search_fields` | the display settings panel |
| **`@admin.register()`** | Decorator to register a model with admin | Decorator on a `ModelAdmin` subclass; equivalent to `admin.site.register(Model, AdminClass)` | the decorator stamp |
| **`admin.site.register()`** | Function to register a model | Either bare (`admin.site.register(Model)`) or with a `ModelAdmin` class (`admin.site.register(Model, AdminClass)`) | the registration desk |
| **`list_display`** | Columns in admin list view | Tuple of field names shown as table columns in the admin list page | the column headers |
| **`search_fields`** | Fields that get a search box | Tuple of field names; Django runs `LIKE` queries on these; adds a search bar to admin list | the search window |
| **`list_filter`** | Fields that get sidebar filters | Tuple of field names; Django adds filter panels to the admin list sidebar | the filter rack |
| **`ordering`** | Default sort of records | Tuple of field names; `-field` for descending; sets the default `ORDER BY` | the default sort |
| **Decorator** | A function that wraps a class/function | `@decorator` syntax: `@admin.register` wraps `StudentAdmin` before it's defined | the label stamp |

---

## 💡 Real-World Analogy

**The admin with `ModelAdmin` is a spreadsheet with built-in tools.** `list_display` is the column headers you choose to show (hiding the columns you don't need). `search_fields` is the spreadsheet's Find function — search by name or city. `list_filter` is the Autofilter dropdown — click a column header and pick values to filter by. `ordering` is the Sort A→Z button — the default view is always sorted. Without `ModelAdmin`, you'd have a raw data dump with no tools. With it, you have a working dashboard.

---

## ❌ Common Beginner Mistakes

1. **Using field names in `list_display` that don't exist** — Django raises `FieldError` at admin load time. Fix: only use actual model field names or defined `ModelAdmin` methods.

2. **Adding non-indexed fields to `search_fields` on large datasets** — `LIKE '%query%'` queries are slow on large tables. Fix: only add frequently searched fields; consider database-level full-text search for large datasets.

3. **Adding a field to `list_filter` that has too many distinct values** — A `CharField` with 10,000 unique values generates a useless dropdown. Fix: use `list_filter` on fields with reasonable cardinality (under ~100 distinct values typically).

4. **Confusing `admin.site.register(Model)` with `@admin.register(Model)`** — Both work, but you cannot mix them for the same model (double registration raises an error). Fix: choose one method per model.

5. **Forgetting that `@admin.register` returns the class** — Since the decorator returns the class unchanged, you can also assign it: `StudentAdmin = admin.register(Student)(StudentAdmin)`. But in practice, just place the decorator above the class definition.

---

## 🧠 Common Misconceptions

| ✅ ModelAdmin IS … | ❌ It is NOT … |
|---|---|
| A class that customizes admin behavior | The model itself |
| Configured via class attributes (`list_display`, etc.) | Configured via URL patterns |
| Registered via `@admin.register()` or `admin.site.register()` | Automatically created when a model is defined |
| Able to show any method/property as a column | Limited to model fields only (without custom methods) |
| Composable (you can subclass and extend) | A singleton — each model gets its own `ModelAdmin` |

---

## 🧪 Practical Example

```python
# students/admin.py — A028 artifact verbatim
from django.contrib import admin
from students.models import Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'city')
    search_fields = ('name', 'city')
    list_filter = ('age', 'city')
    ordering = ('name',)
```

**Explanation:**
- Line 1: Import `admin` from `django.contrib.admin` — provides `admin.site`, `@admin.register`, and `ModelAdmin`.
- Line 2: Import `Student` from `students.models` — the app name is the Python package path, not the project name `myProject16`.
- Line 5: `@admin.register(Student)` — registers `Student` with the admin site using the class below as the `ModelAdmin`.
- Line 6: `class StudentAdmin(admin.ModelAdmin):` — empty subclass; all configuration is via class attributes.
- Line 7: `list_display = ('name', 'age', 'city')` — shows three columns in the list view instead of the default (which would show `Student object (1)` since `__str__` is commented out).
- Line 8: `search_fields = ('name', 'city')` — adds a search box; searching "Delhi" matches students whose name or city contains "Delhi" (case-insensitive `LIKE`).
- Line 9: `list_filter = ('age', 'city')` — adds two filter panels in the sidebar. `age` shows integer range filters; `city` shows distinct value checkboxes.
- Line 10: `ordering = ('name',)` — default sort A→Z by name. Add `'-age'` for descending.

---

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. What is the difference between `admin.site.register(Model)` and `@admin.register(Model)`?**
A: There is no functional difference. `@admin.register(Model)` is a decorator that wraps `admin.site.register(Model, StudentAdmin)`. Both register a model with its `ModelAdmin` class. You cannot use both for the same model — double registration raises `AlreadyRegistered`.

**Q2. What does `list_display` do?**
A: It controls which model fields are shown as columns in the admin's list view. Without it, only the `__str__` representation is shown. With it, each named field becomes its own column.

**Q3. Why would you use `@admin.register()` instead of `admin.site.register()`?**
A: `@admin.register()` is more concise — it combines the registration and class definition in one place. `admin.site.register()` is more explicit and separates registration from the class. Both are functionally identical.

**Q4. What happens if you add a field to `list_filter` that has 10,000 distinct values?**
A: Django generates a dropdown with 10,000 options — this is slow to load and useless in practice. Fix: use a field with reasonable cardinality, or use `SimpleListFilter` for custom filtering logic.

**Q5. Why does the A028 artifact comment out `__str__`?**
A: To demonstrate that `list_display` works independently. Even without `__str__`, the admin shows meaningful columns because `list_display` explicitly specifies which fields to display. This shows that `list_display` and `__str__` serve different purposes.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. Name the four `ModelAdmin` attributes used in A028 and what each controls.

<details><summary>Answer</summary>

`list_display` — which columns show in the admin list view. `search_fields` — which fields get a search box. `list_filter` — which fields get sidebar filter panels. `ordering` — default sort order of records.
</details>

2. What is the difference between `admin.site.register()` and `@admin.register()`?

<details><summary>Answer</summary>

No functional difference. `@admin.register(Model)` is a decorator equivalent to `admin.site.register(Model, AdminClass)`. Both register a model with a `ModelAdmin` subclass. Cannot be mixed for the same model.
</details>

3. What does the `@admin.register` decorator return?

<details><summary>Answer</summary>

It returns the class unchanged. This is why it can be used as a decorator — the class definition is registered AND defined in one step. The decorator applies after the class is created and returns it.
</details>

4. In A028, `__str__` is commented out but the admin still shows meaningful data. How?

<details><summary>Answer</summary>

`list_display = ('name', 'age', 'city')` explicitly names the fields to show as columns. Without `list_display` or with it, Django uses `__str__` for display. Since `list_display` is set, it takes precedence and shows the named fields regardless of `__str__`.
</details>

5. What would happen if you used both `admin.site.register(Student, StudentAdmin)` AND `@admin.register(Student)` for the same model?

<details><summary>Answer</summary>

Django raises `django.contrib.admin.sites.AlreadyRegistered` — the model is already registered. Fix: use only one registration method per model.
</details>

---

## 📝 Quick Revision

| Attribute | Controls | Example |
|---|---|---|
| `list_display` | Columns in admin list | `('name', 'age', 'city')` |
| `search_fields` | Search box fields | `('name', 'city')` |
| `list_filter` | Sidebar filter panels | `('age', 'city')` |
| `ordering` | Default sort | `('name',)` or `('-age',)` |
| `@admin.register()` | Registration (decorator) | `@admin.register(Model)` above class |
| `admin.site.register()` | Registration (function) | `admin.site.register(Model, AdminClass)` |

---

## 🧠 Final Mental Model

`ModelAdmin` is a **control panel** for one model in the admin:
- **`list_display`** = which instruments are visible on the dashboard
- **`search_fields`** = the search bar on top
- **`list_filter`** = the filter dropdowns on the side
- **`ordering`** = the default sort of the data table

A027 built the dashboard (registered models). A028 furnishes it with controls.

---

## ❓ FAQ

**Q1. Can `list_display` include methods from the `ModelAdmin` class?**
A: Yes — you can define methods on `StudentAdmin` and include their names in `list_display`. Django will call the method for each record and display the return value as a column. The method must take `self` and `obj` (the model instance) as arguments.

**Q2. Can `list_display` include related fields ( ForeignKey)?**
A: Yes — but you need to define a method on `ModelAdmin` that accesses the related field, and include that method's name in `list_display`. You cannot use a double-underscore path (e.g., `profile__location`) directly in `list_display`.

**Q3. What is the import path for the model in `admin.py`?**
A: Use the app name as the package path: `from students.models import Student`. Not the project name (`myProject16`). The app is a separate Python package registered in `INSTALLED_APPS`.

**Q4. Does `@admin.register()` work with the decorator argument syntax?**
A: Yes — `@admin.register(Student)` registers the class below as the `ModelAdmin` for `Student`. You can also pass keyword arguments: `@admin.register(Student, site=custom_site)`.

**Q5. What happens when `list_filter` has an `IntegerField`?**
A: Django shows a range-based filter with dropdowns for "Any value", "0 to 10", "11 to 20", etc. — auto-generated based on the field's data range. This is more useful than a dropdown of every distinct integer.

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — ModelAdmin basics:** I can explain what `ModelAdmin` does and how it differs from plain registration — *§ModelAdmin Customization*
- [ ] **Checkpoint 2 — list_display:** I can set `list_display` and explain why it works even when `__str__` is missing — *§The Four Customizations*
- [ ] **Checkpoint 3 — search & filter:** I can set `search_fields` and `list_filter` and explain the difference between them — *§The Four Customizations*

---

## 🏋️ Exercises

- **Level 1 — Recall:** Name the four `ModelAdmin` attributes from A028. Explain what `@admin.register()` does in one sentence. What does `list_display` show when `__str__` is absent?
- **Level 2 — Understanding:** In the A028 artifact, `__str__` is commented out. What would the admin list view look like if neither `__str__` nor `list_display` were set? Why?
- **Level 3 — Application:** Add a `gpa` field (DecimalField, max_digits=3, decimal_places=2) to the `Student` model, run `makemigrations` and `migrate`, then add `gpa` to `list_display` and `search_fields`. Verify the admin shows the new column and is searchable.
- **Level 4 — Interview reasoning:** A junior developer says: "I registered my model in admin, but the list view only shows `Student object (1)`." Walk through the three possible causes (missing `__str__`, missing `list_display`, model not registered) and how to fix each.

---

## 🏁 Final Takeaways

1. `ModelAdmin` is the customization layer between a registered model and a usable admin interface.
2. Four attributes cover 80% of admin customization needs: `list_display`, `search_fields`, `list_filter`, `ordering`.
3. `@admin.register(Model)` and `admin.site.register(Model, AdminClass)` are interchangeable — choose one per model.
4. `list_display` works independently of `__str__` — it explicitly names which fields to show.
5. A028 takes the admin from A027's "registered but generic" to "functional dashboard."

## 🔄 Next Lecture Connection

A029 will build on admin customization with HTML forms, POST handling, CSRF tokens, and validation — moving from the admin's auto-generated forms to custom views with form handling. See [A029 — HTML Forms, POST, CSRF Token & Validation](../A029_HTML_Forms_POST_CSRF_Token_&_Validation/README.md).

---

<div class="doc-footer">

**Sources used:** `myProject16/` artifact (Django 6.1.1): `settings.py` (`students` in `INSTALLED_APPS`, `DIRS: [BASE_DIR / 'templates']`, `STATICFILES_DIRS` set), `myProject16/urls.py` (admin only, no app URLs), `students/models.py` (`Student` model with `name`/`age`/`city`, `__str__` commented out), `students/admin.py` (`@admin.register(Student)` with `StudentAdmin` class — all four attributes quoted verbatim), `students/migrations/0001_initial.py` (table creation). Reference: `docs/MEMORY.md` (A026 admin prerequisites, A027 model registration, A022 model conventions). No lecture transcript in folder — chapter built from on-disk artifact and official Django documentation.

**Navigation:** ← [A027 — Register & Manage Models in Django Admin](../A027_Register_&_Manage_Models_in_Django_Admin/README.md) · [Series hub](../../README.md) · [A029 — HTML Forms, POST, CSRF Token & Validation](../A029_HTML_Forms_POST_CSRF_Token_&_Validation/README.md) →

</div>
