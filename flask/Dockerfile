FROM python:3.8.2-alpine3.11

WORKDIR /usr/src/app

ENV DB_USER=postgres
ENV DB_PASSWORD=password
ENV DB_NAME=postgres
ENV DB_HOST=postgres
ENV DB_PORT=5432

COPY . /usr/src/app
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

CMD python app.py --db_user ${DB_USER} --db_password ${DB_PASSWORD} --db_name ${DB_NAME} --db_host ${DB_HOST} --db_port ${DB_PORT}
