
#Users url.py




from django.contrib import admin
from django.urls import path, include
from .views import ProfileView, NewUserProfileView, profile,error, setup
urlpatterns = [
    path('setup/',NewUserProfileView.as_view(), name='setup'),
]
