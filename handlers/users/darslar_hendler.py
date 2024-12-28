from utils.misc.funksiyalar import send_file_to_user
from io import BytesIO
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import ADMINS
from filters import IsPrivate, IsAdmin_bot
from loader import dp, db, bot
from states.malumot_qoshish import Dars_jadvali_state, malumot_berish





@dp.message_handler(text='/cancel', state='*')
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.finish()
        await message.reply("Jarayon to'xtatildi!")




@dp.callback_query_handler(text="Stop", state='*')
async def stop(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.finish()
        await call.message.delete()
        await call.message.answer(text="jarayon yakunlandi")
    except Exception as e:
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")


@dp.message_handler(IsPrivate(), IsAdmin_bot(), text="📚 Darslar nazorati")
async def qoshish(message: types.Message):
    try:
        malumotlar = await db.select_from_dars_jadvali()
        if not malumotlar:
            text = """
            dars Jadvallari topilmadi
            """
            tugma = InlineKeyboardMarkup(row_width=2)
            tugma.insert(InlineKeyboardButton(text="+ qoshish", callback_data="+ qoshish"))
            await message.answer(text=text, reply_markup=tugma)
            await message.delete()
        else:
            tugma = InlineKeyboardMarkup(row_width=2)
            for malumot in malumotlar:
                tugma.insert(InlineKeyboardButton(text=f"{malumot['guruh_nomi']}", callback_data=f"boshlash:{malumot['guruh_nomi']}"))
            tugma.insert(InlineKeyboardButton(text="➕", callback_data="boshlash:+ qoshish"))
            await message.delete()
            await message.answer(text="quydagilardan birini tanlang", reply_markup=tugma)
    except Exception as e:
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")


@dp.callback_query_handler(lambda call: "boshlash:" in call.data)
async def qoshish_boshlash(call: types.CallbackQuery, state: FSMContext):
    try:
        data = call.data.replace('boshlash:', '').strip()
        if data == "+ qoshish":
            text = "Guruh nomini kiritng"
            tugma = InlineKeyboardMarkup(row_width=2)
            tugma.insert(InlineKeyboardButton(text="Stop 🛑", callback_data="Stop"))
            await call.message.delete()
            call_msg = await call.message.answer(text=text, reply_markup=tugma)
            await state.update_data(
                {"call_id": call_msg.message_id}
            )
            await Dars_jadvali_state.next()
        else:
            guruh_nomi = data
            habar = await call.message.answer("yuborilmoqda ...")
            await send_file_to_user(call.from_user.id, guruh_nomi)
            await habar.delete()
    except Exception as e:
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")







@dp.message_handler(state=Dars_jadvali_state.guruh_nomi)
async def Guruh_nomi(msg: types.Message, state: FSMContext):
    try:
        malumot = await db.select_one_dars_jadvlali(msg.text)
        state_data = await state.get_data()
        call_id = state_data.get('call_id')
        await bot.delete_message(chat_id=msg.from_user.id, message_id=call_id)
        await state.update_data(
            {'guruh_nomi': msg.text}
        )
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="Stop 🛑", callback_data="Stop"))
        if malumot is None:
            await state.update_data(
                {'qoshish': 'insert'}
            )
            await msg.answer(text="Dars jadvali hujjatini yuboring", reply_markup=tugma)

        else:
            await state.update_data(
                {'qoshish': 'update'}
            )
            text = ("Bu guruh dars jadvali mavjud !!"
                    "\nyangilash uchun dars jadvalini yuboring")
            await msg.answer(text=text, reply_markup=tugma)
        await Dars_jadvali_state.next()
        await msg.delete()
    except Exception as e:
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")





@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=Dars_jadvali_state.filename)
async def faylni_qabul_qilish(msg: types.Message, state: FSMContext):
    try:
        file_id = msg.document.file_id
        file_name = msg.document.file_name

        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        file_data = BytesIO()
        await bot.download_file(file_path, file_data)

        state_data = await state.get_data()
        guruh_nomi = state_data.get('guruh_nomi')
        qoshish_turi = state_data.get('qoshish')
        if qoshish_turi == "insert":
            await db.add_dars_jadvali(
                guruh_nomi=guruh_nomi,
                filename=file_name,
                filedata=file_data.getvalue()
            )
        else:
            await db.update_dars_jadvali(
                guruh_nomi=guruh_nomi,
                filename=file_name,
                filedata=file_data.getvalue()
            )

        await msg.answer("Fayl muvaffaqiyatli saqlandi.")
        await state.finish()

    except Exception as e:
        await msg.answer(f"Xatolik yuz berdi: {str(e)}")
        await state.finish()

