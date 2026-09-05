from django.urls import path
from . import views

locals
urlpatterns = [
    path('', views.all_chai, name='all_chai'),
]