import pytest
import allure

from .data import ORDER_COLORS
from .api import register_new_courier_and_return_login_password, login_courier, create_order, delete_courier


@allure.epic("API тестирование курьерского сервиса ")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Параметризация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание заказа с цветом {description} возвращает 201 и track")
    @allure.description("Создание заказа с различными наборами цветов")
    @pytest.mark.parametrize("color,description", ORDER_COLORS)
    def test_create_order_returns_201_with_track(self, color, description):
        courier = register_new_courier_and_return_login_password()
        login, password, _ = courier
        login_response = login_courier(login, password)
        courier_id = login_response.json()["id"]
        response = create_order(courier_id, color=color)
        assert response.status_code == 201
        body = response.json()
        assert "track" in body
        assert isinstance(body["track"], int)
        # курьер после теста не нужен
        delete_courier(courier_id)
