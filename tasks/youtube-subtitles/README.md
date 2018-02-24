# Зависимости #

1. Установить [SAPI 5](https://www.microsoft.com/en-us/download/details.aspx?id=10121) (только для Windows).
2.
        cd youtube-subtitles
        pip install -r requirements.txt
3. Установить [ffmpeg](https://www.ffmpeg.org/download.html) и добавить его в PATH.


# Использование #

    cd youtube-subtitles
    python -myoutube_subtitles ..\text.txt QCTF{test_flag} ..\video.mp4 ..\subtitles.srt

Здесь: \
— `..\text.txt` — путь к тексту, на основе которого надо сгенерировать видео; \
— `QCTF{test_flag}` — флаг, который нужно вставить в середину текста; \
— `..\video.mp4` — путь, по которому нужно сохранить сгенерированное видео (расширение определяет формат); \
— `..\subtitles.srt` — путь, по которому нужно сохранить сгенерированные субтитры.
