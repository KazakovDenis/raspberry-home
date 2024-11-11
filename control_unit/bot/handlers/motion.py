from aiogram import types

import settings
from adapters import motion
from dispatcher import dp


@dp.message_handler(commands=['motion_restart'], user_id=settings.OWNER_ID)
async def motion_restart(message: types.Message):
    result = await motion.restart()
    await message.reply(result)


@dp.message_handler(commands=['motion_quit'], user_id=settings.OWNER_ID)
async def motion_quit(message: types.Message):
    result = await motion.quit()
    await message.reply(result)


@dp.message_handler(commands=['motion_event_start'], user_id=settings.OWNER_ID)
async def motion_event_start(message: types.Message):
    result = await motion.event_start()
    await message.reply(result)


@dp.message_handler(commands=['motion_event_stop'], user_id=settings.OWNER_ID)
async def motion_event_stop(message: types.Message):
    result = await motion.event_stop()
    await message.reply(result)
