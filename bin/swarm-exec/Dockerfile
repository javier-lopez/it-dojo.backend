FROM  python:alpine

ENV TERM=xterm

WORKDIR /app

RUN  ln -s /usr/local/bin/python3 /usr/bin/python3
RUN  pip install docker requests

COPY ./swarm-exec ./skpp.py /app/

ENTRYPOINT [ "./swarm-exec" ]
