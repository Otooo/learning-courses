FROM python:3.6
LABEL maintainer 'Yo 0/'

RUN useradd www && \
    mkdir /app && \
    mkdir /log && \
    chown www /log

USER www
VOLUME /log
WORKDIR /app
EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/python"]
CMD ["run.py"]
