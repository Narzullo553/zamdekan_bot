
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import ADMINS
from filters import IsAdmin_bot, IsPrivate
from loader import dp, db, bot



@dp.message_handler(IsPrivate(), text="✉️Murojaat")
async def xabar_yuborish(msg: types.Message):
    tugma = InlineKeyboardMarkup(row_width=2)
    tugma.insert(InlineKeyboardButton(text="✍️ Yozish", callback_data="yozish"))
    text = "yozishni boshlash uchun tugmani bosing"
    await msg.answer(text, reply_markup=tugma)


@dp.callback_query_handler(text="yozish", state=None)
async def zamdekanga_murojaat_boshlash(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Zamdekanga murojaatingizni yozishingiz munkin:")
    await state.set_state("zamdekanga_murojaat")


@dp.message_handler(state="zamdekanga_murojaat")
async def zamdekanga_murojaat_qabul(msg: types.Message, state: FSMContext):
    """Foydalanuvchi murojaatini qabul qilish va zamdekanga yuborish."""
    try:
        murojaat_matni = msg.text
        zamdekanga_id = ADMINS[0]  # Zamdekaning Telegram ID'si
        tugma = InlineKeyboardMarkup(row_width=2)
        tugma.insert(InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"cancel:{msg.from_user.id}"))
        tugma.insert(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm:{msg.from_user.id}"))
        tugma.insert(InlineKeyboardButton(text="✍️ Javob yozish", callback_data=f"yozish:{msg.from_user.id}"))
        await bot.send_message(
            chat_id=zamdekanga_id,
            text=f"Yangi murojaat:\n\n"
                 f"👤 Foydalanuvchi: {msg.from_user.full_name}\n"
                 f"🆔 ID: {msg.from_user.id}\n\n"
                 f"📩 Murojaat: {murojaat_matni}", reply_markup=tugma
        )
        await db.add_sorov(msg.from_user.full_name, msg.from_user.id, murojaat_matni)
        await msg.answer("Rahmat! Sizning murojaatingiz zamdekanga yuborildi. Tez orada javob olasiz.")
        await state.finish()

    except Exception as e:
        await msg.answer("Xatolik yuz berdi! Keyinroq urinib ko'ring.")
        await state.finish()
        raise e


@dp.callback_query_handler(lambda call: "cancel:" in call.data)
async def cancel_xabar(call: types.CallbackQuery):
    data = int(call.data.replace('cancel:', '').strip())
    await bot.send_message(chat_id=data, text="Murojatingiz rad etildi !!")
    await call.message.delete()
    await db.delete_tg_id_sorovlar(telegram_id=data)
    await call.answer("Murojaat rad qilindi!")

@dp.callback_query_handler(lambda call: "confirm:" in call.data)
async def confirm_xabar(call: types.CallbackQuery):
    foydalanuvchi_id = call.data.split(":")[1]
    await bot.send_message(chat_id=foydalanuvchi_id, text="Sizning murojaatingiz qabul qilindi!")
    await call.answer("Murojaat qabul qilindi!")
    await call.message.delete()

@dp.callback_query_handler(IsAdmin_bot(), lambda call: "yozish:" in call.data, state=None)
async def javob_yozish(call: types.CallbackQuery, state: FSMContext):
    tg_id = int(call.data.replace("yozish:", '').strip())
    await call.message.answer("javob yozishingiz mumkin !!")
    await state.update_data(
        {
            'id': tg_id
        }
    )
    await state.set_state("javob_yozish_boshlash")

@dp.message_handler(state='javob_yozish_boshlash')
async def foydalanuchiga_habar_yuborish(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    id_t = data.get('id')
    await bot.send_message(chat_id=id_t, text=msg.text)
    await msg.answer(text="xabaringiz yuborildi")
    await state.finish()