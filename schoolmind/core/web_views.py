from django.http import HttpResponse, JsonResponse

def profile_web_view(request):
    return HttpResponse("<h1>Профили</h1>")

def category_web_view(request):
    return HttpResponse("<h1>Категории</h1>")

def course_web_view(request):
    return HttpResponse("<h1>Курсы</h1>")

def courseschedule_web_view(request):
    return HttpResponse("<h1>Расписание курсов</h1>")

def attendance_web_view(request):
    return HttpResponse("<h1>Посещаемость</h1>")

def health_check(request):
    """
    Простая «живая» проверка — возвращает 200, если приложение запущено.
    """
    return JsonResponse({"status": "ok"})
