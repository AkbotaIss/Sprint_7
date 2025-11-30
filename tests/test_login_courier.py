import requests
import pytest
import allure

from urls import LOGIN_COURIER_URL, CREATE_COURIER_URL
from helpers import generate_random_string
from data import LOGIN_MISSING_FIELD_MESSAGE, ACCOUNT_NOT_FOUND_MESSAGE


def create_courier(login=None, password=None, first_name=None):

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


@allure.title("Курьер может авторизоваться и получить id")
def test_courier_can_login_successfully():
    login, password = create_courier()

    payload = {
        "login": login,
        "password": password,
    }

    with allure.step("Отправляем запрос на логин курьера"):
        response = requests.post(LOGIN_COURIER_URL, data=payload)

    assert response.status_code == 200

    body = response.json()
    assert "id" in body
    assert isinstance(body["id"], int)
    assert body["id"] > 0


@allure.title("Авторизация без обязательного поля login возвращает ошибку 400")
@pytest.mark.parametrize("missing_field", ["login"])
def test_login_missing_required_field_returns_error(missing_field):
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
    }

    payload.pop(missing_field)

    with allure.step("Пробуем авторизоваться без обязательного поля"):
        response = requests.post(LOGIN_COURIER_URL, data=payload)

    assert response.status_code == 400

    body = response.json()
    assert body.get("message") == LOGIN_MISSING_FIELD_MESSAGE


@allure.title("Авторизация с неверным логином возвращает 404 и сообщение об ошибке")
def test_login_wrong_login_returns_error():
    login, password = create_courier()

    payload = {
        "login": generate_random_string(),  # ломаем логин
        "password": password,
    }

    with allure.step("Отправляем запрос с неверным логином"):
        response = requests.post(LOGIN_COURIER_URL, data=payload)

    assert response.status_code == 404

    body = response.json()
    assert body.get("message") == ACCOUNT_NOT_FOUND_MESSAGE


@allure.title("Авторизация с неверным паролем возвращает 404 и сообщение об ошибке")
def test_login_wrong_password_returns_error():
    login, _ = create_courier()

    payload = {
        "login": login,
        "password": generate_random_string(),  # ломаем пароль
    }

    with allure.step("Отправляем запрос с неверным паролем"):
        response = requests.post(LOGIN_COURIER_URL, data=payload)

    assert response.status_code == 404

    body = response.json()
    assert body.get("message") == ACCOUNT_NOT_FOUND_MESSAGE


@allure.title("Авторизация несуществующего курьера возвращает 404 и сообщение об ошибке")
def test_login_nonexistent_courier_returns_error():
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
    }

    with allure.step("Пробуем авторизоваться под несуществующим курьером"):
        response = requests.post(LOGIN_COURIER_URL, data=payload)

    assert response.status_code == 404

    body = response.json()
    assert body.get("message") == ACCOUNT_NOT_FOUND_MESSAGE
