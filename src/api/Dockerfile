FROM rustybrooks/bikes-base:latest
RUN apt-get -y update \
 && mkdir /srv/logs && mkdir /var/log/gunicorn
COPY . /srv/src
ENTRYPOINT /srv/src/api/entrypoint.sh
