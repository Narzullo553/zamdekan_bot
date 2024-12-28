from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default.bosh_menu import bosh_menu
from keyboards.default.zamdekan_uchun_tugmalar import zamdekan_menu
from loader import dp, db


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    try:
        user = message.from_user
        m_user = await db.select_one_users(user.id)
        if not m_user:
            await db.add_users(fullname=user.full_name, telegram_id=user.id)
    except Exception as err:
        pass
    if str(message.from_user.id) not in ADMINS:
        await message.answer(f"Salom! 🌟 {message.from_user.full_name} xush kelibsiz! "
                             f"Sizga qanday yordam bera olishim mumkin? ", reply_markup=bosh_menu)
    else:
        await message.answer("Assalomu alaykum \nbo'limlardan birini tanlang!!",
                             reply_markup=zamdekan_menu)

