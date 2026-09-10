from django.shortcuts import render
from datetime import datetime

# Create your views here.
def blog_details(request):
    post = {
        "title": "My Second Templates Post",
        "descriptions": "Django is a high level python framework that ",
        "author": None,
        "created_at": datetime(2026, 8, 26, 14, 20, 30),
        "comment_count": 5,
        "tags": ["Django", "python", "web devlopment"],
        "price":100,
        "number":7,
    }
    return render(request, 'blog/blog_details.html', {"post": post})