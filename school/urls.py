from django.urls import path
from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('main_dashboard/', IndexView.as_view(), name='main_dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LoginView.as_view(), name='logout'),
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/create/', SubjectCreateView.as_view(), name='subject_create'),
    path('class_time_slots/create/', ClassTimeSlotCreateView.as_view(), name='class_time_slot_create'),
    path('enroll/', EnrollmentView.as_view(), name='enrollment'),
    path('classes/', ClassListView.as_view(), name='class_list'),
    path('classes/create/', ClassCreateView.as_view(), name='class_create'),
    path('attendance/', AttendanceView.as_view(), name='attendance'),
    path('timetable/', TimetableView.as_view(), name='timetable'),
    path('teacher/attendance/', TeacherAttendanceView.as_view(), name='teacher_attendance'),
    path('classes/', ClassListView.as_view(), name='class_list'),

]