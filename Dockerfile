FROM python:3.10-alpine

LABEL org.opencontainers.image.authors="William Woodruff <william@trailofbits.com>"

ADD requirements.txt /requirements.txt
ADD start.sh /start.sh

RUN apk add python3 && \
    pip install -r requirements.txt

ENTRYPOINT ["/action.py"]
