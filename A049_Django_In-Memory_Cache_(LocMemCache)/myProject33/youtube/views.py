from django.shortcuts import render
from .models import YouTubeUser
from django.core.cache import cache

# Create your views here.
def users_list(request):
    # Check if the data is already cached
    users = cache.get('users_data')  # Try to get the cached data with the key 'users_data'

    if not users:
        print("Cache miss: Fetching data from the database.")
        # If not cached, fetch from the database
        users = YouTubeUser.objects.all()
        # Cache the data for 5 minutes (300 seconds)
        cache.set('users_data', users, timeout=60)  # Cache the data for 60 seconds (1 minute)
    else:
        print("Cache hit: Using cached data.")

    return render(request, 'users_list.html', {'users': users})