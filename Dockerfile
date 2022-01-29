FROM python:3.9.10-slim-buster

WORKDIR /usr/src/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m pip install flask
COPY main.py .
ENTRYPOINT  FLASK_APP=main flask run --host=0.0.0.0

EXPOSE 5000