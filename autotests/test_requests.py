def test_create_request(client, mock_db):
    """Авторизованный пользователь создаёт заявку."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = [101]  # ID заявки

    with patch('models.sync_search_web_sellers_by_category', return_value=[]):
        response = client.post('/create_request', data={
            'category': 'Автомобили',
            'subcategory': 'Запасные части',
            'description': 'Нужен бампер для Kia Rio 2018',
            'city': 'Минск'
        }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Заявка #101 успешно создана' in response.data

def test_list_user_requests(client, mock_db):
    """Просмотр списка своих заявок."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchall.return_value = [
        (101, 1, 'Автомобили', 'Запасные части', 'Нужен бампер', 'Минск', 'active', '2025-01-01', '2025-01-01'),
        (102, 1, 'Электроника', None, 'Ищу ноутбук', 'Москва', 'active', '2025-01-02', '2025-01-02')
    ]
    response = client.get('/requests')
    assert response.status_code == 200
    assert b'Нужен бампер' in response.data
    assert b'Ищу ноутбук' in response.data

def test_create_request_unauthenticated(client):
    """Неавторизованный пользователь перенаправляется на логин."""
    response = client.get('/create_request', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.location
