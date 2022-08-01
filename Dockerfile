FROM ubuntu:20.04

USER root

# Install base
RUN apt-get update && apt-get -y upgrade && \
    apt-get install python3-pip -y

ADD ./requirements.txt /opt/requirements.txt

WORKDIR /opt

RUN pip install supervisor \
    && pip install uwsgi \
    && pip install -r requirements.txt 

ARG  DEBIAN_FRONTEND=noninteractive
RUN apt-get install ffmpeg libsm6 libxext6  -y

ADD . /opt/attendance-server

COPY ./supervisor/supervisord.conf /etc/supervisord.conf

EXPOSE 8888

CMD ["supervisord", "-n", "-c", "/opt/attendance-server/supervisor/supervisord.conf"]