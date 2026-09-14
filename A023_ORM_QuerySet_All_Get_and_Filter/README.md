# 🚀 A023 — ORM QuerySet All/Get/Filter

📖 Lecture A023 · 🎓 Track: Core Django · 📶 Level: Beginner · ✅ Status: Documented

> [!NOTE]
> **About this chapter's sources:** no lecture transcript or notes exist for A023 — this chapter is built from the repo's own commands.txt (Django setup commands and ORM QuerySet examples from the owner's command journal) and official Django docs (ORM, QuerySet API reference). Everything marked 📌 comes from official Django documentation. All code snippets were verified against the commands.txt journal entries and the Django ORM reference.

---

## 🧭 What You Will Learn

- [ ] Explain what a **Django QuerySet** is and how it differs from a SQL query result
- [ ] Use Model.objects.all() to retrieve every record from a database table
- [ ] Use Model.objects.get() to retrieve a single record by exact criteria
- [ ] Use Model.objects.filter() to retrieve records matching one or more conditions
- [ ] Apply field lookups (__gt, __lt, __gte, __lte, __startswith, __icontains, __exact) to build precise queries
- [ ] Chain multiple filters together to narrow down query results
- [ ] Trace how Django's ORM translates Python query methods into SQL SELECT statements

## 🎯 Why This Lecture Matters

QuerySets are the **primary way Django reads data** from the database. Every view that displays data, every admin interface that lists records, and every form that pre-populates fields relies on QuerySets. Without understanding all(), get(), and filter(), you cannot retrieve any data from your Django project.

The distinction between get() and filter() is critical: get() returns a **single object** and raises an exception if zero or multiple results are found, while filter() returns a **QuerySet** (a list-like collection) that may be empty. Choosing the wrong one causes runtime errors that are confusing for beginners.

Field lookups (__gt, __lt, __startswith, etc.) are the **bridge between Python and SQL**. They let you express conditions like "age greater than 18" or "name starts with 'a'" directly in Python, and Django translates them into the correct SQL WHERE clause. This is the core of Django's ORM philosophy — write Python, not SQL.

What breaks if you skip this lecture: every subsequent lecture that displays or searches data — A024 (admin integration), A025 (form-based queries), and beyond — will be impossible without understanding how to retrieve records from the database. QuerySets are the **read side** of the data layer triad that models and migrations build.

## ✅ Prerequisites

- [ ] Understand how to define a Django model in models.py (covered in A022)
- [ ] Know how to run makemigrations and migrate to create database tables (covered in A022)
- [ ] Can activate a virtual environment and run manage.py shell
- [ ] Basic Python list operations (iteration, indexing) 📌
- [ ] Familiarity with SQL SELECT statements is helpful but not required 📌

## 🧠 Models — The Data Layer Recap

Before querying, recall the Student model from A022:

```python
from blog.models import Student
```

The Student model has fields like name, age, email, and enrollment_date. Each Student instance represents one row in the database table. The objects manager is Django's gateway to the database — it provides the QuerySet methods (all(), get(), filter()) that let you retrieve records.

## 🧠 QuerySets — The Database Gateway

A **QuerySet** is a lazy collection of database objects. It does not hit the database until you actually iterate over it or evaluate it. This means you can build up queries without paying the database cost until the very end.

Think of a QuerySet as a **search query you construct step by step** — you define what you want, and Django generates the SQL only when you need the results.

```python
# This does NOT hit the database yet:
students = Student.objects.filter(age__gt=18)

# This DOES hit the database (iteration):
for s in students:
    print(s.name, s.age, s.city)
```

## 🧠 The Three Core QuerySet Methods

### objects.all() — Retrieve Everything

all() returns **every record** in the table. It is equivalent to SELECT * FROM blog_student;.

```python
student = Student.objects.all()
print(student)
```

**Output:** A QuerySet containing every Student object. You iterate over it with a for loop to access individual records.

### objects.get() — Retrieve One Exact Match

get() returns a **single object** matching the exact criteria. It raises DoesNotExist if no match is found, and MultipleObjectsReturned if more than one match exists.

```python
student = Student.objects.get(id=1)
print(student)
```

**Output:** The single Student object with id = 1. Think of get() as asking "give me the one and only record that matches" — if there's zero or more than one, Django tells you something is wrong.

### objects.filter() — Retrieve Zero, One, or Many Matches

filter() returns a **QuerySet** of all records matching the conditions. It never raises an exception — if nothing matches, you get an empty QuerySet.

```python
student = Student.objects.filter(age=30)
print(student)
```

**Output:** A QuerySet of all Student objects where age equals 30. This is the safest method for querying because it always returns a collection, never a single object.

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| QuerySet | A lazy list of database objects | A collection that hasn't hit the DB yet until evaluated | "Lazy list that waits" |
| objects | The manager that talks to the DB | The default Manager instance on every Django model | "The gateway object" |
| all() | Get everything | SELECT * FROM table | "All = everything" |
| get() | Get one exact match | SELECT * FROM table WHERE ... LIMIT 1 | "Get = one and only" |
| filter() | Get matching records | SELECT * FROM table WHERE ... | "Filter = narrow down" |
| Lookup | A field condition | __gt, __lt, __startswith, etc. | "Lookup = the condition" |
| Lazy evaluation | Delayed execution | Query runs only when iterated | "Lazy = wait and see" |

## 💡 Real-World Analogy

Imagine a **library catalog** where every book is a database record.

- all() is like **pulling every book off the shelf** and laying them on a table — you now have everything, but you still need to look at each one.
- get() is like asking the librarian **"Give me the book with barcode 12345"** — you expect exactly one book. If it doesn't exist, you're told "not found." If two copies exist, you're told "too many."
- filter() is like telling the librarian **"Show me all books published after 2020"** — you get a stack of matching books, possibly zero, possibly many.

The **lookups** (__gt, __startswith) are the **search filters on the catalog terminal** — they let you say "show me books with titles starting with 'Python'" instead of just "show me all books."

## ❌ Common Beginner Mistakes

1. **Using get() when you expect multiple results** — get() expects exactly one result. If you use it for a condition that matches multiple records, you get a MultipleObjectsReturned exception. Use filter() instead.
2. **Using filter() when you expect exactly one result and then accessing attributes without checking** — filter() always returns a QuerySet, not a single object. You must iterate or use [0] to access the first result.
3. **Forgetting that QuerySets are lazy** — Student.objects.filter(age=30) does not run a query. The database is only hit when you iterate, slice, or call len() on the QuerySet.
4. **Chaining get() and filter() incorrectly** — Student.objects.get().filter(...) is wrong because get() returns a single object, not a QuerySet. Use Student.objects.filter(...).get() instead, or better yet, put all conditions in a single filter() call.
5. **Case sensitivity surprises** — filter(name="Alice") is case-sensitive by default. Use __iexact or __icontains for case-insensitive matching.

## 🧠 Common Misconceptions

| ✅ Django IS … | ❌ It is NOT … |
|---|---|
| QuerySets are lazy and evaluated only when needed | QuerySets execute SQL immediately when created |
| filter() always returns a QuerySet (possibly empty) | filter() returns a single object like get() |
| get() raises exceptions for zero or multiple results | get() returns None when nothing is found |
| ORM queries look like Python code | ORM queries look like raw SQL strings |
| You can chain filter() calls for AND logic | Each filter() call replaces the previous query |

## 🧪 Practical Example

```python
# Import the Student model from the blog app
from blog.models import Student

# --- ALL: Get every student in the database ---
all_students = Student.objects.all()
print("All students:")
for s in all_students:
    print(f"  {s.name}, Age: {s.age}, City: {s.city}")

# --- GET: Get the single student with id=1 ---
try:
    first_student = Student.objects.get(id=1)
    print(f"\nStudent #1: {first_student.name}, Age: {first_student.age}")
except Student.DoesNotExist:
    print("\nNo student with id=1 found!")

# --- FILTER with exact match ---
age_30_students = Student.objects.filter(age=30)
print(f"\nStudents aged 30 ({len(age_30_students)} found):")
for s in age_30_students:
    print(f"  {s.name}")

# --- FILTER with __gt (greater than) ---
older_than_18 = Student.objects.filter(age__gt=18)
print(f"\nStudents older than 18 ({len(older_than_18)} found):")
for s in older_than_18:
    print(f"  {s.name}, Age: {s.age}")

# --- FILTER with __startswith ---
names_starting_a = Student.objects.filter(name__startswith="a")
print(f"\nNames starting with 'a':")
for s in names_starting_a:
    print(f"  {s.name}")
```

**Explanation:**

- **Line 1** imports the Student model — this is the same model defined in A022.
- **Lines 4-8** use objects.all() to retrieve every Student record and print each one's details.
- **Lines 11-15** use objects.get(id=1) to fetch a single record. The try/except block catches DoesNotExist in case id 1 is not in the database.
- **Lines 18-22** use objects.filter(age=30) for an exact-match query. The len() function evaluates the QuerySet and returns the count.
- **Lines 25-29** use objects.filter(age__gt=18) — the __gt lookup translates to WHERE age > 18 in SQL.
- **Lines 32-35** use objects.filter(name__startswith="a") — the __startswith lookup translates to WHERE name LIKE 'a%' in SQL.

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1: What is the difference between get() and filter()?**
A: get() returns a **single object** and raises DoesNotExist or MultipleObjectsReturned exceptions. filter() returns a **QuerySet** (a list-like collection) that is always safe to iterate — even if empty. Use get() when you expect exactly one result; use filter() when you expect zero, one, or many.

**Q2: Why are QuerySets described as "lazy"?**
A: A QuerySet does not execute a database query when it is created. The query is only run when you **evaluate** the QuerySet — by iterating over it, converting it to a list, calling len(), slicing it, or accessing a specific index. This allows you to chain filters together without hitting the database until the final result is needed.

**Q3: What happens if get() finds no matching record?**
A: Django raises a DoesNotExist exception. You must handle this with a try/except block, or the program crashes. This is why filter() is often safer for queries where you're not certain a record exists.

**Q4: Explain the difference between __gt and __gte.**
A: __gt means "greater than" (exclusive, like > in SQL), while __gte means "greater than or equal to" (inclusive, like >= in SQL). Similarly, __lt is "less than" and __lte is "less than or equal to."

**Q5: Can you chain multiple filter() calls? What happens?**
A: Yes! Chaining filter() calls applies **AND logic** — each additional filter narrows the results further. Student.objects.filter(age__gt=18).filter(name__startswith="a") returns students who are both older than 18 AND whose names start with "a".

## 🔁 Active Recall

Answer from memory first, then expand each <details>.

1. What is the difference between objects.all() and objects.filter()?

<details><summary>Answer</summary>

objects.all() returns **every record** in the table (equivalent to SELECT *). objects.filter(condition) returns only records matching the condition (equivalent to SELECT * WHERE ...). all() always returns everything; filter() returns a subset.

</details>

2. When should you use get() instead of filter()?

<details><summary>Answer</summary>

Use get() when you **expect exactly one result** — for example, fetching a user by a unique id. Use filter() when you expect **zero, one, or many results** — for example, finding all students older than 18.

</details>

3. What lookup would you use to find records where age is less than or equal to 25?

<details><summary>Answer</summary>

Use __lte (less than or equal to): Student.objects.filter(age__lte=25). This translates to WHERE age <= 25.

</details>

4. Why does filter(name__startswith="a") not match a student named "Alice"?

<details><summary>Answer</summary>

Actually, it **does** match "Alice" — __startswith is case-sensitive and matches names that start with lowercase "a". To match "Alice" (capital A), use __istartswith for case-insensitive matching, or filter(name__startswith="A").

</details>

## 📝 Quick Revision

- Model.objects.all() → get everything (SELECT *)
- Model.objects.get(field=value) → get one exact match (raises exceptions)
- Model.objects.filter(field=value) → get matching records (safe, always returns QuerySet)
- __gt → greater than, __lt → less than, __gte → greater than or equal, __lte → less than or equal
- __startswith → starts with (case-sensitive), __icontains → contains (case-insensitive), __exact → exact match
- QuerySets are **lazy** — no database hit until evaluated
- Chaining filter() calls applies **AND** logic

## 🧠 Final Mental Model

```
┌─────────────────────────────────────────────┐
│          Django ORM Query Pipeline          │
├─────────────────────────────────────────────┤
│                                             │
│  Python Code                                │
│  Student.objects.filter(age__gt=18)         │
│       │                                     │
│       ▼                                     │
│  QuerySet (lazy)                            │
│  [not evaluated yet]                        │
│       │                                     │
│       ▼  (iteration / len / list)           │
│  SQL Translation                            │
│  SELECT * FROM blog_student WHERE age > 18  │
│       │                                     │
│       ▼                                     │
│  Database Result                            │
│  [list of Student objects]                  │
│                                             │
│  ── all()   → SELECT * FROM table           │
│  ── get()   → SELECT * FROM table WHERE ... │
│               LIMIT 1                       │
│  ── filter() → SELECT * FROM table WHERE... │
└─────────────────────────────────────────────┘
```

## ❓ FAQ

**Q1. Can I chain more than two filter() calls?**
A: Yes, there is no limit. Each filter() adds another condition with AND logic. Student.objects.filter(age__gt=18).filter(name__startswith="a").filter(city="Lahore") is perfectly valid.

**Q2. What is the difference between __exact and just using = in filter()?**
A: There is no functional difference. filter(age=30) and filter(age__exact=30) are equivalent — __exact is the default behavior and is used for clarity or to override when a custom lookup is registered.

**Q3. Can get() return multiple records if I pass multiple conditions?**
A: No. get() always expects a single result regardless of how many conditions you pass. If multiple records match all conditions, it raises MultipleObjectsReturned. Use filter() instead.

**Q4. How do I count results without retrieving all objects?**
A: Use .count() on a QuerySet: Student.objects.filter(age__gt=18).count(). This runs SELECT COUNT(*) in SQL and is much more efficient than iterating over all results.

**Q5. What happens if I call print() on a QuerySet without iterating?**
A: Django evaluates the QuerySet and prints it as a list-like representation (e.g., <QuerySet [<Student: Student object (1)>, ...]>). The database query is executed at this point.

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Retrieve all records:** I can use Student.objects.all() and iterate over the results — *§QuerySets*
- [ ] **Checkpoint 2 — Retrieve a single record:** I can use Student.objects.get(id=1) with proper try/except handling — *§The Three Core QuerySet Methods*
- [ ] **Checkpoint 3 — Filter with lookups:** I can use filter(age__gt=18) and filter(name__startswith="a") to narrow results — *§The Three Core QuerySet Methods*
- [ ] **Checkpoint 4 — Understand lazy evaluation:** I can explain why Student.objects.filter(age=30) doesn't hit the database until iteration — *§QuerySets — The Database Gateway*

## 🏋️ Exercises

- **Level 1 — Recall:** Write the Django ORM code to get all students whose age is exactly 20. What lookup would you use?
- **Level 2 — Understanding:** Write code to get all students whose email ends with @gmail.com. Which lookup (__endswith or __icontains) is more appropriate and why?
- **Level 3 — Application:** Given a Student model with fields name, age, city, write code that: (1) gets all students older than 25, (2) from that result, filters for those whose name starts with "S", (3) prints each matching student's name and city.
- **Level 4 — Interview reasoning:** Explain why Student.objects.get(age=30) is dangerous when multiple students can have age 30. What exception is raised, and how would you rewrite this safely?

## 🏁 Final Takeaways

1. objects.all(), objects.get(), and objects.filter() are the **three fundamental ways** to query data in Django's ORM.
2. get() returns a **single object** (with exceptions); filter() returns a **QuerySet** (always safe).
3. Field lookups (__gt, __lt, __gte, __lte, __startswith, __icontains, __exact) translate Python conditions into SQL WHERE clauses.
4. QuerySets are **lazy** — they don't hit the database until you evaluate them.
5. Chaining filter() calls applies **AND** logic, making queries more precise.

## 🔄 Next Lecture Connection

This lecture covers the **read operations** of Django's ORM. The next lecture builds on this foundation by retrieving and presenting database rows in application code. → [A024 — Retrieve Data from a Database Table](../A024_Retrieve_Data_from_Database_Table/README.md) ← *documented*

---

<div class="doc-footer">

**Sources used:** repo's own commands.txt (Django setup commands and ORM QuerySet examples from the owner's command journal), [Django ORM Documentation](https://docs.djangoproject.com/en/stable/topics/db/queries/) 📌, [Django Field Lookup Reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/) 📌, [Django Model Managers](https://docs.djangoproject.com/en/stable/topics/db/managers/) 📌
**Navigation:** ← [A022 — Create Model, Migration Files & SQLite DB](../A022_Create_Model_Migration _iles_&_SQLite_DB/README.md) · [Series hub](../README.md) · [A024 — Retrieve Data from Database Table](../A024_Retrieve_Data_from_Database_Table/README.md) →

</div>
