# Тестирование проекта Ceny 24.by

Проект покрыт автоматическими тестами на базе **pytest**. Тесты проверяют ключевые сценарии работы веб-приложения: регистрацию, авторизацию, работу с заявками, админ-панель и чат.

## Технологии

- **pytest** — фреймворк для написания и запуска тестов
- **Flask** — тестируемое веб-приложение
- **unittest.mock** — мокирование внешних зависимостей (БД, модели)

---

## Структура тестов

| Файл | Описание |
|------|----------|
| `tests/test_auth.py` | Тесты регистрации, входа, выхода, подтверждения email |
| `tests/test_admin.py` | Тесты админ-панели (просмотр продавцов, активация) |
| `tests/test_requests.py` | Тесты создания и просмотра заявок |
| `tests/test_messages.py` | Тесты чата (отправка сообщений, просмотр диалога) |

---

## Запуск тестов

### 1. Установка зависимостей

Убедитесь, что установлены все необходимые пакеты:

```bash
pip install -r requirements.txt
Если requirements.txt нет, установите вручную:

bash
pip install pytest flask Flask-WTF
2. Запуск всех тестов
Из корневой директории проекта выполните:

bash
pytest -v
Флаг -v (verbose) показывает подробный вывод по каждому тесту.

3. Запуск конкретного файла с тестами
bash
pytest tests/test_auth.py -v
4. Запуск конкретного теста по имени
bash
pytest tests/test_auth.py::test_login_success -v
5. Запуск с отчётом о покрытии (опционально)
Если установлен pytest-cov:

bash
pip install pytest-cov
pytest --cov=. -v
Что проверяют тесты
Авторизация (test_auth.py)
test_register_success — успешная регистрация нового пользователя

test_login_success — вход с корректными учётными данными

test_login_wrong_password — отклонение входа с неверным паролем

test_logout — выход из системы с очисткой сессии

Админ-панель (test_admin.py)
test_admin_login_success — вход администратора в панель управления

test_admin_pending_sellers — просмотр списка продавцов, ожидающих проверки

test_admin_activate_seller — активация продавца после проверки

Заявки (test_requests.py)
test_create_request — создание заявки авторизованным пользователем

test_list_user_requests — просмотр списка своих заявок

test_create_request_unauthenticated — перенаправление на логин для неавторизованных

Чат (test_messages.py)
test_send_message — отправка сообщения в активном диалоге

test_view_conversation — просмотр диалога с историей сообщений

Примечания
Мокирование
Тесты используют моки для изоляции от реальной базы данных. Это означает, что тесты выполняются быстро и не требуют запущенного PostgreSQL.

Все моки находятся в фикстуре mock_db и подменяют models.get_connection().

Запуск в CI (GitHub Actions, GitLab CI)
Пример команды для CI-пайплайна:

bash
pytest --maxfail=1 --disable-warnings -v
Устранение неполадок
Проблема: ModuleNotFoundError: No module named 'app'

Решение: Запускайте тесты из корневой директории проекта или добавьте путь в PYTHONPATH:

bash
export PYTHONPATH=$(pwd)
pytest -v
Проблема: pytest не найден

Решение: Убедитесь, что pytest установлен:

bash
pip install pytest
Контакты
Автор тестов: Алексей Соколов
GitHub: glorybet42-cmyk
Проект: Ceny 24.by
