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