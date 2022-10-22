FROM python:3.9-alpine

ADD . /app

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev bash\
    && apk add --no-cache libffi openssl \
    && pip install --no-cache-dir --upgrade pip setuptools wheel\
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

CMD gunicorn 'domain_admin.main:app'