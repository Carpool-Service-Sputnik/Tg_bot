from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from json import load
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import threading
import schedule
from time import sleep as ts


storage=MemoryStorage()

# Reading "BOT_TOKEN"
with open("data/config.json", 'r') as config:
    bt_token = load(config)["BOT_TOKEN"]

# Reading "DB_HTTP_URL"
with open("data/config.json", 'r') as config:
    BASE_URL = load(config)["DB_HTTP_URL"]
    

bot = Bot(token=bt_token)
dp = Dispatcher(bot, storage=storage)

