from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=400)
    division=models.CharField(max_length=20)
    roll_no=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20)
    uid=models.CharField(max_length=255, unique=True)

    def __str__ (self):
        return self.name
    
class Teacher(models.Model):
    name = models.CharField(max_length=400)
    division=models.CharField(max_length=20)
    email=models.EmailField()
    role=models.CharField(max_length=20)
    uid=models.CharField(max_length=255, unique=True)

    def __str__ (self):
        return self.name
    
