from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'base.html')

def blog(request):
    students_list = [
        {"name":"Adnan", "class":"10th"},
        {"name":"Md", "class":"9th"},
        {"name":"Umar", "class":"8th"},
    ]
    return render(request, 'blog.html', {'students':students_list})