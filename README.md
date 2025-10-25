# PastaHouse — E-commerce backend (Django)

## Кратко

Это бэкенд для интернет‑магазина PastaHouse на Django + Django REST Framework. Включает модули пользователей, товаров, корзины и заказов, с поддержкой JWT (SimpleJWT), загрузки изображений и WYSIWYG редактора (django-ckeditor).

## Структура проекта (важные файлы/папки)

- `backend/` — основной Django проект (settings, urls, wsgi/asgi)
- `users/` — приложение пользователей (кастомный User с email)
- `products/` — товары, категории, теги, отзывы
- `carts/` — корзина (CartItem)
- `orders/` — заказы и позиции заказа
- `api_endpoinst.txt` — полный список API-эндпоинтов (использует http://localhost:8080)
- `models.txt` — спецификация моделей (источник эндпоинтов)

## Требования (рекомендуемые)

- Python 3.11+ / 3.12
- virtualenv (venv)
- SQLite (по умолчанию) или Postgres для production
- Рекомендуемые пакеты (pip):
  - Django
  - djangorestframework
  - djangorestframework-simplejwt
  - django-cors-headers
  - django-filter
  - django-ckeditor
  - Pillow

## Быстрая установка (Windows PowerShell)

Откройте терминал в корне проекта (где `manage.py`) и выполните:

```powershell
# создать/активировать виртуальное окружение
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# обновить pip и установить зависимости (минимальный набор)
pip install --upgrade pip
pip install Django djangorestframework djangorestframework-simplejwt django-cors-headers django-filter django-ckeditor Pillow
```

## Конфигурация окружения

- `backend/settings.py` использует `AUTH_USER_MODEL = 'users.User'`.
- CORS настроен разрешать только `localhost` и `127.0.0.1` через `CORS_ALLOWED_ORIGIN_REGEXES`.
- `MEDIA_URL` и `MEDIA_ROOT` настроены; при `DEBUG=True` медиа-файлы будут обслуживаться автоматически.
- CKEditor: `CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor/'`.

## Миграции и запуск

```powershell
.\.venv\Scripts\python.exe manage.py makemigrations
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8080
```

Если вы столкнулись с ошибкой InconsistentMigrationHistory (например, "Migration admin.0001_initial is applied before its dependency users.0001_initial"), ознакомьтесь с советами ниже в разделе "Если что-то пошло не так".

## API — кратко

- Полный список эндпоинтов и примеры запросов в `api_endpoinst.txt`.
- Аутентификация: JWT (SimpleJWT). Endpoints для получения токена: `/api/auth/token/` и `/api/auth/token/refresh/`.
- Регистрация и вход:
  - `POST /api/users/register/` — регистрация, возвращает `tokens` (access + refresh) и данные пользователя.
  - `POST /api/users/login/` — вход (можно использовать `email` или `username` + `password`), возвращает `tokens`.

## Media и CKEditor

- Поля изображений у продуктов сохранены через `ImageField` в `MEDIA_ROOT/products/images/`.
- Если используется CKEditor, загрузки через редактор сохраняются в `MEDIA_ROOT/uploads/ckeditor/`.
- Убедитесь, что `Pillow` установлен для поддержки `ImageField`.

## Админка

- Админ доступен по `/admin/`.
- Используйте `createsuperuser` для создания администратора.

## Проверка endpoint'ов (curl)

Регистрация:

```powershell
curl -X POST http://localhost:8080/api/users/register/ -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"secret123","name":"Test"}'
```

Вход:

```powershell
curl -X POST http://localhost:8080/api/users/login/ -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"secret123"}'
```

## Дополнительные заметки и рекомендации

- Username: модель `User` использует `email` как поле для аутентификации, но хранит `username` (сгенерированный, если не указан). Если вы хотите полностью удалить `username`, потребуется миграция и изменение `REQUIRED_FIELDS`.
- Безопасность: добавьте rate limiting на endpoint регистрации/логина и настройте HTTPS в production.
- Рекомендуется добавить тесты (pytest + pytest-django) для основных потоков: регистрация, создание продукта, создание заказа.

## Если что-то пошло не так

- Ошибка миграций (InconsistentMigrationHistory): обычно значит, что порядок применения миграций нарушен. Возможные решения:
  - Если вы в локальном dev и можете сбросить БД: удалить `db.sqlite3` и папку `migrations` в приложениях, затем запустить `makemigrations`/`migrate` заново.
  - Если БД не удаляется (на проде), аккуратно использовать `manage.py migrate --fake app_label migration_name` чтобы пометить зависимости как применённые. Делайте это только понимая последствия.

## Что можно добавить дальше (next steps)

- Пагинация и фильтрация продуктов (по цене, рейтингу, тегам) — частично присутствует.
- Загрузка изображений через отдельный endpoint и обработка миниатюр.
- Интеграция платежного шлюза (Stripe/PayPal).
- Очереди (Celery + Redis) для фоновых задач (уведомления, отчёты).

## Контакты и вклад

Если хотите, я могу продолжить: добавить тесты, CI, docker-compose (web+db+redis), или доработать права/валидацию. Просто скажите, что приоритетнее.

---

README сгенерирован автоматически инструментом разработчика. Подправьте/дополниет в репозитории по необходимости.
