from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import settings


dp = Dispatcher(
    bot=Bot(token=settings.API_TOKEN),
    storage=JSONStorage(path=settings.FILE),
)
dp.middleware.setup(LoggingMiddleware())
