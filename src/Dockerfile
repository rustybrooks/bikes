FROM python:3.10

WORKDIR /srv/src

RUN apt-get -y update \
    && apt-get install -y sudo build-essential curl libspatialindex-dev \
               libpq-dev gcc libgdal-dev \
    && pip3 install --upgrade pip \
    && mkdir /srv/logs && mkdir /var/log/gunicorn

COPY requirements.txt /srv
COPY api/requirements.txt /srv/api_requirements.txt
COPY bikedb/requirements.txt /srv/bikedb_requirements.txt
RUN pip3 install -r /srv/requirements.txt -r /srv/api_requirements.txt -r /srv/bikedb_requirements.txt

COPY . /srv/src


