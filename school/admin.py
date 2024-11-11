from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(ClassTimeSlot)
admin.site.register(Enrollment)
admin.site.register(Attendance)
