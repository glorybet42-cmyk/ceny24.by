import pytest
from app import create_app
from models import sync_create_user
from unittest.mock import MagicMock, patch

@pytest.fixture
def app():
    """Тестовое Flask-приложение с отключённой CSRF."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost.localdomain'
    })
    return app

@pytest.fixture
def client(app):
    """Тестовый клиент."""
    return app.test_client()

@pytest.fixture
def mock_db():
    """Мокает подключение к БД и базовые операции."""
    with patch('models.get_connection') as mock:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock.return_value = mock_conn
        yield mock_cursor, mock_conn

@pytest.fixture
def create_test_user(mock_db):
    """Вспомогательная фикстура для создания пользователя."""
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = [1]
    mock_cursor.rowcount = 1

    def _create(username='testuser', password='testpass', email='test@example.com', role='Покупатель'):
        user_id, msg = sync_create_user(username, password, email, role)
        return user_id, msg
    return _create
