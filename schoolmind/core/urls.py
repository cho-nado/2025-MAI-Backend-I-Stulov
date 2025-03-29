from django.urls import path
from .views import (
    search_profile_view, list_profiles_view, create_profile_view,
    search_category_view, list_categories_view, create_category_view,
    search_course_view, list_courses_view, create_course_view,
    search_course_schedule_view, list_course_schedule_view, create_course_schedule_view,
    search_attendance_view, list_attendance_view, create_attendance_view,
)

urlpatterns = [
    # Profile endpoints
    path('profile/search/', search_profile_view, name='search_profile'),
    path('profile/', list_profiles_view, name='list_profiles'),
    path('profile/create/', create_profile_view, name='create_profile'),
    
    # Category endpoints
    path('category/search/', search_category_view, name='search_category'),
    path('category/', list_categories_view, name='list_categories'),
    path('category/create/', create_category_view, name='create_category'),
    
    # Course endpoints
    path('course/search/', search_course_view, name='search_course'),
    path('course/', list_courses_view, name='list_courses'),
    path('course/create/', create_course_view, name='create_course'),


    
    # CourseSchedule endpoints
    path('courseschedule/search/', search_course_schedule_view, name='search_course_schedule'),
    path('courseschedule/', list_course_schedule_view, name='list_course_schedule'),
    path('courseschedule/create/', create_course_schedule_view, name='create_course_schedule'),
    
    # Attendance endpoints
    path('attendance/search/', search_attendance_view, name='search_attendance'),
    path('attendance/', list_attendance_view, name='list_attendance'),
    path('attendance/create/', create_attendance_view, name='create_attendance'),
]
