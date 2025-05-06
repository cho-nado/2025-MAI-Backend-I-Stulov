import pytest, json
from django.test import Client
from django.contrib.auth.models import User
from core import views
from core.models import Category, Course, Attendance

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_legacy_list_attendance_empty(client):
    resp = client.get('/legacy-json/attendance/')
    assert resp.status_code == 200
    assert resp.json() == {"attendances": []}

@pytest.mark.django_db
def test_legacy_create_and_list_attendance(client):
    cat = Category.objects.create(name="C")
    course = Course.objects.create(title="T", description="D", category=cat, duration="1h")
    student = User.objects.create_user("u", "", "p")
    payload = {
        "course_id": course.id,
        "student_id": student.id,
        "lesson_date": "2025-01-01",
        "attendance_status": "attended_paid"
    }
    resp1 = client.post(
        '/legacy-json/attendance/create/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert resp1.status_code == 201
    da = resp1.json()
    assert da["student"] == "u"
    assert Attendance.objects.filter(id=da["id"]).exists()

    resp2 = client.get('/legacy-json/attendance/')
    assert resp2.status_code == 200
    assert len(resp2.json()["attendances"]) == 1

@pytest.mark.django_db
def test_legacy_create_attendance_invalid_json(monkeypatch, client):
    def bad(body):
        doc = body.decode("utf-8")
        raise json.JSONDecodeError("e", doc, 0)
    monkeypatch.setattr(views, 'json', type('js', (), {
        'loads': bad, 'JSONDecodeError': json.JSONDecodeError
    }))
    resp = client.post(
        '/legacy-json/attendance/create/',
        data=b'xxx',
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.json() == {"error": "Invalid JSON"}
