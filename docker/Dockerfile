FROM python:3.11

EXPOSE 8080

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV DJANGO_STATIC_ROOT '/static'
ENV DJANGO_MEDIA_ROOT '/media'
ENV DJANGO_SETTINGS_MODULE: "mos.settings.deploy_env"

RUN mkdir /code
COPY . /code/

RUN apt-get update \
    && apt-get install -y --force-yes libmariadb-dev libjpeg-dev netcat-traditional locales \
    && pip3 install --no-cache-dir -vvv -r /code/requirements.txt \
    && pip3 install --no-cache-dir -vvv -Ur /code/requirements-dev.txt
    
RUN sed -i -e 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && locale-gen

WORKDIR /code
ENTRYPOINT ["docker/entrypoint.sh"]
