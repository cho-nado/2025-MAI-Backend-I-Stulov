from django.urls import path
from .api_views import (
    ProfileListCreateAPIView, ProfileRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView,
    CourseListCreateAPIView, CourseRetrieveUpdateDestroyAPIView,
    CourseScheduleListCreateAPIView, CourseScheduleRetrieveUpdateDestroyAPIView,
    AttendanceListCreateAPIView, AttendanceRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # === Profile ===
    path('profile/', ProfileListCreateAPIView.as_view(), name='api_profile_list'),
    path('profile/<int:pk>/', ProfileRetrieveUpdateDestroyAPIView.as_view(), name='api_profile_detail'),

    # === Category ===
    path('category/', CategoryListCreateAPIView.as_view(), name='api_category_list'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='api_category_detail'),

    # === Course ===
    path('course/', CourseListCreateAPIView.as_view(), name='api_course_list'),
    path('course/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='api_course_detail'),

    # === CourseSchedule ===
    path('courseschedule/', CourseScheduleListCreateAPIView.as_view(), name='api_schedule_list'),
    path('courseschedule/<int:pk>/', CourseScheduleRetrieveUpdateDestroyAPIView.as_view(), name='api_schedule_detail'),

    # === Attendance ===
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='api_attendance_list'),
    path('attendance/<int:pk>/', AttendanceRetrieveUpdateDestroyAPIView.as_view(), name='api_attendance_detail'),
]
