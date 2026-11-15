import requests
import json
import allure

from .data import BASE_URL
from .helpers import generate_courier_credentials


@allure.step("Создание курьера")
def create_courier(payload):
    response = requests.post(f"{BASE_URL}/courier", data=payload, timeout=60)
    return response


@allure.step("Регистрация курьера и возврат логина и пароля")
def register_new_courier_and_return_login_password():
    login, password, first_name = generate_courier_credentials()
    payload = {"login": login, "password": password, "firstName": first_name}
    response = create_courier(payload)
    if response.status_code == 201:
        return [login, password, first_name]
    return []


@allure.step("Авторизация курьера")
def login_courier(login, password):
    payload = {"login": login, "password": password}
    response = requests.post(f"{BASE_URL}/courier/login", data=payload, timeout=60)
    return response


@allure.step("Авторизация курьера с неполным payload")
def login_courier_payload(payload):
    # без password стенд отвечает только через 2 минуты (504 от nginx)
    response = requests.post(f"{BASE_URL}/courier/login", data=payload, timeout=150)
    return response


@allure.step("Создание заказа")
def create_order(courier_id, color=None):
    payload = {"courier": courier_id}
    if color is not None:
        payload["color"] = color
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{BASE_URL}/orders", data=json.dumps(payload), headers=headers, timeout=60
    )
    return response


@allure.step("Удаление курьера по id")
def delete_courier(courier_id):
    response = requests.delete(f"{BASE_URL}/courier/{courier_id}", timeout=60)
    return response


@allure.step("Получение списка заказов")
def get_order_list(page=1, limit=5):
    response = requests.get(
        f"{BASE_URL}/orders", params={"page": page, "limit": limit}, timeout=60
    )
    return response
