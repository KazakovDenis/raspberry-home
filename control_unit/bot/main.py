"""The bot to control Raspberry Pi & other units remotely.

Available commands:
    ping - Check bot is alive
    pi_shutdown - Shutdown Raspberry Pi
    pi_reboot - Reboot Raspberry Pi
    pi_temp - Get Raspberry Pi temperature

Unused now:
    motion_restart - Restart video monitoring with Motion
    motion_quit - Stop video monitoring with Motion
    motion_event_start - Start a Motion event
    motion_event_stop - Stop a Motion event
"""
from aiogram import executor

import handlers  # noqa
import settings
from dispatcher import dp


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
