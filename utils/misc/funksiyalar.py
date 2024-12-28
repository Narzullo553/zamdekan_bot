from io import BytesIO

from openpyxl.workbook import Workbook

from data.config import ADMINS
from loader import db, bot


def create_excel_file(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Users Data"

    sheet.append(["ID", "Full Name", "Telegram ID"])
    for row in data:
        sheet.append(row)
    excel_stream = BytesIO()
    workbook.save(excel_stream)
    excel_stream.seek(0)
    return excel_stream

async def send_file_to_user(user_id: int, guruh_nomi: str):
    try:
        result = await db.select_one_dars_jadvlali(guruh_nomi)

        if result:
            file_data = result['filedata']
            file_name = result['filename']

            file_stream = BytesIO(file_data)
            file_stream.name = file_name

            await bot.send_document(user_id, file_stream, caption="Sizning so‘rovingiz bo‘yicha fayl:")
            file_stream.close()
        else:
            await bot.send_message(user_id, "Fayl topilmadi.")

    except Exception as e:
        await bot.send_message(user_id, "Faylni yuborishda xatolik yuz berdi. Keyinroq urinib ko‘ring.")
        await bot.send_message(ADMINS[0], f"Xatolik: {e}")

async def create_excel_file_sorovlar(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sorovlar"

    sheet.append(["id", "fullname", "telegram_id", "sorov", "vaqti"])
    for row in data:
        sheet.append([row['id'], row['fullname'], row['telegram_id'], row['sorov'], str(row['vaqti'])[:16]])
    excel_stream = BytesIO()
    workbook.save(excel_stream)
    excel_stream.seek(0)
    return excel_stream