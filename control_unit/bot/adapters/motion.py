import logging

from httpx import HTTPError

import settings

from .base import HTTPAdapter


class Motion(HTTPAdapter):
    api_path = '/0000/action/{}'

    def __init__(self):
        super().__init__(
            base_url=settings.MOTION_BASE_URL,
            auth=(settings.MOTION_USER, settings.MOTION_PASS),
            verify=False,
        )

    async def restart(self) -> str:
        return await self._invoke_cmd('restart')

    async def quit(self) -> str:
        return await self._invoke_cmd('quit')

    async def event_start(self) -> str:
        return await self._invoke_cmd('eventstart')

    async def event_stop(self) -> str:
        return await self._invoke_cmd('eventend')

    async def _invoke_cmd(self, cmd: str) -> str:
        try:
            response = await self.get(self.api_path.format(cmd))
        except HTTPError as e:
            logging.exception('Error during %s request', cmd)
            return f'Error: {e.__class__.__name__}'
        return 'OK' if response.status_code < 400 else 'ERROR'


motion = Motion()
