"""
Pure standard Python HTTP server to match HTTP requests to system commands in one module.

1. Put `cmd_agent.service` into `/etc/systemd/system/` directory
2. Enable and start service:
    $ sudo systemctl enable cmd_agent.service
    $ sudo systemctl start cmd_agent.service
3. [Optional] Generate certificates to enable SSL:
    $ mkdir -p /opt/cmd_agent
    $ openssl req -x509 -newkey rsa:2048 -keyout /opt/cmd_agent/key.pem -out /opt/cmd_agent/cert.pem -days 365
3.1. Enable SSL setting ENABLE_SSL=True
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


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
ENABLE_SSL = os.getenv('ENABLE_SSL')

ADDRESS = ('0.0.0.0', 443 if ENABLE_SSL else 80)
CERT_KEY = Path('/opt/cmd_agent/key.pem')
CERT_PATH = Path('/opt/cmd_agent/cert.pem')


def shutdown(sig_num, frame):
    sig = signal.Signals(sig_num).name
    logging.info('%s received. Shutting down.', sig)
    raise KeyboardInterrupt


class ClientError(Exception):
    pass


class Command:

    def exec(self) -> Tuple[int, bytes]:
        raise NotImplementedError


class Shutdown(Command):

    def exec(self) -> Tuple[int, bytes]:
        result = subprocess.run(['sudo', 'shutdown', '+1'])
        return (201, b'SCHEDULED') if result.returncode == 0 else (500, b'ERROR')


class Reboot(Command):

    def exec(self) -> Tuple[int, bytes]:
        result = subprocess.run(['sudo', 'shutdown', '-r', '+1'])
        return (201, b'SCHEDULED') if result.returncode == 0 else (500, b'ERROR')


class TestCommand(Command):

    def exec(self) -> Tuple[int, bytes]:
        result = subprocess.run(['echo', f'test {datetime.now()}'])
        return (201, b'OK') if result.returncode == 0 else (500, b'ERROR')


commands = {
    'SHUTDOWN': Shutdown(),
    'REBOOT': Reboot(),
    'TEST': TestCommand(),
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
