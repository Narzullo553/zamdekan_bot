from aiogram import types
from aiogram.types import InputFile
from filters import IsAdmin_bot, IsPrivate
from loader import dp, db, bot
from utils.misc.funksiyalar import create_excel_file, create_excel_file_sorovlar


@dp.message_handler(IsPrivate(), text="📰 Yangiliklar")
async def eslatma(msg: types.Message):
    await msg.delete()
    await msg.answer("hozirda bu bo'limda tehnik ishlar olib borilmoqda")