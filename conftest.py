import pytest

from helpers import generate_courier_credentials
from api import create_courier, login_courier, delete_courier


@pytest.fixture
def courier_credentials():
    """Сгенерированные креды курьера. После теста удаляем курьера, если он был создан."""
    credentials = generate_courier_credentials()
    yield credentials
    login, password, _first_name = credentials
    response = login_courier(login, password)
    if response.status_code == 200:
        delete_courier(response.json()["id"])


@pytest.fixture
def courier(courier_credentials):
    """Готовый созданный курьер; удаление — в teardown, независимо от исхода теста."""
    login, password, first_name = courier_credentials
    payload = {"login": login, "password": password, "firstName": first_name}
    create_courier(payload)
    yield [login, password, first_name]
