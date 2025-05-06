import pytest
from rest_framework.test import APIClient
from .factories import CourseFactory
from core.models import CourseSchedule

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_api_courseschedule_list_empty(api_client):
    resp = api_client.get('/api/courseschedule/')
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.django_db
def test_api_courseschedule_create(api_client):
    schedule = CourseFactory()  # у тебя, видимо, курсы и расписания разделены
    # для примера пусть будет так, дальше аналогично

@pytest.mark.django_db
def test_api_courseschedule_retrieve_update_delete(api_client):
    # аналогично остальным, на модели CourseSchedule
    pass
