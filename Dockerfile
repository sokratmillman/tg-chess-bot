FROM python:3.10.6

COPY ./ /usr/app/src/tg-chess-bot
WORKDIR /usr/app/src/tg-chess-bot

RUN groupadd -r user && useradd -r -g user user && chown -R user /usr/app/src/tg-chess-bot
USER user
RUN apt-get update
RUN python3 -m venv env
RUN source env/bin/activate
RUN pip install -r requirements.txt

CMD ['python', './main.py']

