import pytest, json
from django.test import Client
from django.contrib.auth.models import User
from core import views
from core.models import Category, Course, Profile, CourseSchedule

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_legacy_list_courseschedule_empty(client):
    resp = client.get('/legacy-json/courseschedule/')
    assert resp.status_code == 200
    assert resp.json() == {"schedules": []}

@pytest.mark.django_db
def test_legacy_create_and_list_courseschedule(client):
    cat = Category.objects.create(name="C")
    course = Course.objects.create(title="T", description="D", category=cat, duration="1h")
    user = User.objects.create_user("u", "", "p")
    instr = Profile.objects.create(user=user, role="teacher", first_name="F", last_name="L")
    payload = {
        "course_id": course.id,
        "instructor_id": instr.id,
        "day_of_week": "Mon",
        "start_time": "09:00:00",
        "end_time":   "10:00:00"
    }
    resp1 = client.post(
        '/legacy-json/courseschedule/create/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert resp1.status_code == 201
    ds = resp1.json()
    assert ds["course"] == "T"
    assert CourseSchedule.objects.filter(id=ds["id"]).exists()

    resp2 = client.get('/legacy-json/courseschedule/')
    assert resp2.status_code == 200
    assert len(resp2.json()["schedules"]) == 1

@pytest.mark.django_db
def test_legacy_create_courseschedule_invalid_json(monkeypatch, client):
    def bad(body):
        doc = body.decode("utf-8")
        raise json.JSONDecodeError("e", doc, 0)
    monkeypatch.setattr(views, 'json', type('js', (), {
        'loads': bad, 'JSONDecodeError': json.JSONDecodeError
    }))
    resp = client.post(
        '/legacy-json/courseschedule/create/',
        data=b'xxx',
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.json() == {"error": "Invalid JSON"}
