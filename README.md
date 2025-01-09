# Благотворительный фонд QRKot

## Описание проекта

### QRKot — это API-приложение, предназначенное для создания благотворительных проектов и организации пожертвований для котиков. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Установка и настройка

1. **Клонирование репозитория:**
    
    ```bash
    git clone git@github.com:closecodex/cat_charity_fund.git
    cd cat_charity_fund
    ```

2. **Создание и активация виртуального окружения:**

    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```

3. **Обновление менеджера пакетов и установка зависимостей:**
   
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Выполнение миграций:**
    
    ```bash
    alembic upgrade head
    ```

5. **Запуск приложения:**
    ```bash
    uvicorn app.main:app --reload
    ```

## Примеры эндпоинтов

### Аутентификация

- POST /auth/register — регистрация нового пользователя.

- POST /auth/jwt/login — логин и получение JWT.

### Благотворительные проекты

- GET /charity_project/ — список всех проектов.

- POST /charity_project/ — создание нового проекта.

### Пожертвования

- GET /donation/my — список ваших пожертвований.

- POST /donation/ — отправка нового пожертвования.

## Дополнительная информация

1. **Автор: ([Мария Осмоловская](https://github.com/closecodex/cat_charity_fund/wiki/))**

2. **Технологии: Python, FastAPI, SQLAlchemy, Alembic, SQLite, Pydantic**

3. **Полная техническая документация API: Swagger UI (доступна на /docs), ReDoc (доступна на /redoc)**
