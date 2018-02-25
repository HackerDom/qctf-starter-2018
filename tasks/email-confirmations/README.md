# Запуск через docker #

Перед самым первым запуском для инициализации данных в базе:

`docker-compose run --rm email-confirmations init; docker-compose down`

Для последующих запусков:

`docker-compose up`

# Запуск вручную #

0. `pip install -r requirements.txt`
1. Создать базу в Postgres
2. Создать файл `config.py` и определить там переменные `SECRET_KEY` (случайная строка для подписи кук) и `SQLALCHEMY_DATABASE_URI` (строка подключения к базе в Postgres, включающая в себя логин и пароль)
3. Присвоить переменной окружения `APP_CONFIG` путь к только что созданному файлу `config.py`
4. Присвоить переменной окружения `MAIL_TOKEN` токен от Postmark
5. Запустить `python manage.py db upgrade`
6. Запустить `python manage.py generate_flag_owner <flag>` и `python manage.py generate_dummies <count>`, где `<flag>` — флаг этого таска, а `<count>` — количество дополнительно генерируемых фейковых аккаунтов, например, 15
7. Присвоить переменной окружения `FLASK_APP` значение `app.py` и запустить приложение: `flask run --host=0.0.0.0 --port=80`
