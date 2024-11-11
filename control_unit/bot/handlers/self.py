from aiogram import types

import settings
from dispatcher import dp


@dp.message_handler(commands=['ping'], user_id=settings.OWNER_ID)
async def ping(message: types.Message):
    await message.reply('pong')
