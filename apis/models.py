from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Division(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=400)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name="students")
    roll_no = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)
    uid = models.CharField(max_length=255, unique=True)
    subject = models.ManyToManyField(Subject, related_name='students')

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    name = models.CharField(max_length=400)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name="teachers")
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)
    uid = models.CharField(max_length=255, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="teachers")

    def __str__(self):
        return self.name

class Day(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    
class DaySchedule(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="days")
    subject=models.ManyToManyField(Subject, related_name="days")

    def __str__(self) -> str:
        return self.day.name

class WeekSchedule(models.Model):
    daySchedule = models.ForeignKey(DaySchedule, on_delete=models.CASCADE, related_name="daysSchedule")

    def __str__(self) -> str:
        return self.daySchedule.day.name
    

class Announcements(models.Model):
    title =  models.CharField(max_length=400)
    description = models.TextField()
    type = models.CharField(max_length=400)
    division = models.ManyToManyField(Division, related_name="announcements")

    def __str__(self):
        return self.title
