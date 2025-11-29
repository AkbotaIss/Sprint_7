import requests
import random
import string
import pytest

BASE_URL = "https://qa-scooter.praktikum-services.ru"


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def create_courier(login=None, password=None, first_name=None):
    """Создаёт нового курьера и возвращает его логин и пароль."""
    login = login or generate_random_string()
    password = password or generate_random_string()
    first_name = first_name or generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)
    assert response.status_code == 201  # убеждаемся, что курьер создан

    return login, password


def test_courier_can_login_successfully():
    """Курьер может залогиниться успешно, и возвращается id."""
    login, password = create_courier()

    payload = {
        "login": login,
        "password": password,
    }

    response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

    assert response.status_code == 200

    body = response.json()
    assert "id" in body
    assert isinstance(body["id"], int)
    assert body["id"] > 0


@pytest.mark.parametrize("missing_field", ["login"])
def test_login_missing_required_field_returns_error(missing_field):
    """Если нет обязательного поля (например login) — ошибка 400."""
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
    }

    payload.pop(missing_field)

    response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

    assert response.status_code == 400

    body = response.json()
    assert body.get("message") == "Недостаточно данных для входа"


@pytest.mark.parametrize("field_to_break", ["login", "password"])
def test_login_wrong_login_or_password_returns_error(field_to_break):
    """Если логин или пароль неверные — ошибка 404."""
    login, password = create_courier()

    payload = {
        "login": login,
        "password": password,
    }

    if field_to_break == "login":
        payload["login"] = generate_random_string()
    else:
        payload["password"] = generate_random_string()

    response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

    assert response.status_code == 404

    body = response.json()
    assert body.get("message") == "Учетная запись не найдена"


def test_login_nonexistent_courier_returns_error():
    """Если курьера не существует — ошибка 404."""
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
    }

    response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

    assert response.status_code == 404

    body = response.json()
    assert body.get("message") == "Учетная запись не найдена"
