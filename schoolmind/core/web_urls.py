from django.urls import path
from . import web_views

urlpatterns = [
    path('profile/', web_views.profile_web_view, name='web_profile'),
    path('category/', web_views.category_web_view, name='web_category'),
    path('course/', web_views.course_web_view, name='web_course'),
    path('courseschedule/', web_views.courseschedule_web_view, name='web_courseschedule'),
    path('attendance/', web_views.attendance_web_view, name='web_attendance'),
    path('health/',             web_views.health_check,           name='health'),
]
