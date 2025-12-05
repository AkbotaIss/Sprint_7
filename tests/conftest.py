import pytest
import requests

from helpers import generate_random_string
from urls import CREATE_COURIER_URL


@pytest.fixture
def created_courier_payload():
    """Создаёт курьера и возвращает payload, которым он был создан."""
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    response = requests.post(CREATE_COURIER_URL, data=payload)
    assert response.status_code == 201  # проверяем, что курьер создан

    return payload
