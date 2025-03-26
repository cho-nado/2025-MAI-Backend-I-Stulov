from django.urls import path
from .views import (
    profile_view,
    courses_list_view,
    categories_list_view
)

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('courses/', courses_list_view, name='courses'),
    path('categories/', categories_list_view, name='categories'),
]
