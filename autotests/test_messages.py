def test_send_message(client, mock_db):
    """Отправка сообщения в активном диалоге."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    mock_cursor, mock_conn = mock_db
    # Мокаем получение диалога (существует и активен)
    mock_cursor.fetchall.return_value = [
        {'id': 10, 'buyer_id': 1, 'seller_id': 2, 'is_active': True}
    ]
    # Мокаем вставку сообщения
    mock_cursor.fetchone.return_value = [201]

    response = client.post('/conversation/10/send', data={
        'message': 'Здравствуйте, есть ли товар в наличии?'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Здравствуйте, есть ли товар в наличии?' in response.data

def test_view_conversation(client, mock_db):
    """Просмотр диалога с историей сообщений."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1

    mock_cursor, mock_conn = mock_db
    # Информация о диалоге
    mock_cursor.fetchall.side_effect = [
        [{'id': 10, 'buyer_id': 1, 'seller_id': 2, 'is_active': True,
          'buyer_username': 'buyer1', 'seller_username': 'seller1'}],
        [{'id': 1, 'sender_id': 1, 'message_text': 'Привет', 'created_at': '2025-01-01'},
         {'id': 2, 'sender_id': 2, 'message_text': 'Здравствуйте!', 'created_at': '2025-01-01'}]
    ]

    response = client.get('/conversation/10')
    assert response.status_code == 200
    assert b'Привет' in response.data
    assert b'Здравствуйте!' in response.data
