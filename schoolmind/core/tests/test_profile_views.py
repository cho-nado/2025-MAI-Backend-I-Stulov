import pytest, json
from django.test import Client
from django.contrib.auth.models import User
from core import views
from core.models import Profile

@pytest.fixture
def client():
    return Client()

def fake_loads(body):
    # приводим к str, иначе JSONDecodeError падает из-за bytes
    doc = body.decode("utf-8")
    raise json.JSONDecodeError("msg", doc, 0)

@pytest.mark.django_db
def test_legacy_list_profiles_empty(client):
    resp = client.get('/legacy-json/profile/')
    assert resp.status_code == 200
    assert resp.json() == {"profiles": []}

@pytest.mark.django_db
def test_legacy_create_and_list_profile(client):
    payload = {
        "username": "u1",
        "password": "p1",
        "role": "student",
        "first_name": "A",
        "last_name": "B",
    }
    resp1 = client.post(
        '/legacy-json/profile/create/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert resp1.status_code == 201
    data1 = resp1.json()
    assert data1["username"] == "u1"
    assert Profile.objects.filter(id=data1["id"]).exists()

    resp2 = client.get('/legacy-json/profile/')
    assert resp2.status_code == 200
    assert len(resp2.json()["profiles"]) == 1

@pytest.mark.django_db
def test_legacy_search_profile(client):
    u = User.objects.create_user('john', '', 'pw')
    Profile.objects.create(user=u, role="teacher", first_name="John", last_name="Smith")
    resp = client.get('/legacy-json/profile/search/?q=john')
    assert resp.status_code == 200
    assert resp.json()["profiles"][0]["username"] == "john"

@pytest.mark.django_db
def test_legacy_create_profile_invalid_json(monkeypatch, client):
    monkeypatch.setattr(views, 'json', type('js', (), {
        'loads': fake_loads,
        'JSONDecodeError': json.JSONDecodeError
    }))
    resp = client.post(
        '/legacy-json/profile/create/',
        data=b'not a json',
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert resp.json() == {"error": "Invalid JSON"}
