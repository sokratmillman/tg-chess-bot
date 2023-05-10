from firebase.my_database import MyDatabase
from os import environ as env
from dotenv import load_dotenv

load_dotenv()

db_url = env['DB_URL']
cred_path = env['DB_KEY_PATH']

database = MyDatabase(cred_path=cred_path, db_URL=db_url)

