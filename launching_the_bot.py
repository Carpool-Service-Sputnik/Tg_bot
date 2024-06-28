from aiogram import Bot, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token="5993797965:AAGGFyPK2NIiZmmfFZv02lOqXsaDaFBscZQ")
dp = Dispatcher(bot)


async def send_message_to_users(user_ids, text):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/start"))
    for user_id in user_ids:
        await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        
async def on_startup(dp):
    user_ids = [1643807540] # Список идентификаторов пользователей
    text = "Техническое обслуживание закончено, возобновляю работу." # Текст сообщения
    await send_message_to_users(user_ids, text)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
