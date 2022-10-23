FROM python:3.9-slim as base

RUN apt-get update -qq \
  && apt-get install --no-install-recommends -y \
        libpq-dev make\
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY mlapi mlapi
COPY Makefile Makefile

RUN pip install -r mlapi/requirements.txt
WORKDIR mlapi
EXPOSE 5001
ENTRYPOINT ["python", "flask_server.py"]