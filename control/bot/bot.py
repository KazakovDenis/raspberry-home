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
import logging
import os

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = os.getenv('BOT_API_TOKEN')
OWNER_ID = int(os.getenv('BOT_OWNER_ID', 0))
assert API_TOKEN, 'No token specified'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    if message.from_user != OWNER_ID:
        await message.reply("Sorry, you can't send messages to this bot.")
    await message.reply('Hello!')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
