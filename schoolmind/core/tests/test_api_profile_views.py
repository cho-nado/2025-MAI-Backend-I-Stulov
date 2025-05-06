import pytest
from rest_framework.test import APIClient
from .factories import ProfileFactory, UserFactory
from core.models import Profile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_api_profile_list_empty(api_client):
    resp = api_client.get('/api/profile/')
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.django_db
def test_api_profile_create(api_client):
    user = UserFactory()
    payload = {
        "user": user.id,
        "role": "student",
        "first_name": "Jane",
        "last_name": "Doe",
        "middle_name": "",
        "bio": "",
        "address": ""
    }
    resp = api_client.post('/api/profile/', payload, format='json')
    assert resp.status_code == 201
    data = resp.json()
    assert data["role"] == "student"
    assert Profile.objects.filter(pk=data["id"]).exists()

@pytest.mark.django_db
def test_api_profile_retrieve_update_delete(api_client):
    profile = ProfileFactory()
    r1 = api_client.get(f'/api/profile/{profile.pk}/')
    assert r1.status_code == 200

    r2 = api_client.patch(
        f'/api/profile/{profile.pk}/',
        {"first_name": "X"},
        format='json'
    )
    assert r2.status_code == 200
    assert r2.json()["first_name"] == "X"

    r3 = api_client.delete(f'/api/profile/{profile.pk}/')
    assert r3.status_code == 204
    assert not Profile.objects.filter(pk=profile.pk).exists()
