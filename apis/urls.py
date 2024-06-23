from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register-student', views.register_student, name="register_student"),
    path('register-teahcer', views.register_teacher, name="register_teacher"),
    path('get-user-details', views.get_user_details, name="get-user-details")
]