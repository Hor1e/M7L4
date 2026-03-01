import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users, user_choice

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."



def test_alreadyexistinglogin_bysanya(setup_database, connection):
    """Тест добавления пользователя с существующим логином."""
    login = "test"
    add_user(login, "testuser@example.com", "password123")
    add_user(login, "seconduser@example.com", "password456")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?;", (login,))
    users = cursor.fetchall()
    assert len(users) == 1, "Логин не должен повторяться в дб"

def test_wrongPassword_bysanya(setup_database,connection):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('testuser', 'testuser@example.com', 'password123')
    result = add_user('testuser', 'testuser@example.com', 'wrongpassword')
    assert not result, 'неправильный пароль'




#Добавил 3 теста снизу, рома
def test_auth_wrong_password():
    #Попытка с неверным паролем
    authenticate_user("hor1e", 123)
    assert "Неверный логин или пароль."

def test_auth_sucess():
    #Тест на успешную автризацию
    authenticate_user("hor1e", 1234)
    assert "Авторизация успешна."

def test_auth_user_not_exist():
    #Что произойдет, если с неуществуюищим логином попытаться
    authenticate_user("asasas", 1234)
    assert "Введите пароль: "

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""
