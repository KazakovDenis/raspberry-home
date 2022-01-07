from aiortc import MediaStreamTrack
from aiortc.mediastreams import MediaStreamError
from video import effects


class VideoTrackConverter(MediaStreamTrack):
    kind = 'video'

    def __init__(self, track: MediaStreamTrack, effect: str = ''):
        super().__init__()
        self.track = track
        self.effect = effect

    async def recv(self):
        try:
            frame = await self.track.recv()
            self.track._queue.task_done()
        except MediaStreamError:
            if self.readyState == 'live':
                self.track._queue.task_done()
            raise

        if not self.effect:
            return frame

        effect = getattr(effects, self.effect)
        return effect(frame)
