FROM python:3.5

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
COPY requirements.deploy.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.deploy.txt

COPY . /app

EXPOSE 80

CMD ["./run-with-gunicorn.sh"]
