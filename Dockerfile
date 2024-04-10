FROM python:3.10-slim

COPY requirements.txt /tmp/requirements.txt

RUN set -ex \
    && pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt 


COPY src /app/src

WORKDIR /app

CMD ["python3", "-m", "src.server"]
