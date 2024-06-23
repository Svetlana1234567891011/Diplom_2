import pytest
from conftest import create_payload, fake
import allure




@allure.feature('Проверка авторизации пользователя, успешный запрос возвращает id')
class TestLogin:
    @allure.title('Пользователь может авторизоваться с существующей учетной записью')
    def test_user_can_login(self, create_payload, courier_with_payload):
        response_login = courier_with_payload.post_login_user(data=courier_with_payload.payload,
                                                              token=courier_with_payload.access_token)  # Аутентификация
        assert response_login["success"] == True


    @allure.title('Пользователь с отсутствующим паролем не может залогиниться')
    def test_user_cannot_login(self, courier_with_payload):
        courier_with_payload.payload['password'] = None  # Убираем пароль
        response = courier_with_payload.post_login_user(data=courier_with_payload.payload,
                                                        token=courier_with_payload.access_token)

        assert response['message'] == 'email or password are incorrect'


    @allure.title('Пользователь с отсутствующим логином не может залогиниться')
    def test_user_cannot_name(self, courier_with_payload):
        courier_with_payload.payload['email'] = None  # Убираем мейл
        response = courier_with_payload.post_login_user(data=courier_with_payload.payload,
                                                        token=courier_with_payload.access_token)

        assert response['message'] == 'email or password are incorrect'
