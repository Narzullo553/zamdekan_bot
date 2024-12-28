
from io import BytesIO
from utils.misc.funksiyalar import send_file_to_user

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import ADMINS
from filters import IsPrivate
from loader import dp, db, bot


@dp.message_handler(IsPrivate(), text="📚 Dars Jadvali")
async def qoshish(message: types.Message):
    try:
        malumotlar = await db.select_from_dars_jadvali()
        if not malumotlar:
            text = """
            dars Jadvallari topilmadi
            """
            await message.delete()
            await message.answer(text=text)
        else:
            tugma = InlineKeyboardMarkup(row_width=2)
            for malumot in malumotlar:
                tugma.insert(InlineKeyboardButton(text=f"{malumot['guruh_nomi']}", callback_data=f"top:{malumot['guruh_nomi']}"))
            await message.delete()
            await message.answer(text="quydagilardan birini tanlang", reply_markup=tugma)
    except Exception as e:
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")

@dp.callback_query_handler(lambda call: "top:" in call.data)
async def jonatish(call: types.CallbackQuery):
    try:
        guruh_nomi = call.data.replace('top:', '').strip()
        await call.message.delete()
        habar = await call.message.answer("yuborilmoqda ...")
        await send_file_to_user(call.from_user.id, guruh_nomi)
        await habar.delete()
    except Exception as e:
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")