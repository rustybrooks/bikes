FROM python:3.12-slim-bookworm AS base

WORKDIR /srv/src/app

RUN apt-get -y update \
    && apt-get install -y build-essential libspatialindex-dev \
               libpq-dev gcc libgdal-dev \
    && pip3 install --upgrade pip

COPY requirements.txt requirements.dev.txt api/gunicorn.py api/pyproject.toml ./
RUN pip3 install -r /srv/src/app/requirements.txt -r requirements.dev.txt

COPY api/bikes/ /srv/src/app/bikes/
COPY api/static/ /srv/src/app/static/
COPY api/manage.py api/entrypoint.sh /srv/src/app/

FROM python:3.12-slim-bookworm AS final
WORKDIR /srv/src/app

RUN apt-get -y update \
    && apt-get install -y curl \
    && apt-get clean

# RUN addgroup --gid 1111 nonroot \
#     && adduser --gid 1111 --uid 1111 nonroot

# USER nonroot

COPY --from=base /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /usr/local/lib/ /usr/local/lib/
COPY --from=base /srv/src/app/ ./
#COPY --from=base /srv/src/app/static/ ./static/
#COPY --from=base /srv/src/app/manage.py /srv/src/app/entrypoint.sh /srv/src/app/gunicorn.py ./

# RUN DJANGO_SECRET_KEY=foo ./manage.py collectstatic

ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["/srv/src/app/entrypoint.sh"]
