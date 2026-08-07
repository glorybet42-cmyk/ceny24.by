def test_register_success(client, mock_db):
    """Успешная регистрация нового пользователя."""
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.side_effect = [
        None,  # username свободен
        None,  # email свободен
        [1]    # ID нового пользователя
    ]
    mock_conn.commit.return_value = None

    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'secure123',
        'confirm_password': 'secure123',
        'role': 'Покупатель',
        'country': '🇧🇾 Беларусь',
        'region': 'г.Минск',
        'city': 'Минск',
        'agreed_to_terms': 'on'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'На ваш email отправлено письмо для подтверждения' in response.data

def test_login_success(client, mock_db):
    """Успешный вход с правильными учётными данными."""
    with patch('models.sync_verify_user_password') as mock_verify:
        mock_verify.return_value = {
            'user_id': 1,
            'username': 'testuser',
            'role': 'Покупатель',
            'email': 'test@example.com',
            'city': 'Минск',
            'is_email_verified': True,
            'full_registration_completed': True
        }
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Успешный вход' in response.data
        with client.session_transaction() as sess:
            assert sess['user_id'] == 1

def test_login_wrong_password(client, mock_db):
    """Вход с неверным паролем возвращает ошибку."""
    with patch('models.sync_verify_user_password', return_value=None):
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrong'
        }, follow_redirects=True)
        assert b'Неверное имя пользователя или пароль' in response.data

def test_logout(client, mock_db):
    """Выход из системы очищает сессию."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert 'user_id' not in sess
    assert b'Вы успешно вышли' in response.data
