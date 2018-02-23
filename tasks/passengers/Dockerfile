FROM python:3.5

RUN echo 123

RUN apt-get update
RUN apt-get install -y xinetd && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY . /app

RUN mkdir -p /passengers/teams
RUN python3 /app/router.py prepare

RUN useradd passengers

RUN chmod -R o-rwx /app
RUN chmod -R o-w /passengers
RUN chmod -R o+rx /passengers

EXPOSE 9999

ENTRYPOINT [ "xinetd", "-dontfork" ]
