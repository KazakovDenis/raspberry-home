from aiogram import types

import settings
from adapters import pi
from dispatcher import dp


@dp.message_handler(commands=['pi_shutdown'], user_id=settings.OWNER_ID)
async def pi_shutdown(message: types.Message):
    result = await pi.shutdown()
    await message.reply(result)


@dp.message_handler(commands=['pi_reboot'], user_id=settings.OWNER_ID)
async def pi_reboot(message: types.Message):
    result = await pi.reboot()
    await message.reply(result)


@dp.message_handler(commands=['pi_temp'], user_id=settings.OWNER_ID)
async def pi_temp(message: types.Message):
    result = await pi.temperature()
    await message.reply(result)
