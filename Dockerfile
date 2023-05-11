FROM python:3.10.6

COPY ./ /usr/app/src/tg-chess-bot
WORKDIR /usr/app/src/tg-chess-bot

RUN apt update
RUN apt install build-essential
RUN pip3 install --upgrade pip

RUN groupadd -r user && useradd -r -g user user && chown -R user /usr/app/src/tg-chess-bot

RUN python3 -m venv env
RUN source env/bin/activate
RUN pip3 install -r requirements.txt --no-cache-dir


RUN git clone https://github.com/official-stockfish/Stockfish --branch sf_15.1 \
	cd ./Stockfish/src \
    make net \
    make build ARCH=x86-64-modern \
    cd ../../

USER user
CMD ['python', './main.py']

