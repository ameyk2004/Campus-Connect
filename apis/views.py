from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Teacher
import json

# Create your views here.

@csrf_exempt
def register_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        role = 'Student'

        student, created = Student.objects.update_or_create(uid=data['uid'])
        student.email = data['email']
        student.name = data['name']
        student.division = data['division']
        student.roll_no = data['roll_no']
        student.role = role

        student.save()
        return  JsonResponse({'status': 'success'})
    
    else:
       return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})
    
@csrf_exempt    
def get_user_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid=data["uid"]
        role = None

        try:
            student = Student.objects.get(uid=uid)
            role = student.role
            
        except Student.DoesNotExist:
            pass

        try:
            teacher = Teacher.objects.get(uid=uid)
            role = teacher.role
        except Teacher.DoesNotExist:
            pass
    
        return  JsonResponse({'status': 'success', 'role' : f'{role}'})
    
    else:
       return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

@csrf_exempt
def register_teacher(request):
    if request.method == "POST":
        data = json.loads(request.body)

        teacher, created = Teacher.objects.get_or_create(uid=data["uid"])
        teacher.name = data["name"]
        teacher.division=data["division"]
        teacher.email=data["email"]
        teacher.role="Teacher"

        teacher.save()

        return JsonResponse({"status" : "Success"})
    
    else:
         return JsonResponse({"status" : "Fail", "message" : "Not Allowed"})

