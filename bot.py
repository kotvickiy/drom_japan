from config import TOKEN, CHAT_ID
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from sys import platform
import os



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
b4 = KeyboardButton("Secret")
b5 = KeyboardButton("rm out.log")
b6 = KeyboardButton("Statistic")
b7 = KeyboardButton("Start")
b8 = KeyboardButton("Clear")


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


def rm_out():
    if os.path.exists("./out.log"):
        if platform == "linux":
            os.system(f"rm ./out.log")
        elif platform == "win32":
            os.system(f"del out.log")
        return f"out.log deleted!"
    else:
        return "no file"


def get_statistic():
    res = []

    aqua = 0
    note = 0
    vitz = 0
    freed = 0
    sienta = 0
    stepwgn = 0
    noah = 0
    voxy = 0
    esquire = 0
    axio = 0
    vezel = 0
    fielder = 0
    prius = 0
    alpha = 0

    items = out("./history.txt")
    for i in items:
        name = i.split("/")[-2]
        if name == "aqua":
            aqua += 1
        elif name == "note":
            note += 1
        elif name == "vitz":
            vitz += 1
        elif name == "freed":
            freed += 1
        elif name == "sienta":
            sienta += 1
        elif name == "stepwgn":
            stepwgn += 1
        elif name == "noah":
            noah += 1
        elif name == "voxy":
            voxy += 1
        elif name == "esquire":
            esquire += 1
        elif name == "corolla_axio":
            axio += 1
        elif name == "vezel":
            vezel += 1
        elif name == "corolla_fielder":
            fielder += 1
        elif name == "prius":
            prius += 1
        elif name == "prius_a":
            alpha += 1
    data = {"aqua": aqua, "note": note, "vitz": vitz, "freed": freed, "sienta": sienta, "stepwgn": stepwgn, "noah": noah, "voxy": voxy, "esquire": esquire, "axio": axio, "vezel": vezel, "fielder": fielder, "prius": prius, "alpha": alpha}
    for k, v in data.items():
        res.append(f"{k}: {v}")
    return res


@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    return


@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(b1, b3, b6).row(b2, b4, b8))


@dp.message_handler()
async def send(message : types.Message):
    if message.text == "Start":
        await message.delete()
        await bot.send_message(message.from_user.id, "/start", reply_markup=kb().row(b1, b3, b6).row(b2, b4, b8))
    elif message.text == "History":
        out_history = out("./history.txt")
        if len(out_history) > 50:
            temp = [f"{out_history.index(i) + 1}: {i}" for i in out_history]
            for x in range(0, len(temp), 50):
                await bot.send_message(message.from_user.id, "\n".join(temp[x:x+50]), disable_web_page_preview=True)
        else:
            temp = [f"{out_history.index(i) + 1}: {i}" for i in out_history]
            await bot.send_message(message.from_user.id, "\n".join(temp), disable_web_page_preview=True)
    elif message.text == "Old":
        out_old = out("./old.txt")
        if len(out_old) > 50:
            temp = [f"{out_old.index(i) + 1}: {i}" for i in out_old]
            for x in range(0, len(out_old), 50):
                await bot.send_message(message.from_user.id, "\n".join(temp[x:x+50]), disable_web_page_preview=True)
        else:
            temp = [f"{out_old.index(i) + 1}: {i}" for i in out_old]
            await bot.send_message(message.from_user.id, "\n".join(out_old), disable_web_page_preview=True)
    elif message.text == "Out":
        out_log = out("./out.log")
        if len(out_log) > 50:
            for x in range(0, len(out_log), 50):
                await bot.send_message(message.from_user.id, "\n".join(out_log[x:x+50]), disable_web_page_preview=True)
        else:
            await bot.send_message(message.from_user.id, "\n".join(out_log), disable_web_page_preview=True)
    elif message.text == "rm out.log":
        rm_out()
    elif message.text == "Statistic":
        await message.delete()
        text = get_statistic()
        await bot.send_message(message.from_user.id, "\n".join(text))
    elif message.text == "Secret":
        await message.delete()
        await bot.send_message(message.from_user.id, "Secret", reply_markup=kb().row(b5, b7))
    elif message.text == "Clear":
        new_message_id = message.message_id
        for i in range(100):
            try:
                await bot.delete_message(chat_id=message.from_user.id, message_id=new_message_id)
            except Exception:
                pass
            new_message_id = new_message_id - 1


executor.start_polling(dp, skip_updates=True)
