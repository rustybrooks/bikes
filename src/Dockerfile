FROM ubuntu:18.04

RUN apt-get -y update \
 && apt-get install -y sudo \
                       build-essential \
                       python3 \
                       python3-pip curl \
                       libspatialindex-dev \
  && pip3 install --upgrade pip

COPY requirements.txt /srv
COPY api/requirements.txt /srv/api_requirements.txt
COPY bikedb/requirements.txt /srv/bikedb_requirements.txt
RUN pip3 install -r /srv/requirements.txt -r /srv/api_requirements.txt -r /srv/bikedb_requirements.txt



