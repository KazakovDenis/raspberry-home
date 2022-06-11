from control.bot import settings
from control.bot.adapters.base import HTTPAdapter


class Motion(HTTPAdapter):

    def __init__(self):
        super().__init__(
            base_url=settings.MOTION_BASE_URL,
            auth=(settings.MOTION_USER, settings.MOTION_PASS),
            verify=False,
        )

    async def restart(self):
        pass

    async def quit(self):
        pass

    async def event_start(self):
        pass

    async def event_stop(self):
        pass


motion = Motion()
