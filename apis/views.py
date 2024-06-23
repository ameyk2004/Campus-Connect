from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Student
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
def get_stud_details(request):
    if request.method == 'GET':
        data = json.loads(request.body)

        try:
            student = Student.objects.get(uid=uid)
            return student, 'Student'
        except Student.DoesNotExist:
            pass
    

        student.save()
        return  JsonResponse({'status': 'success', 'role' : f'{student.role}'})
    
    else:
       return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})

