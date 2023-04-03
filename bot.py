from config import TOKEN, CHAT_ID
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

acl = (CHAT_ID, 5550131546)
admin_only = lambda message: message.from_user.id not in acl


def kb():
    kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
    return kb_client


b1 = KeyboardButton("History")


def out():
    try:
        with open(f"./history.txt") as file:
            return file.read()
    except:
        return "no file"


@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    return


@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(b1))


@dp.message_handler()
async def send(message : types.Message):    
    if message.text == "History":
        await message.delete()
        out_history = out()
        await bot.send_message(message.from_user.id, out_history)


executor.start_polling(dp, skip_updates=True)
