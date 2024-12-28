from aiogram import types
from aiogram.types import InputFile
from filters import IsAdmin_bot, IsPrivate
from loader import dp, db, bot
from utils.misc.funksiyalar import create_excel_file, create_excel_file_sorovlar


@dp.message_handler(IsPrivate(),text="📥 Yangi Murojaatlar")
async def murojatlarni_olish(msg: types.Message):
    try:
        data = await db.select_all_sorovlar()
        if not data:
            await msg.answer("Ma'lumotlar bazasida hech qanday foydalanuvchi topilmadi.")
            return
        excel_file = await create_excel_file_sorovlar(data)
        await bot.send_document(
            chat_id=msg.chat.id,
            document=InputFile(excel_file, filename="Murojaatlar.xlsx"),
            caption="Foydalanuvchilar sorovlari."
        )

    except Exception as e:
        await msg.answer(f"Xatolik yuz berdi: {e}")







@dp.message_handler(IsAdmin_bot(), commands=['users'])
async def send_excel_file(message: types.Message):
    try:
        data = await db.select_all_users()
        if not data:
            await message.answer("Ma'lumotlar bazasida hech qanday foydalanuvchi topilmadi.")
            return
        data = [list(row.values()) for row in data]
        excel_file = create_excel_file(data)

        await bot.send_document(
            chat_id=message.chat.id,
            document=InputFile(excel_file, filename="users_data.xlsx"),
            caption="Foydalanuvchilar ma'lumotlari."
        )

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")


