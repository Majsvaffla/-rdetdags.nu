# Bookworm for linux/amd64
FROM python:3.13-slim@sha256:3ee7fc7aee9be3dc9baff00dbde162f20ad686439963b2118e866eb18979ef99 AS base

RUN apt-get -qq update
RUN pip install --upgrade pip

FROM base AS ci

WORKDIR /var/lib/ärdetdags

COPY requirements.txt dist/
COPY *.whl dist/

RUN pip wheel -q -w dist -r dist/requirements.txt
RUN pip install --no-cache --no-index --find-links=dist dist/*.whl
RUN python -m compileall -q $(python -c "import sys; print(sys.path[-1])")
RUN rm dist/requirements.txt dist/*.whl

FROM ci AS runtime

ENV DIST_PATH=/var/lib/ärdetdags/dist
ENV LOGS_PATH=/var/log/ärdetdags

VOLUME ${LOGS_PATH}

EXPOSE 8000
