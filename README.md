# Telegram Chess Bot

## Features

1. Users can play vs other player knowing their UID
2. Users can play vs bot powerd by Stockfish Engine
3. Users can watch their match history
4. Users can see leaderboard with the best players 
5. Users can see the analysis of the game while playing vs AI

## How to use

### Our solution
Go to `https://t.me/my_new_chess_bot`, start the bot.

`/help` can display description of the bot and its commands.

### Run yourself
0) Clone this repo
1) Create Firebase Realtime Database \
2) Save certificate for connection into `creds.json` in a root directory \
3) Initialize your bot via @BotFather, save a token\
4) Create `.env` file with the following content:
```
API_TOKEN = $TELEGRAM_BOT_TOKEN
DB_URL = $URL_TO_FIREBASE
DB_KEY_PATH = "creds.json"
```
5) We recommend using virtualenv (on Linux):
```
python3 -m venv env
source env/bin/activate
```
6) Install the dependencies
```
pip install -r requirements.txt
```
7) Run your bot:
```
python main.py
```
## Contributors

* Tagir Shigapov
* Maxim Stepanov
* Timur Belov
* Rashid Galliulin
* Evgeniy Trantsev

You are free to contribute as well, but check that the actions are passing before pull requests!