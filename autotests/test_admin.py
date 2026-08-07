def test_admin_login_success(client, mock_db):
    """Вход администратора в админ-панель."""
    with patch('models.sync_verify_user_password') as mock_verify:
        mock_verify.return_value = {
            'user_id': 1,
            'username': 'admin',
            'role': 'Администратор',
            'email': 'admin@example.com',
            'is_email_verified': True
        }
        response = client.post('/admin/login', data={
            'login': 'admin',
            'password': 'adminpass'
        }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Панель управления' in response.data
    with client.session_transaction() as sess:
        assert sess['user_id'] == 1

def test_admin_pending_sellers(client, mock_db):
    """Администратор видит список продавцов на проверку."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchall.return_value = [
        {'id': 10, 'username': 'seller1', 'company_name': 'ООО АвтоДеталь',
         'email': 'seller1@example.com', 'city': 'Минск',
         'legal_registration_number': '12345678', 'created_at': '2025-01-01'}
    ]
    response = client.get('/admin/pending-sellers')
    assert response.status_code == 200
    assert b'ООО АвтоДеталь' in response.data
    assert b'12345678' in response.data

def test_admin_activate_seller(client, mock_db):
    """Администратор активирует продавца."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    mock_cursor, mock_conn = mock_db
    mock_cursor.rowcount = 1

    response = client.post('/admin/activate-seller/10', data={
        'notes': 'Проверка пройдена'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Продавец активирован' in response.data
