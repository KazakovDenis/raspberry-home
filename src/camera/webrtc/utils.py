from functools import cache

import settings
from aiortc.contrib.media import MediaPlayer, MediaRelay
from starlette.responses import HTMLResponse
from video.converters import VideoTrackConverter


class TrackType:
    AUDIO = 'audio'
    VIDEO = 'video'


class Player(MediaPlayer):
    containers = set()

    def __init__(self, file, fmt, options):
        super().__init__(file, fmt, options)
        Player.containers.add(self)

    async def stop(self):
        # stop player worker thread
        if self.private('thread_quit'):
            self.private('thread_quit').set()

        if self.video:
            self.video.stop()
        if self.audio:
            self.audio.stop()

        Player.containers.discard(self)

    def private(self, attr):
        return getattr(self, f'_MediaPlayer__{attr}')

    @classmethod
    def close_all(cls):
        for container in cls.containers:
            container.close()
        cls.containers.clear()


def get_camera():
    return Player(**settings.CAMERA_OPS)


@cache
def html_response(filename):
    with open(settings.STATIC_PATH / filename, 'r') as file:
        return HTMLResponse(content=file.read())


def create_local_tracks():
    relay = MediaRelay()
    webcam = get_camera()

    video = relay.subscribe(webcam.video)
    audio = None
    if webcam.audio:
        audio = relay.subscribe(webcam.video)

    return webcam, audio, VideoTrackConverter(video)
