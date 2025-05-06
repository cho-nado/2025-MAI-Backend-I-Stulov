import pytest, json
from django.test import Client
from core import views
from core.models import Category

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_legacy_list_categories_empty(client):
    resp = client.get('/legacy-json/category/')
    assert resp.status_code == 200
    assert resp.json() == {"categories": []}

@pytest.mark.django_db
def test_legacy_create_and_list_category(client):
    payload = {"name": "Cat1", "description": "Desc"}
    resp1 = client.post(
        '/legacy-json/category/create/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert resp1.status_code == 201
    data1 = resp1.json()
    assert data1["name"] == "Cat1"
    assert Category.objects.filter(id=data1["id"]).exists()

    resp2 = client.get('/legacy-json/category/')
    assert resp2.status_code == 200
    assert len(resp2.json()["categories"]) == 1

@pytest.mark.django_db
def test_legacy_search_category(client):
    Category.objects.create(name="Foo", description="Bar")
    resp = client.get('/legacy-json/category/search/?q=foo')
    assert resp.status_code == 200
    assert resp.json()["categories"][0]["name"] == "Foo"

@pytest.mark.django_db
def test_legacy_create_category_invalid_json(monkeypatch, client):
    def bad(body):
        doc = body.decode("utf-8")
        raise json.JSONDecodeError("e", doc, 0)
    monkeypatch.setattr(views, 'json', type('js', (), {
        'loads': bad, 'JSONDecodeError': json.JSONDecodeError
    }))
    resp = client.post(
        '/legacy-json/category/create/',
        data=b'xxx',
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.json() == {"error": "Invalid JSON"}
