FROM ubuntu:20.04

RUN apt-get update && apt-get install python3.8 -y
RUN python3.8 -m pip install supervisor uwsgi

CMD ["supervisord", "-c", "supervisor/supervisor.conf"]