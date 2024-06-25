from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Teacher, Division, Subject,Announcements
import json

# Create your views here.

@csrf_exempt
def register_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            print(data)

            # Ensure required fields are present
            required_fields = ['uid', 'email', 'name', 'division', 'roll_no', 'subjects']
            if not all(field in data for field in required_fields):
                return JsonResponse({'status': 'error', 'message': 'Missing required parameters'}, status=400)

            # Get or create Division
            division, created = Division.objects.get_or_create(name=data["division"])

            # Update or create Student
            student, created = Student.objects.update_or_create(
                uid=data['uid'],
                defaults={
                    'email': data['email'],
                    'name': data['name'],
                    'division': division,
                    'roll_no': data['roll_no'],
                    'role': 'Student'
                }
            )

            # Update Student's subjects
            subject_names = data["subjects"]
            subjects = []
            for subject_name in subject_names:
                try:
                    subject = Subject.objects.get(name=subject_name)
                    subjects.append(subject)
                except Subject.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': f'Subject {subject_name} does not exist'}, status=400)

            student.subject.set(subjects)
            student.save()

            return JsonResponse({'status': 'success'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        except Division.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Division does not exist'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)

@csrf_exempt    
def get_user_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid=data["uid"]
        role = None

        try:
            student = Student.objects.get(uid=uid)
            role = student.role
            name = student.name
            division = student.division
            email = student.email
            
        except Student.DoesNotExist:
            pass

        try:
            teacher = Teacher.objects.get(uid=uid)
            role = teacher.role
            name = teacher.name
            division = student.division
            email = student.email

        except Teacher.DoesNotExist:
            pass
    
        return  JsonResponse(
            {
                'status': 'success', 
                'role' : f'{role}',
                'name' : f'{name}',
                'division' : f'{division}',
                'email' : f'{email}',
            }
            )
    
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

@csrf_exempt
def get_users(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        subject_name = data.get("subject", "")
        division_name = data.get("division", "")
        role = data.get("role", "")

        students = Student.objects.all()

        try:
            if subject_name:
                subject = Subject.objects.get(name=subject_name)
                students.filter(subject=subject).distinct()
                
            if division_name:
                division = Division.objects.get(name=division_name)
                students.filter(division=division).distinct()

            response = {}
            for student in students:
                {
                    response.update({
                        f"{student.uid}" : {
                        "name" : {student.name},
                        "email" : {student.email},
                        "roll_no" : {student.roll_no},
                        "division" : {student.division},
                    }
                })
                }

                print(response)

            return JsonResponse({"status": "success",})

        except Subject.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Subject does not exist"}, status=400)
        except Division.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Division does not exist"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
@csrf_exempt
def get_announcements(request):
    if request.method == "POST":
        data = json.loads(request.body)

        division_name = data["division"]

        division = Division.objects.get(name=division_name)
        announcements =  division.announcements.all()
    
        announcements_response = []

        for announcement in announcements:
            context = {
                "title" : announcement.title,
                "description" : announcement.description,
                "type" : announcement.type,
            }
            announcements_response.append(context)

        return JsonResponse({"status" : "success", "announcements" : announcements_response})
    
    else:
        return JsonResponse({"status" : "failed"})
    