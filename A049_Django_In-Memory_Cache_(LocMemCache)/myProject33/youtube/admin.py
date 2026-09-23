from django.contrib import admin
from .models import YouTubeUser
from django.core.cache import cache
from django.contrib import messages

@admin.action(description='Clear Users Cache')
def clear_users_cache(modeladmin, request, queryset):
    # Clear the cache for users data
    cache.delete('users_data')
    messages.success(request, "Users cache cleared successfully.")

# Register your models here.
@admin.register(YouTubeUser)
class YouTubeUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subscribers')
    # search_fields = ('name', 'email')
    # list_filter = ('subscribers',)
    actions = [clear_users_cache]