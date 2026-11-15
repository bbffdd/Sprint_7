# Sprint_7

API-тесты курьерского сервиса (Яндекс Практикум, спринт 7).

## Структура

- `conftest.py` — фикстуры (создание и удаление курьера)
- `data.py` — статика: BASE_URL, ожидаемые сообщения, цвета заказов
- `helpers.py` — генерация случайных данных
- `api.py` — методы API с `@allure.step`
- `tests/` — тестовые модули
  - `test_courier_create.py` — создание курьера (3 теста)
  - `test_courier_login.py` — авторизация курьера (5 тестов)
  - `test_create_order.py` — создание заказа (параметризация, 4 кейса)
  - `test_order_list.py` — список заказов (1 тест)
- `allure-report/` — HTML-отчёт Allure

## Запуск

```bash
pip install pytest allure-pytest requests
pytest tests/ -v
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

Всего 14 тестов, все проходят (~2 минуты).
