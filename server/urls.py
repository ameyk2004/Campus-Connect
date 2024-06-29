from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('keep-alive', views.keep_alive, name="keep-alive"),
]
