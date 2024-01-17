import unittest
from tkinter import Entry, Message, Tk, Label, Button
import tkinter.font as tkFont
from unittest.mock import patch
from tkinter import Tk
from unittest.mock import patch, MagicMock
from main import validate_data, is_valid_length, check_existing_username, check_number, check_unique_digits, create_user_table, register_user
from main import login_user, game  # Добавьте эти импорты

class TestValidateData(unittest.TestCase):
    def test_valid_data(self):
        self.assertTrue(validate_data("username123"))

    def test_invalid_data(self):
        self.assertFalse(validate_data("user name"))
        self.assertFalse(validate_data("user@name"))

class TestIsValidLength(unittest.TestCase):
    def test_valid_length(self):
        self.assertTrue(is_valid_length("abcde"))

    def test_invalid_length(self):
        self.assertFalse(is_valid_length("abc"))
        self.assertFalse(is_valid_length("12"))

class TestCheckExistingUsername(unittest.TestCase):
    def test_existing_username(self):
        self.assertTrue(check_existing_username("existing_user"))

    def test_non_existing_username(self):
        self.assertFalse(check_existing_username("non_existing_user"))

class TestRegistrationFunctions(unittest.TestCase):

    def test_check_existing_username(self):
        window_login = Tk()
        window_login.title("Авторизация")
        window_login.resizable(False, False)

        create_user_table()
        self.assertFalse(check_existing_username("NonExistingUser"))
        register_user(window_login)
        self.assertFalse(check_existing_username("ValidUser"))

        window_login.destroy()


class TestGameFunctions(unittest.TestCase):
    UserNumber = None
    msg = None

    def setUp(self):
        # Создаем экземпляры переменных UserNumber и msg перед каждым тестом
        self.UserNumber = Entry()
        self.msg = Message()

    def test_check_number(self):
        # Тест проверки ввода числа (должно быть в диапазоне от 1023 до 9876)
        self.assertTrue(check_number("1234", self.UserNumber, self.msg))
        self.assertFalse(check_number("100", self.UserNumber, self.msg))
        self.assertFalse(check_number("98765", self.UserNumber, self.msg))

    def test_check_unique_digits(self):
        # Тест проверки уникальности цифр в числе
        self.assertTrue(check_unique_digits(1234, self.UserNumber, self.msg))
        self.assertFalse(check_unique_digits(1122, self.UserNumber, self.msg))
        self.assertTrue(check_unique_digits(9876, self.UserNumber, self.msg))

if __name__ == '__main__':
    unittest.main()