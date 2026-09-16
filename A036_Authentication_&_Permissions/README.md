# 🚀 A036 — Authentication & Permissions

`📖 Lecture A036` · `🎓 Track: Core Django` · `📶 Level: Intermediate` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder. The chapter is built from the `myProject20/` artifact — a Django 6.1.1 project with a `demo` app whose `views.py`, `models.py`, and `admin.py` are empty scaffolds. The lecture's content is delivered entirely through the Django admin UI: creating users, building groups, assigning permissions, and handling passwords. There is no custom Python code to quote from the artifact beyond `settings.py` and `urls.py`. All Django behaviour described below is grounded in `django.contrib.auth` — the authentication framework that ships with Django and is already active in `myProject20`.
>
> This lecture builds directly on [A035 — Django Messages Framework](../A035_Debug_Info_Success_Warning_&_Error/README.md).

---

## 🧭 What You Will Learn

- [ ] How to create and manage users through the Django Admin Panel
- [ ] How to create Groups and assign users to them for role-based access control
- [ ] How to grant and revoke permissions for users and groups
- [ ] How Django's built-in password change and password reset flows work
- [ ] How `django.contrib.auth` provides all of this without writing a single line of custom code

## 🎯 Why This Lecture Matters

Every application from A031 to A034 has been completely open — any visitor can create, edit, or delete records. That is fine for learning CRUD, but no real application works that way. A healthcare portal, an e-commerce site, a blog — all of them need at least two things: knowing *who* a user is (authentication) and deciding *what they may do* (authorisation/permissions). Django ships both in `django.contrib.auth`, and the admin panel exposes them through a polished UI that requires zero custom code to use.

This lecture is the bridge between "I can build CRUD" and "I can build CRUD that only the right people can access". The four skills it covers — creating users, organising them into groups, assigning permissions, and managing passwords — are the daily operational tasks every Django developer and site admin performs in production.

## ✅ Prerequisites

- [ ] Django Admin and superuser creation (A026)
- [ ] Registering and managing models in admin (A027)
- [ ] Admin list display, search, and filters (A028)
- [ ] The `Student` CRUD app from A031–A034 — provides the models whose permissions are exercised here

---

## 🧠 `django.contrib.auth` — What Ships in the Box

### The Infrastructure Already Running in `myProject20`

The `myProject20` project uses the standard Django project template. `django.contrib.auth` is active by default — no installation, no migration needed beyond the initial `migrate`:

```python
# myProject20/settings.py — verbatim (relevant excerpt)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',          # ← authentication framework
    'django.contrib.contenttypes',  # ← required by auth (generic relations)
    'django.contrib.sessions',      # ← required for login sessions
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'demo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   # ← session persistence
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # ← attaches request.user
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Explanation:**
- `django.contrib.auth` — the authentication app: provides the `User` model, `Group` model, `Permission` model, login/logout views, and password management utilities.
- `django.contrib.contenttypes` — a dependency of `auth`; tracks all model types in the project so permissions can be attached to any model generically.
- `django.contrib.sessions.middleware.SessionMiddleware` — manages the session cookie that keeps the user logged in across requests.
- `django.contrib.auth.middleware.AuthenticationMiddleware` — reads the session on each request and attaches the corresponding `User` object as `request.user`. If no session exists, `request.user` is an `AnonymousUser`.

Running `py manage.py migrate` on a fresh project creates all required auth tables:

| Table | Purpose |
|---|---|
| `auth_user` | Stores user accounts (username, password hash, email, flags) |
| `auth_group` | Stores group definitions (name only) |
| `auth_permission` | Stores all permissions (one per CRUD action per model) |
| `auth_user_groups` | Many-to-many: which users belong to which groups |
| `auth_user_user_permissions` | Many-to-many: direct permissions on users |
| `auth_group_permissions` | Many-to-many: permissions on groups |

---

## 🧠 1 — Create & Manage Users in the Admin Panel

### The `User` Model

Django's built-in `User` model (`django.contrib.auth.models.User`) has these fields:

| Field | Type | Notes |
|---|---|---|
| `username` | CharField (150) | Required, unique — the login identifier |
| `password` | CharField | Stored as a hash — never plain text |
| `email` | EmailField | Optional but conventional |
| `first_name` | CharField | Optional |
| `last_name` | CharField | Optional |
| `is_active` | BooleanField | `True` = account is usable; `False` = soft-deleted |
| `is_staff` | BooleanField | `True` = can log into the admin panel |
| `is_superuser` | BooleanField | `True` = all permissions automatically, no explicit grants needed |
| `date_joined` | DateTimeField | Auto-set on creation |
| `last_login` | DateTimeField | Updated on each login |

### Creating a User via the Admin Panel

1. Log in to `/admin/` as a superuser.
2. Navigate to **Authentication and Authorization → Users → Add User**.
3. Django's add-user form is a two-step form: first set `username` and `password`, then fill optional fields (`first_name`, `last_name`, `email`) and permission flags.

The three boolean flags and their effects:

| Flag | Effect |
|---|---|
| `is_active` | Unchecked = the account is disabled. Login attempts fail silently. Use this instead of deleting to preserve foreign-key history. |
| `is_staff` | Checked = the user can log into `/admin/`. Without this, the admin login page rejects them even with a valid password. |
| `is_superuser` | Checked = all permissions granted automatically. The user can see and modify everything in the admin — no explicit permission grants needed. |

> [!WARNING]
> A user with `is_staff=True` but no permissions sees an empty admin dashboard (no models listed). `is_staff` is the door key; permissions are the room keys.

### Managing Existing Users

From the user list (`/admin/auth/user/`):

- **Search** by username or email.
- **Filter** by staff status, superuser status, active status.
- **Bulk actions** — Django ships a "Delete selected users" bulk action.
- **Edit** — click a username to open the change form: update fields, change password, assign permissions and groups.

The password field on the change form renders as a read-only hash display with a "Change password" link — you cannot read the stored password (it is hashed), only replace it.

---

## 🧠 2 — Groups for Role-Based Access Control

### What a Group Is

A **Group** is a named collection of permissions. Assign a user to a group and they inherit all the group's permissions automatically. Remove them from the group and the permissions are revoked.

```
Group: "Content Editors"
  └── permissions:
        ├── blog.add_post
        ├── blog.change_post
        └── blog.view_post

User: alice  ──belongs to──▶  "Content Editors"
  → alice inherits: blog.add_post, blog.change_post, blog.view_post

User: bob    ──belongs to──▶  "Content Editors"
  → bob  inherits: same three permissions
```

Without groups, assigning permissions to 50 editors means 50 individual grant operations — and revoking one permission means 50 revocations. With groups, it is one change that flows to all members. This is **role-based access control (RBAC)** at the simplest level.

### Creating a Group in Admin

1. Navigate to **Authentication and Authorization → Groups → Add Group**.
2. Enter a name (e.g. `Content Editors`, `Moderators`, `Viewers`).
3. Use the permission picker to move permissions from "Available" to "Chosen".
4. Save. The group now exists and can be assigned to users.

### Assigning a User to a Group

On the user's change form (`/admin/auth/user/<id>/change/`), scroll to the **Groups** section. The widget shows available groups on the left; move the target group(s) to the "Chosen groups" box on the right. Save.

### Checking Effective Permissions

A user's effective permissions are the union of:
1. **Direct permissions** — explicitly granted on the user object.
2. **Group permissions** — inherited from every group the user belongs to.
3. **Superuser override** — if `is_superuser=True`, all permissions pass automatically regardless of grants.

---

## 🧠 3 — Permissions: How They Work

### Auto-Generated Permissions

When you run `migrate`, Django automatically creates **four permissions per model**:

| Permission codename | What it allows |
|---|---|
| `<app>.<action>_<model>` format | |
| `demo.add_mymodel` | Create new instances |
| `demo.change_mymodel` | Edit existing instances |
| `demo.delete_mymodel` | Delete instances |
| `demo.view_mymodel` | View instances (read-only) |

For every registered model across all installed apps, these four permissions exist in `auth_permission`. For the student CRUD from A031: `student.add_student`, `student.change_student`, `student.delete_student`, `student.view_student`.

Django's own built-in models (User, Group, LogEntry, etc.) also have their four auto-generated permissions — you can see them all in the permission picker.

### Assigning Permissions Directly to a User

On the user's change form, scroll to **User permissions**. The picker shows all available permissions (grouped by app). Move the desired permissions to "Chosen user permissions". Save.

Direct permissions are useful for one-off grants that don't fit an existing group, or for exceptions (e.g. one user who can delete but cannot add).

### Assigning Permissions to a Group

On the group's change form (**Authentication and Authorization → Groups → \<group name\>**), the same picker adds permissions to the group. All group members inherit them immediately.

### Checking Permissions Programmatically

```python
# In a view or shell — checking if a user has a permission
request.user.has_perm('student.add_student')     # True / False
request.user.has_perm('student.delete_student')  # True / False

# Checking group membership
request.user.groups.filter(name='Content Editors').exists()  # True / False
```

**Explanation:**
- `has_perm('app.action_model')` — checks direct permissions AND group-inherited permissions. Returns `True` for superusers always.
- The permission string format is `'<app_label>.<codename>'` — the app label is the `app_name` in `apps.py`, and the codename is `add_`, `change_`, `delete_`, or `view_` + the model name in lowercase.

> [!TIP]
> In templates, `{{ perms.student.add_student }}` returns `True`/`False` and can be used in `{% if perms.student.add_student %}` blocks to show/hide UI elements based on the logged-in user's permissions (📌 — covered in depth in a future authentication views lecture).

---

## 🧠 4 — Password Change & Reset

### Two Distinct Flows

| Flow | Who initiates? | Entry point | What it does |
|---|---|---|---|
| **Password Change** | Logged-in user | `/admin/password_change/` | User knows current password; enters old + new + confirm |
| **Password Reset** | User who forgot password | `/admin/password_reset/` | User enters email; receives a reset link; sets new password without knowing the old one |

Both flows are built into `django.contrib.admin` — they require no custom view, no custom URL, and no template. They work out of the box.

### Password Change (for logged-in users)

1. In the admin, click the username in the top-right corner → **"Change password"**.
2. Enter the old password, the new password, and confirm the new password.
3. Django validates the new password against `AUTH_PASSWORD_VALIDATORS` (configured in `settings.py`):

```python
# myProject20/settings.py — verbatim
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

| Validator | What it rejects |
|---|---|
| `UserAttributeSimilarityValidator` | Passwords too similar to the username, email, first name, or last name |
| `MinimumLengthValidator` | Passwords shorter than 8 characters (default) |
| `CommonPasswordValidator` | Passwords from a list of 20,000 common passwords |
| `NumericPasswordValidator` | Passwords that are entirely numeric |

> [!IMPORTANT]
> Django **never stores plain-text passwords**. When a password is saved, Django hashes it using PBKDF2 with SHA-256 (the default hasher). The stored value looks like `pbkdf2_sha256$870000$<salt>$<hash>`. There is no way to recover the original password — only to verify a submitted password matches the hash, or to replace the hash with a new one.

### Password Reset (for users who forgot their password)

1. From the admin login page, click **"Forgotten your password?"** or navigate to `/admin/password_reset/`.
2. Enter the email address associated with the account.
3. Django sends an email with a time-limited reset link containing a UUID token.
4. The user clicks the link, enters a new password (validated by `AUTH_PASSWORD_VALIDATORS`), and the hash is updated.

> [!NOTE]
> Password reset requires an email backend configured in `settings.py`. In `myProject20`, the `MAILERS` block uses a non-standard key (`MAILERS` instead of `EMAIL_BACKEND`) — this is the same inert pattern seen in A031–A035. For reset emails to actually send, the standard Django setting is:
> ```python
> EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # dev: prints to terminal
> ```
> The `MAILERS` key in the artifact has no effect on Django's email system (📌 — this is a recurring artefact of the project template used in this series; see A029 §12 note).

### Changing a User's Password from the Superuser Account

Superusers can reset any user's password without knowing the current password:

1. Go to **Authentication and Authorization → Users → \<username\>**.
2. On the change form, below the password field, click **"Change password"** (the direct link, which bypasses the old-password check).
3. Set the new password and save.

This is the standard admin "password reset by staff" flow — no email is sent; the admin sets the password directly.

---

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **Authentication** | Who are you? | The process of verifying a user's identity, typically by checking username + password against stored hashes | The ID card check at the door |
| **Authorisation** | What may you do? | The process of checking whether an authenticated user has permission to perform a specific action | The room-key check inside |
| **`User` model** | A person with an account | `django.contrib.auth.models.User` — the built-in model with username, password hash, flags (`is_staff`, `is_superuser`, `is_active`) | The employee record |
| **`is_staff`** | Can enter the admin? | BooleanField; `True` allows login to `/admin/`; does not grant any model permissions automatically | The building pass |
| **`is_superuser`** | Unlimited access | BooleanField; `True` grants every permission automatically with no explicit grant required | The master key |
| **`is_active`** | Account enabled? | BooleanField; `False` disables login without deleting the account — soft-delete pattern | The on/off switch |
| **Group** | A role with permissions | `django.contrib.auth.models.Group` — a named set of permissions; users inherit all group permissions | The job title |
| **Permission** | One allowed action | Auto-generated: four per model (`add`, `change`, `delete`, `view`); stored in `auth_permission`; codename format: `app.action_model` | The room key |
| **`has_perm()`** | Does this user have this permission? | `user.has_perm('app.action_model')` — checks direct + group permissions; always `True` for superusers | The bouncer's check |
| **Password hashing** | Storing passwords safely | Django hashes passwords with PBKDF2-SHA256 before storing; plain text is never stored | A one-way fingerprint |
| **Password change** | Update password (knows old one) | Built-in admin flow at `/admin/password_change/`; requires current password + new password × 2 | Upgrade with ID |
| **Password reset** | Update password (forgot old one) | Token-based email flow; time-limited link; no old password required | Locksmith visit |
| **`AUTH_PASSWORD_VALIDATORS`** | Password strength rules | List of validators that reject weak passwords (too short, too common, too similar to username, all digits) | The password door policy |
| **RBAC** | Role-based access control | Assigning permissions to groups (roles) rather than individual users — one group change propagates to all members | Job titles, not name badges |

> New terms must also be added to `docs/MEMORY.md` §2.

## 💡 Real-World Analogy

**Django's auth system is a corporate office building.**

- **`User`** is the employee record: name, photo ID, active status, whether they have a building pass (`is_staff`) or a master key (`is_superuser`).
- **`Group`** is the job title: "Content Editor", "Moderator", "Finance". The title comes with a standard set of room keys (permissions). Promote someone by changing their title, not by re-issuing individual keys.
- **`Permission`** is a room key: `student.add_student` is the key to the "add student" room. Four keys exist per room (`add`, `change`, `delete`, `view`).
- **`has_perm()`** is the key reader at each door — the user swipes, the reader checks their keyring (direct + group permissions), the door opens or stays shut.
- **Password change** is updating your badge PIN at the security desk while you're present — you must prove you know the old PIN first.
- **Password reset** is calling the locksmith when you've lost your PIN entirely — they verify your identity (email), then issue a temporary code (the reset link) that lets you set a new PIN.
- **`is_superuser`** is the building's owner — every door opens, no swipe needed.

## ❌ Common Beginner Mistakes

1. **Setting `is_staff=True` but no permissions, then wondering why the admin is empty** — `is_staff` grants admin login access but not model visibility. The user sees "Authentication and Authorization" only if they have at least one permission. Fix: assign explicit permissions or add to a group.

2. **Using `is_superuser=True` for all admin users** — superusers bypass every permission check. A content editor who is a superuser can accidentally delete any model. Fix: use groups with targeted permissions; reserve `is_superuser` for site admins only.

3. **Disabling `is_active` thinking it deletes the user** — it doesn't; it just prevents login. The record still exists and its foreign-key relationships are intact. This is actually the correct approach (soft-delete), but beginners sometimes set it expecting the user to disappear from the admin list.

4. **Assigning permissions directly to every user instead of using groups** — works initially but doesn't scale. When a permission changes, you must update every affected user individually. Fix: create groups for each role; add users to groups.

5. **Forgetting `EMAIL_BACKEND` for password reset** — the reset link is delivered by email. If `EMAIL_BACKEND` is not set (or is set to the wrong key, as with `MAILERS` in this project's template), reset emails are never sent and the user is stuck. Fix: set `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` in development.

6. **Trying to read a stored password** — Django's admin shows the hash, not the plain text. There is no "reveal password" button — by design. If a user forgets their password, the only path is the reset flow; there is no recovery.

## 🧠 Common Misconceptions

| ✅ Django auth IS … | ❌ It is NOT … |
|---|---|
| Built-in and active by default in every project | Something you install separately |
| `is_staff` = can log into admin | `is_staff` = has all admin permissions |
| `is_superuser` = all permissions automatically | `is_superuser` = just another staff flag |
| `is_active=False` = login disabled (soft-delete) | `is_active=False` = user deleted |
| Group permissions are inherited automatically | Groups need to be manually "activated" per view |
| Password stored as a one-way hash | Password stored in any recoverable form |
| `has_perm()` checks both direct + group permissions | `has_perm()` only checks direct permissions |

## 🧪 Practical Example

The following shows how to check permissions in a view and protect it — the programmatic side of what this lecture configures in the admin UI:

```python
# demo/views.py — permission check in a view (📌 beyond the admin-UI scope of this lecture)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

# Protect a view: user must be logged in
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Protect a view: user must have a specific permission
@permission_required('student.add_student', raise_exception=True)
def add_student(request):
    return render(request, 'add_student.html')
```

**Explanation:**
- `@login_required` — redirects unauthenticated users to the login page (`settings.LOGIN_URL`, default `/accounts/login/`). The permission check doesn't even run if the user isn't logged in.
- `@permission_required('student.add_student', raise_exception=True)` — checks `request.user.has_perm('student.add_student')`. If `False` and `raise_exception=True`, returns 403 Forbidden instead of redirecting to login.
- The permission string `'student.add_student'` matches the auto-generated permission for the `Student` model in the `student` app from A031.

Checking permissions in a template:

```html
<!-- any template — shows the button only if the user can add students -->
{% if perms.student.add_student %}
    <a href="{% url 'student_create' %}">Add Student</a>
{% endif %}
```

**Explanation:**
- `perms` is injected by `django.contrib.auth.context_processors.auth` (already in `myProject20/settings.py`).
- `perms.student.add_student` evaluates to `True` if `request.user.has_perm('student.add_student')`.

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Q1. What is the difference between authentication and authorisation?**
A: Authentication answers "who are you?" — verifying identity via credentials (username + password). Authorisation answers "what may you do?" — checking whether the verified identity has permission to perform a specific action. Django handles both: `AuthenticationMiddleware` attaches the verified user, `has_perm()` checks what they may do.

**Q2. What is the difference between `is_staff` and `is_superuser`?**
A: `is_staff=True` grants access to the admin login page but no model permissions. The user lands on an empty or limited dashboard. `is_superuser=True` grants every permission automatically — no explicit grant needed. Use `is_staff` + explicit permissions for real staff; reserve `is_superuser` for developers and site owners.

**Q3. Why use groups instead of assigning permissions directly to users?**
A: Scalability and maintainability. Direct assignments require updating every individual user when a permission changes. Groups centralise permissions under a role name. Adding or revoking a permission from a group instantly affects all members — that's RBAC. It also makes access audits simpler: look at the group definition, not 50 user records.

**Q4. How many permissions does Django auto-generate per model, and what are they?**
A: Four: `add_<model>`, `change_<model>`, `delete_<model>`, `view_<model>`. They are created automatically when `migrate` runs and stored in `auth_permission`.

**Q5. How does Django store passwords, and why can't you recover them?**
A: Django applies PBKDF2-SHA256 (plus a random salt) to the plain-text password and stores only the resulting hash. Hashing is one-way — given the hash, there is no algorithm to reverse it to the original. Verification works by hashing the submitted attempt and comparing the result to the stored hash. If a user forgets their password, the only resolution is the reset flow — the old password is unrecoverable by design.

**Q6. What does `has_perm('student.add_student')` check?**
A: It checks the user's effective permissions: direct permissions granted on the user object, plus all permissions inherited from every group the user belongs to. For a superuser, it always returns `True` regardless of grants.

---

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. What is the difference between `is_staff` and `is_superuser`?

<details><summary>Answer</summary>

`is_staff=True` allows the user to log into `/admin/` but grants no model permissions. `is_superuser=True` grants every permission automatically — the user can see and modify everything. A staff user with no permissions sees an empty admin.
</details>

2. What four permissions does Django auto-generate for every model?

<details><summary>Answer</summary>

`add_<model>`, `change_<model>`, `delete_<model>`, `view_<model>` — one per CRUD action. Format: `<app_label>.<codename>` e.g. `student.add_student`.
</details>

3. Why are groups preferred over direct permission assignments?

<details><summary>Answer</summary>

Groups implement RBAC. Changing a group's permissions propagates to all members instantly. Direct assignments require updating every user individually and are hard to audit.
</details>

4. What does `is_active=False` do to a user account?

<details><summary>Answer</summary>

Disables login — the account cannot be used to sign in. The record still exists with all its data and foreign-key relationships intact. It is a soft-delete, not a deletion.
</details>

5. What is the difference between the password change and password reset flows?

<details><summary>Answer</summary>

Password change: the user is logged in and knows their current password. They enter old + new + confirm at `/admin/password_change/`. Password reset: the user has forgotten their password. They enter their email, receive a time-limited link, and set a new password without needing the old one.
</details>

6. How does `has_perm('app.action_model')` compute the result?

<details><summary>Answer</summary>

It checks the union of: (1) permissions granted directly on the user, and (2) permissions inherited from all groups the user belongs to. For superusers it always returns `True`.
</details>

---

## 📝 Quick Revision

| Concept | Where in Admin | Key point |
|---|---|---|
| Create user | Auth → Users → Add | Two-step: set credentials, then fill fields + flags |
| `is_staff` | User change form | Admin login access — no permissions implied |
| `is_superuser` | User change form | All permissions automatically |
| `is_active` | User change form | `False` = soft-disable login, not delete |
| Create group | Auth → Groups → Add | Name + permission picker |
| Assign user to group | User change form → Groups | Move group to "Chosen" |
| Direct permission | User change form → User permissions | One-off grant |
| Permission format | — | `<app>.<action>_<model>` e.g. `student.add_student` |
| Password change | Admin top-right → Change password | Requires old password |
| Password reset | Admin login → Forgot password | Email token, no old password |
| Superuser reset any user | Users → \<user\> → Change password link | No old password required |
| Password storage | — | PBKDF2-SHA256 hash — never plain text |

---

## 🧠 Final Mental Model

```
django.contrib.auth
        │
        ├── User ──────── is_active (login gate)
        │      │           is_staff  (admin door)
        │      │           is_superuser (master key — bypasses all checks)
        │      │
        │      ├── direct permissions ─────────────────────────────────┐
        │      └── group memberships → Group → group permissions ───── ┤
        │                                                               ▼
        │                                                      effective permissions
        │                                                      (has_perm() = union)
        │
        ├── Permission — auto-generated: add/change/delete/view × every model
        │
        ├── Group — named role: N permissions assigned → all members inherit
        │
        └── Password — stored as PBKDF2-SHA256 hash
              ├── change: logged in + knows old password → /admin/password_change/
              └── reset:  forgot password → email token → /admin/password_reset/
```

Authentication verifies **who**. Permissions decide **what**. Groups organise **who gets what** at scale.

---

## ❓ FAQ

**Q1. Can I create custom permissions beyond the auto-generated four?**
A: Yes — define them in the model's `Meta` class with `permissions = [('can_publish', 'Can publish articles')]`. They appear in the admin's permission picker after running `migrate` (📌 — beyond this lecture's admin-UI scope).

**Q2. What happens if I delete a user who has created records?**
A: If the related model uses `ForeignKey` to `User` with `on_delete=CASCADE`, those records are deleted too. With `on_delete=SET_NULL`, the FK column is nulled. This is why `is_active=False` (soft-disable) is safer than deletion for accounts that own data.

**Q3. Can a non-superuser admin user change another user's password?**
A: Only if they have `auth.change_user` permission. With that permission they can open any user's change form and use the "Change password" link — no knowledge of the target user's current password is required (the form skips the old-password check for staff).

**Q4. How is the password reset link secured?**
A: The link contains a UUID token (`<uidb64>/<token>/`) generated using Django's `PasswordResetTokenGenerator`. The token is time-limited (default 3 days, configurable via `PASSWORD_RESET_TIMEOUT`) and single-use — once used, it becomes invalid.

**Q5. What is the difference between `auth.change_user` and `is_superuser`?**
A: `auth.change_user` is a regular permission that allows editing user objects in the admin — changing names, emails, flags, group memberships. `is_superuser` bypasses all permission checks entirely. A user with `auth.change_user` can edit users; with `is_superuser` they can do anything.

**Q6. Can I use the same `User` model for a non-admin public-facing site?**
A: Yes — `django.contrib.auth` powers both the admin and the public site. Login views (`LoginView`, `LogoutView`) and decorators (`@login_required`) work with the same `User` model. The admin is just one interface to it (📌 — public-facing auth views are covered in a future lecture).

---

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — Users:** I can create a user in the admin panel, set `is_staff`/`is_active`/`is_superuser` correctly, and explain the difference between these three flags — *§1 Create & Manage Users*
- [ ] **Checkpoint 2 — Groups:** I can create a group, assign permissions to it, and add users to it; I can explain why groups are preferred over direct permission grants — *§2 Groups for Role-Based Access Control*
- [ ] **Checkpoint 3 — Permissions:** I can name the four auto-generated permissions per model, describe the `app.action_model` format, and explain how `has_perm()` computes effective permissions — *§3 Permissions*
- [ ] **Checkpoint 4 — Passwords:** I can distinguish the password change flow (logged in, knows old password) from the password reset flow (email token, no old password), and explain why plain-text recovery is impossible — *§4 Password Change & Reset*
- [ ] **Checkpoint 5 — Infrastructure:** I can identify the four `settings.py` components that power `django.contrib.auth` (`INSTALLED_APPS`, `MIDDLEWARE`, `AUTH_PASSWORD_VALIDATORS`, context processor) — *§Infrastructure*

---

## 🏋️ Exercises

- **Level 1 — Recall:** List the three boolean flags on the `User` model and what each controls. Name all four auto-generated permissions for a `Student` model in a `student` app.
- **Level 2 — Understanding:** A colleague sets `is_staff=True` on a new editor account but the editor sees an empty admin. Explain why and describe exactly what steps fix it. Why is `is_active=False` safer than deleting a user who has created records?
- **Level 3 — Application:** In `myProject20`, create two groups: `Viewers` (only `view_*` permissions for the `demo` app) and `Editors` (add + change + view, no delete). Create two users, assign one to each group. Verify in the admin that each user sees only the permitted actions.
- **Level 4 — Interview reasoning:** A junior developer proposes assigning permissions directly to each user because "we only have 10 users now". Explain RBAC, the cost of direct assignments at scale, and how groups solve the permission-change propagation problem. Include what `has_perm()` would need to check in each scenario.

---

## 🏁 Final Takeaways

1. `django.contrib.auth` ships with every Django project and requires no additional installation — just `migrate` to create the auth tables.
2. Three flags control account access: `is_active` (login enabled), `is_staff` (admin entry), `is_superuser` (all permissions, no explicit grants needed).
3. Django auto-generates four permissions per model — `add`, `change`, `delete`, `view` — in `app.action_model` format.
4. Groups implement RBAC: assign permissions once to the group; all members inherit them. Use groups, not direct assignments, for any team larger than one.
5. `has_perm()` returns the union of direct permissions and all group-inherited permissions; always `True` for superusers.
6. Passwords are stored as PBKDF2-SHA256 hashes — never plain text, never recoverable. Change = old password required; Reset = email token, no old password.
7. All four capabilities — user management, groups, permissions, password flows — work through the built-in admin UI with zero custom code.

## 🔄 Next Lecture Connection

A036 covers authentication and permissions through the admin UI. The next step is exposing these concepts to end users via public-facing views: login/logout pages, registration forms, `@login_required` on CRUD views, and permission-gated template blocks — bringing authentication out of the admin and into the application itself.

---

<div class="doc-footer">

**Sources used:** `myProject20/` artifact (Django 6.1.1): `myProject20/settings.py` (`INSTALLED_APPS` includes `django.contrib.auth`, `django.contrib.contenttypes`, `django.contrib.sessions`, `django.contrib.messages`, `demo`; `MIDDLEWARE` includes `AuthenticationMiddleware`, `SessionMiddleware`, `MessageMiddleware`; `AUTH_PASSWORD_VALIDATORS` 4 validators; `STATICFILES_DIRS` ghost shelf W004; `MAILERS` inert key — recurring artefact), `myProject20/urls.py` (`admin/` + `include('demo.urls')`), `demo/views.py` (empty scaffold), `demo/models.py` (empty scaffold), `demo/admin.py` (empty scaffold), `demo/urls.py` (empty urlpatterns). No lecture transcript — chapter built from the owner's four stated topics, the `myProject20` artifact, and official Django documentation (`django.contrib.auth`, `User` model, permissions, groups, password management). Practical Example (§) and template `perms` usage marked 📌 as beyond the admin-UI scope of the artifact.

**Navigation:** ← [A035 — Django Messages Framework](../A035_Debug_Info_Success_Warning_&_Error/README.md) · [Series hub](../README.md) · A037 →

</div>
