# A037 - Django Authentication: User Signup, Login & Restrict Pages

## What You Will Learn

- ✅ Build a **User Registration System** with custom form validation
- ✅ Implement **Login & Logout** functionality
- ✅ Restrict access to pages using the **@login_required** decorator
- ✅ Use Django's built-in **User model** and **authentication backend**
- ✅ Create a **Protected Dashboard** accessible only to authenticated users
- ✅ Implement **user feedback** using Django Messages Framework
- ✅ Build a **responsive navbar** with conditional authentication UI
- ✅ Validate **unique email addresses** during registration
- ✅ Extend Django's **UserCreationForm** with custom fields

---

## Why This Lecture Matters

**A036** showed you how to manage users through Django admin. **A037** teaches you how to create **public-facing authentication** — the way users sign up on real websites.

### The Core Differences:
| Aspect | Admin (A036) | Public Auth (A037) |
|--------|-------------|-------------------|
| **Where users register** | Admin panel (`/admin/`) | Custom webpage (`/register/`) |
| **Who creates users** | Superuser/staff only | Users self-register |
| **Form type** | AdminChangeForm | UserCreationForm (custom) |
| **User experience** | Backend admin interface | Modern web UI |
| **Security** | Admin credentials required | Public signup with validation |

This lecture bridges the gap from **admin-only user management** to **user-facing authentication** — essential for any real web application.

---

## Prerequisites

Before starting this lecture, ensure you:
- ✅ Completed **A031** (Update operations in ModelForms)
- ✅ Completed **A032** (Create operations in ModelForms)
- ✅ Completed **A033** (Read operations in ModelForms)
- ✅ Completed **A034** (Delete operations in ModelForms)
- ✅ Completed **A035** (Django Messages Framework)
- ✅ Completed **A036** (User Management via Admin)
- ✅ Understand Django **User model** from `django.contrib.auth`
- ✅ Familiar with **form validation** and **custom forms**
- ✅ Know how to create **function-based views**

---

## Architecture Overview

```
myProject21/
├── myProject21/
│   ├── settings.py              # Auth middleware & User app config
│   ├── urls.py                  # Include accounts.urls
│   └── wsgi.py
├── accounts/
│   ├── migrations/
│   ├── views.py                 # register_view, login_view, logout_view, dashboard_view
│   ├── forms.py                 # RegistrationForm (extends UserCreationForm)
│   ├── urls.py                  # URL routes for auth endpoints
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                # No custom model - uses django.contrib.auth.User
│   ├── tests.py
│   └── templates/accounts/
│       ├── base.html            # Base template with conditional auth navbar
│       ├── register.html        # Signup form
│       ├── login.html           # Login form
│       └── dashboard.html       # Protected user dashboard
└── manage.py
```

### Key Components:

**1. RegistrationForm** — Extends UserCreationForm
- Adds email field (required)
- Validates email uniqueness
- Inherits password strength checks from UserCreationForm

**2. Authentication Views** — Handle user registration/login/logout
- `register_view`: Process form, create User, auto-login
- `login_view`: Authenticate with username/password, set session
- `logout_view`: Clear session, clear messages
- `dashboard_view`: Display user profile (protected with @login_required)

**3. URL Routing** — Public endpoints
- `/register/` → signup page
- `/login/` → login page
- `/logout/` → logout endpoint
- `/dashboard/` → protected user profile

**4. Authentication Middleware** — Already configured in settings.py
- Attaches `request.user` object to every request
- Maintains session for logged-in users
- Available in all views and templates

---

## Registration Form

### The RegistrationForm Class

```python
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput()
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        """
        Custom validator: Check if email already exists
        Raises ValidationError if user with this email already exists
        """
        email = self.cleaned_data.get('email')
        
        # Query User table for matching email
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        
        return email
    
    def clean_password2(self):
        """
        Inherited from UserCreationForm
        Validates that password1 and password2 match
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        
        return password2
    
    def save(self, commit=True):
        """
        Save new User with hashed password
        commit=True: Save to database immediately
        commit=False: Return unsaved User instance for additional processing
        """
        user = super().save(commit=False)
        
        # Use set_password() to hash the password
        # Never store plain passwords in database!
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user
```

### Why This Approach?

| Feature | Explanation |
|---------|------------|
| **Extend UserCreationForm** | Inherits password validation from Django, not reinventing wheel |
| **Add email field** | UserCreationForm doesn't include email, so we add it |
| **clean_email()** | Custom validation to ensure email uniqueness before saving |
| **set_password()** | Hashes password using Django's default PBKDF2 algorithm |
| **commit parameter** | Allows view to perform additional setup before saving to database |

---

## The Four Authentication Views

### 1. Registration View (Create New User)

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistrationForm

def register_view(request):
    """
    Handle user registration
    GET: Display empty registration form
    POST: Validate form, create user, auto-login, redirect to dashboard
    """
    if request.method == 'POST':
        # Form submitted: process registration
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            # Form passed all validation (email unique, passwords match, etc.)
            # save() returns the new User instance
            user = form.save()
            
            # Auto-login the user (set session cookie)
            # Equivalent to user manually logging in
            login(request, user)
            
            # Add success message to be displayed on dashboard
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            
            # Redirect to dashboard (successful registration flow)
            return redirect('dashboard')
        
        # Form validation failed: re-render form with error messages
        # Form object contains error_messages for display in template
    else:
        # Initial page load: display empty form
        form = RegistrationForm()
    
    # Render template with form (empty on GET, with errors on failed POST)
    return render(request, 'accounts/register.html', {'form': form})
```

### 2. Login View (Authenticate Existing User)

```python
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    """
    Handle user login
    GET: Display login form (username + password)
    POST: Authenticate user, create session, redirect to dashboard
    """
    if request.method == 'POST':
        # Form submitted: authenticate user
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Verify username and password against User database
        # Returns User object if credentials valid, None otherwise
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Credentials are correct
            # Create session cookie in browser
            login(request, user)
            
            messages.success(request, f"Welcome back, {username}!")
            return redirect('dashboard')
        else:
            # Credentials invalid: re-render form with error
            messages.error(request, "Invalid username or password.")
    
    # GET request or authentication failed: render login form
    return render(request, 'accounts/login.html')
```

### 3. Logout View (Destroy Session)

```python
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """
    Handle user logout
    Clears session cookie, user is logged out
    """
    # Clear session from server and browser
    logout(request)
    
    messages.info(request, "You have been logged out.")
    
    # Redirect to login page
    return redirect('login')
```

### 4. Dashboard View (Protected Page)

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='login')
def dashboard_view(request):
    """
    Display user profile (protected - requires login)
    
    Decorator behavior:
    - If user is authenticated: render dashboard
    - If user is NOT authenticated: redirect to login page with ?next=/dashboard/
    """
    return render(request, 'accounts/dashboard.html')
```

### Understanding @login_required Decorator

```python
# Without decorator: anyone can access dashboard
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

# With decorator: only logged-in users can access
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')
```

**How @login_required works:**

1. User visits `/dashboard/`
2. Django checks: Is `request.user.is_authenticated` True?
   - **YES** → Render dashboard template
   - **NO** → Redirect to `/login/?next=/dashboard/`
3. After login, redirect back to `/dashboard/` automatically (using `next` parameter)

This ensures only logged-in users see protected pages.

---

## URL Configuration

### accounts/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
```

### myProject21/urls.py (Main Project)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Include accounts URLs at root
]
```

**Result:**
- `/register/` → register_view
- `/login/` → login_view
- `/logout/` → logout_view
- `/dashboard/` → dashboard_view (protected)

---

## Templates

### accounts/templates/accounts/base.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Authentication Demo{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; }
        nav { background-color: #333; color: white; padding: 10px; }
        nav a { color: white; margin-right: 15px; text-decoration: none; }
        nav a:hover { text-decoration: underline; }
        .container { max-width: 800px; margin: 50px auto; }
        .messages { list-style: none; padding: 0; }
        .messages li { padding: 10px; margin-bottom: 10px; background-color: #f0f0f0; border-left: 4px solid #007bff; }
    </style>
</head>
<body>
    <nav>
        {% if user.is_authenticated %}
            <!-- User is logged in: show logout and dashboard links -->
            <span>Hello, {{ user.username }}!</span>
            <a href="{% url 'dashboard' %}">Dashboard</a>
            <a href="{% url 'logout' %}">Logout</a>
        {% else %}
            <!-- User is NOT logged in: show login and register links -->
            <a href="{% url 'login' %}">Login</a>
            <a href="{% url 'register' %}">Register</a>
        {% endif %}
    </nav>

    <div class="container">
        <!-- Display all messages (success, error, info) -->
        {% if messages %}
            <ul class="messages">
                {% for message in messages %}
                    <li class="{% if message.tags %}{{ message.tags }}{% endif %}">
                        {{ message }}
                    </li>
                {% endfor %}
            </ul>
        {% endif %}

        <!-- Page content block -->
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### accounts/templates/accounts/register.html

```html
{% extends 'accounts/base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
<h1>Create an Account</h1>

<form method="POST">
    {% csrf_token %}
    
    {{ form.as_p }}
    
    <button type="submit">Register</button>
</form>

<p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
{% endblock %}
```

### accounts/templates/accounts/login.html

```html
{% extends 'accounts/base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<h1>Login to Your Account</h1>

<form method="POST">
    {% csrf_token %}
    
    <label for="username">Username:</label>
    <input type="text" name="username" id="username" required>
    
    <label for="password">Password:</label>
    <input type="password" name="password" id="password" required>
    
    <button type="submit">Login</button>
</form>

<p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
{% endblock %}
```

### accounts/templates/accounts/dashboard.html

```html
{% extends 'accounts/base.html' %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<h1>Welcome, {{ user.username }}!</h1>

<div class="profile-info">
    <p><strong>Username:</strong> {{ user.username }}</p>
    <p><strong>Email:</strong> {{ user.email }}</p>
    <p><strong>Member Since:</strong> {{ user.date_joined|date:"F d, Y" }}</p>
</div>

<a href="{% url 'logout' %}">Logout</a>
{% endblock %}
```

---

## Key Concepts & Vocabulary

| Term | Definition | Example |
|------|-----------|---------|
| **Authentication** | Process of verifying user identity (who you are) | Login with username/password |
| **Authorization** | Determining what authenticated user can access | @login_required restricts dashboard |
| **Session** | Server-side storage of logged-in user data | Browser cookie containing session ID |
| **Middleware** | Component that processes every request/response | AuthenticationMiddleware sets request.user |
| **Hash Function** | One-way algorithm to encrypt passwords securely | PBKDF2 (Django default) |
| **Decorator** | Function wrapper that modifies behavior | @login_required checks authentication first |
| **CSRF Token** | Security token to prevent cross-site form attacks | {% csrf_token %} in forms |
| **UserCreationForm** | Django form for creating users with password validation | Handles password matching/strength |
| **is_authenticated** | Property that returns True if user logged in | {% if user.is_authenticated %} |
| **request.user** | Current authenticated user object (or AnonymousUser) | {{ user.username }} in template |

---

## Common Mistakes

### ❌ Mistake #1: Storing Plain Passwords

```python
# WRONG - Never do this!
user.password = "plaintext123"
user.save()

# CORRECT - Always use set_password()
user.set_password("plaintext123")
user.save()
```

**Why:** Django hashes passwords. Storing plain text makes them vulnerable to breaches.

---

### ❌ Mistake #2: Forgetting CSRF Token in Forms

```html
<!-- WRONG - Django will reject this form with 403 Forbidden -->
<form method="POST">
    <input type="text" name="username">
    <input type="password" name="password">
    <button type="submit">Login</button>
</form>

<!-- CORRECT - Always include CSRF token -->
<form method="POST">
    {% csrf_token %}
    <input type="text" name="username">
    <input type="password" name="password">
    <button type="submit">Login</button>
</form>
```

**Why:** CSRF protection prevents unauthorized form submissions from third-party sites.

---

### ❌ Mistake #3: Not Using @login_required

```python
# WRONG - Anyone can access this view
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

# CORRECT - Protect sensitive pages
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')
```

**Why:** Without protection, anonymous users can access private data.

---

### ❌ Mistake #4: Not Setting up Messages Middleware

```python
# settings.py - WRONG (incomplete MIDDLEWARE)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Missing: MessageMiddleware
]

# CORRECT - Include all auth-related middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Sets request.user
    'django.contrib.messages.middleware.MessageMiddleware',      # Enables messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Why:** Messages won't display if middleware isn't configured.

---

### ❌ Mistake #5: Checking Authentication in Template Instead of View

```python
# WRONG - Relies on template check (frontend security)
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

# CORRECT - Enforce at view level (server-side security)
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')
```

**Template check alone is not secure** — frontend checks can be bypassed.

---

### ❌ Mistake #6: Using authenticate() Without Checking is_active

```python
# WRONG - Logs in inactive users
user = authenticate(request, username=username, password=password)
if user:
    login(request, user)

# CORRECT - Verify user is active
user = authenticate(request, username=username, password=password)
if user is not None and user.is_active:
    login(request, user)
```

**Why:** Superuser can deactivate accounts; don't login disabled users.

---

## Interview Perspective

### Q1: What's the difference between authentication and authorization?

**Answer:**
- **Authentication** = Proving identity ("Are you really John?")
  - Example: Login with username/password
  
- **Authorization** = Granting access based on identity ("What can John access?")
  - Example: @login_required allows only authenticated users
  - Example: Admin-only pages, role-based access

In A037:
- `authenticate()` and `login()` handle authentication
- `@login_required` decorator handles authorization

---

### Q2: Why should you extend UserCreationForm instead of ModelForm?

**Answer:**
UserCreationForm provides:
- ✅ Password strength validation (no "password123")
- ✅ Password matching verification
- ✅ Proper password hashing with set_password()

If you used plain ModelForm:
- ❌ Would have to write your own password validation
- ❌ Would have to remember to use set_password()
- ❌ Would reinvent Django's existing password strength checks

**DRY Principle:** Don't reinvent; extend what Django provides.

---

### Q3: How does @login_required work with the 'next' parameter?

**Answer:**
```
1. User visits /dashboard/ but not logged in
2. @login_required redirects to /login/?next=/dashboard/
3. After successful login:
   - Django reads 'next' from query parameters
   - Redirects user back to /dashboard/
```

This creates seamless post-login redirect without hardcoding destination.

```python
# The redirect logic (built into Django auth)
if user is authenticated:
    next_url = request.GET.get('next', 'dashboard')
    return redirect(next_url)
```

---

### Q4: Why use sessions instead of passing user data in URL?

**Answer:**
- ❌ **URL approach:** GET /dashboard/?user_id=5 (insecure - user can edit URL)
- ✅ **Session approach:** Server stores user in secure session cookie

Sessions are:
- **Secure:** Data stored on server, not visible in URL
- **Persistent:** Survives page refreshes
- **Sessionless attacks:** Prevent CSRF, session hijacking with proper middleware
- **Scalable:** Can revoke access server-side without client action

---

### Q5: What's the difference between login() and authenticate()?

**Answer:**
- `authenticate(username=..., password=...)` → **Verifies credentials**, returns User or None
- `login(request, user)` → **Creates session**, stores in browser cookie

Must use both:
```python
# Step 1: Verify credentials
user = authenticate(request, username=username, password=password)

# Step 2: Create session
if user:
    login(request, user)  # Now user is "logged in"
```

---

### Q6: How would you implement "Remember Me" functionality?

**Answer:**
Django sessions expire by default. To implement "Remember Me":

```python
if request.POST.get('remember_me'):
    # Keep session for 30 days
    request.session.set_expiry(30 * 24 * 60 * 60)
else:
    # Expire when browser closes
    request.session.set_expiry(0)

login(request, user)
```

This is why sessions are better than just checking a cookie — Django controls expiration.

---

## Learning Checkpoints

### ✏️ Checkpoint 1: Registration Flow
- [ ] User fills form with username, email, password, confirm password
- [ ] Form validates: email is unique, passwords match, password is strong
- [ ] User is created in database (password hashed with set_password())
- [ ] User is auto-logged in (session created)
- [ ] Redirected to dashboard
- [ ] Success message displays

### ✏️ Checkpoint 2: Login Flow
- [ ] User enters username/password
- [ ] Django checks User database (authenticate())
- [ ] Credentials valid → session created, redirected to dashboard
- [ ] Credentials invalid → error message, re-render form

### ✏️ Checkpoint 3: Access Control
- [ ] Logged-in user can access /dashboard/
- [ ] Anonymous user visiting /dashboard/ redirected to /login/
- [ ] After login, redirected back to dashboard (via ?next=)

### ✏️ Checkpoint 4: Conditional Navigation
- [ ] Anonymous user sees "Login" and "Register" links
- [ ] Logged-in user sees username, "Dashboard" and "Logout" links
- [ ] Navigation updated immediately after login/logout

### ✏️ Checkpoint 5: Message Display
- [ ] Success message after registration
- [ ] Error message on failed login
- [ ] Info message on logout
- [ ] Messages disappear after one page load

---

## Hands-On Exercises

### Exercise 1: Add Email Verification
Extend RegistrationForm to send verification email before account activation. (Hint: Use Django email backend)

### Exercise 2: Implement "Forgot Password"
Create a form to reset password via email token. (Hint: Use PasswordResetView, uid, and token)

### Exercise 3: Add Social Login
Integrate Google/GitHub OAuth. (Hint: django-allauth package)

### Exercise 4: Implement Rate Limiting
Prevent brute-force login attacks. (Hint: Track failed attempts per IP)

### Exercise 5: Add Two-Factor Authentication
Require phone/authenticator app for login. (Hint: django-otp package)

---

## Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False` in settings.py
- [ ] Use `DEBUG = False` to test locally: `python manage.py runserver --insecure`
- [ ] Add SECRET_KEY to environment variable (not hardcoded)
- [ ] Configure ALLOWED_HOSTS to production domain
- [ ] Use HTTPS (not HTTP) — enforce with `SECURE_SSL_REDIRECT = True`
- [ ] Set `SESSION_COOKIE_SECURE = True` (cookies only over HTTPS)
- [ ] Set `CSRF_COOKIE_SECURE = True` (CSRF protection only over HTTPS)
- [ ] Run `python manage.py collectstatic` for static files
- [ ] Run `python manage.py migrate` in production database
- [ ] Use environment variables for database credentials

---

## FAQ

**Q: Can I use the same form for registration and user profile update?**
A: Yes! Use `RegistrationForm(instance=user)` to pre-fill form with existing data. In registration: empty form. In edit profile: form with data.

**Q: How do I log out a user programmatically?**
A: Call `logout(request)` in a view. This clears the session and `request.user` becomes AnonymousUser.

**Q: What if password is too weak?**
A: UserCreationForm validates password strength. Django checks against common patterns and minimum length (default 8 chars).

**Q: Can I customize the login error message?**
A: Yes! Modify the message in login_view:
```python
if user is None:
    messages.error(request, "Your custom error message")
```

**Q: How do I check if user is admin?**
A: Use `request.user.is_staff` or `request.user.is_superuser`

**Q: Can I prevent a specific user from logging in?**
A: Yes! Set `user.is_active = False` and save. Even with correct password, authenticate() returns None.

---

## Summary

**A037 teaches public-facing authentication:**

✅ **RegistrationForm** — Extends UserCreationForm, validates email uniqueness  
✅ **Login/Logout** — authenticate() verifies creds, login() creates session  
✅ **Protected Pages** — @login_required decorator restricts access  
✅ **Conditional UI** — {% if user.is_authenticated %} shows different nav  
✅ **User Feedback** — Messages framework for success/error/info  
✅ **Session Management** — Server-side security, browser cookies  

This is the **foundation for real web applications**. Master this pattern and you can build secure user systems.

---

## Related Lectures

- **A035** — Messages Framework (used for user feedback)
- **A036** — User Management via Admin (backend approach)
- **A031-A034** — CRUD forms (foundation for RegistrationForm)

---

**Next Lecture:** A038 — File & Image Upload

> 📌 An earlier revision of this line mislabeled A038 as "Advanced Authentication (Social Login, OAuth, Two-Factor)". Corrected per the series' §12 practice: the real A038 chapter is the file & image upload lecture (`myProject22`).
