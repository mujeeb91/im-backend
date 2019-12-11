FROM python:3.8-alpine
ADD . /code
WORKDIR /code
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
RUN pip install -r requirements.txt
CMD flask run
