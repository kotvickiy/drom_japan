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
b2 = KeyboardButton("Old")
b3 = KeyboardButton("Out")


def out(file_name):
    try:
        with open(file_name) as file:
            res = [i.strip() for i in file.readlines()]
            if res:
                return res
            else:
                return ["empty"]
    except:
        return ["no file"]


@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    return


@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(b1, b2, b3))


@dp.message_handler()
async def send(message : types.Message):    
    if message.text == "History":
        out_history = out("./history.txt")
        if len(out_history) > 50:
            for x in range(0, len(out_history), 50):
                await bot.send_message(message.from_user.id, "\n".join(out_history[x:x+50]), disable_web_page_preview=True)
        else:
            await bot.send_message(message.from_user.id, "\n".join(out_history), disable_web_page_preview=True)
    elif message.text == "Old":
        out_old = out("./old.txt")
        if len(out_old) > 50:
            for x in range(0, len(out_old), 50):
                await bot.send_message(message.from_user.id, "\n".join(out_old[x:x+50]), disable_web_page_preview=True)
        else:
            await bot.send_message(message.from_user.id, "\n".join(out_old), disable_web_page_preview=True)
    elif message.text == "Out":
        out_old = out("./out.log")
        if len(out_old) > 50:
            for x in range(0, len(out_old), 50):
                await bot.send_message(message.from_user.id, "\n".join(out_old[x:x+50]), disable_web_page_preview=True)
        else:
            await bot.send_message(message.from_user.id, "\n".join(out_old), disable_web_page_preview=True)


executor.start_polling(dp, skip_updates=True)
