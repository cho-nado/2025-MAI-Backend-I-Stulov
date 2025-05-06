import pytest
from rest_framework.test import APIClient
from tests.factories import CourseFactory, UserFactory, AttendanceFactory
from core.models import Attendance

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_api_attendance_list_empty(api_client):
    resp = api_client.get('/api/attendance/')
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.django_db
def test_api_attendance_create(api_client):
    course  = CourseFactory()
    student = UserFactory()
    payload = {
        "course": course.id,
        "student": student.id,
        "lesson_date": "2025-01-01",
        "attendance_status": "attended_paid"
    }
    resp = api_client.post('/api/attendance/', payload, format='json')
    assert resp.status_code == 201
    data = resp.json()
    assert data["student"] == student.username
    assert Attendance.objects.filter(pk=data["id"]).exists()

@pytest.mark.django_db
def test_api_attendance_retrieve_update_delete(api_client):
    att = AttendanceFactory()
    # retrieve
    r1 = api_client.get(f'/api/attendance/{att.pk}/')
    assert r1.status_code == 200
    # update
    r2 = api_client.patch(
        f'/api/attendance/{att.pk}/',
        {"attendance_status": "not_attended_paid"},
        format='json'
    )
    assert r2.status_code == 200
    assert r2.json()["attendance_status"] == "not_attended_paid"
    # delete
    r3 = api_client.delete(f'/api/attendance/{att.pk}/')
    assert r3.status_code == 204
    assert not Attendance.objects.filter(pk=att.pk).exists()
