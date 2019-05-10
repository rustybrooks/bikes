FROM rustybrooks/bikes-base:latest
RUN apt-get -y update \
 && mkdir /srv/logs && mkdir /var/log/gunicorn \
 && pip install -U -r /srv/api_requirements.txt

COPY . /srv/src
ENTRYPOINT /srv/src/api/entrypoint.sh
