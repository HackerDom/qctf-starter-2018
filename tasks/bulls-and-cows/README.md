# Запуск через docker #

Перед самым первым запуском для инициализации данных в базе:

`docker-compose build`

`docker-compose run --rm bulls-and-cows init; docker-compose down`

Для последующих запусков:

`docker-compose up`

# Запуск вручную #

0. `pip install -r requirements.txt`
1. Создать базу в Postgres
2. Создать файл `config.py` и определить там переменные `SECRET_KEY` (случайная строка для подписи кук), `SQLALCHEMY_DATABASE_URI` (строка подключения к базе в Postgres, включающая в себя логин и пароль) и `FLAG` (ответ на задание)
3. Присвоить переменной окружения `APP_CONFIG` путь к только что созданному файлу `config.py`
4. Запустить `python3 manage.py db upgrade`
5. Присвоить переменной окружения `FLASK_APP` значение `app.py` и запустить приложение: `flask run --host=0.0.0.0 --port=80`