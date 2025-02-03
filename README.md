# Telegram Bot with Django Admin Panel

Проект представляет собой Telegram-бот с функционалом каталога товаров, корзины, оплаты через платежный шлюз (YooKassa), а также админ-панель на Django для управления товарами, заказами и рассылками.

## Содержание

1. [Описание проекта](#описание-проекта)
2. [Технологии](#технологии)
3. [Установка](#установка)
4. [Запуск](#запуск)
5. [Структура проекта](#структура-проекта)

---

## Описание проекта

### Функционал Telegram-бота:

- Проверка подписки пользователя на канал/группу.
- Каталог товаров с категориями и подкатегориями.
- Корзина с возможностью добавления товаров и оформления заказа.
- Интеграция платежного шлюза (ЮKassa).
- FAQ-раздел с часто задаваемыми вопросами.
- Выгрузка заказов в Excel-файл (доступно только администраторам).

### Функционал админ-панели:

- Управление товарами, категориями и заказами через Django Admin.
- Рассылка сообщений пользователям.

---

## Технологии

- **Telegram Bot**: Aiogram, SQLAlchemy, Asyncpg, Python.
- **Админ-панель**: Django.
- **Платежный шлюз**: Yookassa.
- **Контейнеризация**: Docker, Docker Compose.
- **База данных**: PostgreSQL.

---

## Установка

### Предварительные требования:

1. Установленный Docker и Docker Compose.
2. Переменные окружения в файле `.env` (см. пример ниже).

### Шаги:

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/MaskedGod/test_tbot_dj_admin
   cd your-repository-folder
   ```

2. Создайте файл `.env` в корневой папке проекта и заполните его переменными окружения:

   ```env
    BOT_TOKEN=your_telegram_bot_token
    CHANNEL_ID=-1001234567890
    GROUP_ID=-1009876543210
    ADMIN_IDS=123456789,987654321

    DJANGO_SECRET_KEY=your_django_secret_key

    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password

    PAYMENT_SHOP_ID=your_shop_id
    PAYMENT_SECRET_KEY=your_secret_key
   ```

3. Убедитесь, что Docker и Docker Compose установлены:
   ```bash
   docker --version
   docker-compose --version
   ```

---

## Запуск

1. Соберите и запустите контейнеры:

   ```bash
   docker-compose up --build
   ```

2. После запуска:

   - Telegram-бот будет доступен через Telegram.
   - Админ-панель будет доступна по адресу [http://localhost:8000/admin](http://localhost:8000/admin).

3. Для остановки контейнеров:
   ```bash
   docker-compose down
   ```

---

## Структура проекта

```
project/
├── tg_bot/               # Telegram-бот
│   ├── bot.py            # Основной файл бота
│   ├── handlers/         # Обработчики команд
│   ├── keyboards/        # Клавиатуры
│   ├── database/         # Модели базы данных
│   └── utils/            # Вспомогательные функции
├── admin_panel/          # Админ-панель на Django
│   ├── manage.py         # Управление Django-проектом
│   ├── shop/             # Приложение для управления товарами и заказами
│   └── admin_panel/      # Основное приложение Django
├── .env                  # Переменные окружения
├── docker-compose.yml    # Конфигурация Docker Compose
└── README.md             # Документация
```
