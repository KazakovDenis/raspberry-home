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


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
ENABLE_SSL = os.getenv('ENABLE_SSL')

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

    def exec(self) -> Tuple[int, bytes]:
        raise NotImplementedError


class _Test(Command):

    def exec(self) -> Tuple[int, bytes]:
        result = subprocess.run(['echo', f'test {datetime.now()}'])
        return (201, b'OK') if result.returncode == 0 else (500, b'ERROR')


class Shutdown(Command):

    def exec(self) -> Tuple[int, bytes]:
        result = subprocess.run(['sudo', 'shutdown', '+1'])
        return (201, b'SCHEDULED') if result.returncode == 0 else (500, b'ERROR')


class Reboot(Command):

    def exec(self) -> Tuple[int, bytes]:
        result = subprocess.run(['sudo', 'shutdown', '-r', '+1'])
        return (201, b'SCHEDULED') if result.returncode == 0 else (500, b'ERROR')


class StopMotion(Command):

    def exec(self) -> Tuple[int, bytes]:
        pass


commands = {
    'TEST': _Test(),
    'SHUTDOWN': Shutdown(),
    'REBOOT': Reboot(),
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
