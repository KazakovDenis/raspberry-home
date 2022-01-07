import os
from pathlib import Path
from warnings import filterwarnings

from cryptography.utils import CryptographyDeprecationWarning


filterwarnings('ignore', category=CryptographyDeprecationWarning)

ROOT = Path(__file__).parent

STATIC_PATH = ROOT / 'static'

CAMERA_ID = os.getenv('CAMERA_ID', 0)

CAMERA_OPS = {
    'file': f'/dev/video{CAMERA_ID}',
    'fmt': 'v4l2',
    'options': {
        'framerate': os.getenv('FRAME_RATE', '30'),
        'video_size': os.getenv('VIDEO_SIZE', '640x480'),
    },
}
