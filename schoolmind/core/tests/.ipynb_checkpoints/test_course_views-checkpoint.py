import pytest, json
from django.test import Client
from core import views
from core.models import Category, Course

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_legacy_list_courses_empty(client):
    resp = client.get('/legacy-json/course/')
    assert resp.status_code == 200
    assert resp.json() == {"courses": []}

@pytest.mark.django_db
def test_legacy_create_and_list_course(client):
    cat = Category.objects.create(name="C1")
    payload = {"title": "T1", "description": "D1", "category_id": cat.id, "duration": "1h"}
    resp1 = client.post(
        '/legacy-json/course/create/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert resp1.status_code == 201
    d1 = resp1.json()
    assert d1["title"] == "T1"
    assert Course.objects.filter(id=d1["id"]).exists()

    resp2 = client.get('/legacy-json/course/')
    assert resp2.status_code == 200
    assert len(resp2.json()["courses"]) == 1

@pytest.mark.django_db
def test_legacy_search_course(client):
    c = Category.objects.create(name="Cat")
    Course.objects.create(title="Hello", description="X", category=c, duration="1d")
    resp = client.get('/legacy-json/course/search/?q=hell')
    assert resp.status_code == 200
    assert resp.json()["courses"][0]["title"] == "Hello"

@pytest.mark.django_db
def test_legacy_create_course_invalid_json(monkeypatch, client):
    def bad(body):
        doc = body.decode("utf-8")
        raise json.JSONDecodeError("e", doc, 0)
    monkeypatch.setattr(views, 'json', type('js', (), {
        'loads': bad, 'JSONDecodeError': json.JSONDecodeError
    }))
    resp = client.post(
        '/legacy-json/course/create/',
        data=b'nope',
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.json() == {"error": "Invalid JSON"}
