FROM rustybrooks/bikes-base:latest
RUN apt-get -y update \
 && mkdir /srv/logs && mkdir /var/log/gunicorn

COPY . /srv/src
RUN pip install -U -r /srv/src/requirements.txt -r /srv/src/api/requirements.txt
ENTRYPOINT /srv/src/api/entrypoint.sh
