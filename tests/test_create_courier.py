import requests
import pytest
import allure

from urls import CREATE_COURIER_URL
from helpers import generate_random_string
from data import (
    COURIER_CONFLICT_MESSAGE,
    COURIER_CREATE_MISSING_FIELD_MESSAGE,
)


@pytest.fixture
def created_courier_payload():

    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    response = requests.post(CREATE_COURIER_URL, data=payload)

    assert response.status_code == 201

    return payload


@allure.title("Создание курьера: успешный кейс")
def test_create_courier_success():
    with allure.step("Генерируем данные нового курьера"):
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name,
        }

    with allure.step("Отправляем запрос POST /api/v1/courier"):
        response = requests.post(CREATE_COURIER_URL, data=payload)

    with allure.step("Проверяем статус-код и тело ответа"):
        assert response.status_code == 201

        body = response.json()
        assert body.get("ok") is True


@allure.title("Создание курьера: логин уже существует (ошибка 409)")
def test_create_courier_with_existing_login_fails(created_courier_payload):
    with allure.step("Берём уже созданного курьера из фикстуры"):
        payload = created_courier_payload

    with allure.step("Пробуем создать курьера с тем же логином ещё раз"):
        response_second = requests.post(CREATE_COURIER_URL, data=payload)

    with allure.step("Проверяем, что вернулась ошибка 409 и корректное сообщение"):
        assert response_second.status_code == 409

        body = response_second.json()
        assert body.get("message") == COURIER_CONFLICT_MESSAGE


@allure.title("Создание курьера: отсутствие обязательного поля даёт 400")
@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_create_courier_missing_required_field(missing_field):
    with allure.step(f"Готовим тело запроса без поля {missing_field}"):
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string(),
        }
        payload.pop(missing_field)

    with allure.step("Отправляем запрос POST /api/v1/courier"):
        response = requests.post(CREATE_COURIER_URL, data=payload)

    with allure.step("Проверяем, что вернулся статус-код 400 и нужное сообщение"):
        assert response.status_code == 400

        body = response.json()
        assert body.get("message") == COURIER_CREATE_MISSING_FIELD_MESSAGE
