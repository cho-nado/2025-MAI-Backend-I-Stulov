import pytest
from rest_framework.test import APIClient
from .factories import CategoryFactory
from core.models import Category

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_api_category_list_empty(api_client):
    resp = api_client.get('/api/category/')
    assert resp.status_code == 200
    assert resp.json() == []

@pytest.mark.django_db
def test_api_category_create(api_client):
    payload = {"name": "Cat1", "description": "Desc1"}
    resp = api_client.post('/api/category/', payload, format='json')
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Cat1"
    assert Category.objects.filter(pk=data["id"]).exists()

@pytest.mark.django_db
def test_api_category_retrieve_update_delete(api_client):
    cat = CategoryFactory()
    r1 = api_client.get(f'/api/category/{cat.pk}/')
    assert r1.status_code == 200

    r2 = api_client.patch(
        f'/api/category/{cat.pk}/',
        {"description": "NewDesc"},
        format='json'
    )
    assert r2.status_code == 200
    assert r2.json()["description"] == "NewDesc"

    r3 = api_client.delete(f'/api/category/{cat.pk}/')
    assert r3.status_code == 204
    assert not Category.objects.filter(pk=cat.pk).exists()
