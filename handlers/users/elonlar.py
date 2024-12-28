from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from filters import IsAdmin_bot, IsPrivate
from loader import dp, db, bot
from utils.misc.funksiyalar import create_excel_file, create_excel_file_sorovlar


@dp.message_handler(IsAdmin_bot(),IsPrivate(), text="📢 Eslatmalar va E'lonlar")
async def eslatma(msg: types.Message):
    tugma = InlineKeyboardMarkup(row_width=2)
    tugma.insert(InlineKeyboardButton(text="✍️E'lon Yozish", callback_data=f"yangilik: yozish"))
    tugma.insert(InlineKeyboardButton(text="✍️Habar Yozish", callback_data=f"habar: yozish"))
    await msg.delete()
    await msg.answer("Habar yuborish bo'limlaridan birini tanlang", reply_markup=tugma)

@dp.callback_query_handler(lambda call: "yangilik:" in call.data, state=None)
async def yangilik_yuborish(call: types.CallbackQuery, state: FSMContext):
    text  = ("Bu 📧 habar hamma foydalanuvchilarga yuboriladi!!"
             "\nyozishni boshlang")
    await call.message.delete()
    await call.message.answer(text=text)
    await state.set_state("Elon_yozish")

@dp.message_handler(state="Elon_yozish", content_types=types.ContentType.ANY)
async def Elon_yoborish(msg: types.Message, state: FSMContext):
    try:
        users = await db.select_all_users_id()
        if not users:
            await msg.answer("foydalanuvchilar topilmadi")
            return
        sent_count = 0
        for user in users:
            if str(user['telegram_id']) not in ADMINS:
                try:
                    await msg.copy_to(chat_id=user['telegram_id'])
                    sent_count += 1
                except Exception as e:
                    await bot.send_message(
                        chat_id=ADMINS[0],
                        text=f"Xatolik: Foydalanuvchi {user['telegram_id']} ga xabar yuborilmadi.\nSabab: {e}"
                    )
        await state.finish()
        await msg.answer(f"Xabar muvaffaqiyatli {sent_count}/{len(users)} foydalanuvchiga yuborildi.")
    except Exception as e:
        await bot.send_message(
            chat_id=ADMINS[0],
            text=f"Xatolik {e}"
        )



@dp.callback_query_handler(lambda call: "habar:" in call.data, state=None)
async def yangilik_yuborish(call: types.CallbackQuery, state: FSMContext):
    text  = ("Bu 📧 habar yuborish uchun "
             "\nfoydalnuvchilarni telegram idsini kiriting!!"
             "\nid larni , bilan ajratib yozing")
    await call.message.delete()
    await call.message.answer(text=text)
    await state.set_state("id_yozish")

@dp.message_handler(state="id_yozish")
async def id_orqali_xabar_yuborish(msg: types.Message, state: FSMContext):
    try:
        users_id = list(map(str, msg.text.split(',')))
        await msg.answer("Habarni yozishingiz mumkin !!")
        await state.update_data(
            {'users': users_id}
        )
        await state.set_state("Habar_yozish")
    except Exception as e:
        print(e)

@dp.message_handler(state="Habar_yozish", content_types=types.ContentType.ANY)
async def jonatish(msg: types.Message, state: FSMContext):
    malumot = await state.get_data()
    id: list = malumot.get('users')
    for i in id:
        if str(i).isdigit():
            try:
                await msg.copy_to(chat_id=int(i))
            except:
                await msg.answer(text=f"{i} idli foydalanuvchi topilmadi")
        else:
            await msg.answer(text=f"{i} idli foydalanuvchi topilmadi")





