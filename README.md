# Chai aur Django

A Django web project built while learning Django with the "Chai aur Django" tutorial series. It demonstrates a complete project setup from virtual environment creation to a multi-page Django application with static files and templates.

Django version: 6.1.1

## Project Structure

```
.
├── .gitignore                  # Files/folders ignored by Git
├── commands.txt                # Setup and run commands reference
├── README.md                   # This file
├── chaiaurDjango/              # Project root (created by `startproject`)
│   ├── manage.py               # Django CLI entry point
│   ├── db.sqlite3              # SQLite database (gitignored)
│   ├── chaiaurDjango/          # Project configuration package
│   │   ├── __init__.py         # Package marker
│   │   ├── asgi.py             # ASGI application entry point
│   │   ├── settings.py         # Project settings (apps, DB, static, etc.)
│   │   ├── urls.py             # Root URL configuration
│   │   ├── views.py            # Root-level view functions (home, about, contact)
│   │   └── wsgi.py             # WSGI application entry point
│   ├── chai/                   # `chai` Django app
│   │   ├── __init__.py         # Package marker
│   │   ├── admin.py            # Admin site registration
│   │   ├── apps.py             # App configuration (ChaiConfig)
│   │   ├── migrations/
│   │   │   └── __init__.py     # Migrations package marker
│   │   ├── models.py           # Data models (currently empty)
│   │   ├── templates/chai/
│   │   │   └── all_chai.html   # Template rendered by the chai app
│   │   ├── tests.py            # App tests
│   │   ├── urls.py             # App URL configuration
│   │   └── views.py            # App view functions (all_chai)
│   ├── static/
│   │   └── style.css           # Global stylesheet
│   └── templates/
│       ├── layout.html         # Base template (extends for pages)
│       └── website/
│           └── index1.html     # Home page template
├── .venv/                      # Python virtual environment (gitignored)
└── __pycache__/                # Python bytecode cache (gitignored)
```

## Setup

These commands set up the development environment (see `commands.txt` for the full reference):

```bash
# 1. Install the uv package manager
pip install uv

# 2. Create a virtual environment
uv venv

# 3. Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 4. Install Django
uv pip install Django

# 5. Create the Django project (already done in this repo)
django-admin startproject chaiaurDjango

# 6. Create the chai app (already done in this repo)
py manage.py startapp chai
```

## Running the Development Server

```bash
py manage.py runserver
```

The app is served by default on `http://127.0.0.1:8000/`. To run on a different port:

```bash
py manage.py runserver 8001
```

## Application Overview

### chai app

The `chai` app is registered in `INSTALLED_APPS` (`chaiaurDjango/chai/apps.py`) and provides a single page at the route `chai/` that renders the `all_chai.html` template.

### URL Routes

Defined in `chaiaurDjango/chaiaurDjango/urls.py`:

| Route      | View       | Template                       |
|------------|------------|--------------------------------|
| `/`        | `views.home`     | `website/index1.html`        |
| `/about/`  | `views.about`    | HttpResponse (text)         |
| `/contact/`| `views.contact`  | HttpResponse (text)         |
| `/chai/`   | `chai.views.all_chai` | `chai/all_chai.html`    |
| `/admin/`  | Django admin     | Admin interface            |

### Settings (`chaiaurDjango/chaiaurDjango/settings.py`)

- **Database:** SQLite (`db.sqlite3`)
- **Allowed hosts:** `[]` (localhost only in development)
- **Static files:** Served from `STATIC_URL = 'static/'` with templates looking up `layout.html` via the `APP_DIRS` and `DIRS` settings
- **Templates:** Configured to load from a top-level `templates/` directory
- **Email backend:** Console (for development)
- **Password validators:** Default Django set enabled

### Templates

- `layout.html` — Base template with a navigation bar, title block, and content block. Loads `static/style.css` globally.
- `website/index1.html` — Home page extending `layout.html`, displaying a heading.
- `chai/all_chai.html` — Chai page extending `layout.html`, displaying an "All Chai" heading.

### Static Files

- `static/style.css` — A dark-themed stylesheet applied to all pages via the base layout.

## Notes

- The project uses `uv` as the package manager for fast installation and virtual environment management.
- The virtual environment (`.venv`) is created at the project root.
- `db.sqlite3` and `__pycache__` directories are excluded from version control via `.gitignore`.
