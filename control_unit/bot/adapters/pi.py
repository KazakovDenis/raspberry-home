import logging

from httpx import HTTPError

import settings

from .base import HTTPAdapter


class RaspberryPi(HTTPAdapter):

    def __init__(self):
        super().__init__(
            base_url=settings.PI_BASE_URL,
            verify=False,
        )

    async def reboot(self) -> str:
        return await self._invoke_cmd('REBOOT')

    async def shutdown(self) -> str:
        return await self._invoke_cmd('SHUTDOWN')

    async def temperature(self) -> str:
        return await self._invoke_cmd('TEMPERATURE')

    async def _invoke_cmd(self, cmd: str) -> str:
        data = {
            'command': cmd.upper(),
            'token': settings.PI_TOKEN,
        }
        try:
            response = await self.post('/', json=data)
        except HTTPError as e:
            logging.exception('Error during %s request', cmd)
            return f'Error: {e.__class__.__name__}'
        return response.text


pi = RaspberryPi()
