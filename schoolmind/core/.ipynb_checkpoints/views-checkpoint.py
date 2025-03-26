from django.shortcuts import render

from django.http import JsonResponse

def profile_view(request):
    if request.method == 'GET':
        return JsonResponse({"username": "john_doe", "role": "student"})
    elif request.method == 'POST':
        return JsonResponse({"status": "profile updated"})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def courses_list_view(request):
    if request.method == 'GET':
        return JsonResponse({
            "courses": [
                {"id": 1, "title": "Python Basics"},
                {"id": 2, "title": "Math for Beginners"},
            ]
        })
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def categories_list_view(request):
    if request.method == 'GET':
        return JsonResponse({
            "categories": [
                {"id": 1, "name": "Programming"},
                {"id": 2, "name": "Math"},
                {"id": 3, "name": "English"}
            ]
        })
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


