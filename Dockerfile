FROM alpine AS base  
RUN apk add python3 && python3 -m pip install  flask flask-restplus flask-mail celery  redis  requests

FROM base 
COPY . /email/
WORKDIR /email
ENV FLASK_APP=email.py
ENV FLASK_DEBUG=1







