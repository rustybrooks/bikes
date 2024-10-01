FROM python:3.12 AS base

WORKDIR /srv/src/app

RUN apt-get -y update \
    && apt-get install -y build-essential libspatialindex-dev \
               libpq-dev gcc libgdal-dev \
    && pip3 install --upgrade pip

COPY requirements.txt requirements.dev.txt api/pyproject.toml ./
RUN pip3 install -r /srv/src/app/requirements.txt -r requirements.dev.txt

FROM python:3.12-slim-bookworm AS final
WORKDIR /usr/src/api

RUN addgroup --gid 1111 nonroot \
    && adduser --gid 1111 --uid 1111 nonroot \
    && echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

USER nonroot

COPY --from=base /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /usr/local/lib/ /usr/local/lib/
COPY api/bikes/ ./bikes/
COPY api/manage.py ./
COPY api/entrypoint.sh ./

# RUN DJANGO_SECRET_KEY=foo ./manage.py collectstatic

ENV PYTHONUNBUFFERED 1
ENTRYPOINT /usr/src/app/entrypoint.sh