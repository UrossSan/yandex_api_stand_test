import sender_stand_request
import data
import pytest

def test_create_user():
    test_cases = [
        ("Aa", True, 201),  # Успешное создание пользователя. Параметр firstName состоит из 2 символов
        ("Ааааааааааааааа", True, 201),  # Успешное создание пользователя. Параметр firstName состоит из 15 символов
        ("A", False, 400),  # Ошибка. Параметр firstName состоит из 1 символа
        ("Аааааааааааааааa", False, 400),  # Ошибка. Параметр firstName состоит из 16 символов
        ("QWErty", True, 201),  # Успешное создание пользователя. Параметр firstName состоит из английских букв
        ("Мария", True, 201),  # Успешное создание пользователя. Параметр firstName состоит из русских букв
        ("Человек и КО", False, 400),  # Ошибка. Параметр firstName состоит из слов с пробелами
        ("\"№%@\","), False, 400),  # Ошибка. Параметр firstName состоит из строки спецсимволов
        ("123", False, 400),  # Ошибка. Параметр firstName состоит из строки цифр
        (None, False, 400),  # Ошибка. В запросе нет параметра firstName
        ("", False, 400),  # Ошибка. Параметр состоит из пустой строки
        (12, False, 400)  # Ошибка. Тип параметра firstName: число
    ]

    for name, success, status_code in test_cases:
        if success:
            assert_create_user_success(name, status_code)
        else:
            assert_create_user_error(name, status_code)


def assert_create_user_success(name, status_code):
    user_body = data.user_body.copy()
    user_body["firstName"] = name
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == status_code
    if status_code == 201:
        assert response.json()["authToken"] != ""


def assert_create_user_error(name, status_code):
    user_body = data.user_body.copy()
    user_body["firstName"] = name
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == status_code
    assert response.json()["code"] == status_code
    if status_code == 400:
        assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                             "Имя может содержать только русские или латинские буквы, " \
                                             "Длина должна быть не менее 2 и не более 15 символов"