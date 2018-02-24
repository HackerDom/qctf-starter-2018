FROM python:3.5

RUN apt-get update
RUN apt-get install -y libgmp3-dev
RUN apt-get install -y libmpfr-dev libmpfr-doc libmpfr4 libmpfr4-dbg
RUN apt-get install -y libmpc-dev

ENV DOCKERIZE_VERSION v0.3.0
RUN wget -q https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
	&& rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80

ENTRYPOINT ["./docker-entry-point.sh"]
