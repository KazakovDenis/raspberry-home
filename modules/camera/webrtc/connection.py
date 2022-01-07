import asyncio
import logging
from typing import Callable, Optional

from aiortc import RTCPeerConnection


logger = logging.getLogger(__name__)


class WebRTCConnection(RTCPeerConnection):
    established = set()

    def __init__(self):
        super().__init__()
        WebRTCConnection.established.add(self)

    def on_state_change(self, func: Optional[Callable] = None):
        if func:
            return self.on('connectionstatechange', func)

        async def default():
            logger.info('Connection state is %s', self.connectionState)
            if self.connectionState == ConnectionState.FAILED:
                await self.close()

        return self.on('connectionstatechange', default)

    async def close(self):
        await super().close()
        WebRTCConnection.established.discard(self)

    @classmethod
    async def close_all(cls):
        coroutines = [pc.close() for pc in cls.established]
        await asyncio.gather(*coroutines)
        cls.established.clear()


class ConnectionState:
    NEW = 'new'
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    CLOSED = 'closed'
    FAILED = 'failed'
