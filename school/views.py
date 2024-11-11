from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import *
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password


class IndexView(TemplateView):
    template_name = 'school/main_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class RegisterView(View):
    def get(self, request):
        return render(request, 'school/signup.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password),
            role=role
        )

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'school/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                login(request, user)
                return redirect(reverse_lazy('main_dashboard'))
            else:
                messages.error(request, "Invalid email or password")
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login')


class SubjectListView(View):
    def get(self, request):
        subjects = Subject.objects.all()
        return render(request, "school/subject_list.html", {'subjects': subjects})

class SubjectCreateView(View):
    def get(self, request):
        return render(request, "school/subject_form.html")

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        teacher_id = request.POST.get('teacher')

        subject = Subject.objects.create(
            name=name,
            description=description,
            sub_teacher_id=teacher_id
        )

        messages.success(request, "Subject created successfully!")
        return redirect('subject_list')


class ClassTimeSlotCreateView(View):
    def get(self, request):
        subjects = Subject.objects.all()
        return render(request, "school/class_time_slot_form.html", {'subjects': subjects})

    def post(self, request):
        subject_id = request.POST.get('subject')
        class_name = request.POST.get('class_name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        subject = Subject.objects.create(
            subject_id=subject_id,
            class_name=class_name,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(request, "Class time slot created successfully!")
        return redirect('class_time_slot_list')



class EnrollmentView(View):
    def get(self, request):
        subjects = Subject.objects.all()
        time_slots = ClassTimeSlot.objects.all()
        return render(request, 'school/enrollment.html', {'subjects': subjects})

    def post(self, request):
        subject_id = request.POST.get('subject')
        time_slot_id = request.POST.get('time_slot')
        student = request.user

        enrollment = Enrollment.objects.create(
            student=student,
            subject_id=subject_id,
            time_slot_id=time_slot_id
        )
        messages.success(request, "Enrollment successful.")
        return redirect('enrollment_success')


class ClassListView(View):
    def get(self, request):
        classes = Class.objects.all()
        return render(request, 'school/class_list.html', {'classes': classes})


class ClassCreateView(View):
    def get(self, request):
        return render(request, 'school/class_form.html')

    def post(self, request):
        class_name = request.POST.get('class_name')
        capacity = request.POST.get('capacity')

        class_instance = Class.objects.create(
            class_name=class_name,
            capacity=capacity
        )
        messages.success(request, "Class created successfully.")
        return redirect('class_list')


class AttendanceView(View):
    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        return render(request, 'school/attendance.html', {'enrollments': enrollments})

    def post(self, request):
        enrollment_id = request.POST.get('enrollment')
        status = request.POST.get('status')
        date = request.POST.get('date')

        Attendance.objects.create(
            enrollment_id=enrollment_id,
            date=date,
            status=status
        )
        messages.success(request, "Attendance recorded.")
        return redirect('attendance_success')


class TimetableView(View):
    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        timetable = []
        for enrollment in enrollments:
            timetable.append({
                'subject': enrollment.subject.name,
                'time_slot': enrollment.time_slot,
                'date': enrollment.time_slot.start_time,
            })
        return render(request, 'school/timetable.html', {'timetable': timetable})


class TeacherAttendanceView(View):
    def get(self, request):
        classes = Class.objects.filter(teacher=request.user)
        attendance_records = []
        for class_instance in classes:
            attendance = Attendance.objects.filter(enrollment__subject=class_instance.subject)
            attendance_records.append({
                'class': class_instance,
                'attendance': attendance,
            })
        return render(request, 'school/teacher_attendance.html', {'attendance_records': attendance_records})