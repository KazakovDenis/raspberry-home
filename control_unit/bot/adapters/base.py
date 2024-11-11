from httpx import AsyncClient

import settings


class HTTPAdapter(AsyncClient):

    def __init__(self, **kwargs):
        headers = kwargs.pop('headers', {})
        headers.setdefault(b'User-Agent', settings.BOT_NAME)
        super().__init__(headers=headers, **kwargs)
