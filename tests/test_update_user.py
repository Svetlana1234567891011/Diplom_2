import pytest
import allure
from utils.special_request import UserRequests, fake


@allure.feature('Проверка обновления данных юзера')
class TestUserDataUpdate:

    @allure.title('Изменение данных пользователя с авторизацией, например, имени')
    def test_update_auth(self, create_payload, generate_random_string_10):
        new_user = UserRequests().post_create_user(data=create_payload)
        payload = {

            "name": generate_random_string_10
        }
        access_token = new_user.get('accessToken')
        patched_user = UserRequests().patch_user(data=payload, token=access_token)
        rewrite_user = UserRequests().get_user_data(token=access_token)
        assert (patched_user['text']['user']['name'] == rewrite_user['text']['user']['name'])


    @allure.title('Изменение имейл пользователя с авторизацией')
    def test_update_email_auth(self, create_payload):
        new_user = UserRequests().post_create_user(data=create_payload)
        payload = {

            "email": fake.email()
        }

        access_token = new_user.get('accessToken')
        patched_user = UserRequests().patch_user(data=payload, token=access_token)
        rewrite_user = UserRequests().get_user_data(token=access_token)
        assert (patched_user['text']['user']['email'] == rewrite_user['text']['user']['email'])



    @allure.title('Данные пользователя - невозможно получить или изменить без авторизации')
    def test_update_no_auth(self, create_payload, generate_random_string_10):
        new_user = UserRequests().post_create_user(data=create_payload)
        payload_new = {

            "password": generate_random_string_10,

        }

        refreshment = new_user['refreshToken']
        logout_user = UserRequests().post_logout(token=refreshment)  # выход из системы
        patched_user = UserRequests().patch_user(data=payload_new, token=refreshment)
        assert (patched_user['text']['message'] == "You should be authorised")




