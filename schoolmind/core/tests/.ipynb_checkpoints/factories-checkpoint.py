import factory
from django.contrib.auth.models import User
from core.models import Profile, Category, Course, CourseSchedule, Attendance
from datetime import time, date

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda u: f"{u.username}@example.com")
    # обращаем внимание, что пароль должен хешироваться:
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    role = 'student'
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    middle_name = ''
    bio = factory.Faker('text')
    address = factory.Faker('address')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category{n}")
    description = factory.Faker('sentence')

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Sequence(lambda n: f"Course{n}")
    description = factory.Faker('paragraph')
    category = factory.SubFactory(CategoryFactory)
    duration = "1 month"

class CourseScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CourseSchedule

    course = factory.SubFactory(CourseFactory)
    instructor = factory.SubFactory(ProfileFactory)
    day_of_week = "Monday"
    start_time = time(9, 0)
    end_time = time(10, 30)

class AttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attendance

    course = factory.SubFactory(CourseFactory)
    student = factory.SubFactory(UserFactory)
    lesson_date = date.today()
    attendance_status = 'attended_paid'
