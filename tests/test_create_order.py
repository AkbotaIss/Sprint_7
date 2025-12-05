import requests
import pytest
import allure

from urls import CREATE_ORDER_URL
from data import BASE_ORDER_PAYLOAD


@allure.title("Тесты создания заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize(
        "case_name,payload",
        [
            (
                "один цвет BLACK",
                {**BASE_ORDER_PAYLOAD, "color": ["BLACK"]},
            ),
            (
                "один цвет GREY",
                {**BASE_ORDER_PAYLOAD, "color": ["GREY"]},
            ),
            (
                "оба цвета BLACK и GREY",
                {**BASE_ORDER_PAYLOAD, "color": ["BLACK", "GREY"]},
            ),
            (
                "без указания цвета",
                BASE_ORDER_PAYLOAD,
            ),
        ],
    )
    def test_create_order_with_different_colors(self, case_name, payload):
        with allure.step(f"Отправляем запрос на создание заказа: {case_name}"):
            response = requests.post(CREATE_ORDER_URL, json=payload)

        with allure.step("Проверяем корректный статус-код и наличие поля track"):
            assert response.status_code in [200, 201]

            body = response.json()
            assert "track" in body
            assert isinstance(body["track"], int)
            assert body["track"] > 0
