from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User
from .models import Profile, Category, Course, CourseSchedule, Attendance
from datetime import datetime


# ========================
# Profile Endpoints
# ========================

@require_GET
def search_profile_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    profiles = Profile.objects.filter(user__username__icontains=query) | Profile.objects.filter(role__icontains=query)
    profiles = profiles.distinct()
    result = []
    for profile in profiles:
        result.append({
            "id": profile.id,
            "username": profile.user.username,
            "role": profile.role,
            "bio": profile.bio,
            "address": profile.address,
        })
    return JsonResponse({"profiles": result})

@require_GET
def list_profiles_view(request):
    profiles = Profile.objects.all()
    result = []
    for profile in profiles:
        result.append({
            "id": profile.id,
            "username": profile.user.username,
            "role": profile.role,
            "bio": profile.bio,
            "address": profile.address,
        })
    return JsonResponse({"profiles": result})

@csrf_exempt
@require_POST
def create_profile_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    bio = data.get("bio", "")
    address = data.get("address", "")
    if not username or not password or not role:
        return JsonResponse({"error": "Missing required fields (username, password, role)"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    profile = Profile.objects.create(user=user, role=role, bio=bio, address=address)
    return JsonResponse({
        "id": profile.id,
        "username": profile.user.username,
        "role": profile.role,
        "bio": profile.bio,
        "address": profile.address,
    }, status=201)

# ========================
# Category Endpoints
# ========================

@require_GET
def search_category_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    categories = Category.objects.filter(name__icontains=query) | Category.objects.filter(description__icontains=query)
    categories = categories.distinct()
    result = []
    for cat in categories:
        result.append({
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "parent_category": cat.parent_category.id if cat.parent_category else None,
        })
    return JsonResponse({"categories": result})

@require_GET
def list_categories_view(request):
    categories = Category.objects.all()
    result = []
    for cat in categories:
        result.append({
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "parent_category": cat.parent_category.id if cat.parent_category else None,
        })
    return JsonResponse({"categories": result})

@csrf_exempt
@require_POST
def create_category_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    name = data.get("name")
    description = data.get("description", "")
    parent_id = data.get("parent_category")  # optional: id родительской категории
    if not name:
        return JsonResponse({"error": "Missing required field: name"}, status=400)
    parent_category = None
    if parent_id:
        try:
            parent_category = Category.objects.get(id=parent_id)
        except Category.DoesNotExist:
            return JsonResponse({"error": "Parent category not found"}, status=400)
    category = Category.objects.create(name=name, description=description, parent_category=parent_category)
    return JsonResponse({
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "parent_category": category.parent_category.id if category.parent_category else None,
    }, status=201)

# ========================
# Course Endpoints
# ========================

@require_GET
def search_course_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    courses = Course.objects.filter(title__icontains=query) | Course.objects.filter(description__icontains=query)
    courses = courses.distinct()
    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
        })
    return JsonResponse({"courses": result})

@require_GET
def list_courses_view(request):
    courses = Course.objects.all()
    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
        })
    return JsonResponse({"courses": result})

@csrf_exempt
@require_POST
def create_course_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    title = data.get("title")
    description = data.get("description")
    delivery_mode = data.get("delivery_mode", "online")
    category_id = data.get("category_id")
    duration = data.get("duration")
    
    if not title or not description or not category_id or not duration:
        return JsonResponse({"error": "Missing required fields (title, description, category_id, duration)"}, status=400)
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({"error": "Category not found"}, status=400)
    
    course = Course.objects.create(
        title=title,
        description=description,
        delivery_mode=delivery_mode,
        category=category,
        duration=duration
    )
    
    return JsonResponse({
        "id": course.id,
        "title": course.title,
        "description": course.description,
    }, status=201)

# ========================
# CourseSchedule Endpoints
# ========================

@require_GET
def search_course_schedule_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    schedules = CourseSchedule.objects.filter(day_of_week__icontains=query)
    schedules = schedules.distinct()
    result = []
    for sched in schedules:
        result.append({
            "id": sched.id,
            "course": sched.course.title,
            "day_of_week": sched.day_of_week,
            "start_time": sched.start_time.strftime("%H:%M:%S"),
            "end_time": sched.end_time.strftime("%H:%M:%S"),
            "instructor": sched.instructor.user.username if sched.instructor else None,
            "replacement": sched.replacement.user.username if sched.replacement else None,
        })
    return JsonResponse({"schedules": result})

@require_GET
def list_course_schedule_view(request):
    schedules = CourseSchedule.objects.all()
    result = []
    for sched in schedules:
        result.append({
            "id": sched.id,
            "course": sched.course.title,
            "day_of_week": sched.day_of_week,
            "start_time": sched.start_time.strftime("%H:%M:%S"),
            "end_time": sched.end_time.strftime("%H:%M:%S"),
            "instructor": sched.instructor.user.username if sched.instructor else None,
            "replacement": sched.replacement.user.username if sched.replacement else None,
        })
    return JsonResponse({"schedules": result})

@csrf_exempt
@require_POST
def create_course_schedule_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    # Преобразуем идентификаторы в int
    try:
        course_id = int(data.get("course_id"))
        instructor_id = int(data.get("instructor_id"))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid course_id or instructor_id"}, status=400)
    
    day_of_week = data.get("day_of_week")
    start_time_str = data.get("start_time")
    end_time_str = data.get("end_time")
    
    # Проверяем наличие обязательных полей
    if not (course_id and instructor_id and day_of_week and start_time_str and end_time_str):
        return JsonResponse({"error": "Missing required fields"}, status=400)
    
    # Преобразуем время из строки в объект time
    try:
        start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
        end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
    except ValueError:
        return JsonResponse({"error": "Invalid time format, expected HH:MM:SS"}, status=400)
    
    # Обработка поля replacement_id (если передано)
    replacement = None
    replacement_id = data.get("replacement_id")
    if replacement_id:
        try:
            replacement_id = int(replacement_id)
            replacement = Profile.objects.get(id=replacement_id)
        except (ValueError, Profile.DoesNotExist):
            return JsonResponse({"error": "Replacement instructor not found or invalid ID"}, status=400)
    
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=400)
    
    try:
        instructor = Profile.objects.get(id=instructor_id)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Instructor not found"}, status=400)
    
    # Создаем запись расписания
    schedule = CourseSchedule.objects.create(
        course=course,
        instructor=instructor,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        replacement=replacement
    )
    
    return JsonResponse({
        "id": schedule.id,
        "course": schedule.course.title,
        "day_of_week": schedule.day_of_week,
        "start_time": schedule.start_time.strftime("%H:%M:%S"),
        "end_time": schedule.end_time.strftime("%H:%M:%S"),
        "instructor": schedule.instructor.user.username if schedule.instructor else None,
        "replacement": schedule.replacement.user.username if schedule.replacement else None,
    }, status=201)

# ========================
# Attendance Endpoints
# ========================

@require_GET
def search_attendance_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)
    attendances = Attendance.objects.filter(student__username__icontains=query)
    attendances = attendances.distinct()
    result = []
    for att in attendances:
        result.append({
            "id": att.id,
            "course": att.course.title,
            "student": att.student.username,
            "lesson_date": att.lesson_date.isoformat(),
            "attendance_status": att.attendance_status,
            "absence_reason": att.absence_reason,
            "grade": str(att.grade) if att.grade is not None else None,
        })
    return JsonResponse({"attendances": result})

@require_GET
def list_attendance_view(request):
    attendances = Attendance.objects.all()
    result = []
    for att in attendances:
        result.append({
            "id": att.id,
            "course": att.course.title,
            "student": att.student.username,
            "lesson_date": att.lesson_date.isoformat(),
            "attendance_status": att.attendance_status,
            "absence_reason": att.absence_reason,
            "grade": str(att.grade) if att.grade is not None else None,
        })
    return JsonResponse({"attendances": result})

@csrf_exempt
@require_POST
def create_attendance_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    course_id = data.get("course_id")
    student_id = data.get("student_id")
    lesson_date_str = data.get("lesson_date")
    attendance_status = data.get("attendance_status")
    absence_reason = data.get("absence_reason", "")
    grade = data.get("grade")
    
    if not (course_id and student_id and lesson_date_str and attendance_status):
        return JsonResponse({"error": "Missing required fields"}, status=400)
    
    try:
        # Преобразуем строку в объект даты. Ожидаемый формат: YYYY-MM-DD
        lesson_date = datetime.strptime(lesson_date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format, expected YYYY-MM-DD"}, status=400)
    
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=400)
    
    try:
        student = User.objects.get(id=student_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=400)
    
    attendance = Attendance.objects.create(
        course=course,
        student=student,
        lesson_date=lesson_date,
        attendance_status=attendance_status,
        absence_reason=absence_reason,
        grade=grade
    )
    
    return JsonResponse({
        "id": attendance.id,
        "course": attendance.course.title,
        "student": attendance.student.username,
        "lesson_date": attendance.lesson_date.isoformat(),
        "attendance_status": attendance.attendance_status,
        "absence_reason": attendance.absence_reason,
        "grade": str(attendance.grade) if attendance.grade is not None else None,
    }, status=201)
