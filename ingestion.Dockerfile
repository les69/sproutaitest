FROM python:3.9-slim as base

RUN apt-get update -qq \
  && apt-get install --no-install-recommends -y \
        libpq-dev make cron\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY sproutaitest sproutaitest
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY Makefile Makefile

RUN make install

FROM base as main
# Copy hello-cron file to the cron.d directory
COPY backlog-cron /etc/cron.d/backlog-cron
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/backlog-cron
# Apply cron job
RUN crontab /etc/cron.d/backlog-cron
EXPOSE 5000
ENTRYPOINT ["make", "run-django-server"]

FROM base as test

COPY setup.cfg setup.cfg
RUN make install-dev
ENTRYPOINT ["make", "full-test-suite"]