from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Hello World. You are at django Home Page")
    # return render(request, "index.html")
    return render(request, "website/index1.html")

def about(request):
    return HttpResponse("Hello World. You are at django About Page")

def contact(request):
    return HttpResponse("Hello World. You are at django Contact Page")