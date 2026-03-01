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

def test_add_existing_user(setup_database):
    """Тест добавления пользователя с существующим логином."""
    add_user('duplicate_user', 'dup@example.com', 'pass123')
    result = add_user('duplicate_user', 'dup2@example.com', 'pass456')
    assert result is False, "Добавление пользователя с существующим логином должно вернуть False."

def test_authenticate_user_success(setup_database):
    """Тест успешной аутентификации пользователя."""
    add_user('auth_user', 'auth@example.com', 'securepass')
    result = authenticate_user('auth_user', 'securepass')
    assert result is True, "Аутентификация с верными данными должна вернуть True."

def test_authenticate_nonexistent_user(setup_database):
    """Тест аутентификации несуществующего пользователя."""
    result = authenticate_user('ghost_user', 'somepassword')
    assert result is False, "Аутентификация несуществующего пользователя должна вернуть False."

def test_authenticate_wrong_password(setup_database):
    """Тест аутентификации пользователя с неправильным паролем."""
    add_user('wrong_pass_user', 'wrong@example.com', 'correctpass')
    result = authenticate_user('wrong_pass_user', 'wrongpass')
    assert result is False, "Аутентификация с неверным паролем должна вернуть False."

def test_display_users(setup_database, capsys):
    """Тест отображения списка пользователей."""
    add_user('display_user', 'display@example.com', 'displaypass')
    display_users()
    captured = capsys.readouterr()
    assert 'display_user' in captured.out, "Логин пользователя должен отображаться в списке."
    assert 'display@example.com' in captured.out, "Email пользователя должен отображаться в списке."