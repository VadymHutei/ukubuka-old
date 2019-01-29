FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV STATIC_URL /content

COPY ./app /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt