from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sub_teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"Subject is {self.name} and teacher is {self.sub_teacher}"


class Class(models.Model):
    class_name = models.CharField(max_length=55, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    capacity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.class_name


class ClassTimeSlot(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject} and time slot is {self.start_time} to {self.end_time} and class is {self.class_name}"


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(ClassTimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"Enrollment for {self.student} and subject is {self.subject} and time is {self.time_slot}"


class Attendance(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()

    def __str__(self):
        return f"{self.enrollment} is {self.status}"
