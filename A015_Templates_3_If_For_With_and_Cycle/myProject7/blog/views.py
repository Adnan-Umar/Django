from django.shortcuts import render
from datetime import datetime

# Create your views here.
def blog_list(request):
    blogs = [
        {"title":"Django Basic", "is_feature":True, "author":"Adnan"},
        {"title":"Django Advanced", "is_feature":False, "author":""},
        {"title":"Django REST Framework", "is_feature":False, "author":"Deo"},
    ]
    context = {
        "blogs":blogs,
        "today":datetime.now(),
        "html_code": "<b>Welcome to my blog</b>"
    }
    return render(request, 'blog/blog_list.html', context)