from django.shortcuts import render
from datetime import datetime

# Create your views here.
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def home(request):
    context = {
        "name": "Adnan",
        "age": 23,
        "skills": ["python", "django", "React"],
        "user": User("Umar", 22),
        "blog": {
            "title": "Django Template Intro",
            "content": "<b>This is Bold</b>",
            "created_at": datetime(2026, 8, 25, 13, 10, 30)
        },
        "empty_value": None,
    }
    return render(request, "blog/home.html", context)