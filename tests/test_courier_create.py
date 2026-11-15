import pytest
import allure

from .data import MSG_LOGIN_TAKEN, MSG_NOT_ENOUGH_CREATE
from .helpers import generate_courier_credentials
from .api import create_courier, register_new_courier_and_return_login_password, login_courier, delete_courier


@allure.epic("API тестирование курьерского сервиса ")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.story("Позитивный сценарий")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Создание курьера возвращает 201 и ok=true")
    @allure.description("Проверка: курьера можно создать, возвращается 201 и ok=true")
    def test_create_courier_returns_201_and_ok_true(self):
        login, password, first_name = generate_courier_credentials()
        payload = {"login": login, "password": password, "firstName": first_name}
        response = create_courier(payload)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        body = response.json()
        assert body["ok"] is True, f"Expected ok=true, got: {body}"
        # удаляем курьера за собой, чтобы не засорять стенд
        courier_id = login_courier(login, password).json()["id"]
        delete_courier(courier_id)

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Повторная регистрация того же логина возвращает 409")
    @allure.description("Проверка: повторная регистрация того же логина возвращает 409")
    def test_create_courier_duplicate_login_returns_409(self):
        courier = register_new_courier_and_return_login_password()
        login, password, first_name = courier
        payload = {"login": login, "password": password, "firstName": first_name}
        response = create_courier(payload)
        assert response.status_code == 409
        body = response.json()
        assert body["code"] == 409
        assert body["message"] == MSG_LOGIN_TAKEN
        # чистим за собой
        courier_id = login_courier(login, password).json()["id"]
        delete_courier(courier_id)

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Отсутствие обязательного поля возвращает 400")
    @allure.description("Проверка: при отсутствии обязательного поля возвращается 400 с сообщением об ошибке")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_returns_400(self, missing_field):
        login, password, first_name = generate_courier_credentials()
        payload = {"login": login, "password": password, "firstName": first_name}
        del payload[missing_field]
        response = create_courier(payload)
        assert response.status_code == 400
        body = response.json()
        assert body["code"] == 400
        assert body["message"] == MSG_NOT_ENOUGH_CREATE
