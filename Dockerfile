FROM python:3.8-alpine
LABEL maintainer="romani.ae98@gmail.com"

VOLUME /data

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE SimpleVPN.settings.production
ENV DJANGO_DATA_DIR /data

# Install deps
RUN apk add --update --no-cache iptables iproute2 gettext

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /code/requirements.txt
RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev openssl-dev cargo && \
    pip install --upgrade pip && \
    pip install --no-cache -r /code/requirements.txt gunicorn && \
    apk del .build-deps

WORKDIR /code/
COPY . .

RUN python manage.py collectstatic --clear --no-input

EXPOSE 8000
CMD ./docker-entrypoint.sh
