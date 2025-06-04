import pytest
import requests
from faker import Faker
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data import TestData
from utils.driver_factory import DriverFactory


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    # Настройка драйверов браузеров
    driver = DriverFactory.get_driver(request.param)

    # Устанавливаем позицию окна в левый верхний угол
    driver.set_window_position(0, 0)

    # Устанавливаем размер окна
    driver.set_window_size(1280, 800)

    yield driver

    # Закрытие браузера после теста
    driver.quit()

fake = Faker()

@pytest.fixture
def created_user():
    # Создание нового пользователя без авторизации и выдача его данных
    email = f"{fake.random_int()}_{fake.email()}" # Генерируем уникальный email
    password = fake.password()
    name = fake.name()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(TestData.CREATE_USER_API_URL, json=payload)

    return {
        "email": email,
        "password": password,
        "name": name,
        "response": response
    }

@pytest.fixture
def authorized_user(logged_in_user):
    # Удаление пользователя после теста

    yield logged_in_user

    headers = {"Authorization": logged_in_user["accessToken"]}
    requests.delete(TestData.DELETE_USER_API_URL, headers=headers)