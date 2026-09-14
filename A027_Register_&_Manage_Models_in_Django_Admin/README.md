# 🚀 A027 — Register & Manage Models in Django Admin

`📖 Lecture A027` · `🎓 Track: Core Django` · `📶 Level: Beginner` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the `myProject15/` artifact — the same project from A026, now evolved: the `portfolio` app is **registered** in `INSTALLED_APPS`, two models (`Student`, `Profile`) are defined in `models.py`, both are registered in `admin.py`, and three migrations have been created and applied. All file references below are quoted verbatim from the on-disk artifact.
>
> This lecture builds directly on [A026 — Django Admin & Superuser](../A026_Django_Admin_&_Superuser/README.md).

---

## 🧭 What You Will Learn

- [ ] How to define Django models as Python classes subclassing `models.Model`
- [ ] How `makemigrations` and `migrate` create and evolve database tables
- [ ] How to register models in `admin.py` so they appear in the admin interface
- [ ] How model fields (`CharField`, `IntegerField`, `DateField`, `TextField`, `BigAutoField`) map to database columns
- [ ] How to correct a field type via migration (`IntegerField` → `DateField` in migration 0003)

## 🎯 Why This Lecture Matters

Models are the **M** in MVT — the data layer that Django's ORM manages. Without models, there is nothing for the admin to display, no database tables to store data, and no schema to query. This lecture bridges the gap between A026's admin *infrastructure* (URLs, superuser, admin site working but empty) and A028's admin *customization* (list display, search, filtering). You cannot customize what does not exist — models must be defined and registered first.

## ✅ Prerequisites

- [ ] Django admin is accessible at `/admin/` with a superuser (covered in A026)
- [ ] Understanding of `INSTALLED_APPS` and app registration (covered in A006)
- [ ] Basic Python class definition (covered in A001)
- [ ] 📌 How `makemigrations` and `migrate` work (covered in A022)

## 🧠 Models & Admin Registration

### What Is a Django Model?

A Django model is a Python class that subclasses `models.Model`. Each attribute of the class represents a database field. Django's ORM translates these field types into SQL column definitions automatically — you never write `CREATE TABLE` statements.

```python
# portfolio/models.py — two models defined for the admin
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

**Explanation:**
- Line 1: `from django.db import models` — imports Django's model field classes.
- Line 4: `class Student(models.Model)` — defines a model named `Student`. Django auto-creates an `id` primary key (`BigAutoField`) unless you override it. The table will be named `portfolio_student` (app name + underscore + model name, lowercase).
- Lines 5–7: Three fields — `name` (varchar 100), `age` (integer), `city` (varchar 100). Each field type (`CharField`, `IntegerField`) maps to a SQL column type.
- Line 9: `def __str__(self)` — defines the human-readable representation of each record. Used in the admin's list view, shell, and logs. Without it, the admin shows `Student object (1)` — with it, it shows the student's name.

### The Profile Model

```python
class Profile(models.Model):
    bio = models.TextField()
    location = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.location
```

**Explanation:**
- `bio` — `TextField()` — unlimited-length text, no `max_length` constraint.
- `location` — `CharField(max_length=100)` — same as `Student.name`.
- `birth_date` — `DateField()` — stores a calendar date (year-month-day). This field initially had a type discrepancy (see Migration Evolution below).

### How Tables Are Created: Makemigrations + Migrate

Django separates schema definition from schema application:

1. **`python manage.py makemigrations`** — Scans your `models.py` files across all installed apps and generates migration files (Python files that describe `CREATE TABLE` and `ALTER TABLE` operations). It does **not** touch the database.
2. **`python manage.py migrate`** — Reads migration files and applies them to the database (`db.sqlite3`). This creates the actual tables.

The two-step process keeps migrations version-controlled and reviewable before they touch data.

### Model Field Reference (Used in This Lecture)

| Field | Purpose | Maps to SQL |
|---|---|---|
| `BigAutoField` | Auto-incrementing primary key (Django default `id`) | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| `CharField(max_length=N)` | Short text with max length | `VARCHAR(N)` |
| `IntegerField()` | Whole number | `INTEGER` |
| `TextField()` | Long text, no length limit | `TEXT` |
| `DateField()` | Calendar date | `DATE` |

### How Models Appear in Admin

Registering a model in `admin.py` is the only step needed for it to appear in the admin:

```python
# portfolio/admin.py — both models registered
from django.contrib import admin
from portfolio.models import Student, Profile

admin.site.register(Student)
admin.site.register(Profile)
```

**Explanation:**
- Line 2: Imports the admin site and the two model classes. The import uses the app name (`portfolio.models`) as the Python package path.
- Line 6: `admin.site.register(Student)` — adds `Student` to the admin's model registry. After the next server reload, `Student` appears under the "Portfolio" section in the admin sidebar.
- Line 7: Same for `Profile`.
- Line 3 is a commented-out duplicate import (`# from portfolio.models import Profile`) — a common beginner artifact from trying imports in pieces before consolidating.

> [!NOTE]
> **`__str__` impact on admin:** Without `__str__`, the admin's model list shows raw object references like `Student object (1)`, `Profile object (1)`. With `__str__` defined, it shows meaningful names — student names and profile locations. This is a small line that makes the admin dramatically more usable.

---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **Model** | A Python class describing data | Class subclassing `models.Model`; fields = columns; each instance = a row | the app's memory |
| **Field type** | The kind of data a column stores | `CharField`, `IntegerField`, `DateField`, etc. — each maps to a SQL type | the column's shape |
| **`__str__`** | How a model object prints | Method returning a string; used in admin list, shell, logs | the shelf label |
| **Migration** | A version-controlled schema change | A Python file in `migrations/` with `operations` (create, alter, delete) | a renovation permit |
| **`makemigrations`** | Generate migration files from models | Scans `models.py` and writes migration files — does not touch the database | drawing the blueprint |
| **`migrate`** | Apply migrations to the database | Runs `makemigrations` output against `db.sqlite3` — creates/alters tables | building the room |
| **`admin.site.register()`** | Add a model to admin | Tells the admin site to generate CRUD UI for the model | adding to the directory |
| **`BigAutoField`** | Auto-incrementing ID | Django's default primary key type; integer that auto-increments | the row's badge number |
| **`CharField(max_length=N)`** | Short text | Requires `max_length`; maps to `VARCHAR(N)` | the name tag |
| **`TextField()`** | Long text | No `max_length`; maps to `TEXT` | the whiteboard |
| **`DateField()`** | A calendar date | Stores `YYYY-MM-DD`; validated as a real date | the calendar entry |
| **Table name** | How Django names database tables | `appname_modelname` (e.g., `portfolio_student`, `portfolio_profile`) | the locker label |

---

## 💡 Real-World Analogy

**Models are the table of contents in a filing cabinet.** Each model (Student, Profile) is a tab — it defines what information each drawer holds (name, age, city for Student; bio, location, birth date for Profile). The field types are the **paper types** you can file: a form (CharField — limited space), a number pad (IntegerField), a calendar slip (DateField). `makemigrations` is the act of printing the filing instructions. `migrate` is the act of actually building the drawers in the cabinet. `admin.site.register()` is filing the drawer in the front office so staff can open it.

---

## ❌ Common Beginner Mistakes

1. **Forgetting `makemigrations` after adding a model** — The model exists in Python but no table is in the database. Visiting admin shows nothing or raises an error. Fix: run `makemigrations portfolio` then `migrate`.

2. **Registering a model before it's defined in `models.py`** — `admin.py` imports from `models.py`; if the model class doesn't exist yet, `ImportError` fires at startup. Fix: define the model first.

3. **Not adding the app to `INSTALLED_APPS` before `makemigrations`** — `makemigrations portfolio` fails silently or says "No changes" if the app isn't registered. Django only scans apps in `INSTALLED_APPS`. Fix: uncomment `'portfolio',` in `INSTALLED_APPS`.

4. **Missing `__str__` method** — The admin list view shows `Student object (1)` instead of meaningful names. Fix: add a `__str__` method returning a human-readable attribute.

5. **Changing a field type in `models.py` without running `makemigrations`** — The model definition and the database column diverge. Fix: run `makemigrations` (it will detect the change and generate an `AlterField` operation) then `migrate`.

---

## 🧠 Common Misconceptions

| ✅ Models ARE … | ❌ They are NOT … |
|---|---|
| Python classes defining data schema | The same as database tables (they're a layer *above* tables) |
| Applied to the database via `migrate` | Automatically reflected in the DB when you write them |
| Required for admin to show anything | Optional — admin works without models but shows "nothing to manage" |
| Identified by the class name + app name (`portfolio_student`) | Named by the file name or table alias |
| Extended by `__str__` for human readability | Shown as raw memory addresses by default |

---

## 🧪 Practical Example

```python
# portfolio/models.py — complete model definitions
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    bio = models.TextField()
    location = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.location
```

**Explanation:**
- Lines 1–2: Import Django's model base class and field types.
- Lines 4–10: `Student` model with three fields and a `__str__` returning `name`. The table created in SQLite will be `portfolio_student` with columns: `id` (BigAutoField, auto), `name` (varchar 100), `age` (integer), `city` (varchar 100).
- Lines 12–17: `Profile` model with three fields and a `__str__` returning `location`. Table: `portfolio_profile` with columns: `id`, `bio` (text), `location` (varchar 100), `birth_date` (date).
- The `__str__` methods are the only "Python logic" in the models — everything else is field declarations that Django translates to SQL.

---

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. What do `makemigrations` and `migrate` each do?**
A: `makemigrations` scans your model files and generates migration files (describing schema changes). `migrate` applies those migration files to the database, creating or altering actual tables. One writes the plan, the other executes it.

**Q2. Why does a model need `__str__`?**
A: It defines the human-readable name for each object. In the Django admin list view, each row shows the `__str__` value instead of `ModelName object (id)`. It's also used in the shell, logging, and error messages.

**Q3. What happens if you define a model but forget to register it in admin?**
A: The model still creates a database table via migrations and can be queried through the ORM, but it will not appear in the admin interface. Registration in `admin.py` is what makes a model manageable through the admin UI.

**Q4. How does Django name a database table for a model?**
A: `<app_name>_<model_name>` in lowercase. For `Student` in the `portfolio` app → `portfolio_student`. The auto-created `id` primary key column has no prefix.

**Q5. What happens when you change a field type in `models.py` and run `makemigrations`?**
A: Django detects the change and generates an `AlterField` migration operation that modifies the column type in the database when you run `migrate`. In A027, `birth_date` went from `IntegerField` to `DateField` via migration 0003.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. What two commands bridge model definitions to database tables, and what does each do?

<details><summary>Answer</summary>

`makemigrations` generates migration files from `models.py` (writes the plan to disk, no DB change). `migrate` applies migration files to the database (executes the plan, creates/alters tables in `db.sqlite3`).
</details>

2. What three things must be true for a model to appear in the admin?

<details><summary>Answer</summary>

1. The app must be in `INSTALLED_APPS` (`'portfolio',` in `settings.py`). 2. The model must be registered in the app's `admin.py` (`admin.site.register(Student)`). 3. The migration must be applied (`migrate` — the table must actually exist in the database).
</details>

3. What does `__str__` control in the admin?

<details><summary>Answer</summary>

`__str__` controls what text is shown for each model instance in the admin list view, the shell, and logs. Without it: `Student object (1)`. With it: the student's name (or whatever the method returns).
</details>

4. Why does `makemigrations` say "No changes detected" even though a model was added?

<details><summary>Answer</summary>

The app is not in `INSTALLED_APPS`. Django only scans models in registered apps for migration generation. Fix: add the app to `INSTALLED_APPS` then re-run `makemigrations`.
</details>

5. In the A027 artifact, what changed between migration 0002 and 0003?

<details><summary>Answer</summary>

The `birth_date` field on `Profile` changed from `models.IntegerField()` to `models.DateField()`. Migration 0002 initially created it as an integer (incorrect for a date), and migration 0003 altered it to the correct date type via `migrations.AlterField`.
</details>

---

## 📝 Quick Revision

| Concept | Command / Location | Key Detail |
|---|---|---|
| Define a model | `app/models.py` | Subclass `models.Model`, fields as class attributes |
| Generate migrations | `python manage.py makemigrations` | Scans models, writes migration files, no DB change |
| Apply migrations | `python manage.py migrate` | Runs migrations against `db.sqlite3` |
| Register in admin | `app/admin.py` | `admin.site.register(Model)` |
| Human-readable name | `__str__(self)` in model class | Returns a string; shown in admin list |
| Table name convention | Auto | `<app>_<model>` lowercase (e.g., `portfolio_student`) |
| Field → SQL type | Field class | `CharField`→VARCHAR, `IntegerField`→INT, `DateField`→DATE, `TextField`→TEXT |

---

## 🧠 Final Mental Model

The path from Python class to admin row has **four stations**:
1. **`models.py`** — You define: "I need a Student with name, age, city."
2. **`makemigrations`** — Django translates: "Got it — I'll create a `portfolio_student` table with these columns."
3. **`migrate`** — SQLite builds: "Table created, columns ready."
4. **`admin.site.register()`** — Admin announces: "Students are now manageable at `/admin/`."

If any station is skipped, the chain breaks silently. A026 had station 4 (admin) working but stations 1–3 empty. A027 fills stations 1–3 and connects the chain end-to-end.

---

## ❓ FAQ

**Q1. Can you register a model without creating a database table?**
A: Yes — `admin.site.register()` works at Python import time, but attempting to view or interact with the model in the admin will raise a database error because the table doesn't exist. The table must be created via `migrate` first.

**Q2. What is the difference between `makemigrations` and `migrate` in one sentence?**
A: `makemigrations` writes the change plan; `migrate` executes it.

**Q3. Why does `models.py` import `from django.db import models` and not something else?**
A: `django.db.models` is the module that provides the model base class (`models.Model`) and all field types (`CharField`, `IntegerField`, etc.). It is the ORM's public API for schema definition.

**Q4. Can the same model appear under multiple apps in the admin?**
A: A model belongs to exactly one app (determined by which app's directory contains `models.py`). You can reference models from other apps in foreign keys, but the model itself lives in one app and is registered in that app's `admin.py`.

**Q5. What does the commented-out `# from portfolio.models import Profile` in `admin.py` tell us?**
A: It's a leftover from the development process — the developer initially imported `Student` and `Profile` separately, then consolidated into a single import line. It's harmless (commented out) but shows the natural iteration of writing admin registration code.

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Model definition:** I can define a model with `CharField`, `IntegerField`, `DateField`, `TextField`, and `__str__` — *§Models & Admin Registration*
- [ ] **Checkpoint 2 — Migration flow:** I can explain what `makemigrations` and `migrate` do and why they are separate — *§How Tables Are Created*
- [ ] **Checkpoint 3 — Admin registration:** I can register a model in `admin.py` and explain the three prerequisites for it to appear in the admin — *§How Models Appear in Admin*

---

## 🏋️ Exercises

- **Level 1 — Recall:** Name the three prerequisites for a model to appear in the Django admin. List all five field types used in `Student` and `Profile`.
- **Level 2 — Understanding:** In the A027 artifact, `birth_date` was first `IntegerField`, then `DateField`. Why is `IntegerField` wrong for a date? What would happen if migration 0003 was never created?
- **Level 3 — Application:** Create a `Book` model with fields `title` (CharField 200), `author` (CharField 100), `published_year` (IntegerField), `summary` (TextField), `is_available` (BooleanField). Run `makemigrations` and `migrate`. Register it in admin. Verify it appears at `/admin/`.
- **Level 4 — Interview reasoning:** A junior developer says: "I added a model, ran the server, and it doesn't show in admin." Walk through the entire chain (INSTALLED_APPS → models.py → admin.py → makemigrations → migrate → server reload) to diagnose the issue.

---

## 🏁 Final Takeaways

1. Models are Python classes that define database schema — fields map to columns, `__str__` maps to display names.
2. `makemigrations` generates the plan; `migrate` executes it — both are required for a table to exist.
3. `admin.site.register()` makes a model manageable in the admin — but only if the app is in `INSTALLED_APPS` and the table exists.
4. Field type changes require new migrations: `makemigrations` detects them, `migrate` applies them (A027's `birth_date` IntegerField → DateField is the live example).
5. The A027 artifact shows the admin at full readiness: models defined, registered, tables created — ready for A028's customization.

## 🔄 Next Lecture Connection

A028 will customize the admin interface with `ModelAdmin` classes — controlling list display columns, adding search, sorting, and filters. The models are now registered (this lecture's foundation); A028 makes them *useful* in the admin. See [A028 — Admin List Display, Searching, Sorting & Filters](../A028_Admin_List_Display_Searching_Sorting_&_Filters/README.md).

---

<div class="doc-footer">

**Sources used:** `myProject15/` artifact (Django 6.1.1): `settings.py` (portfolio now in INSTALLED_APPS, DIRS updated, STATICFILES_DIRS set), `portfolio/models.py` (Student + Profile models), `portfolio/admin.py` (both models registered), `portfolio/migrations/0001_initial.py` (Student table), `0002_profile.py` (Profile table with IntegerField birth_date), `0003_alter_profile_birth_date.py` (birth_date → DateField), `db.sqlite3` (applied migrations). Reference: `docs/MEMORY.md` (A022 model/migration conventions, A026 admin prerequisites). No lecture transcript in folder — chapter built from on-disk artifact and official Django documentation.

**Navigation:** ← [A026 — Django Admin & Superuser](../A026_Django_Admin_&_Superuser/README.md) · [Series hub](../../README.md) · [A028 — Admin List Display, Searching, Sorting & Filters](../A028_Admin_List_Display_Searching_Sorting_&_Filters/README.md) →

</div>
