FROM python:3-alpine

EXPOSE 8080

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
COPY . /code/

RUN apk update \
    && apk add --virtual build-deps gcc musl-dev libffi-dev gcc python3-dev openssl-dev cargo \
    && apk add --no-cache mariadb-dev jpeg-dev zlib-dev libjpeg \
    && pip3 install --no-cache-dir -vvv -r /code/requirements.txt \
    && pip3 install --no-cache-dir -vvv -Ur /code/requirements-dev.txt \
    && pip3 install --no-cache-dir -vvv daphne \
    && apk del build-deps

WORKDIR /code
ENTRYPOINT ["docker/entrypoint.sh"]
