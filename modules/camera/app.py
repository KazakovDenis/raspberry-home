from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from webrtc.connection import WebRTCConnection
from webrtc.utils import Player


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.on_event('shutdown')
async def shutdown_event():
    await WebRTCConnection.close_all()
    Player.close_all()
