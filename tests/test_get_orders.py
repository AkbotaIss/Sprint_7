import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru"


def test_get_orders_returns_list():
    response = requests.get(f"{BASE_URL}/api/v1/orders")


    assert response.status_code == 200

    body = response.json()


    assert "orders" in body


    assert isinstance(body["orders"], list)
