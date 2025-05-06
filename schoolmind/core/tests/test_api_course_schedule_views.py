import pytest
from rest_framework.test import APIClient
from .factories import CourseFactory, ProfileFactory, CourseScheduleFactory
from core.models import CourseSchedule

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_api_courseschedule_list_empty(api_client):
    # при отсутствии записей возвращается пустой список
    resp = api_client.get('/api/courseschedule/')
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.django_db
def test_api_courseschedule_create(api_client):
    # создаём зависимости
    course = CourseFactory()
    instructor = ProfileFactory()
    payload = {
        "course": course.id,
        "instructor": instructor.id,
        "day_of_week": "Tuesday",
        "start_time": "09:00:00",
        "end_time": "10:30:00"
    }
    resp = api_client.post('/api/courseschedule/', payload, format='json')
    assert resp.status_code == 201

    data = resp.json()
    # DRF по умолчанию сериализует FK как их ID
    assert data["course"] == course.id
    assert data["instructor"] == instructor.id
    assert data["day_of_week"] == "Tuesday"
    assert data["start_time"] == "09:00:00"
    assert data["end_time"] == "10:30:00"
    # запись действительно создана в базе
    assert CourseSchedule.objects.filter(id=data["id"]).exists()

@pytest.mark.django_db
def test_api_courseschedule_retrieve_update_delete(api_client):
    # фабрикой создаём готовый объект расписания
    schedule = CourseScheduleFactory()

    # — RETRIEVE
    r1 = api_client.get(f'/api/courseschedule/{schedule.pk}/')
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["id"] == schedule.id

    # — UPDATE (PATCH одного поля)
    r2 = api_client.patch(
        f'/api/courseschedule/{schedule.pk}/',
        {"day_of_week": "Wednesday"},
        format='json'
    )
    assert r2.status_code == 200
    assert r2.json()["day_of_week"] == "Wednesday"

    # — DELETE
    r3 = api_client.delete(f'/api/courseschedule/{schedule.pk}/')
    assert r3.status_code == 204
    # объекта больше нет
    assert not CourseSchedule.objects.filter(pk=schedule.pk).exists()
