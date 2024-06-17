from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loader import bot, dp

async def on_any_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    with open("data/chat_logs.txt", "a") as f:
        f.write(f"{len(open('data/chat_logs.txt').readlines()) + 1}. {message.date.strftime('%d.%m.%Y %H:%M:%S')} - - - TG_ID:{user_id}\n")
    await bot.send_message(message.from_user.id, "Ушел на техническое обслуживание, сообщу когда вернусь)")


dp.register_message_handler(on_any_message)

executor.start_polling(dp, skip_updates=True)