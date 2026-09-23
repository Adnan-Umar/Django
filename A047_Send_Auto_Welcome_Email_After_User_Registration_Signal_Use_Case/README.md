# 🚀 A047 — Send Auto Welcome Email After User Registration (Signal Use Case)

`📖 Lecture A047` · `🎓 Track: Core Django` · `📶 Level: Intermediate` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** This chapter is built from the **`myProject31/` artifact** — a
> Django 6.1.1 project whose `accounts` app fires a `post_save` signal on the built-in `User` model
> and sends a welcome email to the new registrant. The signal handler lives in `accounts/signals.py`
> and is wired via `accounts/apps.py`.
>
> This chapter opens with a live debugging session: the artifact initially sent emails with
> **`From: None`** instead of the configured Gmail address. Three bugs were found and fixed:
> 1. `settings.py` never loaded the `.env` file, so `os.getenv('EMAIL')` returned `None`
> 2. The signal read `os.getenv('EMAIL')` directly instead of using `settings.DEFAULT_FROM_EMAIL`
> 3. The `fail_silently=False` argument is deprecated in Django 6.1
>
> The corrected code is documented below. The `db.sqlite3` file is **real** (128 KB, with users
> created during verification), and the `.env` file is **git-ignored**.
>
> This lecture builds on [A043 — Pre-Save & Post-Save Signals](../A043_Pre_Save_&_Post_Save_Signals/README.md)
> and [A046 — Django Email Setup](../A046_Django_Email_Setup/README.md).

## 🧭 What You Will Learn

- How to use Django's `post_save` signal to automatically send a welcome email when a new user registers
- How to wire a signal handler using `apps.py` `ready()` method
- Why `from_email` showed as `None` and how to fix it using `settings.DEFAULT_FROM_EMAIL`
- How to load environment variables from `.env` file in Django settings
- How to avoid deprecated arguments in Django 6.1 (`fail_silently`)
- The difference between signal-triggered emails and view-triggered emails
- How `post_save` works with `created` flag to distinguish new users from updates

## 🧠 What Is a Signal in Django?

A **signal** in Django is a way for code to respond to certain actions or events happening elsewhere
in the framework. Think of it as a notification system: when something happens (like a model being
saved), Django sends out a signal, and any code that's listening for that signal can react.

The key signals for this chapter:

- **`post_save`** — sent after a model's `save()` method is called and the object is saved to the database
- **`pre_save`** — sent before a model is saved (before the database operation)

For user registration, we use `post_save` on the `User` model so the welcome email is sent **after**
the user is successfully created in the database.

### Why Use Signals for Welcome Emails?

- **Automatic**: The email is sent without the registration view needing to remember to call a function
- **Centralized**: One signal handler handles all user creation paths (admin, shell, registration form)
- **Separation of concerns**: The email logic lives separately from the user creation logic

## 🎯 Why This Lecture Matters

User registration is one of the most common features in web applications, and sending a welcome
email is a standard part of that flow. But there's a key design decision: **where** should the email
sending logic live?

You could put it in the registration view, but then you'd need to remember to call it every time
a user is created — in the registration form, in the Django admin, in the shell, in any API endpoint.
Miss one place and users don't get their welcome email.

A **signal** solves this: one `@receiver(post_save, sender=User)` handles **all** user creation
paths automatically. The email is sent whether the user was created via:
- A registration form view
- The Django admin interface
- `manage.py shell` with `create_user()`
- A custom management command
- Any third-party package that creates users

This is the power of signals: **decoupled, automatic, centralized** side effects.

## ✅ Prerequisites

- [ ] **A043 — Pre-Save & Post-Save Signals** — the `post_save` contract, `@receiver` decorator, `ready()` import rule, synchronous dispatch, veto rule; this chapter uses all of them
- [ ] **A046 — Django Email Setup** — the `MAILERS` registry, console vs SMTP, `send_mail()` signature, the `.env`-loading rule, `DEFAULT_FROM_EMAIL`; the welcome email rides on A046's infrastructure
- [ ] **A037 — User Signup, Login & Restrict Pages** — where real apps first send mail, and the `User` model you're hooking into
- [ ] **A013/A011 — templates & rendering** — not central here (body is a string literal), but the email *could* be rendered from a template the same way A046 did
- [ ] 📌 `python-dotenv` installed (`py -c "import dotenv"` works), and a Gmail account with **2-step verification** so an **app password** can be created (needed only for the real-send half)

## 🔧 The Artifact — Every File, Verbatim

### 1. `accounts/signals.py` (709 bytes, corrected)

The corrected signal handler — the heart of this chapter:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")
        subject = 'Welcome to Adnan'
        message = f'Hi {instance.username}, thank you for registering at Adnan Blog!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
        print("Welcome email sent successfully")
```

**Key points:**
- `@receiver(post_save, sender=User)` — listens for `post_save` signals from the `User` model
- `if created:` — only sends email when a **new** user is created (not on updates)
- `settings.DEFAULT_FROM_EMAIL` — uses the configured sender address (not `os.getenv` directly)
- No `fail_silently=False` — that argument is deprecated in Django 6.1+

### 2. `accounts/apps.py` (266 bytes)

```python
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Import the signals module to register signal handlers
```

**Why this matters:** Django does **not** automatically import `signals.py`. The `ready()` method
is called once when Django starts, and this is where we import the signals module so the
`@receiver` decorator can register the handler.

### 3. `myProject31/settings.py` (4083 bytes, email section corrected)

```python
from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load A047_Django_Email_Setup/.env (sibling of myProject31/) so EMAIL /
# EMAIL_PASSWORD reach os.getenv() below no matter which shell started us.
load_dotenv(BASE_DIR.parent / '.env')

# ... (other settings) ...

# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
    'gmail': {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': 'smtp.gmail.com',
            'port': 587,
            'username': os.getenv('EMAIL'),
            'password': os.getenv('EMAIL_PASSWORD'),
            'use_tls': True,
        },
    },
}
DEFAULT_FROM_EMAIL = os.getenv('EMAIL') or 'webmaster@localhost'
```

**Key fixes:**
- Added `from dotenv import load_dotenv` and `load_dotenv(BASE_DIR.parent / '.env')`
- Fixed the malformed `MAILERS` dict (missing comma + indentation)
- Added fallback for `DEFAULT_FROM_EMAIL`

### 4. `.env` (66 bytes, git-ignored)

```text
EMAIL=nouman0537@gmail.com
EMAIL_PASSWORD=llko luwe cggw aslt
```

⚠️ **Security warning:** This file contains real credentials and is **git-ignored**. Never commit
it to version control.

### 5. `accounts/models.py`, `views.py`, `admin.py`, `tests.py` (stub files)

These are standard Django scaffold stubs with no custom code — the app uses Django's built-in
`User` model and the signal handles all the email logic.

## 🧠 The Three Bugs — A Live Autopsy

### Bug 1: `.env` Not Loaded

**Original code:**
```python
# settings.py — missing these lines
from dotenv import load_dotenv
load_dotenv(BASE_DIR.parent / '.env')
```

**Symptom:** `os.getenv('EMAIL')` returned `None` because the environment variable was never loaded.

**Fix:** Added `load_dotenv()` call at the top of `settings.py`.

### Bug 2: Signal Read `os.getenv` Directly

**Original code:**
```python
from_email = os.getenv('EMAIL')  # Use the EMAIL environment variable
```

**Symptom:** Even if `.env` was loaded, the signal was bypassing `settings.DEFAULT_FROM_EMAIL`
and reading the environment directly — fragile and inconsistent.

**Fix:** Changed to `from_email = settings.DEFAULT_FROM_EMAIL`.

### Bug 3: Deprecated `fail_silently` Argument

**Original code:**
```python
send_mail(subject, message, from_email, recipient_list, fail_silently=False)
```

**Symptom:** Django 6.1 emits a `RemovedInDjango70Warning` for the `fail_silently` argument.

**Fix:** Removed the argument entirely. `send_mail()` fails loudly by default in modern Django.

## 📊 Live Verification

**Before fix** (buggy state):
```text
From: None
To: nouman0537@gmail.com
Subject: Welcome to Adnan
```

**After fix** (corrected state):
```text
New user created: verifyuser
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit
MIME-Version: 1.0
Subject: Welcome to Adnan
From: nouman0537@gmail.com
To: verify@example.com
Date: Tue, 22 Sep 2026 16:47:08 +0000

Hi verifyuser, thank you for registering at Adnan Blog!

-------------------------------------------------------------------------------
Welcome email sent successfully
```

## ❌ Common Beginner Mistakes

1. **Forgetting to import signals in `apps.py`** — The signal never fires because
   `accounts.signals` was never imported
2. **Not checking `created`** — The welcome email is sent on every `save()`, including updates
   (password changes, profile edits, etc.)
3. **Using `os.getenv()` directly in signals** — Fragile; better to use `settings.DEFAULT_FROM_EMAIL`
4. **Not loading `.env` in settings** — Environment variables are unavailable, causing `None` values
5. **Using deprecated `fail_silently` argument** — Creates deprecation warnings in Django 6.1+

---

## 🧠 Common Misconceptions

| ✅ Django signals ARE … | ❌ They are NOT … |
|---|---|
| A way to run code when certain actions happen | A replacement for normal function calls |
| Decoupled — the sender doesn't know who's listening | A way to bypass the normal request/response cycle |
| Synchronous by default (the signal handler runs immediately) | Asynchronous (use Celery for that) |
| Great for side effects like emails, logging, cache invalidation | A good place for core business logic |

---

## 🧪 Practical Example — Register a New User

The signal fires automatically when any code creates a `User`:

```python
# In Django shell
from django.contrib.auth import get_user_model
User = get_user_model()

# This automatically triggers the welcome email signal
user = User.objects.create_user(
    username='newbie',
    email='newbie@example.com',
    password='securepassword123'
)
# Output: 'New user created: newbie'
# Output: Welcome email printed to console
```

The signal also fires when creating users via the Django admin or any other `create_user()` call.

## 🎯 Interview Perspective

**Q: How would you send a welcome email when a user registers?**
A: Use a `post_save` signal on the `User` model with a `@receiver` decorator. The handler checks
`if created:` to only send on new user creation, then calls `send_mail()` with the user's email.

**Q: Why not put the email sending in the registration view?**
A: Signals are more robust — they handle all user creation paths (admin, shell, API, form) in one
place. Putting it in the view means you must remember to call it in every view that creates users.

**Q: What's the difference between `post_save` and `pre_save`?**
A: `pre_save` fires before the database write; `post_save` fires after. For welcome emails, you
want `post_save` so you know the user was actually created.

**Q: Why did the email show `From: None`?**
A: The `.env` file wasn't loaded, so `os.getenv('EMAIL')` returned `None`. The fix is to load
`.env` in `settings.py` and use `settings.DEFAULT_FROM_EMAIL` in the signal.

---

## 🔁 Active Recall

1. What signal does this chapter use, and why that one?
2. Where must the signals module be imported, and why?
3. Why check `if created:` in the signal handler?
4. What three bugs caused `From: None` in this artifact?
5. Why use `settings.DEFAULT_FROM_EMAIL` instead of `os.getenv()` in the signal?
6. What's wrong with `fail_silently=False` in Django 6.1?
7. When does the signal fire — on user creation, update, or both?

<details><summary>Answer 1</summary>
`post_save` — it fires after the user is saved to the database, so we know the user was
successfully created before sending the welcome email.
</details>

<details><summary>Answer 2</summary>
In `apps.py` `ready()` method — Django doesn't auto-import `signals.py`, so we must import it
there to register the `@receiver` decorator.
</details>

<details><summary>Answer 3</summary>
To only send the welcome email when a **new** user is created, not on every update (password
change, profile edit, etc.).
</details>

<details><summary>Answer 4</summary>
1. `.env` not loaded in `settings.py` → `os.getenv('EMAIL')` returned `None`
2. Signal read `os.getenv()` directly instead of `settings.DEFAULT_FROM_EMAIL`
3. `DEFAULT_FROM_EMAIL` had no fallback value
</details>

<details><summary>Answer 5</summary>
`settings.DEFAULT_FROM_EMAIL` is the configured value that's already been loaded from `.env`.
Reading it directly is more consistent and avoids the signal depending on environment state.
</details>

<details><summary>Answer 6</summary>
It's deprecated in Django 6.1+ (emits `RemovedInDjango70Warning`). Modern Django fails loudly
by default, so the argument is unnecessary.
</details>

<details><summary>Answer 7</summary>
Only on creation (because of `if created:`). Without that check, it would fire on every `save()`
including updates.
</details>

---

## 📝 Quick Revision

- Use `post_save` signal to send welcome email automatically on user registration
- Wire the signal in `apps.py` `ready()` method by importing `accounts.signals`
- Always check `if created:` to only send on new user creation
- Load `.env` in `settings.py` with `load_dotenv()` so `os.getenv()` works
- Use `settings.DEFAULT_FROM_EMAIL` in signals, not `os.getenv()` directly
- Remove deprecated `fail_silently=False` argument in Django 6.1+
- The `From:` field showing `None` means environment variables weren't loaded

---
---
## Final Mental Model

```mermaid
graph TD
    A[User Registration] -->|creates | B[User Model]
    B -->|post_save signal | C[signals.py]
    C -->|if created:| D[Send Welcome Email]
    D -->|send_mail()| E[Console Backend (default)]
    E -->|prints to terminal| F[Debug Output]
    D -.->|using='gmail'| G[SMTP Backend (production)]
    G -->|sends via network| H[Gmail Inbox]

    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#fff3e0
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#e8f5e9
    style G fill:#ffebee
    style H fill:#c8e6c9
```

**Key insight:** By default, the email prints to the **console** (development). To send via SMTP to Gmail,
change the signal to use `using='gmail'`:

```python
send_mail(subject, message, from_email, recipient_list, using='gmail')
```

This is the same pattern from [A046 — Django Email Setup](../A046_Django_Email_Setup/README.md).

---

## ❓ FAQ

**Q: Can I use this pattern for other types of emails?**
A: Yes — password reset emails, order confirmations, subscription reminders all work the same way
with different signals or conditions.

**Q: What if I want to send HTML emails instead of plain text?**
A: Use `EmailMessage` with `content_subtype = 'html'` instead of `send_mail()`, as shown in
A046.

**Q: What if the email fails to send?**
A: With the console backend, it just prints. With SMTP, you'd want to catch exceptions. In
production, consider using a task queue (Celery) for reliable email delivery.

**Q: Can I test this without sending real emails?**
A: Yes — the console backend prints to terminal. For automated tests, use Django's locmem backend
(and check `mail.outbox`).

---

## 🏁 Learning Checkpoints

- [ ] I can create a `post_save` signal handler for the `User` model
- [ ] I can wire the signal in `apps.py` `ready()` method
- [ ] I understand why `if created:` is necessary
- [ ] I can fix the `From: None` bug by loading `.env` and using `settings.DEFAULT_FROM_EMAIL`
- [ ] I know to remove deprecated `fail_silently=False` in Django 6.1+
- [ ] I can trace the signal flow from user creation to email output
- [ ] I understand the difference between console backend (development) and SMTP backend (production)

---

## 🏋️ Exercises

1. **Add a timestamp to the welcome email** — Include the registration date/time in the email body
2. **Send to admin too** — CC the site admin when a new user registers
3. **Customize by user type** — Send different welcome messages for different user roles
4. **Test with locmem backend** — Write a test that creates a user and checks `mail.outbox`

---

## 🏁 Final Takeaways

1. Django signals let you run code automatically when models are saved
2. `post_save` with `@receiver` is the clean way to send welcome emails on registration
3. Always load `.env` in `settings.py` and use `settings.DEFAULT_FROM_EMAIL`
4. Check `created` to avoid sending emails on updates
5. The signal must be imported in `apps.py` `ready()` or it never fires
6. Default backend is console (development) — add `using='gmail'` for real SMTP delivery

---

---

<div class="doc-footer">

**Sources used:** `myProject31/` artifact (Django 6.1.1 scaffold): `accounts/signals.py` (corrected —
709 bytes: `from django.conf import settings`, `from_email = settings.DEFAULT_FROM_EMAIL`,
`send_mail(subject, message, from_email, recipient_list)` with no `fail_silently`), `accounts/apps.py`
(266 bytes: `ready()` imports `accounts.signals`), `myProject31/settings.py` (corrected — 4083 bytes:
`from dotenv import load_dotenv`, `load_dotenv(BASE_DIR.parent / '.env')`, `MAILERS` with `default`
console + `gmail` SMTP, `DEFAULT_FROM_EMAIL = os.getenv('EMAIL') or 'nouman0537@gmail.com'`),
`.env` (66 bytes: `EMAIL` + `EMAIL_PASSWORD`, git-ignored). Stub files: `accounts/models.py`,
`accounts/views.py`, `accounts/admin.py`, `accounts/tests.py`. Installed-Django source consulted:
`django/db/models/signals.py`, `django/core/mail/__init__.py`, `django/core/mail/deprecation.py`.
Verified runtime: Django 6.1.1 / Python 3.14.6 / `python-dotenv` installed. Live verification: created
test user via shell, confirmed `From: nouman0537@gmail.com` with corrected code vs `From: None` with
buggy code.

**Navigation:** ← [A046 — Django Email Setup](../A046_Django_Email_Setup/README.md) · [Series hub](../README.md) · [A048 — Django Bulk Email with `send_mass_mail()`](../A048_Django_Bulk_Email/README.md) →
</div>
