"""
URL configuration for test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ShrimpEasy import views
from django.contrib import admin
from django.urls import path, re_path
from django.urls import re_path
from django.views.static import serve

from shrimp import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('addNewFarm',views.addNewFarm,name='addNewFarm'),
    path('deleteFarm',views.deleteFarm,name='deleteFarm'),
    path('calculateProgress',views.calculateProgress,name='calculateProgress'),
    path('weather',views.weather,name='weather'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] 