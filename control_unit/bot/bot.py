"""The bot to control Raspberry Pi & other units remotely.

Available commands:
    pi_shutdown - Shutdown Raspberry Pi
    pi_reboot - Reboot Raspberry Pi
    pi_temp - Get Raspberry Pi temperature
    motion_restart - Restart video monitoring with Motion
    motion_quit - Stop video monitoring with Motion
    motion_event_start - Start a Motion event
    motion_event_stop - Stop a Motion event
"""
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from . import settings
from .adapters import motion, pi


dp = Dispatcher(
    bot=Bot(token=settings.API_TOKEN),
    storage=JSONStorage(path=settings.FILE),
)
dp.middleware.setup(LoggingMiddleware())


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


if __name__ == '__main__':
    if settings.USE_HOOK:
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=settings.HOOK_PATH,
            host=settings.HOST,
            port=settings.PORT,
        )
    else:
        executor.start_polling(dp)
