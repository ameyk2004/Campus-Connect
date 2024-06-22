from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('server/', views.home_page, name="home"),
]
