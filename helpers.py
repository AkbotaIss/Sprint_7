import random
import string
import requests
import allure

from urls import CREATE_COURIER_URL


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def create_courier(login=None, password=None, first_name=None):
    """Утилита для создания курьера через API (используется в тестах авторизации)."""

    login = login or generate_random_string()
    password = password or generate_random_string()
    first_name = first_name or generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    with allure.step("Создаём курьера через API"):
        response = requests.post(CREATE_COURIER_URL, data=payload)
        assert response.status_code == 201

    return login, password
