from aiortc import RTCSessionDescription
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app import app
from webrtc.connection import WebRTCConnection
from webrtc.utils import html_response, create_local_tracks, TrackType


@app.get('/')
async def view_index():
    return html_response('index.html')


sessions = {}


class SessionDesc(BaseModel):
    sdp: str
    type: str
    timestamp: int


@app.post('/offer')
async def view_offer(params: SessionDesc):
    conn = WebRTCConnection()
    conn.on_state_change()

    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)
    await conn.setRemoteDescription(offer)

    webcam, audio, video = create_local_tracks()
    sessions[params.timestamp] = conn, webcam

    for tr in conn.getTransceivers():
        if tr.kind == TrackType.AUDIO and audio:
            conn.addTrack(audio)
        elif tr.kind == TrackType.VIDEO and video:
            conn.addTrack(video)

    answer = await conn.createAnswer()
    await conn.setLocalDescription(answer)

    return JSONResponse({
        'sdp': conn.localDescription.sdp,
        'type': conn.localDescription.type,
    })


@app.post('/stop')
async def view_stop(params: SessionDesc):
    if data := sessions.pop(params.timestamp, None):
        conn, webcam = data
        await conn.close()
        await webcam.stop()
    return JSONResponse('ok')
