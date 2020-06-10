FROM python:3.8.2-alpine3.11

WORKDIR /usr/app

COPY . /usr/app
RUN apk update && \
    apk add --virtual build-deps gcc build-base linux-headers pcre-dev python3-dev musl-dev postgresql-dev uwsgi uwsgi-python3 
RUN pip install --upgrade pip --no-cache-dir -r /usr/app/requirements.txt

CMD uwsgi uwsgi.ini