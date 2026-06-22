from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),  # ✅ renamed to match your views.py
]
