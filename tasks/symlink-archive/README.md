# Запуск через docker #

Перед самым первым запуском для инициализации данных в базе:

`docker-compose build`

`docker-compose run --rm symlink-archive init; docker-compose down`

Для последующих запусков:

`docker-compose up`
