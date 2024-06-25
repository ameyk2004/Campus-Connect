from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Subject)
admin.site.register(models.Division)
admin.site.register(models.Day)
admin.site.register(models.WeekSchedule)
admin.site.register(models.DaySchedule)
admin.site.register(models.Announcements)