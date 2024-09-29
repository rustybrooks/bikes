FROM python:3.12 AS base

WORKDIR /srv/src/app

COPY requirements.txt requirements.dev.txt ./
RUN pip3 install -r /srv/src/app/requirements.txt -r requirements.dev.txt

RUN apt-get -y update \
    && apt-get install -y sudo build-essential curl libspatialindex-dev \
               libpq-dev gcc libgdal-dev \
    && pip3 install --upgrade pip \
    && mkdir /srv/logs && mkdir /var/log/gunicorn

COPY api/bikes ./api/
COPY api/manage.py api/pyproject.toml ./
RUN ./manage.py collectstatic

# This is maybe too fancy but the idea is that "base" has dev stuff
# and then for production builds it gets removed here
#FROM python:3.12-bookworm AS intermediate
#ARG PRODUCTION=true
#RUN if [ "${PRODUCTION}" != "false" ]; then pip uninstall -y -r requirements.dev.txt; fi


FROM python:3.12-slim-bookworm AS final
WORKDIR /usr/src/api

RUN apt update && apt install -y curl && apt-get clean

COPY --from=base /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /usr/local/lib/ /usr/local/lib/

RUN addgroup --gid 1111 nonroot \
    && adduser --gid 1111 --uid 1111 nonroot \
    && echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

USER nonroot

COPY --from=base /usr/src/app/manage.py ./
COPY --from=base /usr/src/app/bikes/ ./bikes/
COPY entrypoint.sh ./
ENV PYTHONUNBUFFERED 1
ENTRYPOINT /usr/src/app/entrypoint.sh