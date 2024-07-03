from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Teacher, Division, Subject,Announcements, TimeTable, DaySchedule,Day,TimeSlot,Attendance
import json
from datetime import date

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
            student.save()
            print(student.uid)
            print(student.name)

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

        print(uid)

        try:
            student = Student.objects.get(uid=uid)
            role = student.role
            name = student.name
            division = student.division
            email = student.email

            print(role)
            
        except Student.DoesNotExist:
            pass

        try:
            teacher = Teacher.objects.get(uid=uid)
            role = teacher.role
            name = teacher.name
            division = teacher.division
            email = teacher.email

        except Teacher.DoesNotExist:
            pass
    
        return  JsonResponse(
            {
                'status': 'success', 
                'role' : f'{role}',
                'name' : f'{name}',
                'division' : f'{division.name}',
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
def get_students(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subject_name = data.get("subject", "")
            division_name = data.get("division", "")
            role = data.get("role", "")

            students = Student.objects.all()

            if subject_name:
                subject = Subject.objects.get(name=subject_name)
                students = students.filter(subject=subject)

            if division_name:
                division = Division.objects.get(name=division_name)
                students = students.filter(division=division)

            response = []
            for student in students:
                student_info = {
                    "uid": student.uid,
                    "name": student.name,
                    "email": student.email,
                    "roll_no": student.roll_no,
                }
                response.append(student_info)

            return JsonResponse({"status": "success", "students": response})
         
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
    
@csrf_exempt
def get_timetable(request):
    if request.method== "POST":
        data = json.loads(request.body)
        year = data["year"]

    
        # timetables = TimeTable.objects.all()
        days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        start_times = ["9:00","10:00","11:00", "11:15", "12:15", "13:00"]
        time_table = {}

        for day in days:
            day = Day.objects.get(name=f"{year}-{day}")
            day_data={}
            for start_time in start_times:
                time_slot= TimeSlot.objects.get(start_time=start_time)


                daySchedule = DaySchedule.objects.get(day=day, time_slot=time_slot)
                day_data.update({f"{daySchedule.time_slot}": f"{daySchedule.subject}" })

            time_table.update({f"{day.name}": day_data})

        return JsonResponse({"status" : "success",  "time_table" : time_table},)
    
    else:
        return JsonResponse({"status" : "failed"})

@csrf_exempt
def mark_attendance_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        year = data.get('year')
        day_name = data.get('day_name')
        time_slot_start = data.get('time_slot_start')
        time_slot_end = data.get('time_slot_end')
        teacher_uid = data.get('teacher_uid')
        subject_name = data.get('subject_name')
        student_uids = data.get('uids')  # Assuming 'uids[]' is the name of the parameter containing student UIDs
        
        teacher = get_object_or_404(Teacher, uid=teacher_uid)
        subject = get_object_or_404(Subject, name=subject_name)
        day = get_object_or_404(Day, name=day_name)
        time_slot = get_object_or_404(TimeSlot, start_time=time_slot_start, end_time=time_slot_end)
        
        try:
            timetable = TimeTable.objects.get(year=year)
            day_schedule = DaySchedule.objects.get(day=day, subject=subject, time_slot=time_slot)
        except (TimeTable.DoesNotExist, DaySchedule.DoesNotExist):
            return JsonResponse({'error': 'Day schedule not found for the given parameters.'}, status=404)
        
        students_present = Student.objects.filter(uid__in=student_uids)
        
        attendance, created = Attendance.objects.get_or_create(
            day_schedule=day_schedule,
            teacher=teacher,
            date=date.today()
        )
        attendance.students_present.set(students_present)
        attendance.save()
        
        present_students_names = [student.name for student in students_present]
        response_data = {
            'message': 'Attendance marked successfully.',
            'subject': subject.name,
            'students_present': present_students_names,
            'time_slot' : time_slot.start_time
        }
        
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)