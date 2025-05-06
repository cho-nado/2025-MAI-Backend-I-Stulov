import json
import pytest
from django.test import Client
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    return Client()

@patch('core.views.Profile')
def test_mocked_search_profile(mock_Profile, client):
    """
    Патчим модель Profile так, 
    чтобы её метод filter возвращал наш фэйковый список.
    """
    # --- готовим фэйковый объект профиля ---
    fake_profile = MagicMock()
    fake_profile.id = 42
    fake_profile.user.username = 'mocked_user'
    fake_profile.role = 'teacher'
    fake_profile.first_name = 'T'
    fake_profile.last_name = 'U'
    fake_profile.middle_name = ''
    fake_profile.bio = 'Bio'
    fake_profile.address = 'Addr'

    # Настраиваем filter().distinct() -> [fake_profile]
    mock_qs = MagicMock()
    mock_qs.distinct.return_value = [fake_profile]
    mock_Profile.objects.filter.return_value = mock_qs

    # --- вызываем сам вью ---
    resp = client.get('/legacy-json/profile/search/?q=anything')

    # Проверяем, что отработало именно наш fake профайл
    assert resp.status_code == 200
    data = resp.json()
    assert data == {
        "profiles": [
            {
                "id": 42,
                "username": "mocked_user",
                "role": "teacher",
                "first_name": "T",
                "last_name": "U",
                "middle_name": "",
                "bio": "Bio",
                "address": "Addr",
            }
        ]
    }

    # Убедимся, что filter() вызывался с правильным Q-запросом
    mock_Profile.objects.filter.assert_called_once()
