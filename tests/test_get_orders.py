import requests
import allure

from urls import ORDERS_URL


@allure.title("Тесты получения списка заказов")
class TestGetOrders:

    @allure.title("Получение списка заказов")
    def test_get_orders_returns_list(self):
        with allure.step("Отправляем запрос на получение списка заказов"):
            response = requests.get(ORDERS_URL)

        with allure.step("Проверяем код ответа и структуру данных"):
            assert response.status_code == 200
            body = response.json()
            assert "orders" in body
            assert isinstance(body["orders"], list)
