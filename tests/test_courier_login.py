import allure

from data import MSG_NOT_FOUND, MSG_NOT_ENOUGH_LOGIN, MSG_GATEWAY_TIMEOUT
from api import login_courier, login_courier_payload


@allure.epic("API тестирование курьерского сервиса ")
@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.story("Позитивный сценарий")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Успешная авторизация возвращает 200 и id")
    @allure.description("Проверка: курьер может авторизоваться, возвращается 200 и id")
    def test_login_success(self, courier):
        login, password, _ = courier
        response = login_courier(login, password)
        assert response.status_code == 200
        body = response.json()
        assert "id" in body

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Неправильный пароль возвращает 404")
    @allure.description("Проверка: неправильный пароль возвращает 404 и сообщение 'Учетная запись не найдена'")
    def test_login_wrong_password_returns_404(self, courier):
        login, _password, _ = courier
        response = login_courier(login, "wrongpassword")
        assert response.status_code == 404
        body = response.json()
        assert body["code"] == 404
        # стенд отвечает "Учетная запись не найдена" и по неверному паролю
        assert body["message"] == MSG_NOT_FOUND

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Авторизация под несуществующим пользователем возвращает 404")
    @allure.description("Проверка: авторизация под несуществующим пользователем возвращает 404")
    def test_login_nonexistent_user_returns_404(self):
        response = login_courier("nonexistent_user_xyz", "anypassword123")
        assert response.status_code == 404
        body = response.json()
        assert body["code"] == 404
        assert body["message"] == MSG_NOT_FOUND

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Отсутствие логина при авторизации возвращает 400")
    @allure.description("Проверка: без поля login возвращается 400 и сообщение о недостающих данных")
    def test_login_missing_login_returns_400(self, courier_credentials):
        _login, password, _first_name = courier_credentials
        payload = {"password": password}
        response = login_courier_payload(payload)
        assert response.status_code == 400
        body = response.json()
        assert body["code"] == 400
        assert body["message"] == MSG_NOT_ENOUGH_LOGIN

    @allure.story("Негативный сценарий")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Отсутствие пароля при авторизации возвращает 504")
    @allure.description("Проверка: без поля password стенд не отвечает и nginx отдаёт 504 Gateway Time-out")
    def test_login_missing_password_returns_504(self, courier_credentials):
        login, _password, _first_name = courier_credentials
        payload = {"login": login}
        response = login_courier_payload(payload)
        assert response.status_code == 504
        assert MSG_GATEWAY_TIMEOUT in response.text
