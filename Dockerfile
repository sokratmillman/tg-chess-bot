FROM python:latest

COPY ./ /usr/app/src
WORKDIR /usr/app/src

RUN apt-get update
RUN pip install -r requirements.txt

CMD ['python', './main.py']

