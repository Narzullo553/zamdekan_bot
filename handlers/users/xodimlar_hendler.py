import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import ADMINS
from filters import IsAdmin_bot
from loader import dp, db, bot
from states.malumot_qoshish import Dars_jadvali_state, malumot_berish, ADD_XODIM_state
nomerlar = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
@dp.callback_query_handler(lambda call: "Delete1:" in call.data)
async def ochir(call: types.CallbackQuery):
    try:
        data = call.data
        data = data.replace("Delete1:", '').strip()
        await db.delete_xodimlar(int(data))
        await call.message.delete()
        await call.message.answer("malumot o'chirildi")
    except Exception as err:
        await bot.send_message(ADMINS[0], f"Xatolik: {err}")



@dp.message_handler(IsAdmin_bot(), text="📇 Xodimlar")
async def Xodimlar(msg: types.Message):
    try:
        await msg.delete()
        xodimlar = await db.select_all_xodimlar1()
        tugma = InlineKeyboardMarkup(row_width=1)
        if not xodimlar:
            tugma.insert(InlineKeyboardButton(text="➕", callback_data="xodim:+ qoshish"))
            await msg.answer("xodimlar topilmadi: \nQo'shish uchun bosing 🔗", reply_markup=tugma)
        else:
            for xodim in xodimlar:
                tugma.insert(InlineKeyboardButton(text=f"{xodim['ism_familiya']}", callback_data=f"xodim:{xodim['id']}"))
            tugma.insert(InlineKeyboardButton(text="➕", callback_data="xodim:+ qoshish"))
            await msg.answer("Xodimlar ro'yhati: \nKo‘rish uchun bosing 🔗", reply_markup=tugma)
    except Exception as err:
        await bot.send_message(ADMINS[0], f"Xatolik: {err}")

@dp.callback_query_handler(lambda call: "xodim:" in call.data)
async def all_xodim(call: types.CallbackQuery):
    try:
        data = call.data
        data = data.replace('xodim:', '').strip()
        await call.message.delete()
        if data == "+ qoshish":
            tugma = InlineKeyboardMarkup(row_width=2)
            tugma.insert(InlineKeyboardButton(text="🔙", callback_data="ortga"))
            await ADD_XODIM_state.next()
            await call.message.answer("Ism familiyasini kiriting: ", reply_markup=tugma)
        else:
            data = int(data)
            malumot = await db.select_one_xodimlar(data)
            ism_familiya = malumot['ism_familiya']
            lavozimi = malumot['lavozimi']
            tel_nomer = malumot['tel_nomer']
            tugma = InlineKeyboardMarkup(row_width=2)
            tugma.insert(InlineKeyboardButton(text="Delete", callback_data=f"Delete1:{data}"))
            tugma.insert(InlineKeyboardButton(text="🔙", callback_data="ortga1"))
            text = (f"FIO: {ism_familiya}"
                    f"\nlavozimi: {lavozimi}"
                    f"\ntel: {tel_nomer}")
            await call.message.answer(text, reply_markup=tugma)
    except Exception as e:
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")

@dp.callback_query_handler(text="ortga1")
async def Xodimlar(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        await state.finish()
        xodimlar = await db.select_all_xodimlar1()
        tugma = InlineKeyboardMarkup(row_width=1)
        if not xodimlar:
            tugma.insert(InlineKeyboardButton(text="➕", callback_data="+ qoshish"))
            await call.message.answer("xodimlar topilmadi: \nQo'shish uchun bosing 🔗", reply_markup=tugma)
        else:
            for xodim in xodimlar:
                tugma.insert(InlineKeyboardButton(text=f"{xodim['ism_familiya']}", callback_data=f"xodim:{xodim['id']}"))
            tugma.insert(InlineKeyboardButton(text="➕", callback_data="xodim:+ qoshish"))
            await call.message.answer("Xodimlar ro'yhati: \nKo‘rish uchun bosing 🔗", reply_markup=tugma)
    except Exception as err:
        await state.finish()
        await state.reset_data()
        await bot.send_message(ADMINS[0], f"Xatolik: {err}")

@dp.message_handler(state=ADD_XODIM_state.ism_familiya)
async def Ism_familiya(msg: types.Message, state: FSMContext):
    await state.update_data(
        {
            "ism_familiya": msg.text
        }
    )
    await msg.answer("Lavozimini kiriting")
    await ADD_XODIM_state.next()

@dp.message_handler(state=ADD_XODIM_state.lavozimi)
async def lavozimi(msg: types.Message, state: FSMContext):
    try:
        await state.update_data(
            {
                "lavozimi": msg.text
            }
        )
        await msg.answer("tel nomerini kiriting")
        await ADD_XODIM_state.next()
    except Exception as err:
        await state.finish()
        await state.reset_data()
        await bot.send_message(ADMINS[0], f"Xatolik: {err}")

@dp.message_handler(state=ADD_XODIM_state.tel_nomer)
async def lavozimi(msg: types.Message, state: FSMContext):
    try:
        if re.match(nomerlar, msg.text):
            malumot = await state.get_data()
            ism = malumot.get('ism_familiya')
            lavozimi = malumot.get('lavozimi')
            nomer = msg.text
            await db.add_xodimlar(ism, lavozimi, nomer)
            await msg.answer("kiritish yakunlandi")
            await state.finish()
        else:
            await msg.answer("nomer natog'ri kiritildi"
                             "\nqayta kiriting")
    except Exception as e:
        await state.finish()
        await state.reset_data()
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")

