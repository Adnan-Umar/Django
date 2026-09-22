# 🚀 A044 — Session Storage: Get & Set Methods

`📖 Lecture A044` · `🎓 Track: Core Django` · `📶 Level: Intermediate` · `✅ Status: Documented`

> [!NOTE]
> **About this chapter's sources:** No lecture transcript exists in the folder, and the owner's
> command journal `commands.txt` adds **no new lines** for this lecture — it still ends at its
> 54th line, `pip install Pillow` (the A038 requirement). The chapter therefore rests on a single
> primary source: the **`myProject28/` artifact** — a Django **6.1.1** project whose `blog` app
> implements the session's three verbs with three function views: **set** (two keys),
> **get** (with defaults), and **delete** (`flush()`), on root-mounted routes. Every file quoted
> below is reproduced verbatim from that artifact.
>
> The artifact is the series' second data-free project (like A042): no models, no migrations, no
> templates — because a session is *not* a model. Its real database holds **11 tables including
> `django_session`, and 0 rows**: the table exists (migrations ran), but no session was ever
> created through the real server. That emptiness is itself a fact this chapter explains —
> sessions are created **lazily**, and reading one never creates it (proved live below).
>
> This chapter was **verified live**, not just read: every claim below was measured through the
> Django test client and the in-memory test database (the artifact's `db.sqlite3` was opened
> read-only and never written), plus Django's own source
> (`django/contrib/sessions/backends/base.py`, `db.py`, `middleware.py`, `django/core/signing.py`).
> Verified: the exact cookie attributes, the signed three-segment payload and its plaintext
> readability, tamper detection (`BadSignature` → `SuspiciousSession` warning → empty session),
> the laziness of session creation, the key-minting moment, the `del`/`clear()`/`flush()`
> differences, expiry modes, and `cycle_key()`. Anything supplementary to the artifact is marked 📌.
>
> This lecture builds on [A042 — Django Middleware](../A042_Django_Middleware/README.md)
> (whose `SessionMiddleware` and `AuthenticationMiddleware` layers this chapter finally uses
> hands-on), [A036 — Authentication & Permissions](../A036_Authentication_&_Permissions/README.md)
> (the login state a session underlies), and the GET-form/`request.GET` habits of A029/A040; and
> it is the direct continuation of
> [A043 — Pre-Save & Post-Save Signals](../A043_Pre_Save_&_Post_Save_Signals/README.md), whose
> closing question — *what changes when the bell must ring after the doorway has closed* — this
> chapter answers with the state that *outlives* the request.

---

## 🧭 What You Will Learn

- [ ] What a session **is** and where its two halves live: a **signed cookie holding only a key** (`sessionid`), and the **data hanging in `django_session`** behind it
- [ ] The exact payload format — `<urlsafe-base64(JSON)>:<timestamp>:<HMAC signature>` — and why that makes session data **tamper-evident but not secret** (the JSON reads in plaintext; verified)
- [ ] How tampering is handled: `signing.loads` raises `BadSignature`, but `SessionStore.decode` **swallows it, logs `SuspiciousSession`, and returns `{}`** — the forged session is simply *empty*
- [ ] **Set**: `request.session['k'] = v` marks the session `modified`; the key and the DB row are minted only when something **saves** — and `SessionMiddleware.process_response` is what saves in a real request
- [ ] **Get**: `.get(key, default)` versus `[key]` (`KeyError`) — and the laziness proof that a **read-only request never creates a session or sets a cookie** (verified: no `Set-Cookie`, no new row)
- [ ] **Delete**: the three spellings — `del session[k]` (one key), `clear()` (all data, key kept, row survives), `flush()` (all data + key rotated away + row deleted) — and why `flush()` is the logout verb
- [ ] What the response actually sends on delete: a **cookie deletion** (`expires=Thu, 01 Jan 1970`, `max-age=0`), verified
- [ ] Expiry's two clocks: `SESSION_COOKIE_AGE` (14 days here) vs `session.set_expiry(...)` — including `set_expiry(0)` meaning *at browser close*
- [ ] 📌 `cycle_key()` (new key, data preserved — the session-fixation defence) and the `signed_cookies` engine, where the *whole payload rides in the cookie* — and what that implies for secrets

## 🎯 Why This Lecture Matters

HTTP has no memory. Every request you have written so far arrived at the view as a stranger —
`request` was handed to `home_view`, used, and *thrown away*. That is HTTP's design, and it is why
A029's forms, A039's pagination, and A040's search all carried their state in the URL: a query
string was the only memory the protocol offered.

The moment you need state that **outlives the request but belongs to one visitor** — a login, a
cart, a search you can come back to, a wizard's half-filled step 2 of 3 — neither of the two
obvious homes works:

- **The URL cannot hold it** (it leaks into bookmarks, logs, referrer headers, and other tabs).
- **The database cannot be keyed by it** (which row is *yours*? HTTP gives you no identity).

A **session** is Django's third home: the visitor carries a small, opaque, tamper-proof **ticket**
(a cookie named `sessionid`), and the data hangs in the database **behind the ticket**. The ticket
identifies; the database stores. Both halves are trivially simple — and both are commonly
misunderstood, because the ticket looks like a login and the database looks like a model.

This lecture dissects the artifact's three views — set, get, delete — and, in the process, answers
the questions that decide whether your session code is *correct* or merely *working*:

- Why does the first `GET /get-session/` show **Guest** with **no cookie and no database row**?
- Why does `set_session` alone mint the key — and what actually saves the row (it is not the view)?
- Why is the stored payload **readable in plaintext** — and what exactly does the signature protect?
- Why does the artifact's `delete_session` use `flush()` when the commented-out `del`-based version
  *almost* works — and what does each leave behind?

These are also the A036 questions in disguise: `login(request, user)` is, mechanically, four lines
that attach the user id to `request.session` and call `cycle_key()`. A043 asked what happens when
the bell must ring after the doorway closed; this chapter shows the *doorway itself* keeping a
locker between visits.

## ✅ Prerequisites

- [ ] **A042 — middleware** — `SessionMiddleware` (index 1 of the seven shipped layers) is the
      machinery behind every `request.session` here; you should know it attaches state per request
      and saves on the way out.
- [ ] **A036 — authentication** — `request.user` riding on a session is the motivating case; the
      artifact deliberately implements a *non-login* session so the mechanics are visible.
- [ ] **A029 — GET forms and `request.GET`** — the contrast case: URL state versus server-side
      state, and when each is right.
- [ ] **A039/A040 — the reading room** — every page so far was stateless; this is the first that
      remembers.
- [ ] 📌 **Cookies, generally** — what `Set-Cookie` is (a name, a value, and flags); A045 covers
      raw cookies, so only the browser's side is assumed here.
- [ ] 📌 **Python dict semantics** — `dict.get(key, default)`, `del d[key]`, `KeyError`: the
      session API is deliberately dict-shaped.

## 🧠 What Is the Session?

**Definition (beginner):** the session is Django's per-visitor memory. You write
`request.session['username'] = 'John Doe'` and, on the visitor's *next* request,
`request.session.get('username')` hands the same value back — with nothing in the URL and nothing
in the HTML.

**Definition (technical):** a session is a **server-side key–value store keyed by a random
32-character string**, plus a **cookie** that tells the server which string belongs to this
browser. The cookie carries the key only; the data lives server-side (here, in the `django_session`
table of the artifact's SQLite database, via `SESSION_ENGINE =
django.contrib.sessions.backends.db`).

That split is the entire design, and it is why session data can be rich and even secret-ish:

```text
browser                          server (django_session table)
┌───────────────────────────┐     ┌──────────────────────────────────────────────┐
│ cookie: sessionid =       │ ──► │ session_key:  til4lshjs4kdnmjtypezd85ug12jb4w6
│   til4lshjs4kdnmjtypezd…  │     │ session_data: <signed payload — JSON>        │
│   (32 chars, HttpOnly)    │     │ expire_date:  2026-10-05 07:57:57 UTC        │
└───────────────────────────┘     └──────────────────────────────────────────────┘
```

The cookie is the *address*; the row is the *contents*. Lose the cookie and the server cannot find
your row; lose the row and the cookie points at nothing. Both directions are verified below
(a fresh client reads `Guest`; a flushed row reads `Guest` too).

**Why not just a cookie?** Because cookies travel with *every* request, are size-limited (~4 KB),
and are readable by their owner. Putting `{'username': …, 'course': …}` in the cookie means the
visitor can read and (without the signature) forge it; putting it server-side means the visitor
carries nothing but an opaque 32-character key. A042's tamper lesson applies to the ticket; the
payload never rides along. 📌 (Django *does* ship a cookie-only engine — §Practical Example shows
what it exposes — which is exactly how you can *see* the difference.)

**Why the views here look so plain:** because the session is *already* attached before the view
runs. `SessionMiddleware.process_request` put `request.session` on the request (A042's layer at
index 1); the view just uses the dict. The three views in this artifact are 3, 3, and 2 lines of
real logic — the machinery is the middleware.

## 🔧 The Artifact — Every File, Verbatim

`myProject28/` is a `django-admin startproject` scaffold (Django 6.1.1) plus one app: **no models,
no migrations beyond `__init__`, no templates, no admin registrations**. The three views and three
routes are the lecture; `settings.py` supplies the machinery.

### 1. `blog/views.py` — set, get, delete (verbatim, 24 lines)

```python
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def set_session(request):
    request.session['username'] = 'John Doe'
    request.session['course'] = 'Django'
    return HttpResponse("Session data Saved Successfully.")

def get_session(request):
    username = request.session.get('username', 'Guest')
    course = request.session.get('course', 'Not Enrolled')
    return HttpResponse(f"Welcome: {username}, You are enrolled in: {course}")

def delete_session(request):
    # try:
    #     del request.session['username']
    #     del request.session['course']
    #     return HttpResponse("Session data deleted.")
    # except KeyError:
    #     return HttpResponse("Session data not found.")

    request.session.flush()  # This will delete all session data
    return HttpResponse("All session data deleted.")
```

Line by line, because every choice is load-bearing:

1. **`set_session`** — plain dict assignment on `request.session`. Two keys, no `.save()` call,
   no cookie code: the middleware does the saving (see §Set).
2. **`get_session`** — `.get(key, default)` twice, with sensible fallbacks (`'Guest'`,
   `'Not Enrolled'`). This is why a stranger's first visit still renders a complete sentence
   instead of crashing. The bracket form would raise `KeyError` here.
3. **`delete_session`** — the commented-out block is the **partial delete**: delete each key
   individually, with a `try/except KeyError` guard for the "nothing was stored" case. The active
   line is the **full delete**: `flush()` empties every key *and* abandons the session key (a new
   one is minted on the next use). Both spellings are measured in §Delete.

### 2. `blog/urls.py` — three root-mounted verbs

```python
from django.urls import path
from . import views

urlpatterns = [
    path('set-session/', views.set_session, name='set_session'),
    path('get-session/', views.get_session, name='get_session'),
    path('delete-session/', views.delete_session, name='delete_session'),
]
```

`myProject28/urls.py` includes this app at `path('', include('blog.urls'))` — same root-mount
pattern as every chapter since A020, so the three verbs live at the site root.

### 3. `settings.py` — the machinery this lecture stands on

```python
INSTALLED_APPS = [
    ...
    'django.contrib.sessions',   # the app that owns django_session
    ...
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   # ← attaches request.session
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ← rides on the session
    'django.contrib.messages.middleware.MessageMiddleware',      # ← stores per-session too
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

The session settings are *not* in the file — so every value is the Django default, which is
exactly what makes the probe below general:

| Setting (all defaults) | Value | Meaning for this chapter |
|---|---|---|
| `SESSION_ENGINE` | `django.contrib.sessions.backends.db` | data lives in the `django_session` table |
| `SESSION_COOKIE_NAME` | `sessionid` | the ticket's name |
| `SESSION_COOKIE_AGE` | `1209600` (14 days) | the ticket's printed expiry |
| `SESSION_COOKIE_HTTPONLY` | `True` | JavaScript cannot read the ticket |
| `SESSION_COOKIE_SAMESITE` | `'Lax'` | the ticket is not sent on cross-site POSTs |
| `SESSION_SAVE_EVERY_REQUEST` | `False` | the row is saved only when the session was **modified** |

Two recurring series quirks are also present (flagged per §12, not middleware issues): the
`STATICFILES_DIRS` ghost shelf (`staticfiles.W004`) and the inert `MAILERS` block (Django 6.1.1
knows only `EMAIL_BACKEND`). And the real `db.sqlite3` holds 11 tables — including
`django_session` — with **0 rows**: migrated, but never used by a real browser. That is the
laziness proof's opening exhibit.

## 🧠 Set — What `request.session['k'] = v` Actually Does

The view is two dict assignments. What happens around them is the interesting part, and it is
all measured:

```text
(after SessionMiddleware.process_request)
fresh request.session.session_key  : None      ← no key yet
fresh request.session.accessed     : False

set_session runs both assignments:
after set view: session_key        : None      ← STILL no key — lazy!
after set view: modified           : True
after set view: items              : {'username': 'John Doe', 'course': 'Django'}

after an explicit session.save():
session_key                        : hd01lyljdhsh64t2odbyg3a35beoo6br
row count                          : 1
```

Three facts fall out:

1. **Nothing exists until something saves.** Assignments flip `modified` to `True` and fill the
   in-memory dict — the key (`session_key`) and the `django_session` row are minted only at
   `save()` time. In a real request, *the middleware is the saver*:
   `SessionMiddleware.process_response` calls `request.session.save()` when `modified` is `True`
   (since `SESSION_SAVE_EVERY_REQUEST` is `False`, an unmodified session is not re-saved).
2. **The key is random and opaque**: 32 characters drawn from
   `VALID_KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'` (verified: the minted key
   `hd01lylj…` is all lowercase/digits, 32 long), generated by `_get_new_session_key()` in a loop
   until it is unused in the table.
3. **The response carries two things at once**: the `Set-Cookie: sessionid=…` header
   (`Path=/`, `HttpOnly`, `SameSite=Lax`, `Max-Age=1209600`) *and* the new database row. Verified
   for `GET /set-session/`:

```text
GET /set-session/ → 200 "Session data Saved Successfully."
Set-Cookie: sessionid=til4lshjs4kdnmjtypezd85ug12jb4w6; Path=/; HttpOnly; SameSite=Lax
            Max-Age=1209600
Vary: Cookie                              ← because the session was accessed
django_session rows: 1
```

The `Vary: Cookie` header is a bonus you get for free: because the session was *accessed*,
`SessionMiddleware` patches `Vary: Cookie` so caches never hand one visitor's page to another
(the A039 caching lesson gets a body here).

## 🧠 Get — `.get(key, default)`, `[key]`, and the Laziness Proof

The read view's two lines are a small masterclass in the API:

```python
username = request.session.get('username', 'Guest')
course = request.session.get('course', 'Not Enrolled')
```

`request.session` is dict-shaped *on purpose*: `.get(key, default)` returns the fallback instead
of raising, `[key]` raises `KeyError`, and `setdefault`/`pop`/`keys`/`items` all behave as the
`dict` you know (all verified against the real store). The artifact chose `.get` + defaults
because a *stranger's first visit is normal*, not exceptional — the fallbacks **are** the content
for that case:

```text
GET /get-session/ (the same client that ran set-session)
    → 200 "Welcome: John Doe, You are enrolled in: Django"
    Set-Cookie again: no        (nothing modified → nothing to save)
    django_session rows: still 1

GET /get-session/ (a fresh client, no cookie at all)
    → 200 "Welcome: Guest, You are enrolled in: Not Enrolled"
    Set-Cookie sessionid: absent
    django_session rows: unchanged
```

And the request-level detail that explains the second result — **reading is not writing**:

```text
fresh request.session.session_key : None
after read-only view: session_key  : None
after read-only view: accessed / modified : True / False
```

`.get()` marks the session `accessed` (which is why `Vary: Cookie` appears) but *not* `modified`,
so `process_response` neither saves a row nor sets a cookie. The fresh visitor leaves with no
ticket and no locker — verified: the row count did not move. **Sessions are created lazily, by
writes only.** That is why the artifact's database had 0 rows despite the app being installed all
along.

> ⚠️ The same laziness has a sharp edge: `get_session` never *writes*, so a visitor can read the
> page forever without ever owning a session — and that is correct. If you need a session to exist
> (e.g. a CSRF-token-bearing form page), you must write something (`request.session['seen'] = True`)
> or call `request.session.save()` explicitly.

## 🧠 The Payload — Signed, Not Encrypted

The `session_data` column is not "just the dict". It is one string with three `:`-separated
segments, captured verbatim from the row `set_session` created:

```text
eyJ1c2VybmFtZSI6IkpvaG4gRG9lIiwiY291cnNlIjoiRGphbmdvIn0:1x8YuT:G1Wsox4L329RsdHBy5DwVF5LVzxSSzoDgP7UrasgZTE
```

| Segment | Value | What it is |
|---|---|---|
| 1 | `eyJ1c2VybmFtZSI6…` | **url-safe base64 of the JSON** — unpadded. Decodes to `{"username":"John Doe","course":"Django"}` |
| 2 | `1x8YuT` | base62 **timestamp** (when it was signed) — the max-age check needs it |
| 3 | `G1Wsox4L329R…` | **HMAC signature** — keyed by `SECRET_KEY` with `key_salt = django.contrib.sessions.SessionStore` |

Two consequences, both measured and both security-critical:

1. **Signed, not encrypted.** Segment 1 is *plaintext JSON* in a slightly opaque coat: anyone with
   the string (in this DB-backed engine, anyone who can read the database) can decode it without
   the secret key. Never put a password, a token, or a card number in `request.session` believing
   the format hides it. The *cookie* hides nothing here either — in the DB engine it carries only
   the key; in the `signed_cookies` engine (§Practical Example) it carries this whole string.
2. **The signature is the tamper seal.** Feed the payload one modified byte and the check fails:

```text
signing.loads(raw,      salt='django.contrib.sessions.SessionStore') → {'username': 'John Doe', ...}
signing.loads(tampered, salt='django.contrib.sessions.SessionStore') → BadSignature: Signature … does not match
signing.loads(raw, salt=…, max_age=0)                                → SignatureExpired: Signature age 0.12s > 0
```

What makes the tamper story *interesting* is what Django does with that failure. `SessionStore.decode`
does **not** raise — it catches `BadSignature`, logs a security warning, and returns an empty dict
(quoted from `django/contrib/sessions/backends/base.py`):

```python
def decode(self, session_data):
    try:
        return signing.loads(
            session_data, salt=self.key_salt, serializer=self.serializer
        )
    except signing.BadSignature:
        logger = logging.getLogger("django.security.SuspiciousSession")
        logger.warning("Session data corrupted")
    except Exception:
        # ValueError, unpickling exceptions. If any of these happen, just
        # return an empty dictionary (an empty session).
        pass
    return {}
```

Verified end-to-end: overwrite the row's `session_data` with a forged payload, reload the session
through a real request — the visitor gets **Guest** (the empty session), not the forged values:

```text
tampered payload: <attacker's JSON, signed with the ORIGINAL signature>
st.decode(tampered)               → {}
security log: django.security.SuspiciousSession | WARNING | Session data corrupted
GET /get-session/ with the tampered session → "Welcome: Guest, You are enrolled in: Not Enrolled"
```

Note the asymmetry: the attacker cannot *forge* state (the signature fails), but Django will not
*reject* the request either — the tampered session silently becomes an empty one. The
`SuspiciousSession` warning is the tell for an ops dashboard, not an error page. And the
`expires=…`/max-age check rides on segment 2: a payload older than `SESSION_COOKIE_AGE` is
`SignatureExpired`, not accepted.

> ⚠️ **`SECRET_KEY` rotation and sessions are coupled.** The signature is keyed by `SECRET_KEY`
> (via `SECRET_KEY_FALLBACKS` for rotation). Lose the key and every session's payload becomes
> `BadSignature` — every visitor is logged out at once. That is the mechanism behind the
> "don't leak your secret key" warning on every scaffold since A004.

## 🧠 Delete — `del` vs `clear()` vs `flush()`

The artifact's active line is `flush()`, and the commented-out block is the *almost*-equivalent
`del`-based version. The difference is not stylistic; it is two measured behaviours:

| Spelling | Data | `session_key` | Row on next save | Cookie | Use when |
|---|---|---|---|---|---|
| `del session['username']` | removes one key | **kept** | same row updated | unchanged | remove a cart line |
| `session.clear()` | removes **all** keys | **kept** (`is_empty()` still `False`) | same row, empty payload | unchanged | reset the session's *contents* |
| `session.flush()` | removes all keys | **None** — abandoned | a **new** key is minted | **deleted** (`expires=1970`, `max-age=0`) | **logout**, or after a privilege change |

Measured for the row-visible difference — delete both keys with `del` and save:

```text
after del both keys: items {}   is_empty False   session_key 68plez7r4c76eg7sx7oyozu3m4pc06ky
rows after saving the emptied session: 1   ← the SAME row, now empty
```

…versus `flush()`:

```text
flush(): key before 90lrlwawgdiqi2it8rrite67gjb8441t
flush(): key after  None
rows after flush(): 1   ← (2 sessions existed; the flushed row is GONE)
```

`clear()` empties the payload but keeps the identity; `flush()` destroys the identity *and* the
data, and tells the browser to drop the ticket. The response header on `GET /delete-session/` is
the browser-side proof:

```text
GET /delete-session/ → 200 "All session data deleted."
Set-Cookie: sessionid=""; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0;
            Path=/; HttpOnly; SameSite=Lax
django_session rows: 0
GET /get-session/ afterwards → "Welcome: Guest, You are enrolled in: Not Enrolled"
```

That `expires=Thu, 01 Jan 1970 … Max-Age=0` is a **cookie deletion**, not a new cookie: the
browser's job is to throw the ticket away. The commented-out `del` version would have left the
ticket valid — same session, just emptier — which is why the two blocks are *not* interchangeable,
and why the artifact's choice (flush) is the right one for a verb named *delete session*.

## ⏰ Expiry — Two Clocks, Not One

A session expires on **two** clocks, and they disagree on purpose:

1. **The browser's clock** — the cookie's `Max-Age`/`Expires` (how long the *ticket* is presented).
2. **The server's clock** — the `django_session.expire_date` column (how long the *row* is loadable).

The artifact uses the defaults for both: 14 days (`SESSION_COOKIE_AGE = 1209600`), verified — the
Set-Cookie carried `Max-Age=1209600` and the row's `expire_date` landed `1209599` seconds after
creation. Both clocks must agree for a session to survive; either one running out logs the visitor
out (a valid cookie over an expired row loads as "no session", and an expired cookie never reaches
the row).

Per-session overrides come from `session.set_expiry(...)` (verified):

```text
set_expiry(60)   → get_expiry_age() == 60        (both clocks move)
set_expiry(None) → get_expiry_age() == 1209600   (back to the default)
set_expiry(0)    → get_expire_at_browser_close() == True
```

`set_expiry(0)` is the special one: the **cookie gets no `Max-Age`** (a browser-session cookie,
deleted when the tab closes) while the server still honours the flag — `get_expiry_age()` keeps
reporting the default but `get_expire_at_browser_close()` is `True`, and `SessionMiddleware` omits
`Max-Age` from the header. 📌 That is the switch behind "log me out when I close the browser"
checkboxes, and A036's login flow can pass it through `login(request, user)`'s
`request.session.set_expiry`.

📌 Two housekeeping facts complete the picture: `manage.py clearsessions` deletes expired
`django_session` rows (the DB backend never deletes them itself — schedule it or the table grows
forever); and a session is refreshed in place — `SESSION_SAVE_EVERY_REQUEST = True` would re-save
(and re-date) the cookie on every request.

## 📊 Live Verification — Clean Cycle, Clean Numbers

The phase-1 cycle with the row counter reset before it (in-memory test database; the artifact's own
`db.sqlite3` untouched):

```text
P1 rows before set:                              0
P1 rows after GET /set-session/:                 1
P1 rows after GET /get-session/ (same client):   1
P1 rows after GET /delete-session/:              0
P1 rows after a further read-only GET:           0
```

Every claim in the chapter is one row of that table or of the following captures:

```text
GET /set-session/  → 200 "Session data Saved Successfully."
GET /get-session/  → 200 "Welcome: John Doe, You are enrolled in: Django"      (same client)
GET /get-session/  → 200 "Welcome: Guest, You are enrolled in: Not Enrolled"   (fresh client)
GET /delete-session/ → 200 "All session data deleted."
GET /get-session/  → 200 "Welcome: Guest, You are enrolled in: Not Enrolled"   (after delete)
```

And the request-level states, in order:

```text
fresh request.session.session_key : None ; accessed/modified : False/False
after read-only get_session       : None ; accessed/modified : True/False   ← read ≠ write
after set_session                 : None ; accessed/modified : True/True    ← key still lazy
after explicit save()             : <32-char key> ; rows 1
after flush()                     : None ; the row is gone
```

`manage.py check` on the artifact: only the recurring `staticfiles.W004` (the `static/` ghost
shelf — settings quirk, not session machinery).

## 🧱 Important Vocabulary

| Term | Simple meaning | Technical meaning | 🧷 Memory hook |
|---|---|---|---|
| **Session** | Django's per-visitor memory | a server-side dict keyed by a random 32-char string, addressed by a `sessionid` cookie | 🧷 the cloakroom locker |
| **`sessionid` cookie** | the locker's ticket | name from `SESSION_COOKIE_NAME`; value = the `session_key`; `HttpOnly`, `SameSite=Lax`, `Max-Age=1209600` by default | 🧷 the numbered ticket in your pocket |
| **`session_key`** | the locker's number | 32 chars from `VALID_KEY_CHARS` (lowercase+digits), minted at first save, `None` before; `flush()` abandons it | 🧷 the number stamped on the ticket |
| **`request.session`** | the dict Django attaches | a `SessionStore` instance (from `SESSION_ENGINE`), put on the request by `SessionMiddleware.process_request` | 🧷 the locker the middleware opens for you |
| **`.get(key, default)`** | read with a fallback | returns the default when absent — the right call for a stranger's first visit; never raises | 🧷 the polite question |
| **`session[k] = v`** | write a value | marks the session `modified`; nothing is stored until `save()` — minting the key and the row | 🧷 putting a coat in the locker |
| **`modified` / `accessed`** | "changed" / "looked at" | flags `SessionMiddleware` reads: `modified` → save + cookie; `accessed` → `Vary: Cookie` only | 🧷 touched vs rearranged |
| **`flush()`** | end the session entirely | clears all data, drops the key, deletes the row on the next save; the response deletes the cookie — the logout verb | 🧷 handing back the ticket, coat and all |
| **`clear()`** | empty the locker, keep the key | removes all keys but keeps `session_key` (and the row) — `is_empty()` stays `False` | 🧷 wiping the locker, keeping the ticket |
| **`cycle_key()`** | new locker, same coat | regenerates `session_key`, preserving data — the session-fixation defence used by `login()` | 🧷 moving your coat to a fresh locker |
| **`set_expiry` / `get_expiry_age`** | per-session lifetime | `0` = at browser close; `None` = back to `SESSION_COOKIE_AGE`; integers = seconds | 🧷 a shorter ticket |
| **Signed payload** | tamper-evident session data | `urlsafe_b64(JSON) : timestamp : HMAC(SHA-256)` keyed by `SECRET_KEY` + `key_salt`; *readable without the key* | 🧷 a sealed envelope, not a safe |
| **`SuspiciousSession`** | Django's tamper alarm | logged (WARNING, `django.security.SuspiciousSession`) when `decode()` hits a `BadSignature`; the session becomes `{}` | 🧷 the stamp on a rejected note |
| **`SESSION_ENGINE`** | where the data hangs | `db` (default, `django_session`), `cached_db`, `cache`, `file`, `signed_cookies` — same dict API | 🧷 which warehouse the lockers live in |
| **Laziness** | no session until needed | a read-only request sets no cookie and creates no row; sessions are born from writes only (verified) | 🧷 no locker until you store something |

New terms must also be added to `docs/MEMORY.md` §2.

## 💡 Real-World Analogy — The Cloakroom's Numbered Locker

A038 handed file uploads a **cloakroom**: the coat goes on a rack, the visitor keeps a ticket. This
lecture is the same institution, watched closely — and the session is its **numbered locker**,
which is the exact right shape for "state that outlives the request but belongs to one visitor".

The visitor arrives with nothing (the artifact's `0 rows`). At the **desk** (`SessionMiddleware`,
on the way in), no locker exists yet — just an empty ticket stub. When the visitor *stores*
something (`set_session`: two keys), the clerk mints a locker number, writes the contents to the
locker (`django_session`), and staples the number to a **ticket** (`Set-Cookie: sessionid=…`,
`HttpOnly`, `SameSite=Lax`, good for 14 days). Next visit, the visitor hands over the ticket; the
clerk opens *that* locker; the contents are back — `Welcome: John Doe…`.

Every measured fact has a cloakroom twin:

- **The ticket is a number, not the coat.** Losing the ticket (no cookie) means the clerk cannot
  find the locker — `Guest`, no `Set-Cookie`, no new locker (verified). Losing the locker (row
  flushed) means the ticket points at nothing — also `Guest`.
- **The contents are sealed, not hidden.** Anyone who can open the locker can read the coat's
  pockets (the signed JSON decodes in plaintext); the seal only proves nobody *rewrote* the label.
  Tamper with the label and the clerk finds the seal broken, logs it (`SuspiciousSession`), and
  hands back an **empty** locker — not the forged contents.
- **The clerk is paid per transaction, not per glance.** A visitor who only *peeks* (`get_session`)
  never gets a locker; the clerk files nothing (verified: no cookie, no row). Coats are recorded
  when stored (`modified=True` → save), not when glanced at (`accessed=True` → just `Vary: Cookie`).
- **Three ways to leave, three different effects.** Take one item out (`del`) — the locker keeps
  your number and the other items. Empty it completely but keep the number (`clear()`) — the locker
  stays assigned to you, holding nothing (verified: `is_empty()` still `False`, row survives).
  **Hand back the ticket** (`flush()`) — the locker is released, the record is erased, and the
  ticket you carry is voided at the door (the `Max-Age=0` cookie deletion). That is why a logout
  button must call `flush()`: "clear" leaves you holding a valid ticket to an empty locker.
- **Re-keying on privilege change:** the cloakroom moves your coat to a *fresh* locker and issues a
  new ticket (`cycle_key()`) — the old number is dead, so a ticket that was stolen while you were
  anonymous no longer opens anything. Measured: key changes, contents preserved.

📌 This model extends A038's cloakroom rather than replacing it: the racks were for *files*; the
lockers are for *state*. Same building, same tickets, different shelves.

## ❌ Common Beginner Mistakes

1. **Reading a session key with brackets** — `request.session['username']` on a stranger's first
   visit raises `KeyError` and 500s the page. The artifact's `.get(key, default)` is the pattern:
   *absence is normal*.
2. **Expecting a session to exist after a read** — `get_session` sets no cookie and creates no row
   (verified). If the next page assumes a session, it will find none. Sessions are born from
   **writes**, and only writes.
3. **Saving explicitly everywhere** — `request.session.save()` after every assignment is noise.
   `SessionMiddleware.process_response` saves when `modified` is `True`; the view should just
   mutate the dict (the only times you need an explicit `save()` are "create the row now" cases).
4. **Using `clear()` for logout** — it empties the data but keeps the ticket valid
   (`is_empty()` still `False`, row survives, cookie unchanged). Logout is `flush()`, plus
   `logout(request)` in A036's flow (which calls `flush()` and clears the user).
5. **Storing secrets in the session believing they're encrypted** — the payload is signed, not
   encrypted (segment 1 is plaintext JSON; verified). It is tamper-*evident*, not secret — and in
   the `signed_cookies` engine it is *readable by the visitor* (§Practical Example).
6. **Assuming the session row is cleaned up automatically** — the DB backend never deletes
   expired rows; `manage.py clearsessions` exists for that. An un-cleared `django_session` grows
   one row per visitor forever.
7. **Forgetting `Vary: Cookie` is there for a reason** — the session is accessed on nearly every
   real page, so caching layers *must* vary on the cookie. Strip the header and A039's cache will
   serve John Doe's page to a stranger.
8. **Testing sessions in one request only** — the point of a session is the *next* request. The
   artifact's three views form a sequence for exactly that reason; a test that never revisits
   `get-session/` proves nothing.

## 🧠 Common Misconceptions

| ✅ Django IS … | ❌ It is NOT … |
|---|---|
| A **two-part design**: an opaque cookie key + server-side data | The cookie carrying the session data (except in the `signed_cookies` engine, deliberately 📌) |
| **Signed, tamper-evident** data — a forged payload is rejected by `BadSignature` and degrades to `{}` | **Encrypted** data — the JSON decodes in plaintext without the secret key (verified) |
| **Lazily created** — reads set no cookie, write no row; writes mint key + row on first `save()` | Created for every visitor on first contact |
| Saved **by the middleware** on the way out, when `modified` | Saved by the view, or on every request (`SESSION_SAVE_EVERY_REQUEST=False`) |
| `flush()` as the **logout** verb — key abandoned, row deleted, cookie deleted | Interchangeable with `del`/`clear()`, which keep the key (and the row) alive |
| A **server-side store** keyed by `SESSION_ENGINE` — swappable to cache/file/cookie engines | A model you can query with the ORM (it has its own table and API, deliberately not `models.Model`) |
| Expiry on **two clocks** (cookie `Max-Age` and `expire_date`) with per-session overrides | One clock, or "expires when the browser closes" by default (default is 14 days, `Max-Age=1209600`) |

## 🧪 Practical Example — The Login Shape, and Seeing the Cookie Engine

The artifact's three views are the *skeleton*; A036's real login adds two lines. Seeing them
together is the point of the lecture:

```python
def login_view(request):
    user = authenticate(request, username=…, password=…)   # A036
    if user is not None:
        request.session.cycle_key()      # ① new locker — kills any stolen pre-login ticket
        request.session[views.SESSION_KEY] = user.pk   # ② remember WHO (A036's actual key name)
        return redirect('dashboard')
    return render(request, 'login.html', {'error': 'Invalid credentials'})

def logout_view(request):
    request.session.flush()              # ③ the artifact's verb — same as logout()'s core
    return redirect('login')
```

**Explanation:** ① is why `cycle_key()` exists (measured: new key, data preserved) — a session
created *before* authentication can have been planted by an attacker (session fixation); after
`cycle_key()`, a stolen pre-login ticket opens nothing. ② is all `login()` really stores
(`SESSION_KEY = '_auth_user_id'` 📌) — `request.user` is `AuthenticationMiddleware` reading that
key. ③ is this chapter's `flush()` — `django.contrib.auth.logout()` calls `request.session.flush()`
too, then clears the user. The artifact has, without knowing it, implemented the logout half of
Django's auth system.

### 📌 Seeing the cookie engine — the same views, no database

Flip one setting and the *entire payload* moves into the cookie:

```python
with override_settings(SESSION_ENGINE="django.contrib.sessions.backends.signed_cookies"):
    r = Client().get("/set-session/")
```

Measured — the `sessionid` cookie now **carries the session data itself**:

```text
cookie value: eyJ1c2VybmFtZSI6IkpvaG4gRG9lIiwiY291cnNlIjoiRGphbmdvIn0:1x8Yxe:AsQAZljeI33igT1mo_tsc38OWseaRdAEtQhMKHbj6cM
segment 0 decodes to: {"username":"John Doe","course":"Django"}    ← plaintext
round trip: GET /get-session/ → "Welcome: John Doe, You are enrolled in: Django"
django_session rows written: 0
```

Same three-segment format, same tamper seal — but now the coat rides *in the ticket*. That is the
concrete demonstration of "signed, not encrypted": with this engine the visitor can read their own
session's contents with any base64 decoder. It also shows the trade the engine makes: zero
database rows, at the price of shipping all data on every request. The DB engine (the artifact's)
keeps data server-side and ships 32 opaque characters.

📌 And the engine list is the same API either way — `db`, `cached_db` (Redis/memcache in front of
the DB), `cache`, `file`, `signed_cookies`. Switching is one setting; the three views never change.
That is the "server-side store keyed by `SESSION_ENGINE`" sentence from §Misconceptions, made
measurable.

## 🎯 Interview Perspective

> [!IMPORTANT]
> Interview cards test *understanding*, not recitation.

**Card 1 — "Where is session data stored, and how does the server know whose it is?"**
A: Two parts. The data lives server-side (default: the `django_session` table via
`SESSION_ENGINE=…db`) as a signed JSON payload keyed by a random 32-character `session_key`; the
browser holds only a `sessionid` cookie whose value is that key (`HttpOnly`, `SameSite=Lax`,
14-day default). On each request `SessionMiddleware` reads the cookie, loads the matching row, and
attaches it as `request.session`.

**Card 2 — "Is session data encrypted?"**
A: No — **signed**. The payload is `urlsafe_base64(JSON):timestamp:HMAC-SHA256`, and segment 1
decodes to plaintext JSON without the secret key (verified here). The signature makes it
*tamper-evident*: change a byte and `signing.loads` raises `BadSignature`; Django's `decode()`
swallows that, logs `SuspiciousSession`, and returns `{}` — the visitor silently becomes
anonymous. Never treat session contents as secret from anyone with server/DB access.

**Card 3 — "When exactly is the session created and saved?"**
A: Lazily. `request.session` is an empty `SessionStore` with `session_key=None`; a read-only view
(`.get`) marks it `accessed` but not `modified`, so **no cookie and no row** (verified). Writes
mark it `modified`; `SessionMiddleware.process_response` then calls `save()`, which mints the key
(`_get_new_session_key`, 32 chars from `VALID_KEY_CHARS`) and writes the row — and sets the
cookie. The view never touches cookies or rows.

**Card 4 — "What's the difference between `del`, `clear()`, and `flush()`?"**
A: `del session[k]` removes one key (and a missing key raises `KeyError`); `clear()` removes all
keys but keeps the `session_key`, so the row survives as an empty session (`is_empty()` stays
`False` — verified); `flush()` clears the data *and* abandons the key — the row is deleted and the
response deletes the cookie (`Max-Age=0`, `expires=1970`). Logout must be `flush()` (plus
`logout(request)`), or a stolen empty-but-valid ticket survives.

**Card 5 — "How would you prevent session fixation?"**
A: Rotate the key at privilege change — `session.cycle_key()` (measured: new key, data preserved).
Django's `login()` does exactly that. The attack: an attacker plants a `sessionid` on a victim,
the victim then *logs in*, and if the key never changes, the attacker's known key now points at an
authenticated session. `cycle_key()`/`flush()` invalidates every pre-login ticket.

**Card 6 — "Session vs cookie — when would you use which?"**
A: Sessions when the data should be server-side, larger than ~4 KB, or unknown to the client
(flash data, carts, login state); raw cookies when the data is trivial, non-sensitive, and the
client should own it (preferences, A045's topic). The tiebreaker is *trust*: anything the client
carries, the client can read and (unsigned) forge — so sessions keep the truth server-side and
send only a key. Note Django's own `signed_cookies` engine blurs the line by shipping the payload
in a signed cookie — readable by the visitor, zero server storage.

## 🔁 Active Recall

Answer from memory first, then expand each `<details>`.

1. A fresh visitor requests `GET /get-session/` — no cookie at all. What does the response contain,
   what does the browser receive, and what lands in `django_session`?

<details><summary>Answer</summary>

Body: `200 "Welcome: Guest, You are enrolled in: Not Enrolled"` — the `.get(key, default)`
fallbacks. The browser receives **no `sessionid` cookie at all** (the session was only *accessed*,
not *modified*, so `SessionMiddleware` neither saves a row nor sets a cookie) and `django_session`
gains **no row** (verified). Sessions are created lazily, by writes only — `accessed=True,
modified=False` is the request-level proof.
</details>

2. What exactly is in the `session_data` column, and what does the signature protect — and *not*
   protect?

<details><summary>Answer</summary>

One string of three segments: `urlsafe_base64(JSON) : base62 timestamp : HMAC-SHA256 signature`
(verbatim: `eyJ1c2Vy…:1x8YuT:G1Wsox4L…`). Segment 1 decodes to the session dict in **plaintext**
without the secret key — signed, not encrypted. The signature protects *integrity*: any change to
segment 1 makes `signing.loads` raise `BadSignature`. It does not hide contents, and the browser
never even sees this string in the DB engine (the cookie is only the key).
</details>

3. Someone tampers with a stored `session_data`. What exactly does the visitor see, and what does
   the ops dashboard see?

<details><summary>Answer</summary>

The visitor sees an **empty session** — `SessionStore.decode` catches `BadSignature`, logs
`django.security.SuspiciousSession` (WARNING, "Session data corrupted") and returns `{}`, so
`get_session` renders `Welcome: Guest, You are enrolled in: Not Enrolled` (verified end-to-end).
The dashboard sees the `SuspiciousSession` warning. The attacker gets nothing: the forged values
never appear.
</details>

4. `set_session` assigns two keys but never calls `save()`. Who mints the `session_key` and writes
   the row — and when?

<details><summary>Answer</summary>

`SessionMiddleware.process_response`: when `request.session.modified` is `True` (or
`SESSION_SAVE_EVERY_REQUEST`), it calls `request.session.save()`, which mints the key via
`_get_new_session_key()` — 32 chars from `VALID_KEY_CHARS`, retried until unused — inserts the
`django_session` row, and sets the `sessionid` cookie. Verified at request level: the key is
`None` straight after the assignments (lazy) and materialises only on save.
</details>

5. `del session['username']`, `clear()`, `flush()` — what does each leave behind, and which is the
   logout verb?

<details><summary>Answer</summary>

`del session[k]` removes one key (missing key → `KeyError`), key and row survive. `clear()`
removes all keys but keeps the key — verified: `is_empty()` stays `False`, the row survives as an
empty session. `flush()` clears the data, sets `session_key=None`, deletes the row, and the
response sends a cookie deletion (`expires=Thu, 01 Jan 1970`, `Max-Age=0`). Logout = `flush()`
(Django's `logout()` calls it too), because `clear()` leaves a valid ticket to an empty locker.
</details>

6. Why is `Vary: Cookie` on the response, and why does it matter even though "we don't cache"?

<details><summary>Answer</summary>

`SessionMiddleware` patches `Vary: Cookie` whenever the session was *accessed* (even read-only —
verified on `get_session`). It tells shared caches that this page depends on the requester's
cookie, so John Doe's personalised page must never be served to a stranger. Today the site is
uncached, but the header is the contract A039's cache and any CDN will honour later.
</details>

7. What changes if you switch `SESSION_ENGINE` to `signed_cookies` — and what must you never put
   in the session then?

<details><summary>Answer</summary>

The data moves **into the cookie**: `sessionid` carries the whole signed payload
(`base64(JSON):timestamp:signature` — verified: 0 DB rows, round trip intact, segment 0 decodes to
plaintext JSON). Consequences: no server storage (and `flush()` merely voids the cookie), a ~4 KB
practical ceiling, and — because it is signed, not encrypted — **the visitor can read every key**.
Never store secrets there; the DB engine keeps data server-side and ships only the opaque key.
</details>

## 📝 Quick Revision

- **Two halves:** cookie `sessionid` = the key (opaque, 32 chars, `HttpOnly`); data = server-side
  (`django_session` via `SESSION_ENGINE=…db`), signed JSON payload.
- **Payload format:** `urlsafe_b64(JSON) : timestamp : HMAC` — *signed, not encrypted*; tampering →
  `BadSignature` → `SuspiciousSession` warning → session becomes `{}`.
- **Set:** `session['k'] = v` → `modified=True`; key + row minted at save (middleware saves when
  modified); response carries `Set-Cookie` (`HttpOnly`, `SameSite=Lax`, `Max-Age=1209600`) +
  `Vary: Cookie`.
- **Get:** `.get(k, default)` (never raises) vs `[k]` (`KeyError`); read-only access → `accessed`
  only → no cookie, no row (laziness).
- **Delete:** `del` = one key; `clear()` = all data, key kept (row survives); `flush()` = data +
  key gone, row deleted, cookie deleted (the logout verb).
- **Expiry:** two clocks — cookie `Max-Age` and `expire_date`; default 14 days; `set_expiry(0)` =
  browser close; `manage.py clearsessions` for expired rows.
- **Fixation:** `cycle_key()` = new key, data kept — what `login()` does at privilege change.
- **Artifact:** `myProject28/` — `set_session` (2 keys), `get_session` (2 `.get` + defaults),
  `delete_session` (`flush()`; commented-out `del`-based partial delete); stock 6.1.1 settings,
  `django_session` table present, 0 rows.

## ❓ FAQ

**Q1. Do I need `django.contrib.sessions` in `INSTALLED_APPS` for `request.session` to work?**
A: Only for the DB (and `cached_db`) engines — the `django_session` table comes from that app's
migrations (the artifact's 11 tables include it). `SessionMiddleware` in `MIDDLEWARE` is what
attaches `request.session` in every case. Remove either and `request.session` breaks (middleware:
`AttributeError`; DB engine without the table: `no such table: django_session`).

**Q2. The cookie is named `sessionid` — can I rename it or make it secure?**
A: Yes — `SESSION_COOKIE_NAME` (e.g. `__Host-myapp_session`), `SESSION_COOKIE_SECURE=True` in
production, `SESSION_COOKIE_HTTPONLY` (keep `True`), `SESSION_COOKIE_SAMESITE` (`'Strict'` if you
don't need cross-site logins), `SESSION_COOKIE_DOMAIN`, `SESSION_COOKIE_AGE`. All were stock
defaults here (`sessionid`, `HttpOnly=True`, `Lax`, 14 days) and all verified in the probe.

**Q3. Is `request.session['k'] = v` the same as `setdefault('k', v)`?**
A: No — assignment overwrites; `setdefault` only fills a gap (verified:
`setdefault('course', 'X')` returned the existing `'Django'`). Both mark the session `modified`.
Pick by intent; prefer `.get()` + `setdefault` when absence is normal.

**Q4. Can I store objects (a QuerySet, a model instance) in the session?**
A: Store *data*, not live objects. The payload is JSON, so only JSON-serialisable values survive
(strings, numbers, lists, dicts); a model instance must be saved as its `pk` and re-fetched on the
next request. 📌 Pickle-based engines are an RCE vector if `SECRET_KEY` leaks — JSON is the
default `SESSION_SERIALIZER` for good reason.

**Q5. My session disappears between requests. What do I check first?**
A: In order: is `SessionMiddleware` in `MIDDLEWARE`? Did anything actually *write*
(`modified=True`)? Is `SESSION_COOKIE_SECURE=True` while testing over http? Is the browser sending
the cookie (`SameSite`/domain mismatch)? Is the `django_session` row's `expire_date` in the past?
Each failure mode produces "fresh every request" — and each is one setting away.

**Q6. How big can a session be?**
A: No hard server-side limit (it is a DB row), but the *cookie* is capped by browsers (~4 KB) —
and in the DB engine the cookie only carries the 32-char key, so the data can grow freely. That
asymmetry is a reason the DB engine is the default; `signed_cookies` inherits the 4 KB ceiling
because the data *is* the cookie.

## 🏁 Learning Checkpoints

- [ ] **Checkpoint 1 — The two halves:** I can draw the browser/server split (cookie = key,
      `django_session` = data) and say what each side holds — *§What Is the Session?*
- [ ] **Checkpoint 2 — The laziness proof:** I can predict cookie/row behaviour for read-only vs
      write requests from `accessed`/`modified` alone — *§Get + Live Verification*.
- [ ] **Checkpoint 3 — The payload:** I can name the three segments of `session_data`, decode
      segment 1 by hand, and explain the `BadSignature` → `{}` + `SuspiciousSession` path — *§The
      Payload*.
- [ ] **Checkpoint 4 — The delete matrix:** I can state what `del`/`clear()`/`flush()` each leave
      behind (key, row, cookie) and justify `flush()` for logout — *§Delete*.
- [ ] **Checkpoint 5 — The two clocks:** I can explain cookie `Max-Age` vs `expire_date`, the
      14-day default, and `set_expiry(0)`'s browser-close behaviour — *§Expiry*.

## 🏋️ Exercises

- **Level 1 — Recall:** Write the three views from memory; recite the six session settings and
  values; name the three segments of `session_data`.
- **Level 2 — Understanding:** Predict, then verify: after `set-session` in client A, what does a
  *fresh* client B see at `get-session/`, does B receive a cookie, and does the row count change?
  Explain via `accessed`/`modified`.
- **Level 3 — Application:** Convert the artifact to a tiny login shape (`cycle_key()` +
  `_auth_user_id`-style key on set, `flush()` on delete); prove with the test client that (a) the
  key changes between pre-login and post-login requests, (b) `get_session` reads the stored user,
  and (c) a forged `sessionid` cookie yields the Guest defaults.
- **Level 4 — Interview reasoning:** A teammate proposes storing the user's auth token in the
  session to "keep it handy", and separately proposes `signed_cookies` to skip the DB. Compose the
  security review: what the signature does and does not protect, who can read session contents in
  each engine, what `SECRET_KEY` loss means for both, and where each proposal's data should live
  instead.

## 🏁 Final Takeaways

1. A session is a **two-part design**: an opaque `sessionid` cookie (the ticket) plus server-side
   data in `django_session` (the locker) — the ticket identifies, the database stores.
2. **The payload is signed, not encrypted**: `base64(JSON):timestamp:HMAC` — tamper-evident,
   plaintext-readable, and a `BadSignature` degrades the session to `{}` with a
   `SuspiciousSession` warning.
3. **Laziness is the rule**: read-only requests set no cookie and create no row (`accessed` only);
   writes mint key, row, and cookie at save time — by the middleware, not the view.
4. **Delete has three meanings**: `del` (one key), `clear()` (all data, key kept), `flush()` (data
   + key gone, row deleted, cookie deleted) — and logout means `flush()`.
5. **Expiry runs on two clocks** (cookie `Max-Age`, row `expire_date`), 14 days by default, with
   per-session overrides via `set_expiry(…)` — including `0` = at browser close.
6. **`cycle_key()` is the fixation defence**: new key, data preserved — the same move `login()`
   performs at privilege change.
7. **The artifact is the login/logout skeleton in disguise**: `set_session` is the session-write
   half of `login()`, `delete_session` is `flush()` = the core of `logout()` — with the commented-
   out `del` block documenting the "partial delete" alternative and why it loses.

## 🔄 Next Lecture Connection

This chapter's session is a **server-side** memory: the visitor carries a key, the truth hangs in
`django_session`, and the visitor never reads the data. But three things in that cookie were
deliberately *not* sessions:

- the **cookie flags** themselves (`HttpOnly`, `SameSite=Lax`, `Max-Age`, `Path`) — set by
  `SessionMiddleware`, never by the views;
- the fact that the visitor *carries* something at all — the mechanism, not the data;
- and every "remember me for 30 days", "keep this preference", or "did you close this banner"
  case where the data *should* live on the client.

That is the next lecture's territory — now written (📌):
[A045 — Set & Read Cookies in Django](../A045_Set_&_Read_Cookies_in_Django/README.md) takes the
ticket away from the cloakroom and hands the visitor the contents themselves —
`response.set_cookie(...)` and `request.COOKIES.get(...)` — with the flags, the signing option
(`set_signed_cookie`), and the trust boundary that decides which of the two homes a given fact
belongs in. Its one genuine bug — a guard that reads as "were cookies sent?" and behaves as "are
the cookie *values* non-empty?" — is the quiet twin of A043's loud `NameError`: no crash, just the
wrong name on the branch.

---

<div class="doc-footer">

**Sources used:** `myProject28/` artifact (Django 6.1.1 scaffold): `blog/views.py` — `set_session`
(two `request.session[...] =` assignments), `get_session` (two `.get(key, default)` calls with
`'Guest'`/`'Not Enrolled'` fallbacks), `delete_session` (the commented-out `del`-both-keys +
`try/except KeyError` block, then the active `request.session.flush()`), all comments quoted
verbatim; `blog/urls.py` (`set-session/`, `get-session/`, `delete-session/` on root-mount);
`myProject28/urls.py` (`include('blog.urls')` at `''`); `myProject28/settings.py` (the stock 6.1.1
scaffold with `'blog'` added; `django.contrib.sessions` + `SessionMiddleware` present; every
`SESSION_*` value left at its default — `ENGINE=db`, `COOKIE_NAME=sessionid`, `AGE=1209600`,
`HTTPONLY=True`, `SAMESITE=Lax`, `SAVE_EVERY_REQUEST=False`; the `STATICFILES_DIRS` ghost →
`staticfiles.W004`; the inert `MAILERS` block); stub `models.py`/`admin.py`/`apps.py`/`tests.py`;
`blog/migrations/` holding only `__init__.py`; and `db.sqlite3` (11 tables including
`django_session`, **0 rows** — read directly, never written). Installed-Django source read and
quoted: `SessionBase.encode` / `SessionBase.decode` (with its `django.security.SuspiciousSession`
warning and `{}` return), `_get_new_session_key`, `VALID_KEY_CHARS`
(`django/contrib/sessions/backends/base.py`), the DB store's save/load
(`backends/db.py`), and `SessionMiddleware.process_request` / `process_response`
(`django/contrib/sessions/middleware.py`); `django/core/signing.py` for `dumps`/`loads`/
`BadSignature`/`SignatureExpired`. Verified runtime: Django 6.1.1 / Python 3.14.6. No transcript
or `_source/` material exists; the owner's command journal `commands.txt` (54 lines, ending at
`pip install Pillow`) adds no new lines for this lecture.

**Live verification:** every behaviour was exercised via the Django test client on an **in-memory
test database** — the artifact's own `db.sqlite3` was opened read-only (11 tables, 0
`django_session` rows) and never written. Clean cycle: 0 rows → `GET /set-session/` → 1 →
`GET /get-session/` (same client) → 1 → `GET /delete-session/` → 0 → a further read-only GET → 0.
Captured per request: bodies (`Session data Saved Successfully.` / `Welcome: John Doe, You are
enrolled in: Django` / `Welcome: Guest, You are enrolled in: Not Enrolled` / `All session data
deleted.` / `Welcome: Guest …` after delete); the `Set-Cookie` on set (`sessionid=
til4lshjs4kdnmjtypezd85ug12jb4w6`, 32 chars, `Path=/`, `HttpOnly`, `SameSite=Lax`,
`Max-Age=1209600`) and its absence on read-only access; the `Vary: Cookie` header; the delete
response's cookie deletion (`sessionid=""`, `expires=Thu, 01 Jan 1970 00:00:00 GMT`, `Max-Age=0`).
Request-level states: `session_key` `None` → still `None` after both assignments (lazy) →
`hd01lyljdhsh64t2odbyg3a35beoo6br` after `save()`; `accessed/modified` = `False/False` → `True/
False` (read-only) → `True/True` (after set); `flush()` → key `None`, row deleted; `del` one key →
`{'course': 'Django'}` remains. Storage format: `session_data` verbatim
(`eyJ1c2Vy…:1x8YuT:G1Wsox4L329RsdHBy5DwVF5LVzxSSzoDgP7UrasgZTE`), 3 segments, segment 1 decodes
(plaintext) to `{"username":"John Doe","course":"Django"}`; `expire_date` = creation + `1209599`s.
Security: `key_salt` = `django.contrib.sessions.SessionStore`, serializer =
`django.core.signing.JSONSerializer`, `VALID_KEY_CHARS` =
`abcdefghijklmnopqrstuvwxyz0123456789`; `signing.loads(good, salt=key_salt)` → the dict;
`signing.loads(tampered, …)` → `BadSignature: Signature "…" does not match`;
`signing.loads(good, max_age=0)` → `SignatureExpired: Signature age 0.12s > 0`;
`st.decode(tampered)` → `{}` with `django.security.SuspiciousSession | WARNING | Session data
corrupted` captured; a forged-cookie request → the Guest defaults. API surface:
`exists()`, `is_empty()`, `keys()`, `items()`, `.get(missing, 'fallback')`,
`st['missing']` → `KeyError: 'missing'`, `setdefault`, `pop`, `set_expiry(60)` → age 60,
`set_expiry(None)` → 1209600, `set_expiry(0)` → `get_expire_at_browser_close() == True`,
`cycle_key()` → new key with data preserved. Cookie engine:
`override_settings(SESSION_ENGINE=…signed_cookies)` → the `sessionid` cookie carrying the whole
106-char signed payload, segment 0 decoding to plaintext JSON, round trip `Welcome: John Doe…`,
**0** DB rows. `manage.py check` → only `staticfiles.W004`.

**Beyond the artifact (📌):** the cookie-only `signed_cookies` engine and its
readability/4 KB trade, the `cached_db`/`cache`/`file` engines, `SESSION_SERIALIZER` (JSON as the
RCE-safe default), `SECRET_KEY_FALLBACKS` rotation and the "lose the key, lose every session"
effect, `manage.py clearsessions` housekeeping, `SESSION_SAVE_EVERY_REQUEST`, the
`set_expiry(0)`/browser-close checkbox pattern, `login()`'s `SESSION_KEY`/`cycle_key()` internals
and `logout()`'s `flush()`, the `__Host-` cookie-prefix convention, and the sessions-vs-cookies
trust boundary that hands A045 its topic. General session mechanics cross-checked against
Django's source and documentation (sessions topic guide, `SESSION_*` settings reference,
`django.contrib.sessions` models/API).

**Navigation:** ← [A043 — Pre-Save & Post-Save Signals](../A043_Pre_Save_&_Post_Save_Signals/README.md) · [Series hub](../README.md) · [A045 — Set & Read Cookies in Django](../A045_Set_&_Read_Cookies_in_Django/README.md) →

</div>
