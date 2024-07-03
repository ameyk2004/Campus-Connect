# Generated by Django 5.0.6 on 2024-07-01 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0005_student_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('day_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='apis.dayschedule')),
                ('students_present', models.ManyToManyField(related_name='attendances', to='apis.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='apis.teacher')),
            ],
        ),
    ]
