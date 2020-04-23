FROM python:3-alpine

EXPOSE 8080

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /code
COPY . /code/

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev postgresql postgresql-dev jpeg-dev zlib-dev libjpeg \
    && pip3 install --no-cache-dir -vvv -r /code/requirements.txt \
    && pip3 install --no-cache-dir -vvv -Ur /code/requirements-dev.txt


RUN echo "SECRET_KEY='bla'" > /code/mos/settings/secret_key.py

WORKDIR /code
#ENTRYPOINT ['python3', 'manage.py']
