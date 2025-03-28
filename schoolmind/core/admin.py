from django.contrib import admin
from .models import Profile, Category, Course, CourseSchedule, Attendance

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CourseSchedule)
admin.site.register(Attendance)
