from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Division)
admin.site.register(models.WeekSchedule)
admin.site.register(models.Announcements)
admin.site.register(models.TimeTable)


class DayScheduleInline(admin.TabularInline):
    model = models.DaySchedule
    extra = 1

@admin.register(models.Day)
class DayAdmin(admin.ModelAdmin):
    inlines = [DayScheduleInline]

@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(models.TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time']

@admin.register(models.DaySchedule)
class DayScheduleAdmin(admin.ModelAdmin):
    list_display = ['day', 'time_slot', 'subject', 'order']
    list_filter = ['day']
    ordering = ['day', 'order']