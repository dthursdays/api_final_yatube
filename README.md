# api_final
## Описание:

Это финальная версия api yatube, в нем реализованы все возможности оригинального проекта

## Как запустить:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/dthursdays/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры работы с api:

### Без аутентификации вам доступны:
Некоторые GET запросы...

- /api/v1/posts/ 
- /api/v1/posts/{post_id}/
- /api/v1/groups/
- /api/v1/groups/{group_id}/
- /api/v1/posts/{post_id}/comments/{comment_id}/

...POST запрос для получения bearer-токена...

- /api/v1/jwt/create/
```
{
"username": "string",
"password": "string"
}
```

...а также запросы для обновления и проверки токена:

- /api/v1/jwt/refresh/
- /api/v1/jwt/validate/

### После аутентификации вам будет полностью доступен функционал проекта yatube
Подробное описание всех эндпоинтов можно найти по адресу http://127.0.0.1:8000/redoc/ после запуска проекта на локальном сервере
