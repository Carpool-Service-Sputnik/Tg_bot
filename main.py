from aiogram.utils import executor
from loader import dp
from loader import bot
from handlers import *
from multithreading_bot import passengerDateAndTimeCheck
from data import DirectionRoutesPoints

passengerDateAndTimeCheck()

# Launching grouped registered handlers
startReg(dp)
menuAll(dp)
trips(dp)
car(dp)
adminCommands(dp)


# Starting pooling and skipping messages during the deactivation of the bot
executor.start_polling(dp, skip_updates=True)


