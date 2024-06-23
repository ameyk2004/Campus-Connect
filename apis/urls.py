from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register-student', views.register_student, name="register_student"),
    path('get-stud-details', views.get_stud_details, name="get-stud-details")
]