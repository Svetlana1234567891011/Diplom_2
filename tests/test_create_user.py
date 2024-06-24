import pytest
import allure
from utils.special_request import UserRequests, fake




@allure.feature('Создание Пользователя')
class TestCreateCourier:

    @allure.title('Можно создать Пользователя со случайным логином')
    def test_all_the_fields_are_required(self, generate_random_string_10):
        payload = {
            "login": generate_random_string_10,
            "password": generate_random_string_10,
            "firstName": generate_random_string_10
        }

        response = UserRequests().post_create_user(data=payload)
        assert response['ok']

    @allure.title('Нельзя создать двух Пользователей с одинаковыми логинами')
    def test_cant_create_courier_dupes(self, courier_with_payload):
        response_dupe = courier_with_payload.post_create_user(
            data=courier_with_payload.payload)  # отправляем данные повторно
        assert response_dupe["message"] == "User already exists"

    @pytest.mark.parametrize('login_v, password_v, email_v',
                             [
                                 (None, fake.password(), fake.email()),
                                 (fake.name(), fake.password(), None),
                                 (fake.name(), None, fake.email()),

                             ])
    @allure.title('Для создания Пользователя необходимо задать все обязательные поля (логин, пароль)')
    def test_all_the_fields_are_required(self, login_v, password_v, email_v):
        payload = {
            "name": login_v,
            "password": password_v,
            "email": email_v
        }

        response = UserRequests().post_create_user(data=payload)
        assert response["message"] == "Email, password and name are required fields"

    @allure.title('Нельзя создать пользователя, не заполнив одно из обязательных полей - например, имейл')
    def test_email_field_are_required(self, generate_random_string_10):
        payload = {
            "login": generate_random_string_10,
            "password": generate_random_string_10,
            "email": None
        }

        response = UserRequests().post_create_user(data=payload)
        assert response["message"] == "Email, password and name are required fields"
