import logging

from environs import Env


env = Env()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

API_TOKEN = env('API_TOKEN', default=None)
assert API_TOKEN, 'No token specified'

OWNER_ID = env.int('OWNER_ID', default=0)
FILE = env('FILE', default='bot_data.json')

# Webhook params
USE_HOOK = env.bool('USE_HOOK', default=False)
HOST = env('HOST', default='localhost')
PORT = env.int('PORT', default=8000)
HOOK_PATH = env('HOOK_PATH', default='/webhook')

# Raspberry Pi
PI_BASE_URL = env('PI_BASE_URL', default='http://raspberrypi')
PI_TOKEN = env('PI_TOKEN', default='token')

# Motion
MOTION_BASE_URL = env('MOTION_BASE_URL', default='http://motion')
MOTION_USER = env('MOTION_USER', default='user')
MOTION_PASS = env('MOTION_PASS', default='password')
