import requests
import pytest
import allure

from urls import CREATE_COURIER_URL
from helpers import generate_random_string
from data import (
    COURIER_CONFLICT_MESSAGE,
    COURIER_CREATE_MISSING_FIELD_MESSAGE,
)


@allure.title("Тесты создания курьера")
class TestCreateCourier:

    @allure.title("Создание курьера: успешный кейс")
    def test_create_courier_success(self):
        with allure.step("Генерируем данные курьера"):
            payload = {
                "login": generate_random_string(),
                "password": generate_random_string(),
                "firstName": generate_random_string(),
            }

        with allure.step("Отправляем POST /courier"):
            response = requests.post(CREATE_COURIER_URL, data=payload)

        with allure.step("Проверяем корректность ответа"):
            assert response.status_code == 201
            assert response.json().get("ok") is True

    @allure.title("Создание курьера: логин уже существует")
    def test_create_courier_with_existing_login_fails(self, created_courier_payload):

        with allure.step("Пробуем создать курьера повторно"):
            response = requests.post(CREATE_COURIER_URL, data=created_courier_payload)

        with allure.step("Проверяем ошибку 409 и сообщение"):
            assert response.status_code == 409
            assert response.json().get("message") == COURIER_CONFLICT_MESSAGE

    @allure.title("Создание курьера: отсутствует обязательное поле (400)")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, missing_field):

        with allure.step("Готовим payload"):
            payload = {
                "login": generate_random_string(),
                "password": generate_random_string(),
                "firstName": generate_random_string(),
            }
            payload.pop(missing_field)

        with allure.step("Отправляем запрос"):
            response = requests.post(CREATE_COURIER_URL, data=payload)

        with allure.step("Проверяем ошибку 400"):
            assert response.status_code == 400
            assert response.json().get("message") == COURIER_CREATE_MISSING_FIELD_MESSAGE
