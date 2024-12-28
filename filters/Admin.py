from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS


class IsAdmin(BoundFilter):
    async def check(self, msg: types.Message) -> bool:
        member = await msg.chat.get_member(msg.from_user.id)
        return member.is_chat_admin()

class IsAdmin_bot(BoundFilter):
    async def check(self, msg: types.Message) -> bool:
        id = msg.from_user.id
        return str(id) in ADMINS