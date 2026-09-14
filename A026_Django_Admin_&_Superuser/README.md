# 🚀 A026 — Django Admin & Superuser

`📖 Lecture A026` · `🎓 Track: Core Django` · `📶 Level: Beginner` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the generated artifact `myProject15/` — a fresh Django 6.1.1 project with a `portfolio` app created via `startapp` but intentionally **not yet registered** in `INSTALLED_APPS`. All file references below are quoted verbatim from the on-disk artifact.

---

## 🧭 What You Will Learn

- [ ] How Django's auto-generated admin site works and why it ships as a built-in app
- [ ] How the admin URL is wired into the project and what `path('admin/', admin.site.urls)` does
- [ ] How to create a superuser with `python manage.py createsuperuser` and log in
- [ ] Why models must be registered in `admin.py` to appear in the admin interface
- [ ] The difference between a registered-but-empty admin and an admin with model registrations

## 🎯 Why This Lecture Matters

The Django admin is one of the framework's most powerful built-in features. It provides a fully functional back-office UI for managing data — creating, reading, updating, and deleting records — without writing a single view or template. Understanding how it is enabled, configured, and extended is essential because nearly every Django project uses the admin for internal management, even if the public-facing site is entirely custom.

This lecture establishes the *prerequisites*: the admin site must be in `INSTALLED_APPS`, the URL must be mounted, and a superuser account must exist before anything is visible. These are the three gates every Django developer passes through before customizing the admin for a real project.

## ✅ Prerequisites

- [ ] A Django project running with `manage.py runserver` (covered in A004–A005)
- [ ] An app scaffolded with `python manage.py startapp` and listed in `INSTALLED_APPS` (covered in A006)
- [ ] Basic understanding of `settings.py` and `urls.py` (covered in A004, A007)
- [ ] 📌 Familiarity with `python manage.py migrate` (covered in A022)

## 🧠 Django Admin & Superuser

### What Is the Django Admin?

The Django admin is an auto-generated web interface for managing models. It is not a feature you build — it is a feature Django ships with you. When you register a model in `admin.py`, Django generates HTML forms, lists, and detail pages for that model at the `/admin/` URL. It handles authentication, permissions, validation, and database operations out of the box.

### Why Does It Exist?

Every project needs a back office: someone must add, edit, or delete records. Building this from scratch each time is repetitive and error-prone. The admin solves this by reading your model definitions (Python classes in `models.py`) and generating the UI dynamically. It enforces the same rules the ORM does (field types, constraints, relationships) and never bypasses them.

### How It Is Enabled

Three things must be true for the admin to work:

1. **`django.contrib.admin` is in `INSTALLED_APPS`** — This enables Django's admin app (and its dependencies: auth, contenttypes, sessions, messages).
2. **`path('admin/', admin.site.urls)` is in the root `urls.py`** — This mounts the admin at a URL path.
3. **A superuser account exists** — The admin requires authentication; only superusers can access it by default.

### The Artifact's State (`myProject15/`)

The `myProject15` project has the admin *halfway* ready:

- `myProject15/myProject15/settings.py` line 34: `'django.contrib.admin',` — present in `INSTALLED_APPS`
- `myProject15/myProject15/urls.py` line 21: `path('admin/', admin.site.urls),` — mounted
- The `portfolio` app exists but is **not registered** (line 40: `# 'portfolio',` commented out)

This means the admin *site* is accessible, but no custom models are visible in it. The lecture's learning goal is to reach this understanding — the admin works before any model is registered, but it is *useless* until models are registered and a superuser is created.

### Creating a Superuser

A superuser is a special account with full access to the admin. Create one with:

```bash
python manage.py createsuperuser
```

You will be prompted for a username, email (optional), and password. This command creates an auth user record in `db.sqlite3` using the `django.contrib.auth` app (which is in `INSTALLED_APPS` by default).

> [!WARNING]
> **No superuser exists in `myProject15/`'s database yet.** The `db.sqlite3` file exists (created by `runserver`'s first migration) but contains no custom data. Until `createsuperuser` runs, visiting `/admin/` shows a login page with no valid credentials.

### What You See After Login

Once authenticated, the admin shows a list of registered models under each app. The `auth` app (Django's built-in) shows **User** and **Group** models by default. Any custom app registered in `INSTALLED_APPS` with a registered model would appear under its app name. In `myProject15`, since `portfolio` is commented out and has no models registered, the admin shows only Django's built-in auth models.

### Registering a Model

To make a model manageable in the admin, open the app's `admin.py` and register it:

```python
from django.contrib import admin
from .models import Student

admin.site.register(Student)
```

The artifact's `portfolio/admin.py` contains only the stub comment `# Register your models here.` — no registrations yet. Similarly, `portfolio/models.py` is empty (`# Create your models here.`). This is deliberate: registering models is a later step. The admin infrastructure (URLs, superuser, authentication) is the foundation this lecture builds.

---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **Admin site** | Auto-generated management UI for models | `django.contrib.admin` app; serves model CRUD at `/admin/` | the staff-only back office |
| **Superuser** | A user with full admin access | An `auth.User` instance with `is_superuser=True` and `is_staff=True`; created via `createsuperuser` | the master key |
| **`admin.site`** | The admin site instance | A `AdminSite` object; `admin.site.register(Model)` adds a model to it | the registration desk |
| **`createsuperuser`** | A management command to create an admin account | `python manage.py createsuperuser`; creates an `auth.User` with `is_staff=True` | creates the VIP pass |
| **ModelAdmin** | Controls how a model appears in admin | A class subclassing `ModelAdmin` (or a function passed to `register()`); default behavior is auto-generated | the display settings for each model |
| **`INSTALLED_APPS`** | The app registry in settings | List of app names Django activates; `django.contrib.admin` must be present for admin to work | the mall directory — admin must be listed |
| **`/admin/` URL** | The URL path to the admin | `path('admin/', admin.site.urls)` in root `urls.py`; the admin is mounted at this prefix | the staff entrance |
| **`is_staff`** | Whether a user can access admin | Boolean field on `auth.User`; only `True` users can log in to `/admin/` | the staff badge |

---

## 💡 Real-World Analogy

**The admin is a corporate office building.** When a company grows, not every employee should have access to every room. The admin site is the *executive floor*: it requires a special badge (superuser / `is_staff=True`), and the rooms inside (model lists, detail pages) are built automatically from the company's inventory (models defined in `models.py`). But if no inventory is registered (models not in `admin.py`), the executive floor has empty rooms. And if the building's access control (`django.contrib.auth`) isn't installed (`INSTALLED_APPS`), there is no badge system at all — the doors are just open, which is worse.

---

## ❌ Common Beginner Mistakes

1. **Forgetting to add `django.contrib.admin` to `INSTALLED_APPS`** — The admin URLs exist but the site crashes at runtime because the admin app hasn't been activated. Django raises an `ImproperlyConfigured` error when the URL is accessed without the app installed. Fix: ensure `'django.contrib.admin',` is in `INSTALLED_APPS`.

2. **Not creating a superuser before visiting `/admin/`** — The login page appears, but no credentials work. The database has user tables (from `django.contrib.auth`) but no users. Fix: run `python manage.py createsuperuser`.

3. **Registering a model without it being in an installed app** — If `portfolio` is not in `INSTALLED_APPS` (commented out in `myProject15/settings.py`), even a registered model in `portfolio/admin.py` will not appear in the admin. Django ignores unregistered apps entirely. Fix: uncomment `'portfolio',` in `INSTALLED_APPS` and re-run `migrate`.

4. **Confusing `admin.site.register()` placement** — Calling `admin.site.register()` at import time is correct. Importing models in `admin.py` before they exist (e.g., before `models.py` is written) causes an `ImportError`. The model must be defined before it can be registered.

---

## 🧠 Common Misconceptions

| ✅ Django Admin IS … | ❌ It is NOT … |
|---|---|
| An auto-generated UI for models defined in `models.py` | A public-facing website builder |
| Protected by Django's authentication system (`is_staff`) | An open API accessible without login |
| Extended by registering models in `admin.py` | Something you must manually code views for |
| Enabled by three conditions: `INSTALLED_APPS`, URL mount, superuser | Automatically visible just because Django is installed |
| Capable of CRUD on any registered model | Limited to only the models with `ModelAdmin` classes (default registration works too) |

---

## 🧪 Practical Example

```python
# portfolio/admin.py — registering a model in the admin
from django.contrib import admin
from .models import Student

# Default registration — Django auto-generates add/change/list pages
admin.site.register(Student)
```

**Explanation:**
- Line 1: Import `admin` from `django.contrib.admin` — this provides the `admin.site` registry.
- Line 2: Import the `Student` model from the app's `models.py` — the model must be defined before registration.
- Line 5: `admin.site.register(Student)` tells the admin site: "when you render the list of models, include `Student`." Django automatically creates list views (showing all fields), add forms (validating field types/constraints), and change forms (editing existing records) — no templates or views written by hand.

---

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. What are the three requirements for the Django admin to work?**
A: (1) `django.contrib.admin` must be in `INSTALLED_APPS`, (2) `path('admin/', admin.site.urls)` must be in the root `urls.py`, and (3) a superuser must exist in the database. Missing any one of these means the admin is either non-functional, inaccessible, or shows an empty login page.

**Q2. What does `admin.site.register(MyModel)` actually do?**
A: It registers the model with Django's admin site (`AdminSite`), which tells Django to auto-generate CRUD views, templates, and URLs for that model. The model then appears in the admin interface under its app's name when a superuser is logged in.

**Q3. Why does `/admin/` return a login page instead of the model list?**
A: Two possible reasons — either no superuser was created (the database has the auth tables but no user records), or the user attempting access is not a superuser (`is_staff=False`). The admin enforces authentication and `is_staff` permission at the middleware/view level.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. What three things must be true for `/admin/` to show the model list?

<details><summary>Answer</summary>

1. `django.contrib.admin` is in `INSTALLED_APPS` (in `settings.py`). 2. The root `urls.py` has `path('admin/', admin.site.urls)` (a mounted URLconf). 3. A superuser account exists in the database (created via `python manage.py createsuperuser` with `is_staff=True`).
</details>

2. What command creates a superuser, and what fields does it prompt for?

<details><summary>Answer</summary>

`python manage.py createsuperuser`. It prompts for: **username** (required), **email** (optional — depends on `USER_EMAIL_FIELD`), and **password** (typed silently, confirmed). It creates an `auth.User` record with `is_superuser=True` and `is_staff=True`.
</details>

3. What happens if an app is in `INSTALLED_APPS` but its `admin.py` never calls `register()`?

<details><summary>Answer</summary>

The app is active and its models are available to the ORM, but nothing appears in the admin interface. The admin only shows models that have been explicitly registered. The app is invisible to the admin despite being a registered Django app.
</details>

4. Why does `myProject15/`'s `/admin/` show only Django's built-in auth models?

<details><summary>Answer</summary>

Because the only models registered in any app's `admin.py` are Django's built-in ones (from `django.contrib.admin` and `django.contrib.auth`). The `portfolio` app is not in `INSTALLED_APPS` (commented out at `settings.py` line 40), its `admin.py` is a stub with no registrations, and its `models.py` has no model definitions. No custom model has been registered.
</details>

---

## 📝 Quick Revision

| Requirement | Where | Command/Setting |
|---|---|---|
| Admin app activated | `settings.py` → `INSTALLED_APPS` | `'django.contrib.admin',` |
| Admin URL mounted | `urls.py` → `urlpatterns` | `path('admin/', admin.site.urls)` |
| Superuser created | Terminal | `python manage.py createsuperuser` |
| Model visible in admin | App's `admin.py` | `admin.site.register(Model)` |
| Access control | `auth.User` model | `is_staff=True`, `is_superuser=True` |

---

## 🧠 Final Mental Model

The admin site is a **department store** that opens only with three keys:
- **Key 1**: The store license (`INSTALLED_APPS` includes admin) — without it, the building doesn't exist.
- **Key 2**: The address plaque (`urls.py` has `admin/` route) — without it, customers can't find the store.
- **Key 3**: The manager (superuser) — without a manager, the doors open but nobody can stock or retrieve anything.

Only when all three keys are present can you walk in (`/admin/`), log in as manager, and see all registered departments (models in `admin.py`). The `portfolio` app in `myProject15` is a **leased storefront** — the space is built (app scaffolded), but it hasn't been leased to the mall (`INSTALLED_APPS`), so it appears dark and empty.

---

## ❓ FAQ

**Q1. Does the admin work without any models registered?**
A: Yes, the admin site loads and shows a login page. After login with a superuser, it shows "You don't have any models to manage" (or Django's built-in auth models if present). The admin *site* works — the admin *content* requires registered models.

**Q2. Can I change the admin URL from `/admin/` to something else?**
A: Yes — change the route in `urls.py`: `path('secret/', admin.site.urls)` makes the admin available at `/secret/`. Security through obscurity is not a substitute for authentication, but it does reduce automated bot scanning.

**Q3. What is the difference between `is_staff` and `is_superuser`?**
A: `is_staff` = "can access the admin site" (login to `/admin/`). `is_superuser` = "can do everything" including creating other superusers, deleting any model, and accessing all permissions. A superuser always has `is_staff=True`, but a staff user can have `is_superuser=False` (limited admin access).

**Q4. Why is `portfolio` commented out in `INSTALLED_APPS` in `myProject15`?**
A: Because the lecture is building up to the admin — the app exists (created by `startapp`) but is intentionally not yet registered. This teaches that creating an app and *registering* it are two separate steps (A006's core lesson: `startapp` scaffolds; it does not register).

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Admin prerequisites:** I can name the three requirements (INSTALLED_APPS, URL mount, superuser) and explain what each one does — *§Django Admin & Superuser*
- [ ] **Checkpoint 2 — Superuser creation:** I can run `python manage.py createsuperuser` and explain what it stores in the database — *§Creating a Superuser*
- [ ] **Checkpoint 3 — Model registration:** I can explain why `portfolio` doesn't appear in the admin despite existing as an app — *§Registering a Model*

---

## 🏋️ Exercises

- **Level 1 — Recall:** Name the three conditions for the admin to work. List what each file (`settings.py`, `urls.py`, terminal command) contributes.
- **Level 2 — Understanding:** In `myProject15/`, the `portfolio` app exists but is commented out in `INSTALLED_APPS`. What happens if you uncomment it, run `migrate`, but don't register any models in `admin.py`? What does the admin show after login?
- **Level 3 — Application:** Create a `Student` model in `portfolio/models.py` with fields `name` (CharField) and `age` (IntegerField), uncomment `portfolio` in `INSTALLED_APPS`, run `makemigrations` + `migrate`, register it in `admin.py`, create a superuser, and verify it appears at `/admin/`.
- **Level 4 — Interview reasoning:** A junior developer says: "I created the app, so it should show in the admin automatically." Explain why this is wrong, referencing the difference between `startapp`, `INSTALLED_APPS`, and `admin.site.register()`.

---

## 🏁 Final Takeaways

1. The Django admin is an auto-generated management interface — it ships built-in and only requires activation, mounting, and a superuser to access.
2. Three gates must be open: `INSTALLED_APPS` (license), `admin/` URL (address), superuser (manager badge).
3. `python manage.py createsuperuser` creates the account; without it, the admin is locked.
4. Models only appear in the admin when explicitly registered via `admin.site.register()` — app existence ≠ admin visibility.
5. The `myProject15` artifact deliberately shows the admin *halfway* ready: site functional, no custom models — a teaching state.

## 🔄 Next Lecture Connection

A027 will register models in the admin (the `admin.py` step A026 sets up) and customize the admin with `ModelAdmin` classes (list display, search, filters). The `Student` model from A022–A025 is the natural first model to register, as it was already defined and queried in earlier lectures.

---

<div class="doc-footer">

**Sources used:** Generated artifact `myProject15/` (Django 6.1.1): `settings.py`, `urls.py`, `portfolio/admin.py`, `portfolio/models.py`, `portfolio/views.py`, `portfolio/urls.py`, `portfolio/apps.py`. Reference: `docs/MEMORY.md` (A006 startapp contract, A022 model/migration conventions, A004 admin/`runserver` context). No lecture transcript found in folder — chapter built from on-disk artifact and official Django documentation.

**Navigation:** ← [A025 — Display Table Data in Django Template](../A025_Display_Table_Data_in_Django_Template/README.md) · [Series hub](../../README.md) · [A027 — TBD](../../README.md) →

</div>
