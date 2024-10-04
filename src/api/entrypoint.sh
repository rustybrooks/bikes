#!/usr/bin/env bash

cd /srv/src/app

echo "Server starting DEBUG=${DEBUG}"
echo "DB_NAME=${DB_NAME} DB_USER=${DB_USER} DB_HOST=${DB_HOST} DB_PORT=${DB_PORT}"

# get IP address of container's host and set to ADDITIONAL_ALLOWED_HOSTS
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 3600"`
LOCAL_IPV4=`curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/local-ipv4`
export ADDITIONAL_ALLOWED_HOSTS="$LOCAL_IPV4,$ADDITIONAL_ALLOWED_HOSTS"

DJANGO_WORKERS=${DJANGO_WORKERS:-2}

./manage.py migrate
./manage.py check --deploy

gunicorn --config /srv/src/api/gunicorn.py bikes.wsgi


