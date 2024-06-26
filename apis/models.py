from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=200, default="blank")

    def __str__(self) -> str:
        return self.name

class Division(models.Model):
    name = models.CharField(max_length=20, default="blank")

    def __str__(self) -> str:
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=400, default="none")
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
    
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return f"{self.start_time} - {self.end_time}"
    
class Day(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    
class DaySchedule(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="schedules")
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="schedules", default="")
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, default="1")
    order = models.PositiveIntegerField(default=1)
    
    def __str__(self) -> str:
        return f"{self.day.name} - {self.time_slot} - {self.subject.name}"
    
    class Meta:
        ordering = ['day', 'order']

    def __str__(self) -> str:
        return f'{self.day.name} : {self.time_slot.start_time} - {self.time_slot.end_time}'

class WeekSchedule(models.Model):
    week_day = models.CharField(max_length=200, default = "FE")
    daySchedule = models.ManyToManyField(DaySchedule, related_name="daysSchedule")


    def __str__(self) -> str:
        return f'{self.week_day}'
    

class Announcements(models.Model):
    title =  models.CharField(max_length=400)
    description = models.TextField()
    type = models.CharField(max_length=400)
    division = models.ManyToManyField(Division, related_name="announcements")

    def __str__(self):
        return self.title
    

class TimeTable(models.Model):
    year = models.CharField(max_length=400)
    weeks = models.ManyToManyField(WeekSchedule, related_name="weekschedule")

    def __str__(self):
        return self.year
