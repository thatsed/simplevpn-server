FROM python:3.8-buster
LABEL maintainer="romani.ae98@gmail.com"

VOLUME /data

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE SimpleVPN.settings.production
ENV DJANGO_DATA_DIR /data

# Install WireGuard deps
RUN printf "deb http://httpredir.debian.org/debian buster-backports main non-free\ndeb-src http://httpredir.debian.org/debian buster-backports main non-free" > /etc/apt/sources.list.d/backports.list
RUN apt update -y
RUN apt install iptables iproute2 wireguard -y

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /code/
COPY . /code/

# Set the working directory to /code/
WORKDIR /code/

RUN python manage.py collectstatic --clear --no-input --settings SimpleVPN.settings.development

EXPOSE 8000
CMD ./docker-entrypoint.sh
