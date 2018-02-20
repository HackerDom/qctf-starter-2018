FROM python:3.6

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80

RUN python /app/generate_flags.py 400

CMD ["./run-with-gunicorn.sh"]
