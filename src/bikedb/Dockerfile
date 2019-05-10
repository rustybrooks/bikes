FROM rustybrooks/flannelcat-base:latest
COPY . /srv/src/
RUN pip install -U -r /srv/src/bikedb/requirements.txt
ENTRYPOINT /srv/src/bikedb/entrypoint.sh
