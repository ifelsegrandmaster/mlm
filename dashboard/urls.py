"""mlm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='landing'),
    path('tandcs',tandcs, name='tandcs'),
    path('view/<slug:action>/', home, name='home' ),
    path('view/<slug:action>/<int:id>/',details ,name='details'),
    path('activate/<int:id>/', activate, name='activate'),
    path('fetch/<int:id>/', fetch, name='fetch'),
    path('get_data/<int:id>/', get_user_data, name='get_data'),
    path('search/<str:category>/<str:keyword>/', search, name='search'),
    path('get_payments/<str:keyword>/', get_payments, name='get_payments'),
    path('pay/<int:pk>/', pay, name='pay'),
    path('register/', register, name='register'),
    path('get_dashboard_data/', get_dashboard_data, name='get_dashboard_data'),
    path("fire/<int:id>/", fire, name='fire'),
    path("delete_user/<int:id>/", delete_user, name="delete_user"),
    path("get_admins/", get_users, name='get_users'),
    path("make_admin/<int:id>/", make_admin, name = 'make_admin'),
    path("add-email-address/",add_email_address, name="add_email_address"),
    path("send-email/", send_email, name="send_mail"),
    path("email-sent/", email_sent, name="email_sent"),
    path("unauthorized/", unauthorized, name="unauthorized")    
]
