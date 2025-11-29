import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru"


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def test_create_courier_success():

    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }


    response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)


    assert response.status_code == 201


    body = response.json()
    assert body.get("ok") is True
def test_create_courier_with_existing_login_fails():

    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }


    response_first = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)
    assert response_first.status_code == 201


    response_second = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)


    assert response_second.status_code == 409


    body = response_second.json()
    assert body.get("message") == "Этот логин уже используется. Попробуйте другой."
import pytest

@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_create_courier_missing_required_field(missing_field):

    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }


    payload.pop(missing_field)

    response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)


    assert response.status_code == 400

    body = response.json()
    assert body.get("message") == "Недостаточно данных для создания учетной записи"
