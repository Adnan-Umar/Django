from django.shortcuts import render
from .models import UserProfile
from django.core.cache import cache

# Create your views here.
def user_profile_list(request):
    # Check if the user profile is already cached
    users_data = cache.get('users_data')

    if users_data is None:
        print("Fetch Data from Database")  # For debugging purposes
        # If not cached, retrieve it from the database
        users_data = UserProfile.objects.all()  # Assuming you want all user profiles
        # Cache the user profiles for future requests (e.g., for 5 minutes)
        cache.set('users_data', users_data)
    else:
        print("Fetch Data from Cache")  # For debugging purposes

    return render(request, 'user_profile_list.html', {'users': users_data})