from django.db import models
from django.contrib.auth.models import User

# =========================
# 1. Profile
# =========================
class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('curator', 'Curator'),
        ('parent', 'Parent'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Новые обязательные поля для имени и фамилии, отчество опционально
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    middle_name = models.CharField(max_length=50, blank=True, null=True)  # остаётся необязательным

    
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
    def save(self, *args, **kwargs):
        # Если у профиля уже установлен связанный пользователь, обновляем его имя и фамилию
        if self.user:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()
        super().save(*args, **kwargs)


# =========================
# 2. Category
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories'
    )
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)
    
    def __str__(self):
        return self.name


# =========================
# 3. Course
# =========================
class Course(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    DELIVERY_MODES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructors = models.ManyToManyField(Profile, blank=True, related_name='courses_teaching')
    delivery_mode = models.CharField(max_length=10, choices=DELIVERY_MODES, default='online')
    location = models.CharField(max_length=255, blank=True, help_text="Physical address if offline")
    duration = models.CharField(max_length=50, help_text="E.g., '6 months', '1 year'")
    num_lessons = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    # Ссылка на материалы курса, например, презентация на Google Drive
    presentation = models.URLField(blank=True, null=True, help_text="Link to course presentation/materials")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Запись студентов (пользователи) на курс
    students = models.ManyToManyField(User, blank=True, related_name='courses_enrolled')
    
    def __str__(self):
        return self.title


# =========================
# 4. CourseSchedule
# =========================
class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    instructor = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule_entries'
    )
    day_of_week = models.CharField(max_length=10, help_text="E.g., 'Tuesday', 'Thursday'")
    start_time = models.TimeField()
    end_time = models.TimeField()
    replacement = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='replacement_schedule_entries'
    )
    
    def __str__(self):
        return f"{self.course.title} - {self.day_of_week} {self.start_time}-{self.end_time}"


# =========================
# 5. Attendance
# =========================
class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
         ('attended_paid', 'Attended and Paid'),
         ('attended_not_paid', 'Attended but Not Paid'),
         ('not_attended_paid', 'Not Attended but Paid'),
         ('not_attended_not_paid', 'Not Attended and Not Paid'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    lesson_date = models.DateField()
    attendance_status = models.CharField(max_length=30, choices=ATTENDANCE_CHOICES)
    absence_reason = models.TextField(blank=True, null=True, help_text="Reason for absence, if applicable")
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ('course', 'student', 'lesson_date')
    
    def __str__(self):
        return f"{self.course.title} - {self.student.username} on {self.lesson_date}"
