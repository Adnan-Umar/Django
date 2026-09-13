# 🚀 A021 — ORM: Object-Relational Mapping

`📖 Lecture A021` · `🎓 Track: Core Django` · `📶 Level: Beginner` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** this chapter is built from a **sixteenth standalone
> artifact** — the `ORM.py` file dropped directly into this folder (6 lines, 81 bytes), a
> teaching snippet that names the lecture's central type and two of its fields. It is
> **not** a runnable `startproject`/`startapp` project (no `manage.py`, no `myProject*`,
> no migrations, no server to start) — it is the series' first **conceptual-bridge
> snippet**, marking the moment the curriculum pivots from *templates and the request
> pipeline* (A001–A020) to *the database layer*.
>
> The snippet is quoted verbatim below. Every claim about class→table, field→column,
> manager→queryset, and migration behavior is sourced from the **official Django docs**
> (`Model class`, `migrations overview`, `making queries`) — flagged 📌 in place. No
> transcript exists. `commands.txt` adds no lines — the journal still ends at A019's line
> 29 (`npm run dev`). Django 6.1.1 (the system interpreter) is the reference version.

---

## 🧭 What You Will Learn

- [ ] Translate a **Python class** into a **database table** — explain how `class Student`
  becomes an `students` table and `name`/`age` become columns with types
- [ ] Read the two halves of every model field: **the Python type** (what you write) and
  the **database column** it maps to (what ships to SQL) — and name the one argument
  every `CharField` must carry that `IntegerField` never sees
- [ ] Call **`Student.objects.all()`** correctly — and spot the `.object` typo in the
  artifact as the exact place where a *manager* (not a method you write) lives
- [ ] State what **`.objects`** really is (not a method you write) and why it arrives
  automatically on every model
- [ ] Predict the three steps Django needs before `Student.objects.all()` can return real
  rows — and why the artifact's 0-byte `db.sqlite3` (eighth artifact running) blocks all three
- [ ] Trace **A020's `db.sqlite3` (0 B)** → **A021's `Student` model** → the **migrations**
  that would grow the database — the bridge between the template-only artifacts and the
  data layer

---

## 🎯 Why This Lecture Matters

A001's `Restaurant` mental model always had a silent gap. The waiter (view), the kitchen
(model/ORM), the plating (template), and the dish (response) — but **the kitchen had no
ingredients**. Through A020 the series served pages from context dictionaries, hardcoded
lists, and static files, but `db.sqlite3` sat at **0 bytes** (A016 — seventh artifact
running; A020 — eighth). The `models.py` file in `myProject12/` was empty, and the admin
(`/admin/`) returned **302** → login → **302** in an endless loop, because no migrations
had ever created the `auth_user` table.

A021 opens that gap. The snippet `ORM.py` is six lines that state the **one fact** every
Django model needs:

```python
# A021_ORM_(Object_Relational_Mapping)/ORM.py (verbatim, 6 lines)
class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()

    student = Student.object.all()
```

That class is a **promise**: define a Python class like this, and Django will (a) create a
database table named `students`, (b) map `name` → a `varchar` column and `age` → an
`integer` column, and (c) hand you a **manager** — `.objects` — that is your Python
handle to SELECT/INSERT/UPDATE/DELETE rows. Nothing about this snippet runs on its own:
`models.Model` is undefined without Django's stack, `CharField()` needs a `max_length`
argument, and `.object` is a typo (the manager is `.objects`). Those errors are the
chapter's teaching points, not accidents.

What breaks if you skip it: A022 (migrations) and A023 (queries) will read as magic
incantations if you never see the *why*: a model is a **declarative table schema in
Python syntax**, and the manager is the **gatekeeper query object** every Django model
receives for free. This snippet is the hinge — the last artifact before the series learns
to grow a database from a 0-byte file into something that answers real queries.

---

## ✅ Prerequisites

- [ ] **A013** — `render(request, name, context_dict)`: the context dict is the Python
  data handed to a template; the ORM's `QuerySet` is the Python data handed to a view
- [ ] **A020** — the 0-byte `db.sqlite3` and the 302-loop admin: the exact doors A021
  unlocks; root-mounted `portfolio` app; `{% csrf_token %}` form with no handler
- [ ] **A001** — the `Restaurant` mental model's missing ingredient: where data lives
- [ ] **A007** — views return `HttpResponse`; the view layer (waiter) and the model layer
  (kitchen) are where A021 inserts the ingredients the waiter will later serve

---

## 🧠 Core Idea — The Translation Layer: Python Class to SQL Table

### Definition: what a model really is

A Django **model** is a Python class that subclasses `models.Model`. Each attribute
you declare on the class becomes a **column** on the corresponding **database table**.
Django performs the translation:

| Python (what you write) | Django field | SQL (what ships) |
|---|---|---|
| `class Student(models.Model)` | (implicit) | `students` table |
| `name = models.CharField(...)` | `CharField` | `varchar(N)` |
| `age = models.IntegerField()` | `IntegerField` | `integer` |

The artifact, quoted verbatim:

```python
# A021_ORM_(Object_Relational_Mapping)/ORM.py (verbatim, 6 lines)
class Student(models.Model):
    name = models.CharField()
    age = models.IntegerField()

    student = Student.object.all()
```

Three lines declare the schema; the fourth line is the **teaching error**.

### Why it exists: the impedance mismatch

Databases speak **SQL**: rows, columns, `VARCHAR(255)`, foreign keys as integers. Python
speaks **objects**: attributes, method calls, string types with no length cap. The **ORM**
(Object-Relational Mapper) is Django's translation layer: you write Python, it generates SQL,
and it hands you back Python objects — never raw SQL in your views.

### The field→column contract

Every Django field type encodes exactly **two** decisions:

1. **The database column type** — `CharField` → `varchar`, `IntegerField` → `integer`,
   `TextField` → `text`, `BooleanField` → `boolean`, etc.
2. **Any field-specific arguments** — and `CharField` has exactly one that is
   **mandatory**: `max_length`. Here is why:

📌 **`CharField` must carry `max_length`** because the SQL it maps to (`varchar(N)`)
requires a column width. `IntegerField` maps to `integer` (a fixed type with no
argument), so it needs none. Django's `check` framework will refuse to migrate a
`CharField` without `max_length`: `E132: Field 'name' can only be a CharField with a
max_length argument` — the framework catches it before SQL touches the database.

The artifact's `CharField()` is therefore **deliberately incomplete** — it states "this
is a text column of variable length" without committing to the width. A real model must
write `models.CharField(max_length=100)`.

### The manager: `.objects`, not `.object`

Every Django model receives a **manager** — an attribute called `.objects` — the moment
it subclasses `models.Model`. You do **not** declare it. The manager is your query
interface: it returns `QuerySet` objects, which are lazy, chainable, and Python-native.

```
Student.objects       # the manager (auto-created, not hand-written)
Student.objects.all() # → QuerySet of all rows
Student.objects.filter(...)  # → filtered QuerySet
```

The artifact's fourth line — `student = Student.object.all()` — has **two problems**:

1. **`.object` → should be `.objects`** (plural). `Student.object` raises
   `AttributeError: type object 'Student' has no attribute 'object'`. The manager is
   `.objects`, period. This typo is the #1 beginner mistake when first touching a model
   from a Python shell — everyone writes `.object` once.
2. **It's inside the class body.** `Student.objects.all()` inside `class Student` runs at
   *class-creation time*, when the table doesn't exist yet and the manager may not be
   wired — it's a `NameError` / `AttributeError` waiting to happen. Query calls belong in
   **views**, never in the class body.

This is the hinge: in A013 the view called `render(request, 'template.html', {'key': value})` with a **hand-built** context dict. After A021, the view will call
`Student.objects.all()` to fetch the context dict **from the database**.

### The migration bridge: from 0 bytes to real tables

The artifact has no runnable server and no migrations — but it names the model that A020's
0-byte `db.sqlite3` is waiting for. The three steps Django needs before
`Student.objects.all()` returns rows:

```
1. Define the model (ORM.py: `class Student(models.Model)`)   ← A021 delivers this
2. Run `makemigrations portfolio`  → generates a migration file   ← A022
3. Run `migrate` → writes `students` table to db.sqlite3       ← A022
```

| Stage | Artifact state | Table exists? | Can query? |
|---|---|---|---|
| A016–A020 | `db.sqlite3` = 0 B, `models.py` empty | No — not even `auth_user` | N/A (no model yet) |
| A021 (this) | `ORM.py` snippet, no migration | No | Snippet won't run (`models` undefined) |
| A022 (next) | `makemigrations` → migration file | No — still just a file | No — migration not applied |
| A022+ | `migrate` → `db.sqlite3` grows | Yes | ✅ `Student.objects.all()` works |

📌 **Migrations are not optional.** Django does **not** create tables from your model
class at server startup — the class is a *declaration*, and `migrate` is the act that
materializes it into SQL. The admin's 302-loop in A020 is the symptom: the `auth_user`
table was never created because no migration was ever applied. The fix is exactly the
same one A021 needs for `Student`.

### The journey: where this snippet sits in the request cycle

The Restaurant model (A001) completes its circuit only now:

| Station | Role | Before A021 | After A021 |
|---|---|---|---|
| URL dispatcher | front door | routes `/` → view | unchanged |
| View (waiter) | builds context | `context = {'blogs': [...]}` — a **literal list** | `context = {'students': Student.objects.all()}` — a **QuerySet** |
| Model (kitchen) | holds data | **empty `models.py`** | `class Student(models.Model)` declares the table |
| Manager | query gatekeeper | (nothing) | `Student.objects` auto-created |
| Template (plating) | renders HTML | iterates the literal list | iterates the QuerySet — **identical syntax** |
| Response (dish) | HTTP reply | identical | identical |

The template layer never changes: `{% for student in students %}` works the same whether
`students` is a Python list or a Django `QuerySet`. That is the **contract**: A021 hands
the kitchen its ingredients; the waiter, plating, and dish stay exactly as A013–A020
taught them.

### The migration bridge: from 0 bytes to real tables

The artifact has no runnable server and no migrations — but it names the model that A020's
0-byte `db.sqlite3` is waiting for. The three steps Django needs before
`Student.objects.all()` returns rows:

```
1. Define the model (ORM.py: `class Student(models.Model)`)   ← A021 delivers this
2. Run `makemigrations portfolio`  → generates a migration file   ← A022
3. Run `migrate` → writes `students` table to db.sqlite3       ← A022
```

| Stage | Artifact state | Table exists? | Can query? |
|---|---|---|---|
| A016–A020 | `db.sqlite3` = 0 B, `models.py` empty | No — not even `auth_user` | N/A (no model yet) |
| A021 (this) | `ORM.py` snippet, no migration | No | Snippet won't run (`models` undefined) |
| A022 (next) | `makemigrations` → migration file | No — still just a file | No — migration not applied |
| A022+ | `migrate` → `db.sqlite3` grows | Yes | ✅ `Student.objects.all()` works |

📌 **Migrations are not optional.** Django does **not** create tables from your model
class at server startup — the class is a *declaration*, and `migrate` is the act that
materializes it into SQL. The admin's 302-loop in A020 is the symptom: the `auth_user`
table was never created because no migration was ever applied. The fix is exactly the
same one A021 needs for `Student`.

### The journey: where this snippet sits in the request cycle

The Restaurant model (A001) completes its circuit only now:

| Station | Role | Before A021 | After A021 |
|---|---|---|---|
| URL dispatcher | front door | routes `/` → view | unchanged |
| View (waiter) | builds context | `context = {'blogs': [...]}` — a **literal list** | `context = {'students': Student.objects.all()}` — a **QuerySet** |
| Model (kitchen) | holds data | **empty `models.py`** | `class Student(models.Model)` declares the table |
| Manager | query gatekeeper | (nothing) | `Student.objects` auto-created |
| Template (plating) | renders HTML | iterates the literal list | iterates the QuerySet — **identical syntax** |
| Response (dish) | HTTP reply | identical | identical |

The template layer never changes: `{% for student in students %}` works the same whether
`students` is a Python list or a Django `QuerySet`. That is the **contract**: A021 hands
the kitchen its ingredients; the waiter, plating, and dish stay exactly as A013–A020
taught them.
---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **Object-Relational Mapping (ORM)** | writing database queries in Python | a layer translating Python class/attribute access into SQL `SELECT/INSERT/UPDATE/DELETE` statements | the translator at the UN |
| **Model** | a Python class that *is* a database table | a `models.Model` subclass; one class = one table, one attribute = one column | the blueprint |
| **Field** | a column definition on a model | a class attribute like `CharField`/`IntegerField` carrying a Python type + a SQL type + optional args | the column specification |
| **`CharField`** | a text column | maps to SQL `varchar(N)`; **requires `max_length`** (Django `E132` refuses otherwise) | the measured ribbon |
| **`IntegerField`** | a whole-number column | maps to SQL `integer` (fixed type, no argument needed) | the tally counter |
| **Manager** | the query entry point on a model | the auto-created `.objects` attribute — a `Manager` instance you did **not** write | the gatekeeper |
| **`.objects`** | the manager name (plural!) | auto-attached by `ModelBase` to every `Model` subclass; never hand-declared | the plural checkpoint |
| **`QuerySet`** | a lazy, chainable list of rows | holds the *recipe* for a query; SQL isn't run until evaluated (iterate, slice, `len`, `list`, `bool`) | the unopened recipe card |
| **`.all()`** | builds a query, doesn't run it | returns a QuerySet (`SELECT * FROM …`); **lazy** — SQL waits for evaluation | the recipe you haven't cooked |
| **`.object` (typo)** | the mistake everyone makes | `Student.object` → `AttributeError`; the manager is `.objects` (plural) | the #1 stumble |
| **Migration** | a version-controlled database change file | Python file generated by `makemigrations`, executed by `migrate` as `CREATE TABLE`/`ALTER TABLE` | the construction work order |
| **`db.sqlite3` (0 B)** | an empty database promise | SQLite file from `startproject`, holding no tables until `migrate` — admin 302-loop is the symptom | the empty warehouse |

---

## 💡 Real-World Analogy — The Restaurant Kitchen's Inventory

A001 introduced the **Restaurant**: waiter (view) → kitchen (model) → plating (template) → dish (response). But through A020 the kitchen was empty — the waiter handed the plating a **literal list** of pre-written data. A021 installs the **inventory shelves** and a **catalog**:

- **The model class** is the catalog page: *"Student — columns: name (text), age (number)."* Write it once, and Django knows the shape of your data.
- **The manager (`.objects`)** is the gatekeeper at the shelf: you ask it for items, it sends a runner (a `QuerySet` recipe) to the warehouse.
- **The query set** is the recipe card: *"all students"* — written down but not executed until the plating step actually needs the ingredient.
- **The migration** is the overnight restock: the crew (`makemigrations` + `migrate`) walks into the warehouse with the catalog page and **builds the shelves** — that is when `db.sqlite3` grows from 0 bytes to a file holding the `students` table.
- **The `.object` typo** is asking the gatekeeper for "the item" when they're called "items" — the gatekeeper doesn't answer to a name you made up.

Before A021: the waiter invents the dish from memory (context dict). After A021: the waiter reads the catalog, calls the gatekeeper, the recipe fetches from the shelves, and the dish arrives — but the **kitchen's interior** (`.objects.all()`) changes, not the pass-through (`{% for %}`) or the dish itself.

### The migration bridge: from 0 bytes to real tables

The artifact has no runnable server and no migrations — but it names the model that A020's
0-byte `db.sqlite3` is waiting for. The three steps Django needs before
`Student.objects.all()` returns rows:

```
1. Define the model (ORM.py: `class Student(models.Model)`)   ← A021 delivers this
2. Run `makemigrations portfolio`  → generates a migration file   ← A022
3. Run `migrate` → writes `students` table to db.sqlite3       ← A022
```

| Stage | Artifact state | Table exists? | Can query? |
|---|---|---|---|
| A016–A020 | `db.sqlite3` = 0 B, `models.py` empty | No — not even `auth_user` | N/A (no model yet) |
| A021 (this) | `ORM.py` snippet, no migration | No | Snippet won't run (`models` undefined) |
| A022 (next) | `makemigrations` → migration file | No — still just a file | No — migration not applied |
| A022+ | `migrate` → `db.sqlite3` grows | Yes | ✅ `Student.objects.all()` works |

📌 **Migrations are not optional.** Django does **not** create tables from your model
class at server startup — the class is a *declaration*, and `migrate` is the act that
materializes it into SQL. The admin's 302-loop in A020 is the symptom: the `auth_user`
table was never created because no migration was ever applied. The fix is exactly the
same one A021 needs for `Student`.

### The journey: where this snippet sits in the request cycle

The Restaurant model (A001) completes its circuit only now:

| Station | Role | Before A021 | After A021 |
|---|---|---|---|
| URL dispatcher | front door | routes `/` → view | unchanged |
| View (waiter) | builds context | `context = {'blogs': [...]}` — a **literal list** | `context = {'students': Student.objects.all()}` — a **QuerySet** |
| Model (kitchen) | holds data | **empty `models.py`** | `class Student(models.Model)` declares the table |
| Manager | query gatekeeper | (nothing) | `Student.objects` auto-created |
| Template (plating) | renders HTML | iterates the literal list | iterates the QuerySet — **identical syntax** |
| Response (dish) | HTTP reply | identical | identical |

The template layer never changes: `{% for student in students %}` works the same whether
`students` is a Python list or a Django `QuerySet`. That is the **contract**: A021 hands
the kitchen its ingredients; the waiter, plating, and dish stay exactly as A013–A020
taught them.
---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **Object-Relational Mapping (ORM)** | writing database queries in Python | a layer translating Python class/attribute access into SQL `SELECT/INSERT/UPDATE/DELETE` statements | the translator at the UN |
| **Model** | a Python class that *is* a database table | a `models.Model` subclass; one class = one table, one attribute = one column | the blueprint |
| **Field** | a column definition on a model | a class attribute like `CharField`/`IntegerField` carrying a Python type + a SQL type + optional args | the column specification |
| **`CharField`** | a text column | maps to SQL `varchar(N)`; **requires `max_length`** (Django `E132` refuses otherwise) | the measured ribbon |
| **`IntegerField`** | a whole-number column | maps to SQL `integer` (fixed type, no argument needed) | the tally counter |
| **Manager** | the query entry point on a model | the auto-created `.objects` attribute — a `Manager` instance you did **not** write | the gatekeeper |
| **`.objects`** | the manager name (plural!) | auto-attached by `ModelBase` to every `Model` subclass; never hand-declared | the plural checkpoint |
| **`QuerySet`** | a lazy, chainable list of rows | holds the *recipe* for a query; SQL isn't run until evaluated (iterate, slice, `len`, `list`, `bool`) | the unopened recipe card |
| **`.all()`** | builds a query, doesn't run it | returns a QuerySet (`SELECT * FROM …`); **lazy** — SQL waits for evaluation | the recipe you haven't cooked |
| **`.object` (typo)** | the mistake everyone makes | `Student.object` → `AttributeError`; the manager is `.objects` (plural) | the #1 stumble |
| **Migration** | a version-controlled database change file | Python file generated by `makemigrations`, executed by `migrate` as `CREATE TABLE`/`ALTER TABLE` | the construction work order |
| **`db.sqlite3` (0 B)** | an empty database promise | SQLite file from `startproject`, holding no tables until `migrate` — admin 302-loop is the symptom | the empty warehouse |

---

## 💡 Real-World Analogy — The Restaurant Kitchen's Inventory

A001 introduced the **Restaurant**: waiter (view) → kitchen (model) → plating (template) → dish (response). But through A020 the kitchen was empty — the waiter handed the plating a **literal list** of pre-written data. A021 installs the **inventory shelves** and a **catalog**:

- **The model class** is the catalog page: *"Student — columns: name (text), age (number)."* Write it once, and Django knows the shape of your data.
- **The manager (`.objects`)** is the gatekeeper at the shelf: you ask it for items, it sends a runner (a `QuerySet` recipe) to the warehouse.
- **The query set** is the recipe card: *"all students"* — written down but not executed until the plating step actually needs the ingredient.
- **The migration** is the overnight restock: the crew (`makemigrations` + `migrate`) walks into the warehouse with the catalog page and **builds the shelves** — that is when `db.sqlite3` grows from 0 bytes to a file holding the `students` table.
- **The `.object` typo** is asking the gatekeeper for "the item" when they're called "items" — the gatekeeper doesn't answer to a name you made up.

Before A021: the waiter invents the dish from memory (context dict). After A021: the waiter reads the catalog, calls the gatekeeper, the recipe fetches from the shelves, and the dish arrives — but the **kitchen's interior** (`.objects.all()`) changes, not the pass-through (`{% for %}`) or the dish itself.
---

## ❌ Common Beginner Mistakes

1. **`.object` instead of `.objects`** — the manager is plural. `Student.object.all()`
   raises `AttributeError: type object 'Student' has no attribute 'object'`. The artifact
   commits this typo on its last line. 📌
2. **Forgetting `max_length` on `CharField`** — `CharField()` without an argument fails
   Django's model check (`E132`). SQL's `varchar` needs a width; `IntegerField` does not.
   The artifact's `name = models.CharField()` is the deliberate teaching instance of this.
3. **Writing queries in the class body** — `Student.objects.all()` as a class-level
   attribute runs at *class-creation* time, before `.objects` is wired by `ModelBase`.
   Query calls belong in views (functions), never in class definitions. The artifact's
   fourth line demonstrates all three mistakes at once. 📌
4. **Expecting the model class to create the table** — defining `class Student` does
   **not** touch the database. You must `makemigrations` (generate the work order) and
   `migrate` (execute it). The 0-byte `db.sqlite3` is the proof — a declaration is not
   an action.
5. **Confusing `migrate` with `runserver`** — running the server never creates tables.
   A020's admin returns 302 → login → 302 (empty loop) for exactly this reason: no
   migration created `auth_user`. The fix is `migrate`, not `runserver`.

## 🧠 Common Misconceptions

| ✅ Django/Topic IS … | ❌ It is NOT … |
|---|---|
| A model class **declares** a table | A class statement that **creates** a table — tables are created by `migrate`, not by class execution |
| `CharField` **requires** `max_length` | `CharField(255)` — the argument is keyword (`max_length=255`), and it's **mandatory** |
| `.objects` is **auto-created** by the ORM | A method you must write (`def objects(self): …`) — it arrives with `ModelBase`, you never define it |
| `.all()` **defers** the query | A query that hits the DB immediately — it's **lazy**; SQL runs only on evaluation |
| Calling `.objects.all()` in a view is correct | Calling it anywhere Python can see the class — it must be in a **view** (HTTP scope), not the class body or a migration |
| The admin 302-loop is a template bug | Caused by a missing admin route — it's caused by **un-migrated auth tables** (0-byte db); `migrate` fixes it |

---

## 🧪 Practical Example — From Snippet to Query

The artifact is a **snippet**, not a runnable project — but the path from it to a working
query is exactly four lines. Here is the full journey (📌 — beyond the snippet, from
official Django docs):

```python
# Step 1 — the model (the artifact, corrected + max_length)
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)   # 📌 max_length mandatory
    age = models.IntegerField()

# Step 2 — the migration (generated, not hand-written)
# python manage.py makemigrations portfolio
# → creates portfolio/migrations/0001_initial.py

# Step 3 — the query (in a view, not the class body)
from django.shortcuts import render
from .models import Student

def student_list(request):
    students = Student.objects.all()    # 📌 lazy QuerySet — no SQL yet
    return render(request, 'list.html', {'students': students})

# Step 4 — the template (unchanged from A013/A015 — {% for %} works on QuerySets)
# {% for student in students %}
#   <p>{{ student.name }} — {{ student.age }}</p>
# {% endfor %}
```

**Line-by-line:**

- **`name = models.CharField(max_length=100)`** — declares a `varchar(100)` column. The `max_length` is non-negotiable; without it Django refuses to build the migration.
- **`makemigrations portfolio`** 📌 — Django reads your model, compares it to the last migration file, and writes `0001_initial.py` containing the `CreateModel` operation. No database changes yet.
- **`Student.objects.all()`** — `.objects` (the auto-created manager) returns a `QuerySet`. Calling `.all()` is **lazy**: no SQL runs until the template iterates it.
- **`render(request, 'list.html', {'students': students})`** — the QuerySet is passed as context, exactly like A013's literal dict. The template iterates it with `{% for %}` (A015) — the syntax is identical for lists and QuerySets.
---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. The artifact's fourth line has two errors. Name both — one is a typo, one is a placement
   mistake.

<details><summary>Answer</summary>

**Error 1 (typo):** `Student.object` should be `Student.objects` — the auto-created manager
is plural. `Student.object` raises `AttributeError: type object 'Student' has no attribute
'object'`.

**Error 2 (placement):** The line sits **inside the class body**. At class-creation time
(`ModelBase.__new__` hasn't finished), `.objects` isn't wired yet, and the table doesn't
exist — so even with the typo fixed, a `.all()` call inside the body would fail. Query
calls belong in views, where the full stack is live. The line bundles both novice mistakes
at once: the plural checkpoint and the class-body execution trap.

</details>

2. `name = models.CharField()` — what's wrong, and why does Django *refuse* to let you leave it that way?

<details><summary>Answer</summary>

It's missing `max_length=`, the mandatory argument for `CharField`. Django enforces this at
the model-check layer (`E132`: *"Field 'name' can only be a CharField with a max_length
argument"*). The SQL type `varchar(N)` requires a column width; `IntegerField` maps to
`integer` (fixed, no argument). The snippet's bare `CharField()` is the deliberate
teaching instance of this rule — it won't survive `makemigrations`.

</details>

3. `Student.objects.all()` — does it hit the database?

<details><summary>Answer</summary>

**No.** `.all()` on a manager returns a `QuerySet`, which is **lazy**. The SQL `SELECT`
is *assembled* (the recipe is built) but not *executed*. The database is only queried when
you evaluate the QuerySet — by iterating it (`{% for %}`), slicing it, calling `len()`,
`list()`, `bool()`, or printing it in a shell. The artifact's line would hit the DB if it
ran — but it can't even be constructed because of the `.object` typo and the class-body
placement.

</details>

4. What separates A021 (this snippet) from A022 (migrations)? Name the three steps Django
   needs before `Student.objects.all()` returns real rows.

<details><summary>Answer</summary>

**A021 = the declaration. A022 = the construction.** The three steps:

1. **Define the model** — `class Student(models.Model)` with fields (A021 delivers this).
2. **`makemigrations`** — Django reads the model, writes a migration file (`0001_initial.py`)
   containing `CreateModel`. No database changes yet.
3. **`migrate`** — Django reads the migration files and executes the SQL (`CREATE TABLE
   students ...`) against `db.sqlite3`. Only after this does the table exist.

The 0-byte `db.sqlite3` is the proof across six chapters: a declaration is not an action.

</details>

5. Why does the template `{% for student in students %}` work the same on a Python list
   (A015) and a QuerySet (A021)?

<details><summary>Answer</summary>

Because a `QuerySet` implements the **iteration protocol** (`__iter__`) and **slicing**
(`__getitem__`) — the same interface Python lists expose. The template engine only needs
"iterate me, give me items one at a time." It doesn't know or care whether the source is a
literal list or a lazy database recipe. This is the ORM's **contract**: it hands the kitchen
(QuerySet) to the waiter, and the waiter's pass-through to the plating (`{% for %}`) is
unchanged. The template layer stays stable; only the data source changes.

</details>

6. Name the artifact's ⚠️-flagged quirk and why it is a teaching point, not a bug to fix.

<details><summary>Answer</summary>

The entire `ORM.py` snippet is the "quirk": it is a **6-line, non-runnable teaching fragment**
with three deliberate errors (`CharField` without `max_length`, `.object` typo, query in
class body). It exists to **name** the lecture's central type (`Student`) and two of its
fields — to mark the pivot from template-only artifacts (A001–A020) to the database layer.
It is quoted verbatim, not "fixed," because the errors are the teaching points. No
transcript, no `myProject` project, no server — declared honestly in the opening note.

</details>

7. The admin in A020 returned 302 → login → 302 (loop). What command fixes it, and what
   command is *not* the answer?

<details><summary>Answer</summary>

**Fix:** `python manage.py migrate` — this builds the `auth_user` and related tables that
the admin checks before letting you log in. The 302-loop is the 0-byte `db.sqlite3`
symptom: the database file exists but has **no tables** because no migration was ever
applied.

**Not the answer:** `python manage.py runserver` — the server already runs fine; it just
has nothing to authenticate against. Restarting or re-running the server cannot create
tables that the database doesn't have. The fix is always the **migration**, not the server.

</details>

---

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q: "What happens when you write `class Book(models.Model): title = models.CharField(max_length=200)` in `models.py`?"**
A: Nothing touches the database yet. The class *declares* the schema — Django records that
there should be a `books` table with a `title varchar(200)` column. The table only appears
after `makemigrations book` generates a migration file and `migrate` executes it as SQL.
The class is a blueprint; the migration is the construction crew.

**Q: "Why does `CharField` need `max_length` but `IntegerField` doesn't?"**
A: Because `CharField` maps to SQL `varchar(N)` which requires a column width, while
`IntegerField` maps to SQL `integer` — a fixed-width type. Django enforces this at the
model-check layer (`E132`): a `CharField` without `max_length` refuses to migrate.

**Q: "Explain `.objects` to someone who thinks it's a method you write."**
A: It is **not** code you author — Django's `ModelBase` metaclass attaches a `Manager`
instance to every model class automatically. `.objects` is that instance; calling `.all()` or
`.filter()` on it builds a **lazy `QuerySet`** (a query recipe, not a database hit). SQL
executes only when the QuerySet is *evaluated* — iterated, sliced, `len`'d, `list`'d, or
printed. Confusing `.objects` (plural, auto-created) with `.object` (typo,
`AttributeError`) is the #1 beginner stumble — the artifact's fourth line demonstrates it.

**Q: "The admin redirects you to login and loops forever — 302, 302, 302. Why?"**
A: The `auth_user` table doesn't exist — `db.sqlite3` is 0 bytes because `migrate` was never
run. Django creates the admin interface tables *via migrations*, not by running the server.
`python manage.py migrate` builds the `auth_user` and related tables; the 302-loop dissolves
immediately. The server doesn't make tables — migrations do.

**Q: "Do you rewrite all your templates when you switch from a list to a QuerySet?"**
A: No. A `QuerySet` is iterable and supports indexing/slicing, so `{% for x in items %}`
works identically on a Python list (A015) and a database `QuerySet` (A021+). The template
engine only needs "iterate me, give me items one at a time." It doesn't know or care
whether the source is a literal list or a lazy database recipe. This is the ORM's
**contract**: it hands the kitchen (QuerySet) to the waiter, and the waiter's pass-through
to the plating (`{% for %}`) is unchanged. The template layer stays stable; only the data
source changes.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. The artifact's fourth line has two errors. Name both — one is a typo, one is a placement
   mistake.

