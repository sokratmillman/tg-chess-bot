FROM python:3.10.6

COPY ./ /usr/app/src/tg-chess-bot
WORKDIR /usr/app/src/tg-chess-bot


RUN groupadd -r user && useradd -r -g user user && chown -R user /usr/app/src/tg-chess-bot
USER user

RUN apt-get update
RUN python3 -m venv env
RUN source env/bin/activate
RUN pip install -r requirements.txt

RUN git clone https://github.com/official-stockfish/Stockfish --branch sf_15.1 \
	cd ./Stockfish/src \
    make net \
    make build ARCH=x86-64-modern \
    cd ../../

CMD ['python', './main.py']

