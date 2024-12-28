from venv import create

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.misc import logging
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import ADMINS

async def on_startup(dispatcher):
    try:
        # Birlamchi komandalar (/star va /help)
        await set_default_commands(dispatcher)
        await db.create()
        await db.create_table_users()
        await db.creat_tabe_sorovlar()
        await db.create_table_xodimlar()
        await db.create_table_dars_jadvali()
        # Bot ishga tushgani haqida adminga xabar berish
        await on_startup_notify(dispatcher)
    except Exception as error:
        for admin in ADMINS:
            try:
                await dp.bot.send_message(admin, f"{error}")
            except Exception as err:
                pass



if __name__ == '__main__':
    logging
    executor.start_polling(dp, on_startup=on_startup)
