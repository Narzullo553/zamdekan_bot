from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from loader import db, dp, bot, types


@dp.message_handler(text="📞 Kontaktlar")
async def Xodimlar1(msg: types.Message):
    try:
        await msg.delete()
        xodimlar = await db.select_all_xodimlar1()
        tugma = InlineKeyboardMarkup(row_width=1)
        if not xodimlar:
            await msg.answer("xodimlar topilmadi", reply_markup=tugma)
        else:
            for xodim in xodimlar:
                tugma.insert(InlineKeyboardButton(text=f"{xodim['ism_familiya']}", callback_data=f"xodim1:{xodim['id']}"))
            await msg.answer("Xodimlar ro'yhati: \nKo‘rish uchun bosing 🔗", reply_markup=tugma)
    except Exception as err:
        await bot.send_message(ADMINS[0], f"Xatolik: {err}")

@dp.callback_query_handler(lambda call: "xodim1:" in call.data)
async def all_xodim1(call: types.CallbackQuery):
    try:
        data = call.data
        data = data.replace('xodim1:', '').strip()
        await call.message.delete()
        data = int(data)
        malumot = await db.select_one_xodimlar(data)
        ism_familiya = malumot['ism_familiya']
        lavozimi = malumot['lavozimi']
        tel_nomer = malumot['tel_nomer']
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="🔙", callback_data="ortga"))
        text = (f"FIO: {ism_familiya}"
                f"\nlavozimi: {lavozimi}"
                f"\ntel: {tel_nomer}")
        await call.message.answer(text, reply_markup=tugma)
    except Exception as e:
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")

@dp.callback_query_handler(text="ortga")
async def Xodimlar1(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        await state.finish()
        xodimlar = await db.select_all_xodimlar1()
        tugma = InlineKeyboardMarkup(row_width=2)
        if not xodimlar:
            await call.message.answer("xodimlar topilmadi", reply_markup=tugma)
        else:
            for xodim in xodimlar:
                tugma.insert(InlineKeyboardButton(text=f"{xodim['ism_familiya']}", callback_data=f"xodim1:{xodim['id']}"))
            await call.message.answer("Xodimlar ro'yhati: \nKo‘rish uchun bosing 🔗", reply_markup=tugma)
    except Exception as err:
        await bot.send_message(ADMINS[0], f"Xatolik: {err}")
