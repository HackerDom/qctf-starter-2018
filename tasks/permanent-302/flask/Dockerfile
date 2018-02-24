FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80

RUN ./generate_flags.sh

CMD ["./run-with-gunicorn.sh"]
