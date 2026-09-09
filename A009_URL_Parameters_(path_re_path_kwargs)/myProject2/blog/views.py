from django.http import HttpResponse

# Create your views here.
def post_details(request, post_id):
    return HttpResponse(f"<h1>Show blog Post: {post_id}</h1>")

def user_profile(request, username):
    return HttpResponse(f"<h1>Profile of user: {username}</h1>")

def article_by_year(request, year):
    return HttpResponse(f"<h1>Article from year: {year}</h1>")

# def article_details(request, year, month):
#     return HttpResponse(f"<h1>Article from {year} - {month}</h1>")

def article_details(request, **kwargs):
    return HttpResponse(f"<h1>Data: {kwargs}</h1>")