from django.urls import path
from . import views

urlpatterns = [
    path('bulk-email/', views.send_bulk_email, name='bulk_email'),
    path('bulk-email1/', views.send_bulk_email1, name='bulk_email1'),
]