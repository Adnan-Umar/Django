from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to the blog home page")

def about(request):
    a = 10 + 50
    return HttpResponse(f"About page {a}")