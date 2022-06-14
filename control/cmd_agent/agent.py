"""
HTTP server to match HTTP requests to system commands in one script using only pure standard Python.

1. Copy to a server and create a symbolic link:
    $ export APP_DIR=/opt/cmd_agent && mkdir -p $APP_DIR
    $ sudo ln -s $APP_DIR/cmd_agent.service /etc/systemd/system/cmd_agent.service
2. Enable and start service:
    $ sudo systemctl enable cmd_agent.service
    $ sudo systemctl start cmd_agent.service
3. [Optional] Generate certificates to enable SSL:
    $ openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -out $APP_DIR/agent.crt -keyout $APP_DIR/agent.key
3.1. Enable SSL setting ENABLE_SSL=True
4. Add a firewall rule for port 443 or 80:
    $ sudo ufw allow 443/tcp comment "Command agent"
"""
import json
import logging
import os
import signal
import ssl
import subprocess
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import JSONDecodeError
from pathlib import Path
from typing import Tuple
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import urlopen


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
ENABLE_SSL = os.getenv('ENABLE_SSL')
MOTION_URL = 'https://localhost:8080'

ADDRESS = ('0.0.0.0', 443 if ENABLE_SSL else 80)
CERT_KEY = Path('/opt/cmd_agent/agent.key')
CERT_PATH = Path('/opt/cmd_agent/agent.crt')


def shutdown(sig_num, frame):
    sig = signal.Signals(sig_num).name
    logging.info('%s received. Shutting down.', sig)
    raise KeyboardInterrupt


class ClientError(Exception):
    pass


class Command:
    _ss_ctx = None

    def exec(self) -> Tuple[int, bytes]:
        raise NotImplementedError

    @property
    def ss_ctx(self):
        """Context to use with self-signed server certs."""
        if self._ss_ctx:
            return self._ss_ctx
        self._ss_ctx = ssl.create_default_context()
        self._ss_ctx.check_hostname = False
        self._ss_ctx.verify_mode = ssl.CERT_NONE
        return self._ss_ctx


class _Test(Command):

    def exec(self) -> Tuple[int, bytes]:
        result = subprocess.run(['echo', f'test {datetime.now()}'])
        return (201, b'OK') if result.returncode == 0 else (500, b'ERROR')


class Shutdown(Command):
    command = ['sudo', 'shutdown', '+1']
    in_shutdown = False

    def exec(self) -> Tuple[int, bytes]:
        if Shutdown.in_shutdown:
            return 423, b'IN_SHUTDOWN'

        result = subprocess.run(self.command)
        if result.returncode == 0:
            Shutdown.in_shutdown = True
            return 201, b'SCHEDULED'
        return 500, b'ERROR'


class Reboot(Shutdown):
    command = ['sudo', 'shutdown', '-r', '+1']


class Temperature(Shutdown):
    command = ['sudo', 'vcgencmd', 'measure_temp']

    def exec(self) -> Tuple[int, bytes]:
        result = subprocess.run(self.command, capture_output=True)
        if result.returncode == 0:
            return 201, result.stdout
        return 500, b'ERROR'


class _Motion(Command):
    action: str

    def exec(self) -> Tuple[int, bytes]:
        try:
            with urlopen(urljoin(MOTION_URL, f'/00000/action/{self.action}'), context=self.ss_ctx) as response:
                return response.code, response.msg.encode()
        except URLError:
            logging.exception('Error during executing motion command: %s', self.action)
            return 502, b'ERROR'


class StopMotion(_Motion):
    action = 'quit'


commands = {
    'TEST': _Test(),
    'TEMPERATURE': Temperature(),
    'SHUTDOWN': Shutdown(),
    'REBOOT': Reboot(),
    'MOTION_STOP': StopMotion(),
}


class Handler(BaseHTTPRequestHandler):
    error_message_format = '{"code": "%(code)s", "message": "%(message)s", "details": "%(explain)s"}'
    error_content_type = 'application/json'

    def send_response(self, code, message=None):
        self.log_request(code)
        self.send_response_only(code, message)
        self.send_header('Date', self.date_time_string())
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.wfile.write(b'OK')

    def do_POST(self):
        try:
            cmd = self._validate()
            code, msg = commands[cmd].exec()
        except ClientError as e:
            self.send_response(e.args[0])
            self.wfile.write(e.args[1])
        except Exception:   # noqa
            logging.exception('Error during request.')
            self.send_response(500)
        else:
            self.send_response(code)
            self.wfile.write(msg)

    def _validate(self) -> str:
        body = b''
        try:
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))
            self._auth(body.get('token'))
            command = body.get('command')
        except (AttributeError, TypeError, ValueError, JSONDecodeError):
            logging.warning('Bad request: %s', body)
            raise ClientError(400, b'Bad request')
        if command not in commands:
            logging.warning('Forbidden: %s', body)
            raise ClientError(403, b'Forbidden')
        return command

    @staticmethod
    def _auth(token: str):
        if AUTH_TOKEN and token != AUTH_TOKEN:
            raise ClientError(401, b'Unauthorized')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    httpd = HTTPServer(ADDRESS, Handler)
    if ENABLE_SSL:
        logging.info('SSL enabled.')
        httpd.socket = ssl.wrap_socket(
            sock=httpd.socket,
            keyfile=CERT_KEY,
            certfile=CERT_PATH,
            server_side=True,
        )
    logging.info('Serving on %s:%s.', *ADDRESS)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.server_close()
        logging.info('Server stopped.')
