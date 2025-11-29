import requests
import pytest

BASE_URL = "https://qa-scooter.praktikum-services.ru"


def get_base_order_payload():
    """Базовое тело заказа без учёта цвета."""
    return {
        "firstName": "Naruto",
        "lastName": "Uzumaki",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2025-12-01",
        "comment": "Saske, come back to Konoha",

    }


@pytest.mark.parametrize(
    "colors",
    [
        ["BLACK"],          # один цвет
        ["GREY"],           # один цвет
        ["BLACK", "GREY"],  # оба цвета
        None,               # цвет не указан вообще
    ]
)
def test_create_order_with_different_colors(colors):
    payload = get_base_order_payload()


    if colors is not None:
        payload["color"] = colors


    response = requests.post(f"{BASE_URL}/api/v1/orders", json=payload)


    assert response.status_code in [200, 201]

    body = response.json()


    assert "track" in body
    assert isinstance(body["track"], int)
    assert body["track"] > 0
