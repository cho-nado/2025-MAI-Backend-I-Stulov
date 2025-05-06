import pytest
from rest_framework.test import APIClient
from .factories import CourseFactory, CategoryFactory
from core.models import Course

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_api_course_list_empty(api_client):
    resp = api_client.get('/api/course/')
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.django_db
def test_api_course_create(api_client):
    cat = CategoryFactory()
    payload = {
        "title": "Course1",
        "description": "Desc1",
        "category": cat.id,
        "duration": "10h"
    }
    resp = api_client.post('/api/course/', payload, format='json')
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Course1"
    assert Course.objects.filter(pk=data["id"]).exists()

@pytest.mark.django_db
def test_api_course_retrieve_update_delete(api_client):
    course = CourseFactory()
    r1 = api_client.get(f'/api/course/{course.pk}/')
    assert r1.status_code == 200

    r2 = api_client.patch(
        f'/api/course/{course.pk}/',
        {"description": "Updated"},
        format='json'
    )
    assert r2.status_code == 200
    assert r2.json()["description"] == "Updated"

    r3 = api_client.delete(f'/api/course/{course.pk}/')
    assert r3.status_code == 204
    assert not Course.objects.filter(pk=course.pk).exists()
