FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV STATIC_URL /content

COPY ./app /app