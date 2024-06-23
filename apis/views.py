from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Teacher, Division, Subject
import json

# Create your views here.

@csrf_exempt
def register_student(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        role = 'Student'

        try:
            division, created = Division.objects.get_or_create(name=data["division"])

            student, created = Student.objects.update_or_create(
                uid=data['uid'],
                defaults={
                    'email': data['email'],
                    'name': data['name'],
                    'division': division,
                    'roll_no': data['roll_no'],
                    'role': role
                }
            )

            return JsonResponse({'status': 'success'})
        
        except Division.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Division does not exist'}, status=400)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
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
        role = 'Teacher'

        try:
            division, created = Division.objects.get_or_create(name=data["division"])
            subject,created = Subject.objects.get_or_create(name=data["subject"])
            teacher, created = Teacher.objects.update_or_create(
                uid=data["uid"],
                defaults={
                    'email': data['email'],
                    'name': data['name'],
                    'division': division,
                    'subject': subject,
                    'role': role,
                }
            )

            teacher.save()

        except Division.DoesNotExist:
            pass

        except Student.DoesNotExist:
            pass

        

        return JsonResponse({"status" : "Success"})
    
    else:
         return JsonResponse({"status" : "Fail", "message" : "Not Allowed"})

